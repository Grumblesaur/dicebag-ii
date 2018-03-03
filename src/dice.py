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
      rolls.append((phrase, [snark(display_name, e)]))
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
