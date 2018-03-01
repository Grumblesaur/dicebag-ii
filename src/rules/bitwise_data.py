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

