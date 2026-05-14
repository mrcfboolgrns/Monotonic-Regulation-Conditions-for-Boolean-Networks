import os

from z3 import *

import testingZ3
import utilsZ3


def sim(i, j, target_component, formula, variables):
    s = Solver()
    
    set_param(max_lines=1, max_width=1000000)
    variables = utilsZ3.extract_variables(formula)
    input_expr = utilsZ3.parse_expression(formula, variables)
    wsar = testingZ3.check_WS(formula)
    wa = wsar.get("WA")
    sa = wsar.get("SA")
    wr = wsar.get("WR")
    sr = wsar.get("SR")
    after_wa = input_expr
    if i%3 == 2:
        after_wa = eval_under_assignment(input_expr,a(wa))
    elif i%3 == 1:
        after_wa = eval_under_assignment(input_expr,e(wa,'a'))
    elif i%3 == 0:
        after_wa = eval_under_assignment(input_expr,n(wa))
    if after_wa is True or after_wa is False:
        return after_wa
    after_sa = after_wa
    if i//3 == 2:
        after_sa = eval_under_assignment(after_wa,a(sa))
    elif i//3 == 1:
        after_sa = eval_under_assignment(after_wa,e(sa,'a'))
    elif i//3 == 0:
        after_sa = eval_under_assignment(after_wa,n(sa))
    if after_sa is True or after_sa is False:
        return after_sa
    after_wr = after_sa
    if j%3 == 2:
        after_wr = eval_under_assignment(after_sa,a(wr))
    elif j%3 == 1:
        after_wr = eval_under_assignment(after_sa,e(wr,'r'))
    elif j%3 == 0:
        after_wr = eval_under_assignment(after_sa,n(wr))
    if after_wr is True or after_wr is False:
        return after_wr
    after_sr = after_wr
    if j//3 == 2:
        after_sr = eval_under_assignment(after_wr,a(sr))
    elif j//3 == 1:
        after_sr = eval_under_assignment(after_wr,e(sr,'r'))
    elif j//3 == 0:
        after_sr = eval_under_assignment(after_wr,n(sr))
    if after_sr is True or after_sr is False:
        return after_sr
    else:
        return "-"



def a(components):
    return {component: True for component in components}


def n(components):
    return {component: False for component in components}


def e(components, r_type):
    if len(components) > 1:
        d = {components[i]: i % 2 == 0 for i in range(len(components))}
    elif r_type == 'r':
        d = {components[i]: False for i in range(len(components))}
    else:
        d = {components[i]: True for i in range(len(components))}
    return d


def eval_under_assignment(expr, assignments):


    """
    expr: a Z3 expression
    assignments: dict mapping Z3 variables to Python/Z3 values
                 example: {x: 3, y: 5, p: True}

    Returns:
        True / False if the expression becomes a concrete Boolean
    """
    subs = []

    for var, val in assignments.items():
        if isinstance(var, str):
            z3_var = Bool(var)
            if is_expr(val):
                z3_val = val
            elif isinstance(val, bool):
                z3_val = BoolVal(val)
            elif isinstance(val, int):
                z3_val = IntVal(val)
            elif isinstance(val, float):
                z3_val = RealVal(val)
            else:
                raise TypeError(f"Unsupported value for {var}: {type(val)}")
        else:
            z3_var = var
            sort = var.sort()

            if sort == BoolSort():
                z3_val = BoolVal(val) if not is_expr(val) else val
            elif sort == IntSort():
                z3_val = IntVal(val) if not is_expr(val) else val
            elif sort == RealSort():
                z3_val = RealVal(val) if not is_expr(val) else val
            else:
                raise TypeError(f"Unsupported sort for {var}: {sort}")

        subs.append((z3_var, z3_val))

    evaluated = simplify(substitute(expr, *subs))

    if is_true(evaluated):
        return True
    if is_false(evaluated):
        return False

    return evaluated


# sim(0)
