tokens = ['ADD', 'SUB', 'MUL', 'DIV', 'MOD', 'FDIV', 'NUM', 'CAT']

literals = """
t_ADD = r'\+'
t_SUB = r'-'
t_MUL = r'\*'
t_DIV = r'/'
t_MOD = r'%'
t_FDIV = r'//'
t_CAT  = r'\$'
"""

reserved = {'num' : 'NUM'}

precedence = {
  160 : ('left',  'ADD', 'SUB'),
  170 : ('left',  'MUL', 'DIV', 'MOD', 'FDIV'),
  180 : ('right', 'ABS', 'NEG'),
  70  : ('left',  'CAT'),
  110 : ('right', 'NUM'),
}

