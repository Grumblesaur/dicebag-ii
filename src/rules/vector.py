tokens = ['SUM', 'SAMM', 'AVG', 'LEN', 'EVEN', 'ODD']

literals = """
t_SUM  = r'\#'
t_SAMM = r'\?'
t_AVG  = r'@'
"""
reserved = {'len' : 'LEN', 'even' : 'EVEN', 'odd' : 'ODD'}

precedence = {
  240 : ('right', 'SUM', 'AVG', 'SAMM', 'ODD', 'EVEN', 'LEN')
}

def p_sum(tokens):
  '''expr : SUM expr'''
  try:
    tokens[0] = sum(tokens[2])
  except TypeError:
    tokens[0] = ''.join(tokens[2])

def p_samm(tokens):
  '''expr : SAMM expr'''
  total = sum(tokens[2])
  tokens[0] = [total, total / len(tokens[2]), max(tokens[2]), min(tokens[2])]

def p_avg(tokens):
  '''expr : AVG expr'''
  tokens[0] = sum(tokens[2]) / len(tokens[2])

def p_len(tokens):
  '''expr : LEN expr'''
  tokens[0] = len(tokens[2])

def p_even(tokens):
  '''expr : EVEN expr'''
  tokens[0] = [x for x in tokens[2] if not (x % 2)]

def p_odd(tokens):
  '''expr : ODD expr'''
  tokens[0] = [x for x in tokens[2] if x % 2]


