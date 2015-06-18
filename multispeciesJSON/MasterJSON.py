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


when try to access the multispecies json by model id, loop through reaction and metabolite species attribute
to see if that id is already there. if it is, copy reaction(metabolite) to a new file and, in the mean time,
add identifier to the reaction(metabolite) id if and only if the outside attribute is None. also remember to reset
the species attribute in the new file. If the outside attribute is True, then do not assign identifier.
'''