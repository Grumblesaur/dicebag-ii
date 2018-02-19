dice_vars = {
  '_' : 0,
}

turn_tracker = {
  
}

import turns

def backup_state():
  with open('state/dice', 'r') as _in:
    with open('state/dice.bak', 'w') as out:
      out.write(_in.read())
  with open('state/turns', 'r') as _in:
    with open('state/turns.bak', 'w') as out:
      out.write(_in.read())

def save_state():
  global dice_vars
  global turn_tracker
  with open('state/dice', 'w') as out:
    out.write(repr(dice_vars))
  with open('state/turns', 'w') as out:
    out.write(repr(turn_tracker))

def load_state():
  global dice_vars
  global turn_tracker
  with open('state/dice', 'r') as _in:
    dice_vars = eval(_in.read())
  try:
    with open('state/turns', 'r') as _in:
      turn_tracker = eval(_in.read())
      for order in turn_tracker:
        turn_tracker[order] = turns.TurnOrder(turn_tracker[order])
  except TypeError as e:
    print(e)
    turn_tracker = { }

