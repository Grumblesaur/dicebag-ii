from .operr import OperationError

def p_sum(tokens):
  '''expr : SUM expr'''
  try:
    x = len(tokens[2])
  except TypeError:
    # let scalars pass through
    tokens[0] = tokens[2]
    return
  else:
    del p
  
  try:
    try:
      tokens[0] = sum(tokens[2])
    except TypeError:
      tokens[0] = ''.join(tokens[2])
  except Exception:
    raise OperationError(
      ('vector cannot be joined or summed with elements of '
       + 'disparate type. (%s)') % e
    )


def p_samm(tokens):
  '''expr : SAMM expr'''
  try:
    total = sum(tokens[2])
    tokens[0] = [total, total / len(tokens[2]), max(tokens[2]), min(tokens[2])]
  except Exception as e:
    raise OperationError(
      'argument is not vector or contains objects of disparate type. (%s)'
    )

def p_avg(tokens):
  '''expr : AVG expr'''
  try:
    tokens[0] = sum(tokens[2]) / len(tokens[2])
  except Exception as e:
    raise OperationError(
      ('cannot average a scalar or vector with elements of '
       + 'disparate type. (%s)') % e
    )

def p_len(tokens):
  '''expr : LEN expr'''
  try:
    tokens[0] = len(tokens[2])
  except Exception as e:
    raise OperationError(
      'scalar types have no length property. (%s)' % e
    )

def p_even(tokens):
  '''expr : EVEN expr'''
  try:
    tokens[0] = [x for x in tokens[2] if not (x % 2)]
  except Exception as e:
    raise OperationError(
      'operand is either not a vector type or contains non-numerics. (%s)' % e
    )

def p_odd(tokens):
  '''expr : ODD expr'''
  try:
    tokens[0] = [x for x in tokens[2] if x % 2]
  except Exception as e:
    raise OperationError(
      'operand is either not a vector type or contains non-numerics. (%s)' % e
    )

