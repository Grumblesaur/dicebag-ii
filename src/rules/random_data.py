tokens = [
  'DIE', 'ROLL',
  'HIGH', 'LOW',
  'SEL', 'TO',
  'BY', 'SHUFFLE',
  'RSORT','SORT',
  'FROM',
]

literals = """pass"""

reserved = {
  'd'       : 'DIE',
  'r'       : 'ROLL',
  'l'       : 'LOW',
  'h'       : 'HIGH',
  'sel'     : 'SEL',
  'to'      : 'TO',
  'by'      : 'BY',
  'from'    : 'FROM',
  'sort'    : 'SORT',
  'rsort'   : 'RSORT',
  'shuffle' : 'SHUFFLE'
}

precedence = {
  60  : ('nonassoc', 'BY'),
  50  : ('nonassoc', 'TO'),
  269 : ('left', 'FROM'),
  270 : ('left', 'DIE', 'ROLL'),
  271 : ('left', 'LOW', 'HIGH'),
  240 : ('right', 'SEL', 'SHUFFLE', 'RSORT', 'SORT'),
}



