import os

from z3 import *

import testingZ3
import utilsZ3


def sim(target_dictionary, target_component):
    # dire = "[id-144]__[var-146]__[in-56]__[SNF1-AMPK-PATHWAY]"
    path = 'biodivine-boolean-models/models'  # the BBM dataset is downloaded
    os.chdir(path)
    # os.chdir(dire)
    s = Solver()
    for f in os.listdir():
        if f.endswith('.bnet'):
            file = f
    with open(file, 'rb') as f:
        content = f.readlines()  # Decode from bytes to string
        for line in content[1:]:
            line = line.decode('utf-8')
            # Splitting by comma and extracting the right-hand side (the Boolean formula)
            if ',' in line:
                # Ensure variables are Z3 BoolRefs
                target, formula = line.strip().split(',', 1)
                if target_component == target:
                    set_param(max_lines=1, max_width=1000000)
                    variables = utilsZ3.extract_variables(formula)
                    input_expr = utilsZ3.parse_expression(formula, variables)
                    a = testingZ3.check_WS(formula)
                    wa = a.get("WA")
                    sa = a.get("SA")
                    wr = a.get("WR")
                    sr = a.get("SR")
                    after_wa = input_expr
                    if target_dictionary.get("wa") == "a":
                        after_wa = eval_under_assignment(input_expr,a(wa))
                    elif target_dictionary.get("wa") == "e":
                        after_wa = eval_under_assignment(input_expr,e(wa,'a'))
                    elif target_dictionary.get("wa") == "n":
                        after_wa = eval_under_assignment(input_expr,n(wa))
                    if after_wa is True or after_wa is False:
                        return after_wa
                    after_sa = after_wa
                    if target_dictionary.get("sa") == "a":
                        after_sa = eval_under_assignment(after_wa,a(sa))
                    elif target_dictionary.get("sa") == "e":
                        after_sa = eval_under_assignment(after_wa,e(sa,'a'))
                    elif target_dictionary.get("sa") == "n":
                        after_sa = eval_under_assignment(after_wa,n(sa))
                    if after_sa is True or after_sa is False:
                        return after_sa
                    after_wr = after_sa
                    if target_dictionary.get("wr") == "a":
                        after_wr = eval_under_assignment(after_sa,a(wr))
                    elif target_dictionary.get("wr") == "e":
                        after_wr = eval_under_assignment(after_sa,e(wr,'r'))
                    elif target_dictionary.get("wr") == "n":
                        after_wr = eval_under_assignment(after_sa,n(wr))
                    if after_wr is True or after_wr is False:
                        return after_wr
                    after_sr = after_wr
                    if target_dictionary.get("sr") == "a":
                        after_sr = eval_under_assignment(after_wr,a(sr))
                    elif target_dictionary.get("sr") == "e":
                        after_sr = eval_under_assignment(after_wr,e(sr,'r'))
                    elif target_dictionary.get("sr") == "n":
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
        d = {components[i]: True for i in range(len(components)) if i % 2 == 0}
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
        sort = var.sort()

        if sort == BoolSort():
            z3_val = BoolVal(val) if not is_expr(val) else val
        elif sort == IntSort():
            z3_val = IntVal(val) if not is_expr(val) else val
        elif sort == RealSort():
            z3_val = RealVal(val) if not is_expr(val) else val
        else:
            raise TypeError(f"Unsupported sort for {var}: {sort}")

        subs.append((var, z3_val))

    evaluated = simplify(substitute(expr, *subs))

    if is_true(evaluated):
        return True
    if is_false(evaluated):
        return False

    return evaluated


# sim(0)
