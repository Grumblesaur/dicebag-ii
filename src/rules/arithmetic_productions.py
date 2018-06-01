from operr import OperationError

def p_add(tokens):
  '''expr : expr ADD expr'''
  try:
    tokens[0] = tokens[1] + tokens[3]
  except Exception as e:
    raise OperationError(
      ('add `%s` operands cannot mix types.'
       + 'You may have tried to add a numeric '
       + 'value to a list, and you might need to '
       + 'sum the list with `#`. (%s)'
      ) % (tokens[2], e)
    )

def p_sub(tokens):
  '''expr : expr SUB expr'''
  try:
    tokens[0] = tokens[1] - tokens[3]
  except Exception as e:
    raise OperationError(
      'subtract `%s` requires numeric left and right operands. (%s)' % (
        tokens[2], e
      )
    )

def p_mul(tokens):
  '''expr : expr MUL expr'''
  try:
    tokens[0] = tokens[1] * tokens[3]
  except Exception as e:
    raise OperationError(
      ('multiply `%s` requires numeric left and right operands, OR '
       + 'one string operand and one integral operand, OR '
       + 'one list operand and one integral operand. (%s)') % (
        tokens[2], e
      )
    )

def p_div(tokens):
  '''expr : expr DIV expr'''
  try:
    tokens[0] = tokens[1] / tokens[3]
  except Exception as e:
    raise OperationError(
      'divide `%s` requires numeric left and right operands. (e)' % (
        tokens[2], e
      )
    )

def p_fdiv(tokens):
  '''expr : expr FDIV expr'''
  try:
    tokens[0] = tokens[1] // tokens[3]
  except Exception as e:
    raise OperationError(
      'floor divide `%s` requires numeric left and right operands. (e)' % (
        tokens[2], e
      )
    )

def p_mod(tokens):
  '''expr : expr MOD expr'''
  try:
    tokens[0] = tokens[1] % tokens[3]
  except Exception as e:
    raise OperationError(
      'modulo `%s` requires integral left and right operands. (e)' % (
        tokens[2], e
      )
    )

def p_abs(tokens):
  '''expr : ADD expr %prec ABS'''
  try:
    result = +tokens[2]
  except TypeError:
    result = tokens[2]
  tokens[0] = result

def p_neg(tokens):
  '''expr : SUB expr %prec NEG'''
  try:
    result = -tokens[2]
  except TypeError:
    try:
      result = [x for x in reversed(tokens[2])]
    except Exception:
      result = tokens[2]
  tokens[0] = result

def p_num(tokens):
  '''expr : NUM expr'''
  try:
    x = float(tokens[2])
    y = int(x)
  except ValueError as e:
    raise OperationError("can't convert `%s` to numeric. (%s)" % (
      tokens[2], e)
  )
  tokens[0] = y if y == x else x

def p_cat(tokens):
  '''expr : expr CAT expr'''
  try:
    tokens[0] = int(str(int(tokens[1])) + str(int(tokens[3])))
  except Exception as e:
    raise OperationError(
      'catenate `%s` requires operands convertible to integer. (%s)' % (
        tokens[2], e
      )
    )


    
