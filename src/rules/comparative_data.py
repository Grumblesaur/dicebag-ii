tokens = ['GT', 'LT', 'GE', 'LE', 'EQ', 'NE']

literals = """
t_GT = r'>'
t_GE = r'>='
t_LT = r'<'
t_LE = r'<='
t_EQ = r'=='
t_NE = r'!='
"""

reserved = { }

precedence = {
  140 : ('nonassoc', 'LT', 'GT', 'LE', 'GE', 'NE', 'EQ')
}


