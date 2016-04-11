import json
from pprint import pprint
import sys
import datetime

cluster_host = sys.argv[1]
cluster_port = sys.argv[2]
json_loads_1 = sys.argv[3]
json_loads_2 = sys.argv[4]

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
    pprint(cluster_host+":"+cluster_port)
    
    payload = {}
    payload['cluster'] = cluster_host+":"+cluster_port
    
    payload['index_name_1'] = json_loads_1
    payload['index_name_2'] = json_loads_2
    
    payload['index_data_1'] = data1
    payload['index_data_2'] = data2
    
    payload['issue_type'] = 'discrepancy' 
    payload['issue_message'] = 'discrepancy found between indices: ' + json_loads_1 + ',' + json_loads_2 + ''
    
    payload['@timestamp'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    
    json_data = json.dumps(payload)
    print str(json_data)
    
    import ConfigParser
    Config = ConfigParser.ConfigParser()
    Config.read("json-compare-engine.props")
    
    http_proto = Config.get('HTTPOutput', 'proto')
    http_host = Config.get('HTTPOutput', 'host')
    http_port = Config.get('HTTPOutput', 'port')

    
    r = requests.post(http_proto + '://' + http_host + ':' + http_port, data=json.dumps(payload))
    #r = requests.post('http://localhost:8080', data=json.dumps(payload))
