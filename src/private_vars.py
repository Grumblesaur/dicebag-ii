dice_vars = {

}

def save_state():
  global dice_vars
  with open('state/private-dice', 'w') as out:
    out.write(repr(dice_vars))

def backup_state():
  with open('state/private-dice', 'r') as _in:
    with open('state/private-dice.bak', 'w') as out:
      out.write(_in.read())

def load_state():
  global dice_vars
  with open('state/private-dice', 'r') as _in:
    dice_vars = eval(_in.read())


