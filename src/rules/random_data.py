tokens = ['DIE', 'ROLL', 'HIGH', 'LOW', 'SEL', 'TO', 'BY', 'SHUFFLE', 'SORT']

literals = """pass"""

reserved = {
  'd'       : 'DIE',
  'r'       : 'ROLL',
  'l'       : 'LOW',
  'h'       : 'HIGH',
  'sel'     : 'SEL',
  'to'      : 'TO',
  'by'      : 'BY',
  'sort'    : 'SORT',
  'shuffle' : 'SHUFFLE'
}

precedence = {
  60  : ('nonassoc', 'BY'),
  50  : ('nonassoc', 'TO'),
  270 : ('left', 'DIE', 'ROLL'),
  271 : ('left', 'LOW', 'HIGH'),
  240 : ('right', 'SEL', 'SHUFFLE', 'SORT'),
}



