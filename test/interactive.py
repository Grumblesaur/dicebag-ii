import sys
import os

sys.path.append(os.getcwd().replace('test','src'))

class person(object):
  def __init__(self, n):
    self.display_name = n

class message(object):
  def __init__(self):
    self.author = person('James')

msg = message()

from engine import roll
from dice   import notify

command = ''

while True:
  try:
    command = input('[dicebag ii] ')
    if "exit" in command.casefold():
      break
    print(roll(command.strip(), 'james'))
  except Exception as e:
    print(e)
    raise

