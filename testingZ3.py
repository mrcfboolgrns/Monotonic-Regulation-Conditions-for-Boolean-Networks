import itertools
import copy

from z3 import *
import utilsZ3


def check_symmetry(input_expr, component=0):
    set_param(max_lines=1, max_width=1000000)
    acceptors, repressors = utilsZ3.extract_variables_mono(input_expr)
    variables = copy.deepcopy(acceptors)
    variables.update(repressors)
    # Convert input_expr to Z3 Boolean expression
    expr = utilsZ3.parse_expression(input_expr, variables)
    # Create a z3 Boolean array of 3 elements
    map = [acceptors, repressors]
    x1 = [Bool(f'x1_{i}') for i in map[component]]
    x2 = [Bool(f'x2_{i}') for i in map[component]]
    # Create a z3 Boolean array of 2 elements
    y = [Bool(f'y_{i}') for i in map[(component + 1) % 2]]

    f1 = expr
    f2 = expr

    counter = 0
    for key in map[component]:
        f1 = substitute(f1, (map[component][key], x1[counter]))
        f2 = substitute(f2, (map[component][key], x2[counter]))
        counter += 1
    counter = 0
    for key in map[(component + 1) % 2]:
        f1 = substitute(f1, (map[(component + 1) % 2][key], y[counter]))
        f2 = substitute(f2, (map[(component + 1) % 2][key], y[counter]))
        counter += 1

    # Define a z3 solver
    s = Solver()

    # Add the constraint that f(x1,y) != f(x2,y)
    s.add(f1 != f2)
    # print(s)

    # Add the constraint that x1 != x2
    # t = BoolSortRef
    if len(x1) > 0:
        t = (x1[0] != x2[0])
        for i in range(1, len(x1)):
            t = Or(t, x1[i] != x2[i])
        s.add(t)

        # Add the constraint that at least one element of x1 is true
        t = (x1[0])
        for i in range(1, len(x1)):
            t = Or(t, x1[i])
        s.add(t)
        t = (x2[0])
        for i in range(1, len(x2)):
            t = Or(t, x2[i])
        s.add(t)
        # Add the constraint that at least one element of x2 is true
        # Add the constraint that at least one element of x1 is false
        t = Not(x1[0])
        for i in range(1, len(x1)):
            t = Or(t, Not(x1[i]))
        s.add(t)

        # Add the constraint that at least one element of x2 is false
        t = Not(x2[0])
        for i in range(1, len(x2)):
            t = Or(t, Not(x2[i]))
        s.add(t)

    # Check if the constraints are unsatisfiable
    if s.check() == sat:
        return False
    elif len(y) == 0:
        return True
    elif component == 0:
        return check_symmetry(input_expr, component=1)
    elif component == 1 and s.check() == unsat:
        return True


def check_mono(input_expr):
    set_param(max_lines=1, max_width=1000000)
    variables = utilsZ3.extract_variables(input_expr)

    # Convert input_expr to Z3 Boolean expression
    expr = utilsZ3.parse_expression(input_expr, variables)

    f1 = expr
    f2 = expr
    f3 = expr
    f4 = expr

    x = Int('x')

    y1, y2, y3, y4 = [], [], [], []

    for i in variables:
        y1.append(Bool(f'y1_{i}'))
        y2.append(Bool(f'y2_{i}'))
        y3.append(Bool(f'y3_{i}'))
        y4.append(Bool(f'y4_{i}'))

    counter = 0
    for key in variables:
        f1 = substitute(f1, (variables[key], y1[counter]))
        f2 = substitute(f2, (variables[key], y2[counter]))
        f3 = substitute(f3, (variables[key], y3[counter]))
        f4 = substitute(f4, (variables[key], y4[counter]))
        counter += 1

    # Define a z3 solver
    s = Solver()
    s.add(x >= 0, x < len(variables))
    if len(y1) > 2:
        for i, variable in enumerate(variables):
            s.add(If(x == i, And(y1[i] == True, y2[i] == False), y1[i] == y2[i]))
            s.add(If(x == i, And(y3[i] == True, y4[i] == False), y3[i] == y4[i]))

        # counter = 0
        # for key in vars:
        #     s.add(substitute(f1, (vars[key], y1[counter])))
        #     s.add(substitute(f2, (vars[key], y2[counter])))
        # #     s.add(substitute(f3, (vars[key], y3[counter])))
        # #     s.add(substitute(f4, (vars[key], y4[counter])))
        #     counter += 1
        #
        # s.add(And(f1 == True, f2 == False))
        s.add(And(f1 == True, f2 == False, f3 == False, f4 == True))

        if s.check() == sat:
            return False
    return True

def check_WS(input_expr):
    set_param(max_lines=1, max_width=1000000)
    variables = utilsZ3.extract_variables(input_expr)
    acceptors, repressors = utilsZ3.extract_variables_mono(input_expr)
    input_expr = utilsZ3.parse_expression(input_expr, variables)
    a = check_symmetry_and_monotonicity(input_expr,acceptors,repressors)
    if not a[0]:
        return False
    return a[1]


def check_symmetry_and_monotonicity(input_expr, A_vars, R_vars):
    """
    Checks if there is a partition of A into {WA, SA} and R into {WR, SR} such that:
    1. All 4 groups are internally symmetric.
    2. The Monotonicity/Strength equations are satisfied:
       - WA < SA: Switching a WA OFF and SA ON increases function value.
       - WR < SR: Switching a WR OFF and SR ON decreases function value
                  (or equivalently: WR=1, SR=0 yields higher output than WR=0, SR=1).
    """

    # 1. Setup Variables
    # ---------------------------------------------------------
    # Combine all variables and map them to Z3 Bools
    all_vars = list(set(A_vars) | set(R_vars))
    # Ensure variables are Z3 BoolRefs
    z3_vars = {str(v): Bool(str(v)) for v in all_vars}

    # Define group mapping: 0:WA, 1:SA, 2:WR, 3:SR
    group = {v: Int(f'group_{v}') for v in all_vars}

    s = Solver()

    # 2. Domain Constraints
    # ---------------------------------------------------------
    # Variables in A must be WA (0) or SA (1)
    for v in A_vars:
        s.add(Or(group[v] == 0, group[v] == 1))

    # Variables in R must be WR (2) or SR (3)
    for v in R_vars:
        s.add(Or(group[v] == 2, group[v] == 3))

    # 3. Helper Functions for Logic Checks
    # ---------------------------------------------------------
    def check_always_true(condition):
        """Returns True if the Z3 condition is valid for ALL assignments."""
        check_s = Solver()
        check_s.add(Not(condition))
        return check_s.check() == unsat

    def get_swapped_values(expr, u, v, val_u, val_v):
        """Returns expr with u replaced by val_u and v replaced by val_v."""
        temp = substitute(expr, (z3_vars[str(u)], BoolVal(val_u)))
        return substitute(temp, (z3_vars[str(v)], BoolVal(val_v)))

    # Pre-compute relationships between pairs to avoid high-cost quantifiers in the main solver
    # We store these as boolean flags (True/False)

    # Matrix for Symmetry: sym[u][v] is True if swapping u,v doesn't change output
    is_symmetric = {}
    # Matrix for WA < SA: swap_le[u][v] is True if f(u=1,v=0) <= f(u=0,v=1)
    swap_le = {}
    # Matrix for WR < SR: swap_ge[u][v] is True if f(u=1,v=0) >= f(u=0,v=1)
    swap_ge = {}

    # We only need to compare pairs within A and pairs within R
    relevant_pairs = list(itertools.combinations(A_vars, 2)) + \
                     list(itertools.combinations(R_vars, 2))

    # Add self-loops to handle single-element groups correctly if needed,
    # though combinations usually suffice for pair constraints.

    for u, v in relevant_pairs:
        # A. Symmetry Check
        # -----------------
        # f(..., u, v, ...) == f(..., v, u, ...)
        # We define symmetry as: swapping u and v results in equivalent expression
        # To test: substitute u->temp, v->u, temp->v
        t = Bool('t')
        s1 = substitute(input_expr, (z3_vars[str(u)], t))
        s1 = substitute(s1, (z3_vars[str(v)], z3_vars[str(u)]))
        expr_swapped = substitute(s1, (t, z3_vars[str(v)]))

        is_sym = check_always_true(input_expr == expr_swapped)
        is_symmetric[(u, v)] = is_sym
        is_symmetric[(v, u)] = is_sym  # Symmetry is commutative

        # B. Strength/Order Checks
        # ------------------------
        # Calculate f(u=1, v=0) and f(u=0, v=1)
        # Note: We keep all other variables symbolic!
        f_10 = get_swapped_values(input_expr, u, v, True, False)
        f_01 = get_swapped_values(input_expr, u, v, False, True)

        # Check if f(1,0) <= f(0,1) holds for all inputs (Used for WA vs SA)
        # This implies switching u OFF and v ON increases value -> v is stronger activator
        le_check = check_always_true(Implies(f_10, f_01))  # logical implication acts as <= for bools
        swap_le[(u, v)] = le_check

        # Check reverse for the pair (v stronger than u)
        le_check_rev = check_always_true(Implies(f_01, f_10))
        swap_le[(v, u)] = le_check_rev

        # Check if f(1,0) >= f(0,1) holds for all inputs (Used for WR vs SR)
        # This implies u=1 (Weak Repressor) allows higher value than v=1 (Strong Repressor)
        # i.e., v is a stronger repressor.
        ge_check = check_always_true(Implies(f_01, f_10))  # logical implication acts as <= for bools
        swap_ge[(u, v)] = ge_check

        # Check reverse
        ge_check_rev = check_always_true(Implies(f_10, f_01))
        swap_ge[(v, u)] = ge_check_rev

    # 4. Apply Constraints to the Main Solver
    # ---------------------------------------------------------
    for u, v in relevant_pairs:
        # Constraint 1: If in same group, must be symmetric
        # (group[u] == group[v]) -> is_symmetric[(u,v)]
        if not is_symmetric.get((u, v), False):
            s.add(group[u] != group[v])

        # Constraint 2: WA (0) vs SA (1)
        # Eq 3.2: f(X1, Y0) <= f(X0, Y1) implies if u is WA and v is SA, u is "weaker"
        # If u=WA and v=SA, then swap_le[u][v] must be True
        s.add(Implies(And(group[u] == 0, group[v] == 1), BoolVal(swap_le.get((u, v), False))))
        s.add(Implies(And(group[u] == 1, group[v] == 0), BoolVal(swap_le.get((v, u), False))))

        # Constraint 3: WR (2) vs SR (3)
        # Eq 3.3: f(Z1, W0) >= f(Z0, W1) implies if u is WR and v is SR, u allows higher output
        # If u=WR and v=SR, then swap_ge[u][v] must be True
        s.add(Implies(And(group[u] == 2, group[v] == 3), BoolVal(swap_ge.get((u, v), False))))
        s.add(Implies(And(group[u] == 3, group[v] == 2), BoolVal(swap_ge.get((v, u), False))))

    # 5. Solve
    # ---------------------------------------------------------
    if s.check() == sat:
        m = s.model()
        result_groups = {"WA": [], "SA": [], "WR": [], "SR": []}
        name_map = {0: "WA", 1: "SA", 2: "WR", 3: "SR"}

        for v in all_vars:
            g_id = m[group[v]].as_long()
            result_groups[name_map[g_id]].append(str(v))

        return True, result_groups

    return False, None




