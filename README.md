####FBApy

#xmltojson

The parser reads xml data and converts genome-scale metabolic reconstruction, in the form of sbml level 2 
version 1, to json. 


#multiplespeciesJSON

multiple json reconstruction can be merged, without overlap, into a single **master.json** file, a multispecies 
depository that holds all the metabolites and reactions available.

A **retriever.py** will be setup to allow for selective retrieval of information from **master.json**, to allow for
portability cross internet and interoperability with database/fba.


#FBA

does flux balance analysis with the aid of cobrapy.


#FBAtest

fiddling with possibilities
