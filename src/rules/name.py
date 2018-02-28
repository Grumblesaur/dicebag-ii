import ..gen
import ..names

tokens = ['name']

reserved = {'name' : 'NAME'}

literals = """pass"""

precedence = {
  110 : ('right', 'NAME')
}

def p_name(tokens):
  '''expr : NAME expr'''
  tokens[0] = gen.generateName(names.sanitize(tokens[2]))




