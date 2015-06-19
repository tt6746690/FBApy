'''
when try to access the multispecies json by model id, loop through reaction and metabolite species attribute
to see if that id is already there. if it is, copy reaction(metabolite) to a new file and, in the mean time,
add identifier to the reaction(metabolite) id if and only if the outside attribute is None. also remember to reset
the species attribute in the new file. If the outside attribute is True, then do not assign identifier.
'''

import os
import multispeciesJSON.methods as method

masterJSON = method.load_json_to_object(os.path.join(os.getcwd(), 'master\\', 'Master.json'))
models = ['iJO1366', "Salmonella_consensus_build_1"]
template = method.load_json_to_object('template.json')


output = method.retrieve_all(models, masterJSON, template)
#  use item in models list to fetch data from masterJSON and output to template

method.dump_to_json_for_retriever(output)
