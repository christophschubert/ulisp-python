# Parser for S expressions


def parse(program):
    """Parse the S expression program and convert integer literals to ints

    >>> parse('(+ 1 2)')
    ['+', 1, 2]
    >>> parse('(+ 1 (* 2 3)')
    ['+', 1, ['*', 2, 3]]
    >>> parse('(+ (* 1 2) 3)')
    ['+', ['*', 1, 2], 3]
    >>> parse('(+ (* 1 2) (- 3 2))')
    ['+', ['*', 1, 2], ['-', 3, 2]]
    >>> parse('(+ (* 1 2) (- 3 (+ 4 5)))')
    ['+', ['*', 1, 2], ['-', 3, ['+', 4, 5]]]
    >>> parse('(concat a b c (concat d e f))')
    ['concat', 'a', 'b', 'c', ['concat', 'd', 'e', 'f']]
    """
    return parse_runner(program)[0][0]

def parse_runner(program):
    """
    Returns a list of past tokens from program and the position in program up to
    which the program was parsed.
    """
    tokens = []
    current_pos = 0
    current_token = ''
    while current_pos < len(program):
        c = program[current_pos]
        if c == '(':
            inner_tokens, no_consumed_chars = parse_runner(program[current_pos+1:])
            tokens.append(inner_tokens)
            current_pos += no_consumed_chars
        elif c == ')':
            if current_token:
                tokens.append(convert_to_int(current_token))
            return (tokens, current_pos+1)
        elif c == ' ':
            if current_token:
                tokens.append(convert_to_int(current_token))
            current_token = ''
        else:
            current_token += c
        current_pos += 1
    return (tokens, current_pos)

def convert_to_int(s):
    """Convert s to an int of possible, otherwise return s.
    >>> convert_to_int('33')
    33
    >>> convert_to_int('+')
    '+'
    """
    try:
        return int(s)
    except Exception as e:
        return s

if __name__ == '__main__':
    import doctest
    doctest.testmod()
