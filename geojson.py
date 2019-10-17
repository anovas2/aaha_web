import json

with open('website/db/ga.geojson', 'r') as f:
    data = json.load(f)

#A Python dictionary containing properties to be added to each GeoJSON Feature
properties_dict={
    "property1": "foo",
    "property2": 10,
    "property3": 100
    }
#Convert the dictionary to a list
properties_list=zip(properties_dict.keys(),properties_dict.values())

#Loop over GeoJSON features and add the new properties
for feat in data['features']:
    for i in range(len(properties_list)):
        feat ['properties'][properties_list[i][0]]=properties_list[i][1]

#Write result to a new file
with open('new.geojson', 'w') as f:
    json.dump(data, f)