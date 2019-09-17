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

x = '!roll #("#[1d2,1d3,1d4,1d5,1d6,1d7,1d8,1d9,1d10]"^9)'

pass_cases = [
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
  Message('!roll #(4r4l2)', 'roll'),
  Message('!roll @(4r4l2)', 'roll'),
  Message('!roll ?(4r4l2)', 'roll'),
  Message('!roll #4d4', 'roll'),
  
  Message('!roll [#4r6h3, #4r6h3, #4r6h3, #4r6h3, #4r6h3]', 'last'),
  Message('!roll 80 - #last', 'last'),
  Message('!roll [#4r6h3, #4r6h3, #4r6h3, #4r6h3, #4r6h3] !roll 80 - #last',
    'last'
  ),
  Message('!roll "#4r6h3"^5 !roll 80 - #last', 'repeater'),
  
  Message('!roll @("#4r10 + #4r10"^10) $ 1', 'bananas'),
  Message('!roll 4r16l1 $ 4r16l1', 'cash'),
  Message('!roll 10 $ 1', 'cash'),
  Message('!roll ?("#10r10 - 30" ^ (1d3))', 'concat'),
  Message('!roll @(1$0)r4', 'cash'),
  Message('!roll @(10r(2**1d4))', 'bananas'),
  Message(x,'list'),
  Message('!roll 1d1000000000', 'huge'),
]

def test(msg):
  return notify(scan(msg.text), msg)

if __name__ == '__main__':
  for case in pass_cases:
    print(test(case), '\n')


