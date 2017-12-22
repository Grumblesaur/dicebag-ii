import sys
import os

sys.path.append(os.getcwd().replace('test','src'))

from dice import calc_reps, scan, notify

class Message(object):
  def __init__(self, text, name):
    self.text = text
    self.author = Person(name)

class Person(object):
  def __init__(self, name):
    self.display_name = name

cases = [
  Message('!roll 4d4', 'bin'),
  Message('!roll 4**3', 'bin'),
  Message('!roll 2~3', 'bin'),
  Message('!roll 15 // 6', 'bin'),
  Message('!roll 15 / 6', 'bin'),
  Message('!roll 15 % 6', 'bin'),
  Message('!roll 15 * 6', 'bin'),
  Message('!roll 15 + 6', 'bin'),
  Message('!roll 15 - 6', 'bin'), 
  Message('!roll 4$4', 'bin'),
  
  Message('!roll [1, 2, 3, 4, 5]', 'list'),
  Message('!roll #[1, 2, 3, 4, 5]', 'list'),
  
  Message('!roll 4d4l1', 'roll'),
  Message('!roll #(4d4l2)', 'roll'),
  Message('!roll @(4d4l2)', 'roll'),
  Message('!roll ?(4d4l2)', 'roll'),
  Message('!roll #4d4', 'roll'),
  
  Message('!roll [#4d6h3, #4d6h3, #4d6h3, #4d6h3, #4d6h3]', 'last'),
  Message('!roll 80 - #last', 'last'),
  Message('!roll [#4d6h3, #4d6h3, #4d6h3, #4d6h3, #4d6h3] !roll 80 - #last',
    'last'),
  
  Message('!roll "#4d6h3"^5 !roll 80 - #last', 'repeater')
]

def test(msg):
  return notify(scan(msg.text), msg)

if __name__ == '__main__':
  for case in cases:
    print(test(case), '\n')
