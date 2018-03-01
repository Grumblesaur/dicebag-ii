tokens = ['LOG', 'EXP', 'ROOT', 'FACT', 'CHOOSE']

reserved = {'c' : 'CHOOSE'}

literals = """
t_LOG    = r'~'
t_EXP    = r'\*\*'
t_ROOT   = r'%%'
t_FACT   = r'!'
"""

precedence = {
  190 : ('right', 'ROOT'),
  200 : ('right', 'FACT'),
  205 : ('left',  'CHOOSE'),
  210 : ('left',  'LOG'),
  220 : ('right', 'EXP'),
}

