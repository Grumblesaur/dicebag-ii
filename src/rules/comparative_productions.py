def p_gt(tokens):
  '''expr : expr GT expr'''
  tokens[0] = tokens[1] > tokens[3]

def p_ge(tokens):
  '''expr : expr GE expr'''
  tokens[0] = tokens[1] >= tokens[3]

def p_lt(tokens):
  '''expr : expr LT expr'''
  tokens[0] = tokens[1] < tokens[3]

def p_le(tokens):
  '''expr : expr LE expr'''
  tokens[0] = tokens[1] <= tokens[3]

def p_eq(tokens):
  '''expr : expr EQ expr'''
  tokens[0] = tokens[1] == tokens[3]

def p_ne(tokens):
  '''expr : expr NE expr'''
  tokens[0] = tokens[1] != tokens[3]


