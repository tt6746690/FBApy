from multispeciesJSON.methods import *
import time
start_time = time.time()

master_json = load_json_to_object('template.json')
make_master(master_json)
dump_to_json(master_json)

print("--- %s seconds ---" % (time.time() - start_time))

