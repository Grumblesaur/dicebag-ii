from random import randint
from random import shuffle
from random import choice
from .util.operr import OperationError

def p_range(tokens):
  '''expr : expr TO expr'''
  try:
    if tokens[1] < tokens[3]:
      tokens[0] = [x for x in range(tokens[1], tokens[3])]
    else:
      tokens[0] = [x for x in range(tokens[3], tokens[1], -1)]
  except Exception as e:
    raise OperationError(
      '`%s` requires integral left and right operands.' % (
        tokens[2], e
      )
    )

def p_range_step(tokens):
  '''expr : expr TO expr BY expr'''
  try:
    step = abs(tokens[5])
    if tokens[1] < tokens[3]:
      tokens[0] = [x for x in range(tokens[1], tokens[3], step)]
    else:
      tokens[0] = [x for x in range(tokens[3], tokens[1], -step)]
  except Exception as e:
    raise OperationError(
      'range boundaries and step size must be integers. (%s)' % e
    )

def p_die(tokens):
  '''expr : expr DIE expr'''
  try:
    tokens[0] = [randint(1, tokens[3]) for x in range(tokens[1])]
    tokens[0] = tokens[0][0] if len(tokens[0]) == 1 else tokens[0]
  except Exception as e:
    raise OperationError(
      'dice cannot have fractional sides or have partial count. (%s)' % (
        e
      )
    )

def p_low(tokens):
  '''expr : expr LOW expr'''
  try:
    temp = sorted(tokens[1])[:tokens[3]]
    if len(temp) == 1:
      temp = temp[0]
    tokens[0] = temp
  except Exception as e:
    raise OperationError(
      'copy and paste this error to the developer for analysis (%s)' % e
    )


def p_high(tokens):
  '''expr : expr HIGH expr'''
  try:
    temp = [x for x in reversed(sorted(tokens[1]))][:tokens[3]]
    if len(temp) == 1:
      temp = temp[0]
    tokens[0] = temp
  except Exception as e:
    raise OperationError(
      'copy and paste this error to the developer for analysis (%s)' % e
    )

def p_sel(tokens):
  '''expr : SEL expr'''
  try:
    tokens[0] = choice(tokens[2])
  except Exception as e:
    raise OperationError(
      'cannot select element from scalar item. (%s)' % e
    )

def p_shuffle(tokens):
  '''expr : SHUFFLE expr'''
  try:
    temp = tokens[2]
    shuffle(temp)
    tokens[0] = temp
  except Exception as e:
    raise OperationError(
      'cannot shuffle non-vector object. (%s)' % e
    )


def p_sort(tokens):
  '''expr : SORT expr'''
  try:
    tokens[0] = sorted(tokens[2])
  except Exception as e:
    raise OperationError(
      'cannot sort non-vector object. (%s)' % e
    )


