tokens = ['AND', 'OR', 'NOT', 'IN']

literals = """pass"""

reserved = {'and' : 'AND', 'or' : 'OR', 'not' : 'NOT', 'in' : 'IN'}

precedence = {
  80  : ('nonassoc', 'IN'),
  90  : ('left', 'OR'),
  100 : ('left', 'AND'),
  110 : ('right', 'NOT'),
}


