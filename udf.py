# Extension with user defined functions

import parser
from x86_compiler import emit, emit_prefix, emit_exit_syscall, PARAM_REGISTERS


"""
Since function definitions look like function calls in S expressions, we need
to keep a list of primitive functions calls (such as 'def') which we handle
differently.
"""

import sys

BUILDIN_FUNCTIONS = { '+': 'plus'}

def compile_define(f_def, destination, scope):
    LOCAL_REGISTERS = ['RBX', 'RBP', 'R12']

    name, parameters, *body = f_def

    scope[name] = name.replace('-', '_')

    child_scope = scope.copy()
    emit(0, f'{scope[name]}:')
    for param, param_reg, local_reg in zip(parameters, PARAM_REGISTERS, LOCAL_REGISTERS):
        emit(1, f'PUSH {local_reg}')
        emit(1, f'MOV {local_reg}, {param_reg}')
        child_scope[param] = local_reg

    compile_expression(body[0], 'RAX', child_scope)

    for a, reg in list(zip(parameters, LOCAL_REGISTERS))[::-1]:
        emit(1, 'POP ' + reg)

    emit(1, 'RET\n')

PRIMITIVE_FUNCTIONS = {
    'def': compile_define
}

def compile_expression(arg, destination, scope):
    if isinstance(arg, list):
        compile_call(arg[0], arg[1:], destination, scope)
    elif scope.get(arg) or isinstance(arg, int):
        emit(1, f'MOV {destination}, {scope.get(arg, arg)}')
    else:
        raise "referenced undef variable"


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
        raise "ERROR, unknown function " + fun

    for a, reg in list(zip(args, PARAM_REGISTERS))[::-1]:
        emit(1, 'POP ' + reg)
    if destination and destination != 'RAX':
        emit(1, f'MOV {destination}, RAX')

if __name__ == '__main__':

    scope = {}
    emit_prefix()
    for line in sys.stdin:
        ast = parser.parse(line)
        compile_call(ast[0], ast[1:], 'RAX', scope)

    # the '_main' program
    emit(0, '_main:')
    emit(1, 'CALL main')

    emit_exit_syscall()
