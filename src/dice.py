from engine import roll, ParseError

def calc_reps(msg):
  try:
    die, rep = ((msg, 1), msg.split('^'))['^' in msg]
    rep = abs(int(rep)) or 1
  except (ValueError, TypeError) as e:
    raise ParseError(e)

  return [roll(die) for i in range(rep)]

def scan(msg):
  if '!roll' not in msg:
    return []
  
  tokens = msg.casefold().split('!roll')
  tokens = [token.strip() for token in tokens if token]
  rolls  = [ ]
  for token in tokens:
    try:
      rolls.append((token, [roll(token)]))
    except ParseError as e:
      print('bad roll:', token, e)
  return rolls

def notify(rolls, msg=None):
  return '%s rolled:\n%s' % (
    msg.author.display_name,
    '\n'.join(['\n'.join(
        [result[0]]
        + ['  %s' % die for die in result[1]]
      ) for result in rolls]
    )
  )

