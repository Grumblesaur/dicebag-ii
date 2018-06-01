from engine import roll, ParseError
from random import choice

def scan(msg, display_name, actual_name):
  if '!roll' not in msg:
    return []
  
  clause  = msg.split('!roll')
  phrases = [phrase.strip().split('::')[0] for phrase in clause if phrase]
  rolls  = [ ]
  for phrase in phrases:
    try:
      rolls.append((phrase, [roll(phrase, actual_name)]))
    except ParseError as e:
      print('bad roll:', phrase, e)
      rolls.append((phrase, [e]))
  return rolls

def notify(rolls, msg):
  return '%s rolled:\n  %s' % (
    msg.author.display_name,
    '\n'.join([
      ('%s:\n\t'%roll[0]) + '\n\t'.join([str(res) for res in roll[1]]) for
      roll in rolls
    ])
  )

