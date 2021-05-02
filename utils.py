
LOG_VERBOSE = True

BLANK = [' ', '\n', '\t', '\r']

def is_digit(char):
    return char >= '0' and char <='9'

def is_letter(char):
    return char >= 'a' and char <= 'z'

token_table = {
    'int_value': 1,
    'float_value': 2,
    'char_value': 3,
    '+': 4,
    '-': 5,
    '*': 6,
    '/': 7,
    '=': 8,
    '==': 9,
    '<': 10,
    '<=': 11,
    '>': 12,
    '>=': 13,
    '!=': 14,
    '(': 15,
    ')': 16,
    '{': 17,
    '}': 18,
    ',': 19,
    ';': 20,
    'id': 21,
    'main': 22,
    'if': 23,
    'else': 24,
    'while': 25,
    'do': 26,
    'for': 27,
    'int': 28,
    'float': 29,
    'char': 30
}