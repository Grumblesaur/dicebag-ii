defaults = {
  'race'              : '',
  'gender'            : '',
  'types'             : ['first'],
  'first starts with' : '',
  'last starts with'  : '',
  'subrace'           : '',
  'syllables'         : 0
}

string_fields = (
  'race', 'gender', 'first starts with', 'last starts with', 'subrace'
)

def sanitize(namespec):
  x = normalize(namespec)
  return downcase(x)

def normalize(namespec):
  print(namespec)
  for key in defaults:
    if key not in namespec:
      namespec[key] = defaults[key]
  return namespec

def downcase(namespec):
  temp = namespec
  for key in namespec:
    temp[key.casefold()] = namespec[key]
  namespec = temp
  for key in string_fields:
    namespec[key] = namespec[key].casefold()
  namespec['types'] = [t.casefold() for t in namespec['types']]
  return namespec
  

if __name__ == '__main__':
  print(sanitize({}))

 
