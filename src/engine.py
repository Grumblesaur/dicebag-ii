from math import log, factorial
from random import randint
from global_vars import dicebag_globals
import ply.yacc as yacc

class ParseError(Exception):
  pass

tokens = [ # token declarations
  'MUL',    'DIV',    'LOG',   'EXP',
  'LPAR',   'RPAR',   'MOD',   'LBRK',
  'RBRK',   'ADD',    'SUB',   'SUM',
  'AVG',    'COM',    'SAMM',  'FDIV',
  'REP',    'EVEN',   'ODD',   'ASS',
  'NUMBER', 'MACRO',  'IDENT', 'DEL',
  'ROOT',   'VADD',   'VSUB',  'VMUL',
  'VDIV',   'VFDIV',  'VEXP',  'VLOG',
  'VCAT',   'VMOD',   'VROOT', 'LBRC',
  'RBRC',   'INS',    'DOT',   'CAT',
  'DIE',    'HIGH',   'LOW',   'FACT',
  'VFACT',  'CHOOSE', 'VCHOOSE',
]

# token definitions
def t_DIE(t):
  r'd'
  return t

def t_LOW(t):
  r'l'
  return t

def t_HIGH(t):
  r'h'
  return t

def t_CHOOSE(t):
  r'c'
  return t

def t_NUMBER(t):
  r'\d+'
  try:
    t.value = int(t.value)
  except ValueError:
    raise ParseError('"%s" is not an integer' % t.value)
  return t

def t_MACRO(t):
  r"""(\"(\\.|[^"\\])*\"|\'(\\.|[^'\\])*\')"""
  t.value = eval(t.value)
  return t

t_REP  = r'\^'
t_LPAR = r'\('
t_RPAR = r'\)'
t_LBRK = r'\['
t_RBRK = r'\]'
t_LBRC = r'{'
t_RBRC = r'}'
t_DOT  = r'\.'


t_SUM  = r'\#'
t_AVG  = r'@'
t_SAMM = r'\?'
t_EVEN = r':'
t_ODD  = r'&'

t_EXP  = r'\*\*'
t_VEXP = r'<\*\*>'
t_LOG  = r'~'
t_VLOG = r'<~>'

t_VCHOOSE= r'<c>'
t_FACT = r'!'
t_VFACT= r'<!>'

t_MUL  = r'\*'
t_VMUL = r'<\*>'
t_DIV  = r'/'
t_VDIV = r'</>'
t_FDIV = r'//'
t_VFDIV= r'<//>'
t_MOD  = r'%'
t_VMOD = r'<%>'
t_ROOT = r'%%'
t_VROOT= r'<%%>'

t_ADD  = r'\+'
t_VADD = r'<\+>'
t_SUB  = r'-'
t_VSUB = r'<->'

t_CAT  = r'\$'
t_VCAT = r'<\$>'

t_INS  = r'<-'
t_ASS  = r'='
t_DEL  = r';'

t_COM  = r','

t_IDENT= r'[a-zA-Z_][a-zA-Z0-9_]*'


t_ignore = ' \t\n\r'


def t_error(t):
  raise ParseError('Cannot parse symbol "%s"' % t.value[0])

  
# lexer
import ply.lex as lex
lexer = lex.lex()


# the value of the last roll is saved here, to be identified by `_`
report = None


# parsing rules
precedence = (
  ('right',  'ASS'),
  ('nonassoc', 'INS'),
  ('left',  'CAT', 'VCAT'),
  ('left',  'ADD', 'SUB', 'VADD', 'VSUB'),
  ('left',  'MUL', 'DIV', 'FDIV', 'MOD', 'VMUL', 'VDIV', 'VFDIV', 'VMOD'),
  ('right', 'ABS', 'NEG'),
  ('right', 'ROOT', 'VROOT'),
  ('right', 'FACT', 'VFACT'),
  ('left',  'CHOOSE', 'VCHOOSE'),
  ('left',  'LOG', 'VLOG'),
  ('right', 'EXP', 'VEXP'),
  ('nonassoc', 'SUM', 'AVG', 'SAMM', 'EVEN', 'ODD'),
  ('right', 'LOW', 'HIGH'),
  ('left', 'LBRC', 'RBRC', 'DOT'),
  ('left',  'DIE'),
  ('left', 'REP'),
)


# The dot methods are syntactic sugar
def p_dot(t):
  '''expr : IDENT DOT IDENT'''
  t[0] = dicebag_globals[t[1]][t[3]]

def p_dot_assign(t):
  '''expr : IDENT DOT IDENT ASS expr'''
  t[0] = dicebag_globals[t[1]][t[3]] = t[5]

def p_expr_fact(t):
  '''expr : expr FACT'''
  t[0] = factorial(t[1])

def p_expr_vfact(t):
  '''expr : expr VFACT'''
  t[0] = [factorial(x) for x in t[1]]

def choose(n, k):
  return factorial(n) / (factorial(k) * factorial(n - k))

def p_expr_choose(t):
  '''expr : expr CHOOSE expr'''
  t[0] = choose(t[1], t[3])

def p_expr_vchoose(t):
  '''expr : expr VCHOOSE expr'''
  t[0] = [choose(n, k) for n, k in zip(t[1], t[3])]

def p_expr_vbinop(t):
  '''expr : expr VCAT expr
          | expr VADD expr
          | expr VSUB expr
          | expr VMUL expr
          | expr VDIV expr
          | expr VMOD expr
          | expr VFDIV expr
          | expr VROOT expr
          | expr VLOG expr
          | expr VEXP expr
  '''
  if   t[2] == '<$>':
    t[0] = map(
      lambda x: int(x[0]+x[1]),
      zip(str(int(t[1])), str(int(t[3])))
    )
  elif t[2] == '<+>':
    t[0] = [sum(x) for x in zip(t[1], t[3])]
  elif t[2] == '<->':
    t[0] = [x[0] - x[1] for x in zip(t[1], t[3])]
  elif t[2] == '<*>':
    t[0] = [x[0] * x[1] for x in zip(t[1], t[3])]
  elif t[2] == '</>':
    t[0] = [x[0] / x[1] for x in zip(t[1], t[3])]
  elif t[2] == '<%>':
    t[0] = [x[0] % x[1] for x in zip(t[1], t[3])]
  elif t[2] == '<//>':
    t[0] = [x[0] // x[1], zip(t[1], t[3])]
  elif t[2] == '<%%>':
    t[0] = [x[1] ** (1.0 / x[0]) for x in zip(t[1], t[3])]
  elif t[2] == '<~>':
    t[0] = [log(x[1], x[0]) for x in zip(t[1], t[3])]
  elif t[2] == '<**>':
    t[0] = [x[0] ** x[1] for x in zip(t[1], t[3])]


def p_expr_binop(t):
  '''expr : expr CAT  expr
          | expr ADD  expr
          | expr SUB  expr
          | expr MUL  expr
          | expr DIV  expr
          | expr MOD  expr
          | expr FDIV expr
          | expr ROOT expr
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
  elif t[2] == '%%':
    t[0] = t[3] ** (1.0 / t[1])
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

def p_expr_even(t):
  'expr : EVEN expr'
  t[0] = [x for x in t[2] if not (x % 2)]

def p_expr_odd(t):
  'expr : ODD expr'
  t[0] = [x for x in t[2] if x % 2]


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
          | MACRO
  '''
  if len(t) == 4:
    t[0] = t[2]
  else:
    t[0] = t[1]


def p_ident(t):
  'expr : IDENT'
  t[0] = dicebag_globals[t[1]]


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
  

def p_index_expr(t):
  r'expr : expr LBRC expr RBRC'
  t[0] = t[1][t[3]]

def p_assign_expr(t):
  '''expr : IDENT ASS expr
          | IDENT ASS LBRC RBRC
  '''
  if len(t) == 4:
    t[0] = t[3]
    dicebag_globals[t[1]] = t[3]
  else:
    t[0] = {}
    dicebag_globals[t[1]] = {}


def p_insert_expr(t):
  '''expr : IDENT INS expr COM expr'''
  t[0] = t[5]
  dicebag_globals[t[1]][t[3]] = t[5]

def p_delete(t):
  '''expr : DEL IDENT'''
  t[0] = dicebag_globals[t[2]]
  del dicebag_globals[t[2]]

def p_error(t):
  print(report)
  raise ParseError(str(t) + " hosed us")

parser = yacc.yacc(optimize=1, debug=True)

def roll(expr):
  try:
    dicebag_globals['_'] = parser.parse(expr)
    return dicebag_globals['_']
  except Exception as e:
    raise ParseError(e)







