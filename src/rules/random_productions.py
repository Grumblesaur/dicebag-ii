from random import randint
from random import shuffle
from random import choice
from .operr import OperationError
import random_util

def p_range(tokens):
  '''expr : expr TO expr'''
  try:
    if tokens[1] < tokens[3]:
      tokens[0] = [x for x in range(tokens[1], tokens[3])]
    else:
      tokens[0] = [x for x in range(tokens[3], tokens[1], -1)]
  except Exception as e:
    raise OperationError(
      '`%s` requires integral left and right operands. (%s)' % (
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

dice_error = "Dice cannot have fractional sides or partial count. (%s)"

def p_die(tokens):
  '''expr : expr DIE expr'''
  try:
    tokens[0] = random_util.roll_kernel(tokens[1], tokens[3], return_sum=True)
  except Exception as e:
    raise OperationError(dice_error % e)

def p_die_tern_low(tokens):
  '''expr : expr DIE expr LOW expr'''
  try:
    tokens[0] = random_util.roll_kernel(
      tokens[1],
      tokens[3],
      tokens[5],
      random_util.KeepMode.LOWEST,
      return_sum=True)
  except Exception as e:
    raise OperationError(dice_error % e)

def p_die_tern_high(tokens);
  '''expr : expr DIE expr HIGH expr'''
  try:
    tokens[0] = random_util.roll_kernel(
      tokens[1],
      tokens[3],
      tokens[5],
      random_util.KeepMode.HIGHEST,
      return_sum=True)
  except Exception as e:
    raise OperationError(dice_error % e)

def p_roll(tokens):
  '''expr : expr ROLL expr'''
  try:
    tokens[0] = random_util.roll_kernel(tokens[1], tokens[3])
  except Exception as e:
    raise OperationError(dice_error % e)

def p_low(tokens):
  '''expr : expr LOW expr'''
  try:
    temp = sorted(tokens[1])[:tokens[3]]
    if len(temp) == 1:
      temp = temp[0]
    tokens[0] = temp
  except Exception as e:
    raise OperationError(
      ('`l` requires an iterable left operand and an '
       + 'integral right operand. (%s)') % e
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
      ('`h` requires an iterable left operand and an '
       + 'integral right operand. (%s)') % e
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


