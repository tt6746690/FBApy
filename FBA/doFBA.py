import cobra
import os


input_file = os.path.join(os.getcwd(), 'input\\', 'Master.json')
'''
file = open(input_file)
f = file.read()
p = f[3230000:3232000]
print(p)
print(f[3030105: 3030200])
'''
file = open('target.json')
f = file.read()
file.close()


model = cobra.io.load_json_model('target.json')
model.optimize()
print(model.solution.f)

