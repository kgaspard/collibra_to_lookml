import collibra_sdk as sdk

if __name__ == "__main__":
    community_id = sdk.get_communities('Apex')[0]['id']
    data_dictionary = sdk.get_domains(community_id, 'Logical Data Dictionary')[0]
    lookml_fields = sdk.lookml_from_data_dictionary(data_dictionary['id'])
    # for dim in lookml_fields:
    #     print(dim)

    print('done')
