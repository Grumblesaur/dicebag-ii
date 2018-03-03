import global_vars
import private_vars
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
import rules.tuple_data
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
  rules.tuple_data,       rules.vector_data
)

class ParseError(Exception):
  pass

# `username` determines where to store private variables
username = ''

# Built-in token names
tokens = [ # token declarations
  'REP',    'ASS',   'NUMBER',
  'STRING', 'IDENT', 'DEL',
  'LPAR',   'RPAR',  'LBRK',
  'RBRK',   'COM',   'LBRC',
  'RBRC',   'YIELD', 'IF',
  'ELSE',  'FALSE',  'TRUE',
  'VARS',  'EVAL',   'SEP',
  'COLON', 'MY'
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
  'my'   : 'MY',
  'rep'  : 'REP'
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
 -100 : ('left',   'SEP'),
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
from rules.tuple_productions import *
from rules.vector_productions import *

# Top-level code structure

start = 'stmt_list'

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

# Built-in expressions
def p_assignment_expr(tokens):
  '''expr : assignment'''
  tokens[0] = tokens[1]

def p_assignment(tokens):
  '''assignment : identifier subscript_list ASS expr
                | identifier ASS expr'''
  try:
    var, usr = tokens[1]
  except ValueError:
    var, usr = tokens[1][0], None
  if len(tokens) == 5:
    tokens[0] = tokens[4]
    exec([
        'global_vars.dice_vars','private_vars.dice_vars[%s]' % repr(usr)
      ][bool(usr)]
      + '[%s]' % repr(var)
      + ''.join(['[%s]' % repr(sub) for sub in tokens[2]])
      + ' = '
      + repr(tokens[4])
    )
  else:
    tokens[0] = tokens[3]
    if usr:
      if usr not in private_vars.dice_vars:
        private_vars.dice_vars[usr] = { }
      private_vars.dice_vars[usr][var] = tokens[3]
    else:
      global_vars.dice_vars[var] = tokens[3]

def p_deletion_expr(tokens):
  '''expr : deletion'''
  tokens[0] = tokens[1]

def p_subscript_deletion(tokens):
  '''deletion : DEL identifier subscript_list'''
  try:
    var, usr = tokens[2]
  except ValueError:
    var, usr = tokens[2][0], None
  if usr:
    expr = ('private_vars.dice_vars[%s][%s]' % (
      repr(usr), repr(var)
    )) + ''.join(
      ['[%s]' % repr(sub) for sub in tokens[3]]
    )
    tokens[0] = eval(expr)
    exec(' '.join(('del', expr)))
  else:
    expr = ('global_vars.dice_vars[%s]' % repr(var)) + ''.join(
      ['[%s]' % repr(sub) for sub in tokens[3]]
    )
    tokens[0] = eval(expr)
    exec(' '.join(('del', expr)))

def p_var_deletion(tokens):
  '''deletion : DEL var_list'''
  deleted = [ ]
  for t in tokens[2]:
    try:
      var, usr = t
    except ValueError:
      var, usr = t[0], None
    if usr:
      deleted.append(private_vars.dice_vars[usr][var])
      del private_vars.dice_vars[usr][var]
    else:
      deleted.append(global_vars.dice_vars[var])
      del global_vars.dice_vars[var]
    tokens[0] = deleted
    
def p_var_list(tokens):
  '''var_list : var_list COM identifier
              | identifier'''
  if len(tokens) == 4:
    tokens[0] = tokens[1] + [tokens[3]]
  else:
    tokens[0] = [tokens[1]]

def p_index_expr(tokens):
  '''expr : expr subscript_list'''
  current = tokens[1]
  for sub in tokens[2]:
    current = current[sub]
  tokens[0] = current

def p_var_expr(tokens):
  '''expr : identifier'''
  try:
    var, usr = tokens[1]
  except ValueError:
    var, usr = tokens[1][0], None
  if usr:
    tokens[0] = private_vars.dice_vars[usr][var]
  else:
    tokens[0] = global_vars.dice_vars[var]

def p_identifier(tokens):
  '''identifier : MY IDENT
                | IDENT'''
  if len(tokens) == 3:
    tokens[0] = [tokens[2], username]
  else:
    tokens[0] = [tokens[1]]

def p_subscript_list(tokens):
  '''subscript_list : subscript_list subscript
                    | subscript'''
  if len(tokens) == 3:
    tokens[0] = tokens[1] + [tokens[2]]
  else:
    tokens[0] = [tokens[1]]

def p_subscript(tokens):
  '''subscript : LBRC expr RBRC'''
  tokens[0] = tokens[2]


def p_expr_bool_t(tokens):
  '''expr : TRUE
          | FALSE'''
  tokens[0] = tokens[1].casefold() == 'true'

def p_vars(tokens):
  '''expr : MY VARS
          | VARS'''
  if len(tokens) == 3:
    tokens[0] = '```%s```' % '  '.join(
      sorted(private_vars.dice_vars[username].keys())
    )
  else:
    tokens[0] = '```%s```' % '  '.join(
      sorted(global_vars.dice_vars.keys())
    )

def p_expr_meta_rep(tokens):
  'expr : expr REP expr'
  tokens[0] = [parser.parse(str(tokens[1])) for x in range(tokens[3])]

def p_expr_meta_eval(tokens):
  '''expr : EVAL expr'''
  tokens[0] = parser.parse(tokens[2])

def p_conditional(t):
  '''expr : expr IF expr ELSE expr
          | expr IF ELSE expr'''
  if len(t) == 6:
    t[0] = t[1] if t[3] else t[5]
  else:
    t[0] = t[1] if t[1] else t[4]

# Concrete values
def p_primary(tokens):
  '''expr : LPAR expr RPAR
          | NUMBER
          | STRING'''
  if len(tokens) == 4:
    tokens[0] = tokens[2]
  else:
    tokens[0] = tokens[1]

# Function-related rules
def p_function_literal_expr(tokens):
  '''expr : LBRK RBRK YIELD STRING
          | LBRK MUL RBRK YIELD STRING'''
  macro = tokens[4] if len(tokens) == 5 else tokens[5]
  tokens[0] = {
    'unpack?' : '*' in tokens,
    'logic' : macro
  }
 
def p_function_call(tokens):
  '''expr : identifier expr'''
  global_func = len(tokens[1]) == 1
  var_scope = global_vars.dice_vars if global_func else private_vars.dice_vars
  if not global_func:
    var_scope = var_scope[tokens[1][1]]
  try:
    unpack = var_scope[tokens[1][0]]['unpack?']
    logic  = var_scope[tokens[1][0]]['logic']
  except (KeyError, TypeError):
    raise ParseError('object `%s` is not a function' % repr(tokens[1]))
  if unpack:
    tokens[0] = parser.parse(logic.format(*tokens[2]))
  else:
    tokens[0] = parser.parse(logic.format(tokens[2]))
    
# Variadic constructions
def p_list_expr(tokens):
  '''expr : list'''
  tokens[0] = tokens[1]

def p_list(tokens):
  '''list : LBRK elements RBRK
          | LBRK RBRK'''
  if len(tokens) == 4:
    tokens[0] = tokens[2]
  else:
    tokens[0] = []

def p_list_elements(tokens):
  '''elements : expr COM elements
              | expr'''
  if len(tokens) == 4:
    tokens[0] = [tokens[1]] + tokens[3]
  else:
    tokens[0] = [tokens[1]]
  

# Memory manipulation
def p_expr_dictexpr(tokens):
  '''expr : dict'''
  tokens[0] = tokens[1]

def p_dict(tokens):
  '''dict : LBRC key_value_pairs RBRC
          | LBRC RBRC'''
  if len(tokens) == 4:
    tokens[0] = dict(tokens[2])
  else:
    tokens[0] = { }

def p_key_value_pairs(tokens):
  '''key_value_pairs : expr COLON expr COM key_value_pairs
                     | expr COLON expr'''
  if len(tokens) == 6:
    tokens[0] = [[tokens[1], tokens[3]]] + tokens[5]
  else:
    tokens[0] = [[tokens[1], tokens[3]]]

def p_error(tokens):
  raise ParseError(str(tokens))


parser = yacc.yacc(optimize=1, debug=True)


def roll(expr,user):
  global username
  username = user
  try:
    global_vars.dice_vars['_'] = parser.parse(expr)
    return global_vars.dice_vars['_']
  except Exception as e:
    raise ParseError(e)



