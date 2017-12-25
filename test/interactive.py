import sys
import os

sys.path.append(os.getcwd().replace('test','src'))

from engine import roll

command = ''

while "exit" not in command:
  command = input('[dicebag ii] ')
  print(roll(command.strip()))


