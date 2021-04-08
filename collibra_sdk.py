import requests, base64, configparser

def read_config_file():
    config = configparser.ConfigParser()
    config.read('credentials.ini')
    result = {
        'base_url': config['DEFAULT']['base_url'],
        'username': config['DEFAULT']['username'],
        'password': config['DEFAULT']['password'],
    }
    return result

base_url = read_config_file()['base_url']

def create_auth():
    username = read_config_file()['username']
    password = read_config_file()['password']
    usrPass = "%s:%s" % (username, password)
    b64Val = base64.b64encode(usrPass.encode()).decode("ascii")
    return "Basic %s" % b64Val

def check_status():
    r = requests.get(f'{base_url}/application/info')
    return r.json()

def get_communities(name):
    r = requests.get(f'{base_url}/communities'
        , headers={'Authorization': create_auth()}
        , params={'name': name, 'nameMatchMode': 'ANYWHERE', 'excludeMeta': 'true'})
    return r.json()['results']

def get_domain_types(name):
    r = requests.get(f'{base_url}/domainTypes'
        , headers={'Authorization': create_auth()}
        , params={'name': name, 'nameMatchMode': 'ANYWHERE', 'excludeMeta': 'true'})
    return r.json()['results']

def get_domains(communityId, type=None):
    params={'communityId': communityId, 'excludeMeta': 'true', 'includeSubCommunities': 'false'}
    if type: params['typeId'] = get_domain_types(type)[0]['id']
    r = requests.get(f'{base_url}/domains'
        , headers={'Authorization': create_auth()}
        , params=params)
    return r.json()['results']

def get_domain_details(domainId):
    r = requests.get(f'{base_url}/domains/{domainId}'
        , headers={'Authorization': create_auth()})
    return r.json()

def get_domain_assets(domainId):
    r = requests.get(f'{base_url}/assets'
        , headers={'Authorization': create_auth()}
        , params={'domainId': domainId, 'excludeMeta': 'true'})
    return r.json()['results']

def lookup_data_dictionary_glossary_terms(data_dictionary_domainId):
    communityId = get_domain_details(data_dictionary_domainId)['community']['id']
    communityDomains = get_domains(communityId)
    communityGlossaries = [domain for domain in communityDomains if domain['type']['name']=='Glossary' or domain['type']['name']=='Business Glossary']
    assets = get_domain_assets(data_dictionary_domainId)
    glossary_assets = [get_domain_assets(glossary['id']) for glossary in communityGlossaries]
    for asset in assets:
        for glossary in glossary_assets:
            for elem in glossary:
                asset['description'] = elem['description']
    return assets

def lookml_from_data_dictionary(data_dictionary_domainId):

    def pascalcase_string(string):
        return string.lower().replace(' ','_')

    assets = get_domain_assets(data_dictionary_domainId)
    community_name = get_domain_details(data_dictionary_domainId)['community']['name']

    fields = []
    for asset in assets:
        asset_type = asset['type']['name']
        if asset_type == 'Data Entity' or asset_type == 'Data Attribute':
            asset_name = asset['name']
            group_label = asset_name.split()[0]
            text = f"""dimension: {pascalcase_string(asset_name)} {{
    type: string
    sql: ${{TABLE}}.{pascalcase_string(asset_name)} ;;
    label: \"{asset_name}\"
    group_label: \"{group_label}\"
    required_accrss_grants: {pascalcase_string(community_name)}
}}"""
            fields.append(text)
    text = f"measure: count {{\n\ttype: count\n}}"
    fields.append(text)
    return fields
