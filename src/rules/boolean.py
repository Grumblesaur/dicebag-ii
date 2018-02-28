tokens = ['AND', 'OR', 'NOT']

literals = """pass"""

reserved = {'and' : 'AND', 'or' : 'OR', 'not' : 'NOT', 'in' : 'IN'}

precedence = {
  80  : ('nonassoc', 'IN'),
  90  : ('left', 'OR'),
  100 : ('left', 'AND'),
  110 : ('right', 'NOT'),
}

def p_and(tokens):
  '''expr : expr AND expr'''
  tokens[0] = tokens[1] and tokens[3]

def p_or(tokens):
  '''expr : expr OR expr'''
  tokens[0] = tokens[1] and tokens[3]

def p_not(tokens):
  '''expr : NOT expr'''
  tokens[0] = not tokens[2]

def p_in(tokens):
  '''expr : expr IN expr'''
  tokens[0] = tokens[1] in token[3]


