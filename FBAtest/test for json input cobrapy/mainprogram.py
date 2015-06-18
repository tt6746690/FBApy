import cobra

model = cobra.io.load_json_model('iJO1366.json')
model.optimize()
print(model.solution.x_dictf)