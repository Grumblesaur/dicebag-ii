tokens = ['ADD', 'SUB', 'MUL', 'DIV', 'MOD', 'FDIV', 'NUM', 'CAT']

literals = """
t_ADD = r'\+'
t_SUB = r'-'
t_MUL = r'\*'
t_DIV = r'/'
t_MOD = r'%'
t_FDIV = r'//'
t_CAT  = r'\$'
"""

reserved = {'num' : 'NUM'}

precedence = {
  160 : ('left',  'ADD', 'SUB'),
  170 : ('left',  'MUL', 'DIV', 'MOD', 'FDIV'),
  180 : ('right', 'ABS', 'NEG'),
  70  : ('left',  'CAT'),
  110 : ('right', 'NUM'),
}

productions = """
def p_add(tokens):
  '''expr : expr ADD expr'''
  tokens[0] = tokens[1] + tokens[3]

def p_sub(tokens):
  '''expr : expr SUB expr'''
  tokens[0] = tokens[1] - tokens[3]

def p_mul(tokens):
  '''expr : expr MUL expr'''
  tokens[0] = tokens[1] * tokens[3]

def p_div(tokens):
  '''expr : expr DIV expr'''
  tokens[0] = tokens[1] / tokens[3]

def p_fdiv(tokens):
  '''expr : expr FDIV expr'''
  tokens[0] = tokens[1] // tokens[3]

def p_mod(tokens):
  '''expr : expr MOD expr'''
  tokens[0] = tokens[1] % tokens[3]

def p_abs(tokens):
  '''expr : ADD expr %prec ABS'''
  try:
    result = +t[2]
  except TypeError:
    result = t[2]
  t[0] = result

def p_neg(tokens):
  '''expr : SUB expr %prec NEG'''
  try:
    result = -t[2]
  except TypeError:
    try:
      result = [x for x in reversed(t[2])]
    except Exception:
      result = t[2]
  t[0] = result

def p_num(tokens):
  '''expr : NUM expr'''
  try:
    x = float(tokens[2])
    y = int(x)
  except ValueError as e:
    raise ParseError(e)
  tokens[0] = y if y == x else x

def p_cat(tokens):
  '''expr : expr CAT expr'''
  tokens[0] = int(str(tokens[1]) + str(tokens[3]))

"""



