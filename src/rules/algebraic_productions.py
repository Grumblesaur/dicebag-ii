from math import factorial
from math import log

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
  tokens[0] = factorial(tokens[1]) // (
    factorial(tokens[3]) * factorial(tokens[1] - tokens[3])
  )

def p_exp(tokens):
  '''expr : expr EXP expr'''
  tokens[0] = tokens[1] ** tokens[3]


