from __future__ import print_function
import cobra.test
from cobra import Model, Reaction, Metabolite
model = cobra.test.create_test_model('salmonella')
pgi = model.reactions.get_by_id("PGI")
# print(pgi.name, pgi.reaction)
# print(pgi.lower_bound, "< pgi <", pgi.upper_bound)
# print(pgi.reversibility)
# print(pgi.check_mass_balance())
# print(model.metabolites.get_by_id("g6p_c").reactions)

# building a model
cobra_model = Model('example_cobra_model')

reaction = Reaction('3OAS140')
reaction.name = '3 oxoacyl acyl carrier protein synthase n C140 '
reaction.subsystem = 'Cell Envelope Biosynthesis'
reaction.lower_bound = 0.  # This is the default
reaction.upper_bound = 1000.  # This is the default
reaction.objective_coefficient = 0. # this is the default

ACP_c = Metabolite('ACP_c', formula='C11H21N2O7PRS',
    name='acyl-carrier-protein', compartment='c')
omrsACP_c = Metabolite('3omrsACP_c', formula='C25H45N2O9PRS',
    name='3-Oxotetradecanoyl-acyl-carrier-protein', compartment='c')
co2_c = Metabolite('co2_c', formula='CO2', name='CO2', compartment='c')
malACP_c = Metabolite('malACP_c', formula='C14H22N2O10PRS',
    name='Malonyl-acyl-carrier-protein', compartment='c')
h_c = Metabolite('h_c', formula='H', name='H', compartment='c')
ddcaACP_c = Metabolite('ddcaACP_c', formula='C23H43N2O8PRS',
    name='Dodecanoyl-ACP-n-C120ACP', compartment='c')

reaction.add_metabolites({malACP_c: -1.0,
                          h_c: -1.0,
                          ddcaACP_c: -1.0,
                          co2_c: 1.0,
                          ACP_c: 1.0,
                          omrsACP_c: 1.0})
reaction.gene_reaction_rule = '( STM2378  or STM1197 )'
cobra_model.add_reaction(reaction)
# Now there are things in the model
print('%i reaction in model' % len(cobra_model.reactions))
print('%i metabolites in model' % len(cobra_model.metabolites))
print('%i genes in model' % len(cobra_model.genes))

# Iterate through the the objects in the model
print("Reactions")
print("---------")
for x in cobra_model.reactions:
    print("%s : %s" % (repr(x), x.reaction))
print("Metabolites")
print("-----------")
for x in cobra_model.metabolites:
    print('%s : %s' % (repr(x), x.formula))
print("Genes")
print("-----")
for x in cobra_model.genes:
    reactions_list_str = ", ".join((repr(i) for i in x.reactions))
    print("%s is associated with reactions: %s" % (repr(x), reactions_list_str))


