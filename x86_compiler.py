
import sys

SYSCALL_MAP = {
    'exit': '0x2000001' if sys.platform == 'darwin' else '60'
}


PARAM_REGISTERS = ['RDI', 'RSI', 'RDX']

def emit(depth, code):
    print("   " * depth + code)

def emit_exit_syscall():
    emit(1, 'MOV RDI, RAX')
    emit(1, 'MOV RAX, {}'.format(SYSCALL_MAP['exit']))
    emit(1, 'SYSCALL')

def emit_prefix():
    """
    Emit a global prefix and an implementation of the plus function
    """

    emit(1, '.global _main\n')
    emit(1, '.text\n')

    emit(0, 'plus:')
    emit(1, 'ADD RDI, RSI')
    emit(1, 'MOV RAX, RDI')
    emit(1, 'RET\n')

    emit(0, '_main:')
