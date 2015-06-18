import cobra

ecoli_model = cobra.io.read_sbml_model("modified_1.xml")
# Yersinia_pestis_CO92_iPC815    0.2835583812145318
#iJO1366 and msb ecoli  0.9823718127270421
# salmonella  0.38000797227400634

ecoli_model.optimize()
flux = ecoli_model.solution.f
print(flux)

#output_file.write(str(flux))
# output_file.close()

#cobra.io.json.save_json_model(ecoli_model, "output test.json")