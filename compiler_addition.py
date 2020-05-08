# Compile S expressions involving '+' as function symbol and integer arguments into
# x86 assembler.
#
# Sample usage:
# python compiler_addition '(+ 3 (+ 1 (+ 4 2)))' > program.S
# gcc -mstackrealign -masm=intel -o program program.S
# ./program
# echo $?


import sys

import parser
from x86_compiler import emit, emit_prefix, emit_exit_syscall, PARAM_REGISTERS


def compile_argument(arg, destination):
    if isinstance(arg, list):
        compile_call(arg[0], arg[1:], destination)
        return
    emit(1, "MOV {}, {}".format(destination, arg))

BUILDIN_FUNCTIONS = { '+': 'plus'}

def compile_call(fun, args, destination):
    for a, reg in zip(args, PARAM_REGISTERS):
        emit(1, "PUSH {}".format(reg))
    for a, reg in zip(args, PARAM_REGISTERS):
        compile_argument(a, reg)
    emit(1, 'CALL {}'.format(BUILDIN_FUNCTIONS.get(fun, fun)))
    for a, reg in list(zip(args, PARAM_REGISTERS))[::-1]:
        emit(1, 'POP ' + reg)
    if destination:
        emit(1, 'MOV {}, RAX'.format(destination))
    emit(0, '')





if __name__ == '__main__':
    program = sys.argv[1] if len(sys.argv) > 1 else '(+ 3 (+ 1 2))'
    ast = parser.parse(program)
    emit_prefix()
    compile_call(ast[0], ast[1:], None)
    emit_exit_syscall()
