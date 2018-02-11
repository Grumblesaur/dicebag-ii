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

sans_last = (
  'altmer', 'argonian', 'bosmer', 
  'nord',   'redguard', 'khajiit'
)

options = {
  'race' : (
    'altmer',   'argonian', 'bosmer',
    'breton',   'dunmer',   'khajiit',
    'imperial', 'redguard', 'orsimer',
    'nord',
  ), 'gender' : (
    'male', 'female'
  ), 'subrace' : (
    'cyrodilic', 'reachman', 'cyrodiilic' # correct for spelling on this one
  )
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
  
  if namespec['race'] in sans_last:
    namespec['last'] = False
    namespec['last starts with'] = ''
  
  if not namespec['first starts with'].isalpha():
    namespec['first starts with'] = ''
  if not namespec['last stats with'].isalpha():
    namespec['last starts with' = ''
  
  return namespec
  
  
   
