from .operr import OperationError

def p_bit_and(tokens):
  '''expr : expr BIT_AND expr'''
  try:
    tokens[0] = tokens[1] & tokens[3]
  except Exception as e:
    raise OperationError(
      'bitwise and `%s` requires integral left and right operands. (%s)' % (
        tokens[2], e
      )
    )

def p_bit_or(tokens):
  '''expr : expr BIT_OR expr'''
  try:
    tokens[0] = tokens[1] | tokens[3]
  except Exception as e:
    raise OperationError(
      'bitwise or `%s` requires integral left and right operands. (%s)' % (
        tokens[2], e
      )
    )

def p_lshift(tokens):
  '''expr : expr LSHIFT expr'''
  try:
    tokens[0] = tokens[1] << tokens[3]
  except Exception as e:
    raise OperationError(
      ('bitwise left shift `%s` requires integral left and right '
       + 'operands. (%s)'
      ) % (tokens[2], e)
    )

def p_rshift(tokens):
  '''expr : expr RSHIFT expr'''
  try:
    tokens[0] = tokens[1] >> tokens[3]
  except Exception as e:
    raise OperationError(
      ('bitwise right shift `%s` requires integral left and right '
       + 'operands. (%s)'
      ) % (tokens[2], e)
    )



