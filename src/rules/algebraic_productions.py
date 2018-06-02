from math import factorial
from math import log
from .operr import OperationError

def p_root(tokens):
  '''expr : expr ROOT expr'''
  try:
    tokens[0] = tokens[3] ** (1 / tokens[1])
  except Exception as e:
    raise OperationError(
      'root `%s` requires numeric left and right operands. (%s)' % (
        tokens[2],e
      )
    )

def p_fact(tokens):
  '''expr : expr FACT'''
  try:
    tokens[0] = factorial(tokens[1])
  except Exception as e:
    raise OperationError(
      'factorial `%s` requires integral left operand. (%s)' % (
        tokens[2], e
      )
    )
  
def p_log(tokens):
  '''expr : expr LOG expr'''
  try:
    tokens[0] = log(tokens[3], tokens[1])
  except Exception as e:
    raise OperationError(
      'logarithm `%s` requires numeric left and right operands. (%s)' % (
        tokens[2],e
      )
    )

def p_choose(tokens):
  '''expr : expr CHOOSE expr'''
  try:
    tokens[0] = factorial(tokens[1]) // (
      factorial(tokens[3]) * factorial(tokens[1] - tokens[3])
    )
  except Exception as e:
    raise OperationError(
      'choose `%s` requires integral left and right operands. (%s)' % (
        tokens[2],e
      )
    )

def p_exp(tokens):
  '''expr : expr EXP expr'''
  try:
    tokens[0] = tokens[1] ** tokens[3]
  except Exception as e:
    raise OperationError(
      ('power `\*\*` requires requires numeric left and right '
       + 'operands. (%s)') % e
    )
  
