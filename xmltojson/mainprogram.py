from bs4 import BeautifulSoup
import os
import json

def build_soup(name):
    file = open(name)
    f = file.read()
    f.replace('__', '_')
    soup_m = BeautifulSoup(f)
    return soup_m

def do_everything(just_name):
    path_name = os.path.join(os.getcwd() + '/sbml/' + just_name)
    soup = build_soup(path_name)
#  add [, 'xml'] to incorporate lxml parser if present
    model_tag = soup.model

    output = {}
    compartments = model_tag.listofcompartments.find_all('compartment')
    compartment_list = []
    for item in compartments:
        temp = {}
        temp['id'] = item['id']
        temp['name'] = item['name']
        compartment_list.append(temp)

    species = model_tag.listofspecies.find_all('species')
    species_list = []
    for obj in species:
        temp = {}
        if 'DASH' in obj['id']:
            obj['id'].replace('DASH', '')
        temp['id'] = obj['id'][2:]
        temp['name'] = obj['name']
        temp['compartment'] = obj['compartment']
        temp['species'] = []
        temp['species'].append(model_tag['id'])
        p = obj.find_all('p')
        counter_in = 0
        for item in p:
            if item.text[:8] == 'FORMULA:':
                temp['formula'] = item.text[9:]
            if item.text[:7] == 'CHARGE:':
                if type(item.text[8:]) is int:
                    temp['charge'] = item.text[8:]
                else:
                    temp['charge'] = 0
                    counter_in += 1
        if (obj['id'][-2:] == '_e') or (obj['id'][-10:] == 'e_boundary'):
            temp['outside'] = True
        elif (obj['id'][-2:] == '_c') or (obj['id'][-2:] == '_p') or (obj['id'][-10:] == 'c_boundary'):
            temp['outside'] = None
        else:
            print('error in assigning metabolite outside attribute')
        species_list.append(temp)

    reaction = model_tag.listofreactions.find_all('reaction')
    reaction_list = []
    for good in reaction:
        temp = {}
        if 'DASH' in good['id']:
            good['id'].replace('DASH', '')
        temp['id'] = good['id'][2:]
        temp['name'] = good['name']
        temp['species'] = []
        temp['species'].append(model_tag['id'])
        if good.has_attr('reversible'):
            temp['reversible'] = good['reversible']
        else:
            temp['reversible'] = 'didnt specify'

        p = good.find_all('p')
        for item in p:
            if item.text[:17] == 'GENE_ASSOCIATION:':
                temp['gene association'] = item.text[18:]
            if item.text[:10] == 'SUBSYSTEM:':
                temp['subsystem'] = item.text[11:]
            if item.text[:10] == 'EC Number:':
                temp['EC_Number'] = item.text[11:]
        pp = good.find_all('speciesreference')
        metabolite = {}
        for item in pp:
            if item.has_attr('stoichiometry'):
                number = float(item['stoichiometry'])
                if item.parent.name == 'listofproducts':
                    if 'DASH' in item['species']:
                        item['species'].replace('DASH', '')
                    metabolite[item['species'][2:]] = number
                elif item.parent.name == 'listofreactants':
                    if 'DASH' in item['species']:
                        item['species'].replace('DASH', '')
                    metabolite[item['species'][2:]] = -number
                else:
                    print('error')
            else:
                if item.parent.name == 'listofproducts':
                    metabolite[item['species'][2:]] = float(1)
                elif item.parent.name == 'listofreactants':
                    metabolite[item['species'][2:]] = float(-1)
                else:
                    print('error')
        temp['metabolites'] = metabolite
        ppp = good.find_all('parameter')
        for item in ppp:
            if item['id'] == 'LOWER_BOUND':
                temp['lower_bound'] = float(item['value'])
            if item['id'] == 'UPPER_BOUND':
                temp['upper_bound'] = float(item['value'])
            if item['id'] == 'FLUX_VALUE':
                temp['flux_value'] = float(item['value'])
            if item['id'] == 'OBJECTIVE_COEFFICIENT':
                temp['objective_coefficient'] = float(item['value'])
        temp['outside'] = True
        for item in pp:
            if item['species'][-2:] != '_e':
                temp['outside'] = None
                break
        reaction_list.append(temp)

    output['id'] = model_tag['id']
    output['compartments'] = compartment_list
    output['metabolites'] = species_list
    output['reactions'] = reaction_list
    output['genes'] = []

    fp = open(os.path.join(os.getcwd() + '/speciesjson/' + os.path.splitext(os.path.basename(path_name))[0] + '.json'), 'w')
    fp.write(output)
    fp.close()
#    json.dump(output, fp)

counter = 1
sbmlfiles = []
for filename in os.listdir(os.path.join(os.getcwd() + '/sbml')):
    if filename.endswith('.xml'):
        sbmlfiles.append(filename)

for name in sbmlfiles:
    do_everything(name)



