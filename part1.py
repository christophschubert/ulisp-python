
import sys

import parser

SYSCALL_MAP = {
    'exit': '0x2000001' if sys.platform == 'darwin' else '60'
}


def emit(depth, code):
    print("   " * depth + code)

def compile_argument(arg, destination):
    if isinstance(arg, list):
        compile_call(arg[0], arg[1:], destination)
        return
    emit(1, "MOV {}, {}".format(destination, arg))

BUILDIN_FUNCTIONS = { '+': 'plus'}
PARAM_REGISTERS = ['RDI', 'RSI', 'RDX']

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

def emit_prefix():
    emit(1, '.global _main\n')
    emit(1, '.text\n')

    emit(0, 'plus:')
    emit(1, 'ADD RDI, RSI')
    emit(1, 'MOV RAX, RDI')
    emit(1, 'RET\n')

    emit(0, '_main:')


def emit_postfix():
    emit(1, 'MOV RDI, RAX')
    emit(1, 'MOV RAX, {}'.format(SYSCALL_MAP['exit']))
    emit(1, 'SYSCALL')



if __name__ == '__main__':
    program = sys.argv[1] if len(sys.argv) > 1 else '(+ 3 (+ 1 2))'
    ast = parser.parse(program)
    emit_prefix()
    compile_call(ast[0], ast[1:], None)
    emit_postfix()
