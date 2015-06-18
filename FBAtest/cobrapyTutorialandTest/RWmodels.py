import cobra.test
import cobra
model = cobra.test.create_test_model()
# biomass = model.reactions.get_by_id("biomass_iRR1083_metals")
# print(biomass.objective_coefficient)
# model = cobra.io.load_json_model(cobra.test.ecoli_json)

model.objective

# change the objective to ATPM
# the upper bound should be 1000 so we get the actual optimal value
model.reactions.get_by_id("ATPM").upper_bound = 1000.
model.objective = "ATPM"
print(model.objective)

