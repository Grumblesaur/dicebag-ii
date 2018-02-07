from math import log, factorial
from random import randint, choice
from global_vars import dice_vars
import ply.yacc as yacc
import sys

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
  'RBRC',   'INS',    'CAT',   'IN',
  'DIE',    'HIGH',   'LOW',   'FACT',
  'VFACT',  'CHOOSE', 'VCHOOSE',
  'YIELD',  'GT',     'LT',    'EQ',
  'GEQ',    'LEQ',    'NEQ',   'IF',
  'ELSE',   'AND',    'OR',    'NOT',
  'LEN',    'SEL'
]

reserved = {
  'd'    : 'DIE',    'h'   : 'HIGH', 'l'   : 'LOW',
  'c'    : 'CHOOSE', 'or'  : 'OR',   'and' : 'AND',
  'not'  : 'NOT',    'del' : 'DEL',  'if'  : 'IF',
  'else' : 'ELSE',   'len' : 'LEN',  'sel' : 'SEL',
  'in'   : 'IN'
}

# Identifiers

def t_IDENT(t):
  r'[a-zA-Z_]+'
  # Intercept reserved words before they get treated like identifiers
  if t.value in reserved:
    t.type = reserved[t.value]
  return t

def t_NUMBER(t):
  r'(\d*\.)?\d+'
  n = None
  try:
    f = float(t.value)
    n = int(f)
  except ValueError as e:
    raise ParseError('"%s" is not a number, %s' % (t.value, e))
  t.value = n if f == n else f
  return t

def t_MACRO(t):
  r"""(\"(\\.|[^"\\])*\"|\'(\\.|[^'\\])*\')"""
  t.value = eval(t.value)
  return t


# Grouping symbols and miscellanea
t_REP  = r'\^'
t_LPAR = r'\('
t_RPAR = r'\)'
t_LBRK = r'\['
t_RBRK = r'\]'
t_LBRC = r'{'
t_RBRC = r'}'

# Vector unaries
t_SUM  = r'\#'
t_AVG  = r'@'
t_SAMM = r'\?'
t_EVEN = r':'
t_ODD  = r'&'

# Arithmetic and algebraic operators
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

# Comparison operators
t_EQ   = r'=='
t_NEQ  = r'!='
t_GEQ  = r'>='
t_LEQ  = r'<='
t_GT   = r'>'
t_LT   = r'<'

# Type subverting operators
t_CAT  = r'\$'
t_VCAT = r'<\$>'

# Storage manipulators
t_INS  = r'<-'
t_YIELD= r'->'
t_ASS  = r'='

# Separators
t_COM  = r','


t_ignore = ' \t\n\r'


def t_error(t):
  raise ParseError('Cannot parse symbol "%s"' % t.value[0])

  
# lexer
import ply.lex as lex
lexer = lex.lex()


# parsing rules
precedence = (
  ('right',  'IF'),
  ('right',  'ASS'),
  ('nonassoc', 'INS'),
  ('left',  'CAT', 'VCAT'),
  ('nonassoc', 'IN'),
  ('left',  'OR'),
  ('left',  'AND'),
  ('right', 'NOT'),
  ('nonassoc', 'LT', 'GT', 'LEQ', 'GEQ', 'EQ', 'NEQ'),
  ('left',  'ADD', 'SUB', 'VADD', 'VSUB'),
  ('left',  'MUL', 'DIV', 'FDIV', 'MOD', 'VMUL', 'VDIV', 'VFDIV', 'VMOD'),
  ('right', 'ABS', 'NEG'),
  ('right', 'ROOT', 'VROOT'),
  ('right', 'FACT', 'VFACT'),
  ('left',  'CHOOSE', 'VCHOOSE'),
  ('left',  'LOG', 'VLOG'),
  ('right', 'EXP', 'VEXP'),
  ('nonassoc', 'SUM', 'AVG', 'SAMM', 'EVEN', 'ODD', 'LEN', 'SEL'),
  ('right', 'LOW', 'HIGH'),
  ('left', 'LBRC', 'RBRC'),
  ('left',  'DIE'),
  ('left', 'REP'),
)

# Expressions
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


def p_expr_comp(t):
  ''' expr : expr GT expr
           | expr LT expr
           | expr EQ expr
           | expr NEQ expr
           | expr GEQ expr
           | expr LEQ expr
  '''
  if   t[2] == '>':
    t[0] = t[1] > t[3]
  elif t[2] == '<':
    t[0] = t[1] < t[3]
  elif t[2] == '==':
    t[0] = t[1] == t[3]
  elif t[2] == '!=':
    t[0] = t[1] != t[3]
  elif t[2] == '>=':
    t[0] = t[1] >= t[3]
  elif t[2] == '<=':
    t[0] = t[1] <= t[3]

def p_expr_or(t):
  'expr : expr OR expr'
  t[0] = t[1] or t[3]

def p_expr_and(t):
  'expr : expr AND expr'
  t[0] = t[1] and t[3]

def p_expr_not(t):
  'expr : NOT expr'
  t[0] = not t[2]

def p_expr_in(t):
  'expr : expr IN expr'
  t[0] = t[1] in t[3]

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

def p_expr_len(t):
  'expr : LEN expr'
  t[0] = len(t[2])

def p_expr_sel(t):
  'expr : SEL expr'
  t[0] = choice(t[2])

def p_expr_tail(t):
  '''expr : expr LOW  expr
          | expr HIGH expr
  '''
  if   t[2] == 'l':
    t[0] = sorted(t[1])[:t[3]]
  elif t[2] == 'h':
    t[0] = [x for x in reversed(sorted(t[1]))][:t[3]]
  
  t[0] = t[0][0] if len(t[0]) == 1 else t[0]

def p_conditional(t):
  '''expr : expr IF expr ELSE expr
          | expr IF ELSE expr
  '''
  if len(t) == 6:
    t[0] = t[1] if t[3] else t[5]
  else:
    t[0] = t[1] if t[1] else t[4]



# Concrete values
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
  t[0] = dice_vars[t[1]]


# Function-related rules
def p_func_call(t):
  '''expr : func_expr expr'''
  args, algo = t[1].split('->')
  args = [s.strip() for s in args.split(',')]
  algo = algo.strip().strip('"').strip("'")
  for index in range(len(t[2])):
    algo = algo.replace(args[index], str(t[2][index]))
  t[0] = parser.parse(algo)

def p_named_func_call(t):
  '''expr : IDENT expr'''
  args, algo = dice_vars[t[1]].split('->')
  args = [s.strip() for s in args.split(',')]
  algo = algo.strip().strip('"').strip("'")
  for index in range(len(t[2])):
    algo = algo.replace(args[index], str(t[2][index]))
  t[0] = parser.parse(algo)

def p_func_expr(t):
  '''func_expr : param_list YIELD MACRO'''
  f = "%s -> '%s'" % (','.join(t[1]), t[3])
  t[0] = f

def p_func_assign(t):
  '''expr : IDENT ASS func_expr'''
  t[0] = t[3]
  dice_vars[t[1]] = t[3]



# Variadic constructions
def p_param_list(t):
  '''param_list : LBRK elements RBRK
                | LBRK RBRK
  '''
  if len(t) == 4:
    t[0] = t[2]
  else:
    t[0] = []

def p_expr_list(t):
  '''expr : LBRK elements RBRK
          | LBRK RBRK
  '''
  if len(t) == 4:
    t[0] = t[2]
  else:
    t[0] = []


def p_elements(t):
  '''elements : expr COM elements
              | expr
  '''
  if len(t) == 4:
    t[0] = [t[1]] + t[3]
  else:
    t[0] = [t[1]]
  



# Memory manipulation
def p_index_expr(t):
  r'expr : expr LBRC expr RBRC'
  t[0] = t[1][t[3]]


def p_assign_expr(t):
  '''expr : IDENT ASS expr
          | IDENT ASS LBRC RBRC
  '''
  if len(t) == 4:
    t[0] = t[3]
    dice_vars[t[1]] = t[3]
  else:
    t[0] = {}
    dice_vars[t[1]] = {}


def p_insert_expr(t):
  '''expr : IDENT INS expr COM expr'''
  t[0] = t[5]
  dice_vars[t[1]][t[3]] = t[5]


def p_delete(t):
  '''expr : DEL IDENT'''
  t[0] = dice_vars[t[2]]
  del dice_vars[t[2]]



def p_error(t):
  raise ParseError(str(t) + " hosed us")


parser = yacc.yacc(optimize=1, debug=True)


def roll(expr):
  try:
    dice_vars['_'] = parser.parse(expr)
    return dice_vars['_']
  except Exception as e:
    raise ParseError(e)







