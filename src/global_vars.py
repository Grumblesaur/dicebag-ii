dice_vars = {
  '_' : 0,
}

dice_funcs = {

}

turn_tracker = {
  
}

def save_state():
  with open('state/dice', 'w') as out:
    out.write(repr(dice_vars))
  with open('state/turns', 'w') as out:
    out.write(repr(turn_tracker))

def load_state():
  with open('state/dice', 'r') as _in:
    dice_vars = eval(_in.read())
  with open('state/turns', 'r') as _in:
    turn_tracker = eval(_in.read())
  




