# Extension with user defined functions

import parser
from x86_compiler import emit, emit_prefix, emit_exit_syscall,  PARAM_REGISTERS


"""
Since function definitions look like function calls in S expressions, we need
to keep a list of primitive functions calls (such as 'def') which we handle
differently.
"""

import sys

BUILDIN_FUNCTIONS = { '+': 'plus'}

def compile_define(f_def, destination, scope):
    name, parameters, *body = f_def

    scope[name] = name.replace('-', '_')

    # TODO: properly deal with child_scope:
    child_scope = scope.copy()
    emit(0, f'{scope[name]}:')
    for i, param in enumerate(parameters):
        child_scope[param] = PARAM_REGISTERS[i]

    compile_expression(body[0], 'RAX', child_scope)

    emit(1, 'RET\n')

PRIMITIVE_FUNCTIONS = {
    'def': compile_define
}

def compile_expression(arg, destination, scope):
    if isinstance(arg, list):
        compile_call(arg[0], arg[1:], destination, scope)
    elif scope.get(arg) or isinstance(arg, int):
        p = scope.get(arg, arg)
        emit(1, f'MOV {destination}, {p}')
    else:
        pass # should exit with error


def compile_call(fun, args, destination, scope):
    if PRIMITIVE_FUNCTIONS.get(fun):
        PRIMITIVE_FUNCTIONS.get(fun)(args, destination, scope)
        return

    for a, reg in zip(args, PARAM_REGISTERS):
        emit(1, "PUSH {}".format(reg))
    for a, reg in zip(args, PARAM_REGISTERS):
        compile_expression(a, reg, scope)
    valid_function = BUILDIN_FUNCTIONS.get(fun, scope.get(fun))
    if valid_function:
        emit(1, f'CALL {valid_function}')
    else:
        pass # should throw error!

    for a, reg in list(zip(args, PARAM_REGISTERS))[::-1]:
        emit(1, 'POP ' + reg)
    if destination and destination != 'RAX':
        emit(1, f'MOV {destination}, RAX')

if __name__ == '__main__':
    program = sys.argv[1] if len(sys.argv) > 1 else '(+ 3 (+ 1 2))'
    ast = parser.parse(program)
    emit_prefix()
    compile_call(ast[0], ast[1:], 'RAX', {})

    # the 'main' program
    emit(1, 'CALL main')

    emit_exit_syscall()
