from engine import roll, ParseError

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

def notify(rolls, msg):
  return '%s rolled:\n  %s' % (
    msg.author.display_name,
    str(rolls)
  )


