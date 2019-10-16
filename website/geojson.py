import json

def geojson_convert(census_income_to_rent_dataset):
    with open('../website/db/ga.geojson', 'r') as f:
        data = json.load(f)

    # data['features'].to_json('test.json')
    #A Python dictionary containing properties to be added to each GeoJSON Feature
    properties_dict={
        "property1": "foo",
        "property2": 10,
        "property3": 100
        }
    #Convert the dictionary to a list
    properties_list=zip(properties_dict.keys(),properties_dict.values())

    # census_income_to_rent_dataset.index = census_income_to_rent_dataset['GEOID']
    # census_income_to_rent_dataset = census_income_to_rent_dataset[[census_income_to_rent_dataset['YEAR'] == 2017]].to_dict('index')

    GEOID_LIST = census_income_to_rent_dataset['GEOID'].drop_duplicates().tolist()


    # for keys, values in data['features']:

    # for feat in data['features']:
    # print(feat['properties']['GEOID'])


    for index, row in census_income_to_rent_dataset.iterrows():
        GEOID = str(row['GEOID'])
        YEAR = row['YEAR']
        for feat in data['features']:
            feat1 = feat['properties']['GEOID']
            # print(row['GEOID'])
            #print(row.to_dict())
            if feat1 == GEOID:
                feat['properties']['HH_income'][YEAR] = row.to_dict()
                print('added' + GEOID)


    # for GEOID in GEOID_LIST:
    #     for index, row in census_income_to_rent_dataset.iterrows():
    #         for feat in data['features']:
    #             print(feat['properties']['GEOID'])
    #             print(row['GEOID'])
    #             if feat['properties']['GEOID'] == GEOID and row['GEOID'] == GEOID:
    #                 feat['properties']['HH_income'] = row



    # for GEOID in GEOIDLIST:
    #     var1 = data['features']['properties']['GEOID'] = row[]

    # #Loop over GeoJSON features and add the new properties
    # for feat in data['features']:
    #     for i in range(len(properties_list)):
    #         feat ['properties'][properties_list[i][0]]=properties_list[i][1]

    #Write result to a new file
    with open('new.geojson', 'w') as f:
        json.dump(data, f)
