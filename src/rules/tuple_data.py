tokens = ['TUP', 'LIST', 'TUP_OPEN', 'TUP_CLOSE']

reserved = {
  'tuple' : 'TUP',
  'list'  : 'LIST'
}

literals = """
t_TUP_OPEN  = r'<\('
t_TUP_CLOSE = r'\)>'
"""

precedence = {
  110 : ('right', 'TUP', 'LIST')
}


