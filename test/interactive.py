import sys
import os

sys.path.append(os.getcwd().replace('test','src'))

from engine import roll

command = ''

while True:
  try:
    command = input('[dicebag ii] ')
    if "exit" in command.casefold():
      break
    print(roll(command.strip()))
  except Exception as e:
    print(e)

