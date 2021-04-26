import configparser

def read_config_file():
    config = configparser.ConfigParser()
    config.read('config.ini')
    result = {
        'community_name': config['DEFAULT']['community_name'],
        'data_dictionary_entity_type': config['DEFAULT']['data_dictionary_entity_type'],
    }
    return result