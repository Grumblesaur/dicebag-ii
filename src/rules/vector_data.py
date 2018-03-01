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

