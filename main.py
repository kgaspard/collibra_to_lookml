import collibra_sdk as sdk

community_id = sdk.get_communities('Apex')[0]['id']
data_dictionary = sdk.get_domains(community_id, 'Logical Data Dictionary')[0]
for dim  in sdk.lookml_from_data_dictionary(data_dictionary['id']):
    print(dim)


