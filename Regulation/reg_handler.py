import re

def tokenize_strict(expr):
    pattern = r'!|\(|\)|\&|\||[^()\s&|!]+(?:\s*\?\s*[^():\s]+\s*:\s*[^()\s]+)?'
    tokens = re.findall(pattern, expr)
    return [t.strip() for t in tokens if t.strip()]
def preprocess_negations(expr):
    # (1) Push ! inside parentheses if simple
    # !(X) => !X
    expr = re.sub(r'!\(\s*([a-zA-Z0-9_]+)\s*\)', r'!\1', expr)

    # (2) Push ! inside ternary expressions with TRUE/FALSE
    # !(edge_X ? Y : TRUE) => edge_X ? !Y : FALSE
    expr = re.sub(r'!\(\s*(edge_[a-zA-Z0-9_]+)\s*\?\s*([^:()]+?)\s*:\s*TRUE\s*\)', r'\1 ? !\2 : FALSE', expr)
    expr = re.sub(r'!\(\s*(edge_[a-zA-Z0-9_]+)\s*\?\s*([^:()]+?)\s*:\s*FALSE\s*\)', r'\1 ? !\2 : TRUE', expr)

    return expr

def parse_expr(tokens):
    def helper():
        current = []

        while tokens:
            token = tokens.pop(0)

            if token == '!':
                # Handle NOT: next must be a token or group
                if tokens[0] == '(':
                    tokens.pop(0)
                    inner = helper()
                    current.append(['NOT', inner])
                else:
                    operand = tokens.pop(0)
                    current.append(['NOT', [operand]])

            elif token == '(':
                current.append(helper())

            elif token == ')':
                break

            elif token == '&':
                current.append('AND')

            elif token == '|':
                current.append('OR')

            else:
                current.append([token])

        def group(op, lst):
            i = 0
            while i < len(lst):
                if lst[i] == op:
                    combined = [op, lst[i - 1], lst[i + 1]]
                    lst = lst[:i - 1] + [combined] + lst[i + 2:]
                    i -= 1
                else:
                    i += 1
            return lst

        current = group('AND', current)
        current = group('OR', current)

        return current[0] if len(current) == 1 else current

    return helper()
def extract_edges(expr):
    return [e.lstrip('!') for e in re.findall(r'!?edge_[a-zA-Z0-9_]+\s*\?', expr)]

def extract_edges1(expr):
    return re.findall(r'(edge_[a-zA-Z0-9_]+)\s*\?', expr)

def is_edge_condition(expr):
    return bool(re.match(r'!?edge_[a-zA-Z0-9_]+\s*\?', expr))

def fix_default_in_edge(expr, context, under_not=False):
    def replacer(match):
        condition = match.group(1)
        value_if_true = match.group(2)
        # Flip context if under_not is true
        default_value = 'TRUE' if (context == 'AND') ^ under_not else 'FALSE'
        default_value = 'TRUE' if (context == 'AND')  else 'FALSE'
        return f'{condition}?{value_if_true}:{default_value}'

    pattern = r'(edge_[a-zA-Z0-9_]+)\s*\?\s*([^:()]+)\s*:\s*(TRUE|FALSE)'
    return re.sub(pattern, replacer, expr)

def build_expr(tree, context=None, under_not=False):
    if isinstance(tree, str):
        expr = tree.strip()
        expr = fix_default_in_edge(expr, context, under_not)
        edges = extract_edges(expr)
        return expr, edges, is_edge_condition(expr)

    if isinstance(tree, list):
        if tree[0] == 'NOT':
            subexpr, edges, _ = build_expr(tree[1], context, under_not=not under_not)
            return f'!({subexpr})', edges, False

        if tree[0] in ('AND', 'OR'):
            op = ' & ' if tree[0] == 'AND' else ' | '
            subexprs = []
            all_edges = []
            is_all_edge_conds = True

            for child in tree[1:]:
                subexpr, edges, is_edge = build_expr(child, context=tree[0], under_not=under_not)
                subexprs.append(f'({subexpr})')
                all_edges.extend(edges)
                if not is_edge:
                    is_all_edge_conds = False

            combined_expr = op.join(subexprs)
            if tree[0] == 'OR' and all_edges and is_all_edge_conds and not under_not:
                fallback_cond = ' & '.join([f'!{e}' for e in all_edges])
                fallback_expr = f'({fallback_cond} ? TRUE : FALSE)'
                return f'({combined_expr} | {fallback_expr})', [], True
            elif tree[0]=='AND' and all_edges and is_all_edge_conds and not under_not:
                fallback_cond = ' & '.join([f'!{e}' for e in all_edges])
                fallback_expr = f'({fallback_cond} ? FALSE : TRUE)'
                return f'({combined_expr} | {fallback_expr})', [], True
            else:
                return f'({combined_expr})', [], False

        else:
            return build_expr(tree[0], context, under_not)

def fix_exp(expr):
    expr = preprocess_negations(expr)

    tokens = tokenize_strict(expr)
    print(tokens)
    tree = parse_expr(tokens)
    print(tree)
    expr, _, _ = build_expr(tree)
    return expr

if __name__ == '__main__':
    # expr="(((edge_b_d_positive ? b1:TRUE) ) | ((edge_c_d_positive ? c1:TRUE) )) & (a1 | (edge_c_d_positive ? c1:TRUE)))"
    # print(parse_expr(tokenize_strict(expr)))
    # print(fix_exp("(((edge_b_d_positive ? b1:TRUE) ) | ((edge_c_d_positive ? c1:TRUE) )) & (a1 | !(edge_c_d_positive ? c1:TRUE)))"))
    # print(fix_exp("!((edge_b_d_positive ? b1:FALSE) & !b)"))
    # print(fix_exp("((!(edge_b_d_positive ? b1 : TRUE)) | (edge_c_d_positive ? c1 : TRUE)) & (a1 | (edge_c_d_positive ? c1 : TRUE))"))
    # # Should use TRUE in the negated edge ternary (!...), FALSE in OR fallbacks
    #
    # print(fix_exp("!a & !b"))
    # # Should parse properly
    #
    # print(fix_exp("!((edge_x_y ? a : TRUE) & (edge_y_z ? b : TRUE))"))


    # print(fix_exp("((((((((C0) | (edge_D_res_positive?D0:FALSE))) | (((A0) & (B0))))) & (!(((E0) | (F0)))))) | (!(((G0) & (!(edge_H_res_negative?H0:TRUE))))))"))
    # print(fix_exp("(!((G0) & (!(edge_H_res_negative?H0:TRUE))"))

    print(fix_exp("((((D2|(edge_E_res_positive ? E2:FALSE) )))&(((A2|C2|(edge_B_res_positive ? B2:FALSE) )))&((((edge_F_res_positive ? F2:FALSE) ))))"))
    # Should become (edge_x_y ? a : FALSE) | (edge_y_z ? b : FALSE) | fallback
