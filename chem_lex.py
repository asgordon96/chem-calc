# Using ply to lex and parse chemical formulas
# STARTED: 8/30/12

import lex
import re

tokens = ('ELEMENT', 'RPAREN', 'LPAREN', 'COUNT')

t_ignore = ' '

def load_elements():
    filename = "new_element_list.txt"
    f = open(filename, 'r')
    content = f.readlines()
    data = {}
    for line in content:
        line = line.split(',')
        data[line[1]] = float(line[3])

    return data

d = load_elements()


def t_ELEMENT(token):
    r'[A-Z][a-z]?(?:[0-9]+)?'
    val = token.value
    result = re.match(r'([A-Z][a-z]?)((?:[0-9]+)?)', val)
    parts = result.groups()

    if parts[1]:
        count = int(parts[1])
    else:
        count = 1

    weight = d[parts[0]] * count
    token.value = weight
    return token

def t_COUNT(token):
    r'[0-9]+'
    token.value = int(token.value)
    return token

t_RPAREN = r'\)'
t_LPAREN = r'\('


lexer = lex.lex()

def lex_formula(formula):
    """Break the formula into a list of tokens"""
    token_list = []
    lexer.input(formula)
    for token in lexer:
        if token:
            token_list.append(token)
        else:
            break
    return token_list

def close_parens(token_list, start):
    """Find the closing Right Parentheses from the token list"""
    open_parens = 0
    for i, token in enumerate(token_list[start:]):
        if token.type == 'LPAREN':
            open_parens += 1
        elif token.type == 'RPAREN':
            open_parens -= 1

        if open_parens == 0:
            return i + start


def parse_formula(token_list):
    tokens = token_list
    atomic_mass = 0

    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token.type == 'ELEMENT':
            atomic_mass += token.value

        elif token.type == 'LPAREN':
            end_paren = close_parens(tokens, index)
            inside = tokens[index+1:end_paren]
            count = tokens[end_paren+1].value

            atomic_mass += parse_formula(inside) * count

            index = end_paren + 1

        index += 1
    return atomic_mass


def calc_mass(formula):
    tokens = lex_formula(formula)
    return parse_formula(tokens)

def test():
    print calc_mass("Mg (NO3)2")
    print calc_mass("H2 O")
    print calc_mass("Ca3 (PO4)2")
    print calc_mass("Ag NO3")
    print calc_mass("O2 C (H6 Hg (NO3)2)6")
    print calc_mass("NaOH")

def test2():
    print calc_mass("(H2O)2 C")

if __name__ == '__main__':test2()