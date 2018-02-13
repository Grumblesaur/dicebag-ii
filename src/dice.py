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
  
  clause  = msg.split('!roll')
  phrases = [token.strip().split(';')[0] for token in tokens if token]
  phrases   = [phrase.split('|') for phrase in phrases]
  rolls  = [ ]
  for phrase in phrases:
    i = 0;
    p = len(phrase) - 1
    for expr in phrase:
      if i != p:
        try:
          roll(token)
        except ParseError as e:
          pass
      else:
        try:
          rolls.append((token, [roll(token)]))
        except ParseError as e:
          print('bad roll:', token, e)
          rolls.append((token, [snark(usr, e)]))
      i += 1
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
