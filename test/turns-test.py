import sys
import os

sys.path.append(os.getcwd().replace('test','src'))

from turns import scan, notify

messages = [
  '!initiative create battle',
  '!initiative add battle heniele 14',
  '!initiative add battle vedam 6',
  '!initiative add battle ulfr 19',
  '!initiative add battle falwyn 9',
  '!initiative add battle calvus -3',
  '!initiative start battle',
  '!initiative next battle',
  '!initiative next battle',
  '!initiative add battle caranya 0',
  '!initiative add battle wolf-familiar 20',
  '!initiative next battle',
  '!initiative check battle',
  '!initiative view battle',
  '!initiative next battle',
  '!initiative next battle',
  '!initiative next battle',
  '!initiative clear battle',
  '!initiative stop battle',
  '!initiative clear battle',
]

if __name__ == '__main__':
  for message in messages:
    feedback = scan(message)
    if feedback:
      notify(feedback)


