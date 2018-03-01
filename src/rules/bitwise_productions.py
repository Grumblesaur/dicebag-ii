def p_bit_and(tokens):
  '''expr : expr BIT_AND expr'''
  tokens[0] = tokens[1] & tokens[3]

def p_bit_or(tokens):
  '''expr : expr BIT_OR expr'''
  tokens[0] = tokens[1] | tokens[3]

def p_lshift(tokens):
  '''expr : expr LSHIFT expr'''
  tokens[0] = tokens[1] << tokens[3]

def p_rshift(tokens):
  '''expr : expr RSHIFT expr'''
  tokens[0] = tokens[1] >> tokens[3]


