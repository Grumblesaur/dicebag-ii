import random
import enum

class KeepMode(enum.Enum):
  LOWEST  = -1,
  ALL     = 0,
  HIGHEST = 1

def roll_kernel(dice, sides, count=0, mode=KeepMode.ALL, return_sum=False):
  results = [random.randint(1,sides) for die in dice]
  if mode == KeepMode.LOWEST:
    out = sorted(results)[:count]
  elif mode == KeepMode.HIGHEST:
    out = [x for x in reversed(sorted(results))][:count]
  else:
    out = results
  return sum(out) if return_sum else out


