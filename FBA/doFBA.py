import cobra
import os


input_file = os.path.join(os.getcwd(), 'input\\', 'Master.json')
print(input_file)
'''
file = open(input_file)
f = file.read()
p = f[3230000:3232000]
print(p)
print(f[3030105: 3030200])
'''
file = open('cobrapyoutputjson.json')
f = file.read()
file.close()


model = cobra.io.load_json_model(f)
model.optimize()
print(model.solution.f)