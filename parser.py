# Parser for S expressions

def parse(program):
    return parse_rec([], program)[0][0]

def parse_rec(ast, program):
    current_token = ''
    for pos, c in enumerate(program):
        if c == '(':
            sub_ast, rest = parse_rec([], program[pos+1:])
            ast.append(sub_ast)
            return parse_rec(ast, rest)
        elif c == ')':
            if current_token:
                ast.append(convert_to_int(current_token))
            return [ast, program[pos+1:]]
        elif c == ' ':
            ast.append(convert_to_int(current_token))
            current_token = ''
        else:
            current_token += c
    return (ast, program)

def convert_to_int(s):
    try:
        return int(s)
    except Exception as e:
        return s
