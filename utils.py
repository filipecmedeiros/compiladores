
BLANK = [' ', '\n', '\t', '\r']

def is_digit(char):
    return char >= '0' and char <='9'

def is_letter(char):
    return char >= 'a' and char <= 'z'

token_table = {
    'int': 1,
    'float': 2,
    'char': 3,
    'add': 4,
    'sub': 5,
    'mul': 6,
    'div': 7,
    'attr': 8,
    'equal': 9,
    'min': 10,
    'min_equal': 11,
    'max': 12,
    'max_equal': 13,
    'diff': 14,
    'open_parenthesis': 15,
    'close_parenthesis': 16,
    'open_brackets': 17,
    'close_brackets': 18,
    'comma': 19,
    'semmicolon': 20,
    'id': 21,
    'main': 22,
    'if': 23,
    'else': 24,
    'while': 25,
    'do': 26,
    'for': 27,
    'int_w': 28,
    'float_w': 29,
    'char_w': 30
}