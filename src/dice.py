from engine import roll, ParseError
from random import choice

def scan(msg, usr):
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
      rolls.append((token, [snark(usr, e)]))
  return rolls

def snark(username, error):
  responses = [
    "You really ate the bones, %s.",
    "Yo, %s, would you kindly stop breaking things?",
    "Don't waste my time, %s.",
    "Fuck you, %s!",
    "Sorry, %s, I'm not really feeling up to your bullshit today.",
    "Hey %s! Read the documentation!",
    "Keep your hands to yourself, %s!",
    "Eyes on your own work there, %s!",
    "Syntax error: go fuck yourself, %s.",
    "java.lang.Exception: HAH! This is Python! You really screwed the pooch"
      + " now, %s!",
    "No, %s. Not gonna happen.",
    "Well, %s, that was inconsiderate.",
    "Could you behave for two seconds, %s?",
    "How many times do we have to teach you this lesson, %s?"
  ]
  names = [
    'jerk', 'fuckface', 'moron', 'dirtfarmer',
    'dingus', 'useless', 'bonehead', 'milk-drinker',
    'skeleton man', 'shitlord', 'bird brain',
    'dick twiddler', 'raggedy muffin child',
    'shifty fister', 'ass-wrangler', 'jumbo toddler',
    'turd burglar', 'pit sniffer', 'old fart',
    'witless wonder', 'freakenstein', 'dingus khan'
  ]
  
  return choice(responses) % choice(
    names + ([username] * (len(names) // 3))
  ) + " (%s)" % error
  

def notify(rolls, msg):
  return '%s rolled:\n  %s' % (
    msg.author.display_name,
    '\n'.join([
      ('%s:\n\t'%roll[0]) + '\n\t'.join([str(res) for res in roll[1]]) for
      roll in rolls
    ])
  )


