tokens = ['AND', 'OR', 'NOT']

reserved = {'and' : 'AND', 'or' : 'OR', 'not' : 'NOT'}

precedence = {
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

