import global_vars
import ply.yacc as yacc

class ParseError(Exception):
  pass

tokens = [ # token declarations
  'REP',    'ASS',   'NUMBER',
  'STRING', 'IDENT', 'DEL',
  'LPAR',   'RPAR',  'LBRK',
  'RBRK',   'COM',   'LBRC',
  'RBRC',   'INS',   'YIELD',
  'IF',     'ELSE',  'FALSE',
  'TRUE',   'VARS',  'EVAL',
  'SEP',    'COLON', 
]

reserved = {
  'd'    : 'DIE',    'h'    : 'HIGH', 'l'        : 'LOW',
  'del'  : 'DEL',  'if'       : 'IF',
  'else' : 'ELSE',   'len'  : 'LEN',  'sel'      : 'SEL',
  'in'   : 'IN',     'red'  : 'RED',  'green'    : 'GREEN',
  'str'  : 'STR',    'num'  : 'NUM',  'name'     : 'NAME',
  'false': 'FALSE',  'true' : 'TRUE', 'gray'     : 'GRAY',
  'grey' : 'GRAY',   'eval' : 'EVAL',
  'evens': 'EVEN',   'odds' : 'ODD',  'avg'      : 'AVG',
  'to'   : 'TO',     'by'   : 'BY',   'vars' : 'VARS',
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

def t_STRING(t):
  r"""(\"(\\.|[^"\\])*\"|\'(\\.|[^'\\])*\')"""
  t.value = eval(t.value)
  return t


# Grouping symbols and miscellanea
t_SEP  = r';'
t_REP  = r'\^'
t_LPAR = r'\('
t_RPAR = r'\)'
t_LBRK = r'\['
t_RBRK = r'\]'
t_LBRC = r'{'
t_RBRC = r'}'
t_COLON= r':'

t_INS  = r'<-'
t_YIELD= r'->'
t_ASS  = r'='

# Separators
t_COM  = r','


t_ignore = ' \t\n\r`'


def t_error(t):
  raise ParseError('Cannot parse symbol "%s"' % t.value[0])

  
# lexer
import ply.lex as lex
lexer = lex.lex()


# parsing rules
precedence = {
    0 : ('right',  'EVAL'),
   20 : ('right',  'IF'),
   30 : ('right',  'ASS'),
   40 : ('nonassoc', 'INS'),
  260 : ('left', 'LBRC', 'RBRC'),
  280 : ('left', 'REP'),
}

# Expressions
def p_stmt_list_t(t):
  '''stmt_list : stmt
               | stmt_list SEP stmt'''
  if len(t) == 2:
    t[0] = t[1]
  else:
    t[0] = t[3]
  global_vars.dice_vars['_'] = t[0] 

def p_stmt(t):
  '''stmt : expr'''
  t[0] = t[1]

def p_expr_bool_t(t):
  '''expr : TRUE
          | FALSE'''
  t[0] = t[1].casefold() == 'true'

def p_vars(t):
  '''expr : VARS'''
  t[0] = '```%s```' % '  '.join(sorted(global_vars.dice_vars.keys()))

def p_expr_meta_rep(t):
  'expr : expr REP expr'
  t[0] = [parser.parse(str(t[1])) for x in range(t[3])]

def p_expr_meta_eval(t):
  '''expr : EVAL expr'''
  t[0] = parser.parse(t[2])

def p_conditional(t):
  '''expr : expr IF expr ELSE expr
          | expr IF ELSE expr'''
  if len(t) == 6:
    t[0] = t[1] if t[3] else t[5]
  else:
    t[0] = t[1] if t[1] else t[4]

# Concrete values
def p_primary(t):
  '''expr : LPAR expr RPAR
          | NUMBER
          | STRING'''
  if len(t) == 4:
    t[0] = t[2]
  else:
    t[0] = t[1]


def p_ident(t):
  '''expr : IDENT'''
  t[0] = global_vars.dice_vars[t[1]]


# Function-related rules
def p_func_call(t):
  '''expr : func_expr list_expr'''
  args, algo = t[1].split('->')
  args = [s.strip() for s in args.split(',')]
  algo = algo.strip().strip('"').strip("'")
  for index in range(len(t[2])):
    algo = algo.replace(args[index], str(t[2][index]))
  t[0] = parser.parse(algo)

def p_named_func_call(t):
  '''expr : IDENT list_expr'''
  args, algo = global_vars.dice_vars[t[1]].split('->')
  args = [s.strip() for s in args.split(',')]
  algo = algo.strip().strip('"').strip("'")
  for index in range(len(t[2])):
    algo = algo.replace(args[index], str(t[2][index]))
  t[0] = parser.parse(algo)

def p_func_expr(t):
  '''func_expr : param_list YIELD STRING'''
  f = "%s -> '%s'" % (','.join(t[1]), t[3])
  t[0] = f

def p_func_assign(t):
  '''expr : IDENT ASS func_expr'''
  t[0] = t[3]
  global_vars.dice_vars[t[1]] = t[3]

# Variadic constructions
def p_param_list(t):
  '''param_list : LBRK elements RBRK
                | LBRK RBRK
  '''
  if len(t) == 4:
    t[0] = t[2]
  else:
    t[0] = []

def p_list(t):
  '''expr : list_expr'''
  t[0] = t[1]

def p_list_expr(t):
  '''list_expr : LBRK elements RBRK
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
  '''expr : expr LBRC expr RBRC
          | IDENT LBRC expr RBRC
  '''
  try:
    t[0] = t[1][t[3]]
  except Exception:
    t[0] = global_vars.dice_vars[t[1]][t[3]]

def p_dictexpr(t):
  '''dictexpr : LBRC pairs RBRC
              | LBRC RBRC
  '''
  if len(t) == 4:
    t[0] = dict(t[2])
  else:
    t[0] = { }

def p_pairs(t):
  '''pairs : expr COLON expr COM pairs
           | expr COLON expr
  '''
  if len(t) == 6:
    t[0] = [[t[1], t[3]]] + t[5]
  else:
    t[0] = [[t[1], t[3]]]

def p_expr_dictexpr(t):
  '''expr : dictexpr'''
  t[0] = t[1]

def p_assign_expr(t):
  '''expr : IDENT ASS expr
          | IDENT LBRC expr RBRC ASS expr
  '''
  if len(t) == 4:
    t[0] = t[3]
    global_vars.dice_vars[t[1]] = t[3]
  else:
    t[0] = t[6]
    global_vars.dice_vars[t[1]][t[3]] = t[6]


def p_insert_expr(t):
  '''expr : IDENT INS expr COM expr'''
  t[0] = t[5]
  global_vars.dice_vars[t[1]][t[3]] = t[5]


def p_delete(t):
  '''expr : DEL IDENT
          | DEL IDENT LBRC expr RBRC
  '''
  if len(t) == 3:
    t[0] = global_vars.dice_vars[t[2]]
    del global_vars.dice_vars[t[2]]
  else:
    t[0] = (global_vars.dice_vars[t[2]])[t[4]]
    del (global_vars.dice_vars[t[2]])[t[4]]

def p_name(t):
  '''expr : NAME expr'''
  t[0] = gen.generateName(names.sanitize(t[2])) 


def p_error(t):
  raise ParseError(str(t))


parser = yacc.yacc(optimize=1, debug=True)


def roll(expr):
  try:
    global_vars.dice_vars['_'] = parser.parse(expr)
    return global_vars.dice_vars['_']
  except Exception as e:
    raise ParseError(e)







