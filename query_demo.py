import requests
import csv

##The URI is the localhost, so it will change once the API is online
BASE = "http://127.0.0.1:5000/"

##This is function works like the range() function since range() doesn't work for decimals
def in_range(x, lower, upper):
    if x > lower and x  < upper:
        return True
    else:
        return False

##Send the request to the API
BC_generators = requests.get(BASE + "generators?province=BC")
##Store the generators in the given coordinates
generators_in_area = []
##Open the output file and format the csv file
gens = open('output.csv', mode='w')
references = open('ref.csv', mode='w')
gens_output_file = csv.writer(gens, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
ref_output_file = csv.writer(references, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

##Parse the list of generators
for gen in BC_generators.json():
    ##Check if the latitude is in the range (you can change the range below)
    if in_range(gen['latitude'], 49.49, 50): 
        ##Check if the longitude is in the range
        if in_range(gen['longitude'], -116, -114):
            gen = (gen['project_name'], gen['gen_node_code'], gen['latitude'], gen['longitude'], gen['sources'])
            gens_output_file.writerow(gen)

## Get the source
source = requests.get(BASE + "references?key=663").json()
ref_output_file.writerow(list(source))

references.close()
gens.close()