import cobra
import os
import json

input_file = os.path.join(os.getcwd(), 'input\\', 'Master.json')
'''
file = open('target.json')
f = file.read()
file.close()

f.replace('_DASH_', '')

file1 = open('target.json', 'w')
f1 = file1.write(f)
file1.close()
'''
model = cobra.io.load_json_model('target.json')
model.optimize()
print(model.solution.f)

