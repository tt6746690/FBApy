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
    print('merging ' + source['id'] + ' to ' + sink['id'] + ':')
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
    print('merging ' + source['id'] + ' to ' + sink['id'] + ':')
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




#  //////////////////////////////////////////////////////////////////////////
#  ------- for retriever.py -----

def dump_to_json_for_retriever(target):
    fp = open('target.json', 'w')
    json.dump(target, fp)


def adding_prefix_to_metabolites_in_reaction(reaction_s_metabolite_json, item):
    m_dict = {}
    for obj in reaction_s_metabolite_json.items():
        new = list(obj)
        if new[0][-2:] == '_e' or new[0][-10:] == 'e_boundary':
            new[0] = 'shared' + '-' + new[0]
        elif (new[0][-2:] == '_c') or (new[0][-2:] == '_p') or (new[0][-10:] == 'c_boundary'):
            new[0] = item + '-' + new[0]
# have to modify this part to incorporate what to do with metabolites that end in _boundary
        m_dict[new[0]] = new[-1]
    return m_dict

def include_necessary_attribute(metabolite_or_reaction, item, category):
    new= {}
    new['id'] = item + '-' + metabolite_or_reaction['id']
    new['name'] = metabolite_or_reaction['name']
    if category == 'metabolites':
        new['compartment'] = metabolite_or_reaction['compartment']
        new['charge'] = metabolite_or_reaction['charge']
        new['formula'] = metabolite_or_reaction['formula']
    if category == 'reactions':
        new['metabolites'] = adding_prefix_to_metabolites_in_reaction(metabolite_or_reaction['metabolites'], item)
        new['upper_bound'] = metabolite_or_reaction['upper_bound']
        new['lower_bound'] = metabolite_or_reaction['lower_bound']
        new['objective_coefficient'] = metabolite_or_reaction['objective_coefficient']
        new['subsystem'] = metabolite_or_reaction['subsystem']
    return new



def retrieve_metabolite_or_reaction(model, master, target, category):
    counter1 = 0
    counter2 = 0
    counter3 = 0
    for m_or_r_json in master[category]:
        intersection = list(set(model) & set(m_or_r_json['species']))
        if intersection and (m_or_r_json['outside'] is None):
            for item in intersection:
                target[category].append(include_necessary_attribute(m_or_r_json, item, category))
                counter1 += 1
        elif intersection and (m_or_r_json['outside'] is True):
            target[category].append(include_necessary_attribute(m_or_r_json, 'shared', category))
#   may only have one species that have this extracellular reaction
            counter2 += 1
        elif not intersection:
            print(m_or_r_json['id'], ' not present in the requested model')
            counter3 += 1
        else:
            print('something went wrong :(')
    print(category + ': ' + str(counter1) + ' duplicates || ' + str(counter2) +
          ' shared || ' + str(counter3) + ' not used')
    midway = target
    return midway

def retrieve_all(model, source, sink):
    print('In Target:')
    midway = retrieve_metabolite_or_reaction(model, source, sink, 'metabolites')
    final = retrieve_metabolite_or_reaction(model, source, midway, 'reactions')
    return final

