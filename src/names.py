defaults = {
  'race'              : '',
  'gender'            : '',
  'types'             : ['first'],
  'first starts with' : '',
  'last starts with'  : '',
  'affix'             : False,
  'subrace'           : ''
}

string_fields = (
  'race', 'gender', 'first starts with', 'last starts with', 'subrace'
)

categories = ('first', 'last')

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

def normalize(namespec):
  for key in defaults:
    if key not in namespec:
      namespec[key] = defaults[key]
  return namspec

def downcase(namespec):
  for key in namespec:
    namespec[key.casefold()] = namespec[key]
    del namespec[key]
  for key in string_fields:
    namespec[key] = namespec[key].casefold()
  namespec['types'] = [t.casefold() for t in namespec['types']]
  return downcase

def sanitize(namespec):
  for nametype in namespec['types']:
    if nametype not in categories:
      namespec['types'].pop(nametype)
  
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
    namespec['last starts with'] = ''
  
  return namespec
  
  

if __name__ == '__main__':
  print(sanitize(downcase({ })))


