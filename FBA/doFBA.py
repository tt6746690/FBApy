import cobra
import os
import json

input_file = os.path.join(os.getcwd(), 'input\\', 'iJO1366.json')
'''
file = open('target.json')
f = file.read()
file.close()

f.replace('_DASH_', '')

file1 = open('target.json', 'w')
f1 = file1.write(f)
file1.close()
'''
model = cobra.io.load_json_model(input_file)
model.optimize()
flux_dict = model.solution.x_dict

fp = open('flux_dict.json', 'w')
json.dump(flux_dict, fp)




