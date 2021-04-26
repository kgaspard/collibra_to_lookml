import collibra_sdk as sdk
from util import read_config_file

if __name__ == "__main__":
    config = read_config_file()
    community_id = sdk.get_communities(config['community_name'])[0]['id']
    data_dictionary = sdk.get_domains(community_id, config['data_dictionary_entity_type'])[0]
    lookml_fields = sdk.lookml_from_data_dictionary(data_dictionary['id'])

    print('done')
