import global_vars
import ply.yacc as yacc

# Language module imports
import rules.algebraic_data
import rules.arithmetic_data
import rules.bitwise_data
import rules.boolean_data
import rules.comparative_data
import rules.name_data
import rules.random_data
import rules.string_data
import rules.vector_data

######################################
# Import modules you intend to use   #
# above here and then add their name #
# to the list below accordingly.     #
######################################

modules = (
  rules.algebraic_data,   rules.arithmetic_data,
  rules.bitwise_data,     rules.boolean_data,
  rules.comparative_data, rules.name_data,
  rules.random_data,      rules.string_data,
  rules.vector_data
)

class ParseError(Exception):
  pass

# Built-in token names
tokens = [ # token declarations
  'REP',    'ASS',   'NUMBER',
  'STRING', 'IDENT', 'DEL',
  'LPAR',   'RPAR',  'LBRK',
  'RBRK',   'COM',   'LBRC',
  'RBRC',   'YIELD', 'IF',
  'ELSE',  'FALSE',  'TRUE',
  'VARS',  'EVAL',   'SEP',
  'COLON', 
]

# module-defined token names
for module in modules:
  tokens += module.tokens

# Built in reserved words
reserved = {
  'del'  : 'DEL',
  'if'   : 'IF',
  'else' : 'ELSE',
  'false': 'FALSE',
  'true' : 'TRUE',
  'eval' : 'EVAL',
  'vars' : 'VARS',
}

# Append module-defined reserved words
for module in modules:
  reserved = {**reserved, **module.reserved}

# Variable names
def t_IDENT(t):
  r'[a-zA-Z_]+'
  # Intercept reserved words before they get treated like identifiers
  if t.value in reserved:
    t.type = reserved[t.value]
  return t

# Numeric literals
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

# String objects
def t_STRING(t):
  r"""(\"(\\.|[^"\\])*\"|\'(\\.|[^'\\])*\')"""
  t.value = eval(t.value)
  return t

# Read the stringified definitions of literal tokens
# from the appropriate module to assign them to our
# global namespace without overwriting previous modules.
for module in modules:
  exec(module.literals)

# Builtin literal tokens
t_SEP  = r';'
t_REP  = r'\^'
t_LPAR = r'\('
t_RPAR = r'\)'
t_LBRK = r'\['
t_RBRK = r'\]'
t_LBRC = r'{'
t_RBRC = r'}'
t_COLON= r':'
t_YIELD= r'->'
t_ASS  = r'='
t_COM  = r','
t_ignore = ' \t\n\r`'


def t_error(t):
  raise ParseError('Cannot parse symbol "%s"' % t.value[0])

  
###################
# Build the lexer #
###################
import ply.lex as lex
lexer = lex.lex()


###########################
# Parser Precedence Rules #
###########################
precedence = {
    0 : ('right',  'EVAL'),
   20 : ('right',  'IF'),
   30 : ('right',  'ASS'),
  260 : ('left', 'LBRC', 'RBRC'),
  280 : ('left', 'REP'),
}
# Add precedence rules from modules
precedence = list(precedence.items())
for module in modules:
  precedence += list(module.precedence.items())

# Reduce precedence rules to a format which PLY understands
precedence = [x[1] for x in sorted(precedence, key=lambda e: e[0])]



###########################
# Parser Production Rules #
###########################

# ADD RULE MODULE INPUTS HERE
from rules.algebraic_productions import *
from rules.arithmetic_productions import *
from rules.bitwise_productions import *
from rules.boolean_productions import *
from rules.comparative_productions import *
from rules.name_productions import *
from rules.random_productions import *
from rules.string_productions import *
from rules.vector_productions import *

# Built-in expressions
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
                | LBRK RBRK'''
  if len(t) == 4:
    t[0] = t[2]
  else:
    t[0] = []

def p_list(t):
  '''expr : list_expr'''
  t[0] = t[1]

def p_list_expr(t):
  '''list_expr : LBRK elements RBRK
               | LBRK RBRK'''
  if len(t) == 4:
    t[0] = t[2]
  else:
    t[0] = []


def p_elements(t):
  '''elements : expr COM elements
              | expr'''
  if len(t) == 4:
    t[0] = [t[1]] + t[3]
  else:
    t[0] = [t[1]]
  

# Memory manipulation
def p_index_expr(t):
  '''expr : expr LBRC expr RBRC
          | IDENT LBRC expr RBRC'''
  try:
    t[0] = t[1][t[3]]
  except Exception:
    t[0] = global_vars.dice_vars[t[1]][t[3]]

def p_dictexpr(t):
  '''dictexpr : LBRC pairs RBRC
              | LBRC RBRC'''
  if len(t) == 4:
    t[0] = dict(t[2])
  else:
    t[0] = { }

def p_pairs(t):
  '''pairs : expr COLON expr COM pairs
           | expr COLON expr'''
  if len(t) == 6:
    t[0] = [[t[1], t[3]]] + t[5]
  else:
    t[0] = [[t[1], t[3]]]

def p_expr_dictexpr(t):
  '''expr : dictexpr'''
  t[0] = t[1]

def p_assign_expr(t):
  '''expr : IDENT LBRC expr RBRC ASS expr
          | IDENT ASS expr'''
  if len(t) == 4:
    t[0] = t[3]
    global_vars.dice_vars[t[1]] = t[3]
  else:
    t[0] = t[6]
    global_vars.dice_vars[t[1]][t[3]] = t[6]


def p_delete(t):
  '''expr : DEL IDENT LBRC expr RBRC
          | DEL IDENT'''
  if len(t) == 3:
    t[0] = global_vars.dice_vars[t[2]]
    del global_vars.dice_vars[t[2]]
  else:
    t[0] = (global_vars.dice_vars[t[2]])[t[4]]
    del (global_vars.dice_vars[t[2]])[t[4]]

def p_stmt(t):
  '''stmt : expr'''
  t[0] = t[1]

def p_stmt_list(t):
  '''stmt_list : stmt_list SEP stmt
               | stmt'''
  if len(t) == 2:
    t[0] = t[1]
  else:
    t[0] = t[3]
  global_vars.dice_vars['_'] = t[0] 

def p_error(t):
  raise ParseError(str(t))


parser = yacc.yacc(optimize=1, debug=True)


def roll(expr):
  try:
    global_vars.dice_vars['_'] = parser.parse(expr)
    return global_vars.dice_vars['_']
  except Exception as e:
    raise ParseError(e)



