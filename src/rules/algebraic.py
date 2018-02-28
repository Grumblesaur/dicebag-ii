from math import factorial
from math import log

tokens = ['LOG', 'EXP', 'ROOT', 'FACT', 'CHOOSE']

reserved = {'c' : 'CHOOSE'}

literals = """
t_LOG    = r'~'
t_EXP    = r'\*\*'
t_ROOT   = r'%%'
t_FACT   = r'!'
"""

precedence = {
  190 : ('right', 'ROOT'),
  200 : ('right', 'FACT'),
  210 : ('left',  'LOG'),
  220 : ('right', 'EXP'),
}

def p_root(tokens):
  '''expr : expr ROOT expr'''
  tokens[0] = t[3] ** (1 / t[1])

def p_fact(tokens):
  '''expr : expr FACT'''
  tokens[0] = factorial(tokens[1])

def p_log(tokens):
  '''expr : expr LOG expr'''
  tokens[0] = log(tokens[3], tokens[1])

def p_choose(tokens):
  '''expr : expr CHOOSE expr'''
  tokens[0] = factorial(tokens[1]) / (
    factorial(tokens[3]) * factorial(tokens[1] - tokens[3])
  )

def p_exp(tokens):
  '''expr : expr EXP expr'''
  tokens[0] = tokens[1] ** tokens[3]




