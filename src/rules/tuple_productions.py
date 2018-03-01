def p_tuple_literal(tokens):
  '''expr : TUP_OPEN tup_elements TUP_CLOSE
          | TUP_OPEN TUP_CLOSE'''
  if len(tokens) == 4:
    tokens[0] = tuple(tokens[2])
  else:
    tokens[0] = ()

def p_tuple_elements(tokens):
  '''tup_elements : tup_elements COM expr
                  | expr'''
  if len(tokens) == 4:
    tokens[0] = tokens[1] + [tokens[3]]
  else:
    tokens[0] = [tokens[1]]

def p_tuple_convert(tokens):
  '''expr : TUP expr'''
  try:
    tokens[0] = tuple(tokens[2])
  except TypeError:
    tokens[0] = (tokens[2],)

def p_list_convert(tokens):
  '''expr : LIST expr'''
  try:
    tokens[0] = list(tokens[2])
  except TypeError:
    tokens[0] = [tokens[2]] 


