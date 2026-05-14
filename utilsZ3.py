from z3 import *
import re



set_param(max_lines=1, max_width=1000000)


# Function to extract variable names from the expression and create Z3 Boolean variables
def extract_variables_mono(expr):
    # expr = expr.replace('!', ' ~').replace('&', ' & ').replace('|', ' | ')
    # Use a regular expression to find all variable names
    names = list(re.findall(r'v_[a-zA-Z0-9_]+', expr))
    repressor_names = [match[1:] for match in re.findall(r'!v_[a-zA-Z0-9_]+', expr)]
    acceptor_names = []
    for variable_name in names:
        if variable_name not in repressor_names:
            acceptor_names.append(variable_name)
    # Create a dictionary of Z3 Boolean variables
    return {name: Bool(name) for name in acceptor_names}, {name: Bool(name) for name in repressor_names}
def extract_variables(expr):
    # expr = expr.replace('!', ' ~').replace('&', ' & ').replace('|', ' | ')
    # Use a regular expression to find all variable names
    names = list(re.findall(r'v_[a-zA-Z0-9_]+', expr))
    return {name: Bool(name) for name in names}

def encode_variables(a, r):
    encoded_a = {}
    encoded_r = {}
    variables = {}
    for i in range(len(a)):
        encoded_a[i] = Bool(f"x[{i}]")
        variables[f"x[{i}]"] = Bool(f"x[{i}]")
    for i in range(len(r)):
        encoded_r[i] = Bool(f"y[{i}]")
        variables[f"y[{i}]"] = Bool(f"y[{i}]")
    return encoded_a, encoded_r, variables



def parse_expression(expr, variables):
    expr = expr.replace('!', ' ! ').replace('&', ' & ').replace('|', ' | ')
    expr = expr.replace('(', ' ( ').replace(')', ' ) ')
    tokens = expr.split()

    # Initialize operator and operand stacks for parsing
    operator_stack = []
    operand_stack = []

    def apply_operator():
        """Applies the last operator on the operator stack to the last operands."""
        operator = operator_stack.pop()
        if operator == 'Not':
            operand = operand_stack.pop()
            operand_stack.append(Not(operand))
        else:
            right = operand_stack.pop()
            left = operand_stack.pop()
            if operator == 'And':
                operand_stack.append(And(left, right))
            elif operator == 'Or':
                operand_stack.append(Or(left, right))

    # Mapping from symbol to function
    op_map = {'!': 'Not', '&': 'And', '|': 'Or'}
    precedence = {'Not': 3, 'And': 2, 'Or': 1}
    for token in tokens:
        if token in variables:
            # If the token is a variable, push its Z3 variable onto the operand stack
            operand_stack.append(variables[token])
        elif token == '(':
            operator_stack.append(token)
        elif token == ')':
            # Apply all operators until matching '('
            while operator_stack and operator_stack[-1] != '(':
                apply_operator()
            operator_stack.pop()  # Remove the '('
        elif token in op_map:
            # If the token is an operator, apply any higher precedence operators first
            op = op_map[token]
            while (operator_stack and operator_stack[-1] != '(' and
                   precedence[operator_stack[-1]] >= precedence[op]):
                apply_operator()
            operator_stack.append(op)
        elif token == '!':
            # Not operator has a high precedence; map to "Not"
            operator_stack.append('Not')

    # Apply remaining operators
    while operator_stack:
        apply_operator()

    # Final result
    return operand_stack[0]

def prove(f):
    s = Solver()
    s.add(Not(f))
    if s.check() == unsat:
        print("proved")
    else:
        print("failed to prove")


def checkSymmetry(expr):
    # find x1,x2 EA and Y for inhibitors s.t: f(x1,Y) \neq f(x2,Y) else return AS
    # find x1,x2 ER and Y for activators s.t: f(x1,Y) \neq f(x2,Y) else return RS

    # x is an array of activators
    x1 = BitVec('x1', 5)  # [ 0 0 0 0 0 ]
    x2 = BitVec('x2', 5)  # [ 0 0 0 0 0 ]

    Y = BitVec('Y', 5)

    f = Function('f', BitVecSort(), BitVecSort(), BitVecSort())

    # conditions to define EA
    # UGT(x1, 0)
    # ULT(x1, (2^5)-1)
    # UGT(x2, 0)
    # ULT(x2, (2 ^ 5) - 1)

    s = Solver()
    s.add(UGT(x1, 0), ULT(x1, (2 ^ 5) - 1), UGT(x2, 0), ULT(x2, (2 ^ 5) - 1))  # Add definition for EA
    s.add(f(x1, Y) != f(x2, Y))  # then

    # loop on every  variable and give value from bitvec

    s.add(substitute())

    # Are activators symmetric
    X1 = Array('X1', BoolSort(), BoolSort())  # Boolean Array of Activators
    X2 = Array('X2', BoolSort(), BoolSort())  # Boolean Array of Activators

    Y = Array('Y', BoolSort(), BoolSort())  # Boolean array of Repressors

    # Undefined function from (Array,Array) to Bool
    f = Function('f', ArraySort(), ArraySort(), BoolSort())

    s = Solver()
    s.add()  # Add definition for EA
    s.add()  # Add definition for ER
    s.add(f(X1, Y) == f(X2, Y))  # then

    # Are inhibitors symmetric

