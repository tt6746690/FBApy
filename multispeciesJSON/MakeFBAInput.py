'''
when try to access the multispecies json by model id, loop through reaction and metabolite species attribute
to see if that id is already there. if it is, copy reaction(metabolite) to a new file and, in the mean time,
add identifier to the reaction(metabolite) id if and only if the outside attribute is None. also remember to reset
the species attribute in the new file. If the outside attribute is True, then do not assign identifier.
'''

import os
import multispeciesJSON.methods as method

def load_master():
    src = os.path.join(os.getcwd(), 'master\\', 'Master.json')
    master_in = method.load_json_to_object(src)
    return master_in

master = load_master()