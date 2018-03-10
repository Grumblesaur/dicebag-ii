def p_red(tokens):
  '''expr : RED expr'''
  tokens[0] = "```diff\\n- %s```" % str(tokens[2])

def p_green(tokens):
  '''expr : GREEN expr'''
  tokens[0] = "```diff\\n+ %s```" % str(tokens[2])

def p_gray(tokens):
  '''expr : GRAY expr'''
  tokens[0] = "```%s```" % str(tokens[2])

def p_str(tokens):
  '''expr : STR expr'''
  tokens[0] = str(tokens[2])


