'''
s
the combination of species json file will be constructed based on the assumption
that all metabolite and reaction, if their id(s) are the same, everythin within
the the reaction metabolite is the same.

another attribute inside the combined json file, under reactions and metabolites,
called species will contain id of the species that have that reaction or metabolite.
when forming the multispecies json, for every reaction(metaoblites) loop through what
is already present in the json file and see if their id matches. If a reaction(metabolite)
is already there, add id of species to the species list. If not, append the reaction json
to the reaction list. and append id of species to the species list. species list here does
not equate to metabolite list, as sbml convention suggests. Additionally, create
a outside attribute to each reaction(metabolite). If the metabolite ends in '_e' or if the reaction
happens entirely in extracellular environment(both reactant and product end in '_e'), then assign
the outside attribbute to True. Otherwise, assign the outside attribute to None.
'''
import shutil
import json
import os

def get_sbml_in_a_list():
    list_used = []
    parent_dir = os.path.dirname(os.getcwd())
    where_sbml_is_at = os.path.join(parent_dir, 'xmltojson\speciesjson\\')
    for file_in in os.listdir(where_sbml_is_at):
        if file_in.endswith('.json'):
            full_name = where_sbml_is_at + file_in
            list_used.append(full_name)
    return list_used

def load_json_to_object(name):
    file = open(name)
    f = file.read()
    file.close()
    loaded = json.loads(f)
    return loaded

def check_number_attribute_in_master(midway):
    if midway['number'] == 0:
        return True
    else:
        return None

def increase_number_attribute(final):
    final['number'] += 1

def initial_load(source, sink):
    count = 0
    counter = 0
    print('mergeing ' + source['id'] + ' to ' + sink['id'] + ':')
    for metabolite in source['metabolites']:
        sink['metabolites'].append(metabolite)
        counter += 1
    logging('metabolites', count, counter)
    counter = 0
    for reaction in source['reactions']:
        sink['reactions'].append(reaction)
        counter += 1
    logging('reactions', count, counter)
    increase_number_attribute(sink)

def later_load_metabolite(source, sink):
    counter = 0
    count = 0
    have = False
    for metabolite_source in source['metabolites']:
        for metabolite_sink in sink['metabolites']:
            if metabolite_source['id'] == metabolite_sink['id']:
                metabolite_sink['species'].append(source['id'])
                count += 1
                have = True
                break
        if not have:
            sink['metabolites'].append(metabolite_source)
            counter += 1
        have = False
    logging('metabolites', count, counter)

def logging(category, count, counter):
    print(category + ': sharing ' + str(count) + ' || adding ' + str(counter))

def later_load_reaction(source, sink):
    counter = 0
    count = 0
    have = False
    for reaction_source in source['reactions']:
        for reaction_sink in sink['reactions']:
            if reaction_source['id'] == reaction_sink['id']:
                reaction_sink['species'].append(source['id'])
                count += 1
                have = True
                break
        if not have:
            sink['reactions'].append(reaction_source)
            counter += 1
        have = False
    logging('reactions', count, counter)

def later_load(source, sink):
    print('mergeing ' + source['id'] + ' to ' + sink['id'] + ':')
    later_load_metabolite(source, sink)
    later_load_reaction(source, sink)
    increase_number_attribute(sink)

def reconcile(master):
    print('<===IN MASTER===> ' + str(len(master['metabolites'])) + ' metabolites || ' +
          str(len(master['reactions'])) + ' reactions')

def make_master(master):
    for filename_s in get_sbml_in_a_list():
        model = load_json_to_object(filename_s)
        if check_number_attribute_in_master(master):
            initial_load(model, master)
        else:
            later_load(model, master)
        reconcile(master)

def dump_to_json(master):
    parent_dir = os.path.dirname(os.getcwd())
    src = os.path.join(os.getcwd(), 'master\\', 'Master.json')
    dst = os.path.join(parent_dir, 'FBA\input\\', 'Master.json')
    fp = open(src, 'w')
    json.dump(master, fp)
    shutil.copyfile(src, dst)


