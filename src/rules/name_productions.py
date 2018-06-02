import sys
sys.path.append('..')

import gen
import names
from .util.operr import OperationError

def p_name(tokens):
  '''expr : NAME expr'''
  try:
    tokens[0] = gen.generateName(names.sanitize(tokens[2]))
  except Exception as e:
    raise OperationError(
      ('`%s` error: argument is malformed argument dictionary or '
       + 'not a dictionary at all. (%s)') % (tokens[1], e)
    )

