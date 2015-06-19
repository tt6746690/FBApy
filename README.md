#FBApy

###xmltojson

The parser reads xml data and converts genome-scale metabolic reconstruction, in the form of sbml level 2 
version 1, to json. Incompatibilities are major issues. Excuse the shitty format. I want to vommit too.


###multiplespeciesJSON

**MakeMaster.py** merges metabolic reconstructions, without overlap, into a single **master.json** file, a multispecies 
depository that holds all the metabolites and reactions available.

**Retriever.py** selectively retrieves information from **master.json**, to allow for portability cross internet and interoperability with database/lp solver.


###FBA

does flux balance analysis with the aid of cobrapy.


###FBAtest

fiddling with possibilities
