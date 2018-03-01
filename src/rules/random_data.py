tokens = ['DIE', 'HIGH', 'LOW', 'SEL', 'TO', 'BY', 'SHUFFLE', 'SORT']

literals = """pass"""

reserved = {
  'd'       : 'DIE',
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
  270 : ('left', 'DIE'),
  250 : ('left', 'LOW', 'HIGH'),
  240 : ('right', 'SEL', 'SHUFFLE', 'SORT'),
}



