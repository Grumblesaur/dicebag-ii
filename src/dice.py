from engine import roll, ParseError
from random import choice

insults = []
responses = []

def init_insults():
  insult_file = 'insults/insults'
  response_file = 'insults/responses'
  with open(insult_file, 'r') as fin:
    for line in fin:
      insults.append(line.strip())
  with open(response_file, 'r') as fin:
    for line in fin:
      responses.append(line.strip())

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
  return choice(responses) % choice(
    insults + ([username] * (len(insults) // 4))
  ) + " (%s)" % error
  

def notify(rolls, msg):
  return '%s rolled:\n  %s' % (
    msg.author.display_name,
    '\n'.join([
      ('%s:\n\t'%roll[0]) + '\n\t'.join([str(res) for res in roll[1]]) for
      roll in rolls
    ])
  )

if __name__ != '__main__':
  init_insults()
