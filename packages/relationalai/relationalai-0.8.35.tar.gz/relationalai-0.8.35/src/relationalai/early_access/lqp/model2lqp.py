from relationalai.early_access.lqp.validators import assert_valid_input
from relationalai.early_access.lqp.utils import UniqueNames
from relationalai.early_access.metamodel import ir, builtins as rel_builtins, helpers
from relationalai.early_access.metamodel.types import is_any
from relationalai.early_access.metamodel.visitor import collect_by_type
from relationalai.early_access.lqp import ir as lqp
from relationalai.early_access.lqp.hash_utils import lqp_hash
from relationalai.early_access.lqp.primitives import relname_to_lqp_name, lqp_operator
from relationalai.early_access.lqp.types import meta_type_to_lqp, type_from_constant
from relationalai.early_access.lqp.constructors import mk_and, mk_exists, mk_or, mk_abstraction
import datetime as dt

from typing import Tuple, cast, Union

class TranslationCtx:
    def __init__(self, model):
        # TODO: comment these fields
        # TODO: should we have a pass to rename variables instead of this?
        self.unique_names = UniqueNames()
        self.id_to_orig_name = {}
        self.output_ids = []

""" Main access point. Converts the model IR to an LQP program. """
def to_lqp(model: ir.Model) -> lqp.LqpProgram:
    assert_valid_input(model)
    ctx = TranslationCtx(model)
    program = _translate_to_program(ctx, model)
    return program

def _translate_to_program(ctx: TranslationCtx, model: ir.Model) -> lqp.LqpProgram:
    decls: list[lqp.Declaration] = []
    outputs: list[Tuple[str, lqp.RelationId]] = []

    # LQP only accepts logical tasks
    # These are asserted at init time
    root = cast(ir.Logical, model.root)

    seen_rids = set()
    for subtask in root.body:
        assert isinstance(subtask, ir.Logical)
        decl = _translate_to_decl(ctx, subtask)

        if decl is None:
            continue

        assert isinstance(decl, lqp.Def), "we dont do loops yet m8"
        decls.append(decl)

        rid = decl.name
        assert rid not in seen_rids, f"duplicate relation id: {rid}"
        seen_rids.add(rid)

    for output_id in ctx.output_ids:
        assert isinstance(output_id, lqp.RelationId)
        outputs.append(("output", output_id))

    debug_info = lqp.DebugInfo(ctx.id_to_orig_name)

    return lqp.LqpProgram(decls, outputs, debug_info)

def _make_def(ctx: TranslationCtx, name: str, projection: list[Tuple[lqp.Var, lqp.RelType]], conjs: list[lqp.Formula], is_output: bool = False) -> lqp.Def:
    abstraction = mk_abstraction(projection, mk_and(conjs))
    rel_id = name_to_id(name)
    ctx.id_to_orig_name[rel_id] = name

    if is_output:
        ctx.output_ids.append(rel_id)

    # TODO: is this correct? might need attrs tooo?
    return lqp.Def(rel_id, abstraction, [])

def _effect_bindings(effect: Union[ir.Output, ir.Update]) -> list[ir.Value]:
    if isinstance(effect, ir.Output):
        # TODO: we dont yet handle aliases, so we ignore v[0]
        return [v[1] for v in effect.aliases]
    else:
        return list(effect.args)

def _translate_to_decl(ctx: TranslationCtx, rule: ir.Logical) -> Union[lqp.Declaration,None]:
    effects = collect_by_type((ir.Output, ir.Update), rule)
    aggregates = collect_by_type(ir.Aggregate, rule)

    # TODO: should this ever actually come in as input?
    if len(effects) == 0:
        return None
    assert len(effects) == 1, f"should only have exactly one effect, got {len(effects)}"
    effect = effects[0]

    conjuncts = []
    for task in rule.body:
        if isinstance(task, (ir.Output, ir.Update)):
            continue
        conjuncts.append(_translate_to_formula(ctx, task))

    # Aggregates reduce over the body
    if len(aggregates) > 0:
        aggr_body = mk_and(conjuncts)
        conjuncts = []
        for aggr in aggregates:
            conjuncts.append(_translate_aggregate(ctx, aggr, aggr_body))

    # Handle the bindings
    bindings = _effect_bindings(effect)
    projection, eqs = translate_bindings(ctx, bindings)
    conjuncts.extend(eqs)

    is_output = isinstance(effect, ir.Output)
    def_name = "output" if is_output else effect.relation.name
    return _make_def(ctx, def_name, projection, conjuncts, is_output)

def _translate_aggregate(ctx: TranslationCtx, aggr: ir.Aggregate, body: lqp.Formula) -> lqp.Reduce:
    # TODO: handle this properly
    aggr_name = aggr.aggregation.name
    supported_aggrs = ("sum", "count", "min", "max")
    assert aggr_name in supported_aggrs, f"only support {supported_aggrs} for now, not {aggr.aggregation.name}"

    # TODO: This is not right, we need to handle input args and output args properly
    # Last one is output arg, the rest are input args
    input_args = [_translate_term(ctx, arg) for arg in aggr.args[:-1]]
    output_var, _ = _translate_term(ctx, aggr.args[-1])

    projected_args = [_translate_term(ctx, var) for var in aggr.projection]
    abstr_args = []
    abstr_args.extend(projected_args)
    abstr_args.extend(input_args)
    if aggr_name == "count":
        # Count sums up "1"
        one_var, typ, eq = binding_to_lqp_var(ctx, 1)
        assert eq is not None
        body = mk_and([body, eq])
        abstr_args.append([one_var, typ])

    # Group-bys do not need to be handled at all, since they are introduced outside already
    reduce = lqp.Reduce(
        lqp_operator(ctx.unique_names, aggr.aggregation),
        mk_abstraction(abstr_args, body),
        [output_var],
    )
    return reduce

def _translate_to_formula(ctx: TranslationCtx, task: ir.Task) -> lqp.Formula:
    if isinstance(task, ir.Logical):
        conjuncts = [_translate_to_formula(ctx, child) for child in task.body]
        return mk_and(conjuncts)
    elif isinstance(task, ir.Lookup):
        return _translate_to_atom(ctx, task)
    elif isinstance(task, ir.Not):
        return lqp.Not(_translate_to_formula(ctx, task.task))
    elif isinstance(task, ir.Exists):
        lqp_vars, conjuncts = translate_bindings(ctx, list(task.vars))
        conjuncts.append(_translate_to_formula(ctx, task.task))
        return mk_exists(lqp_vars, mk_and(conjuncts))
    elif isinstance(task, ir.Construct):
        assert len(task.values) >= 1, "construct should have at least one value"
        # TODO: what does the first value do
        terms = [_translate_term(ctx, arg) for arg in task.values[1:]]
        terms.append(_translate_term(ctx, task.id_var))
        return lqp.Primitive(
            "rel_primitive_hash_tuple_uint128",
            [v for [v, _] in terms],
        )
    elif isinstance(task, ir.Union):
        # TODO: handle hoisted vars if needed
        assert len(task.hoisted) == 0, "hoisted updates not supported yet, because idk what it means"
        disjs = [_translate_to_formula(ctx, child) for child in task.tasks]
        return mk_or(disjs)
    elif isinstance(task, ir.Aggregate):
        # Nothing to do here, handled in _translate_to_decl
        return mk_and([])
    else:
        raise NotImplementedError(f"Unknown task type (formula): {type(task)}")

def _translate_term(ctx: TranslationCtx, value: ir.Value) -> Tuple[lqp.Term, lqp.RelType]:
    if isinstance(value, ir.Var):
        name = ctx.unique_names.get_name_by_id(value.id, value.name)
        assert not is_any(value.type), f"unexpected type for var `{value}`: {value.type}"
        t = meta_type_to_lqp(value.type)
        return lqp.Var(name), t
    elif isinstance(value, ir.Literal):
        return _translate_term(ctx, value.value)
    else:
        assert isinstance(value, (str, int, dt.date)), f"unexpected value type: {type(value)}"
        return lqp.Constant(value), type_from_constant(value)

def _translate_to_atom(ctx: TranslationCtx, task: ir.Lookup) -> lqp.Formula:
    # TODO: want signature not name
    rel_name = task.relation.name
    terms = []
    sig_types = []
    for arg in task.args:
        if isinstance(arg, ir.PyValue):
            assert isinstance(arg, lqp.PrimitiveValue)
            term = lqp.Constant(arg)
            terms.append(term)
            t = type_from_constant(arg)
            sig_types.append(t)
            continue
        elif isinstance(arg, ir.Literal):
            term = lqp.Constant(arg.value)
            terms.append(term)
            t = type_from_constant(arg.value)
            sig_types.append(t)
            continue
        assert isinstance(arg, ir.Var), f"expected var, got {type(arg)}: {arg}"
        term, t = _translate_term(ctx, arg)
        terms.append(term)
        sig_types.append(t)

    # TODO: wrong
    if rel_builtins.is_builtin(task.relation):
        lqp_name = relname_to_lqp_name(task.relation.name)
        return lqp.Primitive(lqp_name, terms)

    if helpers.is_external(task.relation):
        return lqp.RelAtom(
            task.relation.name,
            terms,
        )

    rid = get_relation_id(ctx, rel_name, sig_types)
    return lqp.Atom(rid, terms)

def get_relation_id(ctx: TranslationCtx, name: str, types: list[lqp.PrimitiveType]) -> lqp.RelationId:
    relation_id = name_to_id(name)
    ctx.id_to_orig_name[relation_id] = name
    return relation_id

# TODO: should this take types too?
# TODO: should we use unique numbers instead of hashes?
def name_to_id(name: str) -> lqp.RelationId:
    return lqp.RelationId(lqp_hash(name))

def translate_bindings(ctx: TranslationCtx, bindings: list[ir.Value]) -> Tuple[list[Tuple[lqp.Var, lqp.RelType]], list[lqp.Formula]]:
    lqp_vars = []
    conjuncts = []
    for binding in bindings:
        lqp_var, typ, eq = binding_to_lqp_var(ctx, binding)
        lqp_vars.append((lqp_var, typ))
        if eq is not None:
            conjuncts.append(eq)

    return lqp_vars, conjuncts

def binding_to_lqp_var(ctx: TranslationCtx, binding: ir.Value) -> Tuple[lqp.Var, lqp.RelType, lqp.Union[None, lqp.Formula]]:
    if isinstance(binding, ir.Var):
        var, typ = _translate_term(ctx, binding)
        assert isinstance(var, lqp.Var)
        return var, typ, None
    else:
        # Constant in this case
        assert isinstance(binding, lqp.PrimitiveValue)
        value, typ = _translate_term(ctx, binding)

        # TODO: gensym
        var_name = ctx.unique_names.get_name_by_id(1, "cvar")
        var = lqp.Var(var_name)
        eq = lqp.Primitive("rel_primitive_eq", [var, value])
        return var, typ, eq
