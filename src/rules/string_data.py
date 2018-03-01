tokens = ['RED', 'GREEN', 'GRAY', 'STR']

literals = """pass"""

reserved = {
  'red'   : 'RED',
  'green' : 'GREEN',
  'grey'  : 'GRAY',
  'gray'  : 'GRAY',
  'str'   : 'STR'
}

precedence = {
  10  : ('right', 'GRAY', 'GREEN', 'RED'),
  110 : ('right', 'STR')
}

