import json



file = open('salmonella.json')
f = file.read()
file.close()
data = json.loads(f)

del data['compartments']
data['id'] = 'MasterJSON'
del data['metabolites'][0:]
del data['reactions'][0:]
data['number'] = 0

fp = open('template.json', 'w')
json.dump(data, fp)

print(data)

#  data is:  {'id': 'MasterJSON', 'metabolites': [], 'genes': [], 'reactions': []}