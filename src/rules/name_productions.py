import sys
sys.path.append('..')

import gen
import names

def p_name(tokens):
  '''expr : NAME expr'''
  tokens[0] = gen.generateName(names.sanitize(tokens[2]))


