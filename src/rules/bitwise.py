tokens = ['BIT_AND', 'BIT_OR', 'LSHIFT', 'RSHIFT']

literals = """pass"""

reserved = { }

t_BIT_AND = r'&'
t_BIT_OR  = r'\|'
t_LSHIFT  = r'<<'
t_RSHIFT  = r'>>'

precedence = {
  150 : ('left', 'LSHIFT', 'RSHIFT'),
  120 : ('left', 'BIT_OR'),
  130 : ('left', 'BIT_AND')
}

productions = """
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
"""


