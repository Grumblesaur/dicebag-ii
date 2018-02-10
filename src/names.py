defaults = {
  'race'              : '',
  'gender'            : '',
  'first'             : True,
  'last'              : True,
  'first starts with' : '',
  'last starts with'  : '',
  'affix'             : False,
  'subrace'           : ''
}

options = {
  'race' : [
    'altmer',   'argonian', 'bosmer',
    'breton',   'dunmer',   'khajiit',
    'imperial', 'redguard', 'orsimer',
    'nord',
  ], 'gender' : [
    'male', 'female'
  ], 'subrace' : [
    'cyrodilic', 'reachman', 'cyrodiilic' # correct for spelling on this one
  ]
}

def sanitize(namespec):
  # ensure that all fields are supplied
  for key in defaults:
    if key not in namespec:
      namespec[key] = defaults[key]
  
  for key in options:
    if namespec[key] not in options[key]:
      namespec[key] = ''
  
  # correct for a possible common spelling mistake
  if namespec['subrace'] == 'cyrodiilic':
    namespec['subrace'] = 'cyrodilic'
  
  if namespec['subrace'] == 'cyrodilic' and namespec['race'] != 'argonian':
    namespec['subrace'] = ''
  elif namespec['subrace'] == 'reachman' and namespec['race'] != 'breton':
    namspec['subrace'] = ''
  
  return namespec
  
  
   
