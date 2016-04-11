import json
from pprint import pprint

import sys

json_loads_1 = sys.argv[1]
json_loads_2 = sys.argv[2]

#json_loads_1 = "data/index-2016.04.10_hostsarray.json"
#json_loads_2 = "data/index-2016.04.11_hostsarray.json"

print json_loads_1
print json_loads_2

with open(json_loads_1) as data_file:    
    data1 = json.load(data_file)
#pprint(data1)

with open(json_loads_2) as data_file:    
    data2 = json.load(data_file)
#pprint(data2)

def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


result = ordered(data1) == ordered(data2)
print "result was: " + str(result)
if result == False:
    pprint(data1)
    pprint(data2)

    
    
