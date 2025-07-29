from relationalai.early_access.lqp import ir as lqp
from relationalai.early_access.lqp.utils import UniqueNames
from relationalai.early_access.metamodel import ir

rel_to_lqp = {
    "+": "rel_primitive_add",
    "-": "rel_primitive_subtract",
    "*": "rel_primitive_multiply",
    "/": "rel_primitive_divide",
    "=": "rel_primitive_eq",
    "!=": "rel_primitive_neq",
    "<=": "rel_primitive_lt_eq",
    ">=": "rel_primitive_gt_eq",
    ">": "rel_primitive_gt",
    "<": "rel_primitive_lt",
    "abs": "rel_primitive_abs",
    "construct_date": "rel_primitive_construct_date",
    "construct_datetime": "rel_primitive_construct_datetime",
    "starts_with": "rel_primitive_starts_with",
    "ends_with": "rel_primitive_ends_with",
    "contains": "rel_primitive_contains",
    "num_chars": "rel_primitive_num_chars",
    "substring": "rel_primitive_substring",
    "like_match": "rel_primitive_like_match",
    "concat": "rel_primitive_concat",
    "replace": "rel_primitive_replace",
    "date_year": "rel_primitive_date_year",
    "date_month": "rel_primitive_date_month",
    "date_day": "rel_primitive_date_day",
}

def relname_to_lqp_name(name: str) -> str:
    # TODO: do these proprly
    if name in rel_to_lqp:
        return rel_to_lqp[name]
    else:
        raise NotImplementedError(f"missing primitive case: {name}")

def lqp_sum_op(names: UniqueNames) -> lqp.Abstraction:
    # TODO: make sure gensym'd properly
    x = lqp.Var(names.get_name("x"))
    y = lqp.Var(names.get_name("y"))
    z = lqp.Var(names.get_name("z"))
    # TODO: Extract a more refined type from the op relation
    INT = lqp.PrimitiveType.INT
    ts = [(x, INT), (y, INT), (z, INT)]

    body = lqp.Primitive("rel_primitive_add", [x, y, z])
    return lqp.Abstraction(ts, body)

def lqp_max_op(names: UniqueNames) -> lqp.Abstraction:
    # TODO: make sure gensym'd properly
    x = lqp.Var(names.get_name("x"))
    y = lqp.Var(names.get_name("y"))
    z = lqp.Var(names.get_name("z"))
    # TODO: Extract a more refined type from the op relation
    INT = lqp.PrimitiveType.INT
    ts = [(x, INT), (y, INT), (z, INT)]

    body = lqp.Primitive("rel_primitive_max", [x, y, z])
    return lqp.Abstraction(ts, body)

def lqp_min_op(names: UniqueNames) -> lqp.Abstraction:
    # TODO: make sure gensym'd properly
    x = lqp.Var(names.get_name("x"))
    y = lqp.Var(names.get_name("y"))
    z = lqp.Var(names.get_name("z"))
    # TODO: Extract a more refined type from the op relation
    INT = lqp.PrimitiveType.INT
    ts = [(x, INT), (y, INT), (z, INT)]

    body = lqp.Primitive("rel_primitive_min", [x, y, z])
    return lqp.Abstraction(ts, body)

def lqp_operator(names: UniqueNames, op: ir.Relation) -> lqp.Abstraction:
    if op.name == "sum":
        return lqp_sum_op(names)
    elif op.name == "count":
        return lqp_sum_op(names)
    elif op.name == "max":
        return lqp_max_op(names)
    elif op.name == "min":
        return lqp_min_op(names)
    else:
        raise NotImplementedError(f"Unsupported aggregation: {op.name}")
