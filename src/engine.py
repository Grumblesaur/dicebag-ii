from math import log
from random import randint
import ply.yacc as yacc

class ParseError(Exception):
  pass

tokens = ( # token declarations
  'DIE',  'LOW',  'HIGH', 'CAT',
  'MUL',  'DIV',  'LOG',  'EXP',
  'LPAR', 'RPAR', 'MOD',  'LBRK',
  'RBRK', 'ADD',  'SUB',  'SUM',
  'AVG',  'COM',  'SAMM', 'FDIV',
  'LAST', 'REP',
  'NUMBER',       'MACRO', 
)

# token definitions

t_LAST = r'last'

t_REP  = r'\^'
t_LPAR = r'\('
t_RPAR = r'\)'
t_LBRK = r'\['
t_RBRK = r'\]'

t_DIE  = r'd'

t_LOW  = r'l'
t_HIGH = r'h'

t_SUM  = r'\#'
t_AVG  = r'@'
t_SAMM = r'\?'

t_EXP  = r'\*\*'
t_LOG  = r'~'

t_MUL  = r'\*'
t_DIV  = r'/'
t_FDIV = r'//'
t_MOD  = r'%'

t_ADD  = r'\+'
t_SUB  = r'-'

t_CAT  = r'\$'

t_COM  = r','


def t_NUMBER(t):
  r'\d+'
  try:
    t.value = int(t.value)
  except ValueError:
    raise ParseError('"%s" is not an integer' % t.value)
  return t

def t_MACRO(t):
  r'\"(\\.|[^"\\])*\"'
  r"'(\\.|[^'\\])*'"
  t.value = eval(t.value)
  return t

t_ignore = ' \t\n\r'


def t_error(t):
  raise ParseError('Cannot parse symbol "%s"' % t.value[0])

  
# lexer
import ply.lex as lex
lexer = lex.lex()


# the value of the last roll is saved here, to be identified by `_`
last_roll = 0
report = None


# parsing rules
precedence = (
  ('left',  'CAT'),
  ('left',  'ADD', 'SUB'),
  ('left',  'MUL', 'DIV', 'FDIV', 'MOD'),
  ('right', 'ABS', 'NEG'),
  ('left',  'LOG'),
  ('right', 'EXP'),
  ('nonassoc', 'SUM', 'AVG', 'SAMM'),
  ('right', 'LOW', 'HIGH'),
  ('left',  'DIE'),
  ('left', 'REP'),
  ('nonassoc', 'LPAR', 'RPAR'),
)


def p_expr_binop(t):
  '''expr : expr CAT  expr
          | expr ADD  expr
          | expr SUB  expr
          | expr MUL  expr
          | expr DIV  expr
          | expr MOD  expr
          | expr FDIV expr
          | expr LOG  expr
          | expr EXP  expr
          | expr DIE  expr
  '''
  if   t[2] == '$':
    t[0] = int(''.join(map(lambda x: str(int(x)), (t[1], t[3]))))
  elif t[2] == '+':
    t[0] = t[1] + t[3]
  elif t[2] == '-':
    t[0] = t[1] - t[3]
  elif t[2] == '*':
    t[0] = t[1] * t[3]
  elif t[2] == '/':
    t[0] = t[1] / t[3]
  elif t[2] == '%':
    t[0] = t[1] % t[3]
  elif t[2] == '//':
    t[0] = t[1] // t[3]
  elif t[2] == '~':
    t[0] = log(t[3], t[1])
  elif t[2] == '**':
    t[0] = t[1] ** t[3]
  elif t[2] == 'd':
    t[0] = [randint(1, t[3]) for x in range(t[1])]
    t[0] = t[0][0] if len(t[0]) == 1 else t[0]

def p_expr_sign(t):
  '''expr : ADD expr %prec ABS
          | SUB expr %prec NEG
  '''
  if t[1] == '+':
    t[0] = abs(t[2])
  else:
    t[0] = -t[2]

def p_expr_meta_rep(t):
  'expr : expr REP expr'
  t[0] = [parser.parse(str(t[1])) for x in range(t[3])]

def p_expr_sum(t):
  'expr : SUM expr'
  t[0] = sum(t[2])

def p_expr_avg(t):
  'expr : AVG expr'
  t[0] = sum(t[2]) / len(t[2])

def p_expr_samm(t):
  'expr : SAMM expr'
  t[0] = [sum(t[2]), (sum(t[2]) / len(t[2])), max(t[2]), min(t[2])]


def p_expr_tail(t):
  '''expr : expr LOW  expr
          | expr HIGH expr
  '''
  if   t[2] == 'l':
    t[0] = sorted(t[1])[:t[3]]
  elif t[2] == 'h':
    t[0] = [x for x in reversed(sorted(t[1]))][:t[3]]
  
  t[0] = t[0][0] if len(t[0]) == 1 else t[0]

def p_expr_unit(t):
  '''expr : LPAR expr RPAR
          | NUMBER
          | var
          | MACRO
  '''
  if len(t) == 4:
    t[0] = t[2]
  else:
    t[0] = t[1]

def p_expr_last(t):
  'var : LAST'
  t[0] = last_roll


def p_expr_list(t):
  'expr : LBRK elements RBRK'
  t[0] = t[2]

def p_elements(t):
  '''elements : elements COM expr
              | expr
  '''
  if len(t) == 4:
    t[0] = t[1] + [t[3]]
  else:
    t[0] = [t[1]]
  

def p_error(t):
  print(report)
  raise ParseError(str(t) + " hosed us")

parser = yacc.yacc(optimize=1, debug=True)

def roll(expr):
  try:
    global last_roll
    last_roll = parser.parse(expr)
    return last_roll
  except Exception as e:
    raise ParseError(e)







