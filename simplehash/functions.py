import requests
import pprint
import os
from dotenv import load_dotenv
import json
load_dotenv()

bored_ape = "0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d"
headers = {
        "Accept": "application/json",
        "X-API-KEY": os.environ.get("sh_key"), 
        
}

def get_collection_tokens(contract_addr, headers):
    all_tokens = []
    request_url = f'https://api.simplehash.com/api/v0/nfts/ethereum/{contract_addr}'  # 0-49
    api_response = requests.get(request_url, headers=headers)
    cursor = api_response.json()['next']  # 49-99
    
    
    for value in api_response.json()['nfts']:
        temp_dict = {}
        temp_dict.update({'token_id': value['token_id']})
        temp_dict.update({'collection_id': value['collection']['collection_id']})
        temp_dict.update({'contract_addr': value['contract_address']})
        temp_dict.update({'date_created': value['created_date']})
        all_tokens.append(temp_dict) 
    
    while cursor:
        new_set = requests.get(cursor, headers=headers)
        cursor = new_set.json()['next'] 

        for value in new_set.json()['nfts']:
            temp_dict = {}
            temp_dict.update({'token_id': value['token_id']})
            temp_dict.update({'collection_id': value['collection']['collection_id']})
            temp_dict.update({'contract_addr': value['contract_address']})
            temp_dict.update({'date_created': value['created_date']})
            temp_dict.update({'owner': []})
            if len(value['owners']) > 0:
                for _dict in value['owners']:
                    temp_dict['owner'].append(_dict['owner_address'])
            
            all_tokens.append(temp_dict)
    return all_tokens

# pprint.pprint(get_collection_tokens(bored_ape, headers))

def get_contract_transfers(contract_addr, headers):
    contract_transfers = []
    request_url = f'https://api.simplehash.com/api/v0/nfts/transfers/ethereum/{contract_addr}'
    api_response = requests.get(request_url, headers=headers)
    cursor = api_response.json()['next']
    file = open("transfers.txt", 'w+')

    for _dict in api_response.json()['transfers']:
        temp_dict = {}
        temp_dict.update({'token_id': _dict['token_id']})
        temp_dict.update({'from_addr': _dict['from_address']})
        temp_dict.update({'to_addr': _dict['to_address']})
        temp_dict.update({'contract_address': _dict['contract_address']})
        temp_dict.update({'transaction': _dict['transaction']})
        temp_dict.update({'log_index': _dict['log_index']})
        temp_dict.update({'time': _dict['timestamp']})
        file.write(json.dumps(temp_dict))
        file.write("\n")
        contract_transfers.append(temp_dict)
    
    while cursor:
        new_set = requests.get(cursor, headers=headers)
        cursor = new_set.json()['next']
        
        for _dict in api_response.json()['transfers']:
            temp_dict = {}
            temp_dict.update({'token_id': _dict['token_id']})
            temp_dict.update({'from_addr': _dict['from_address']})
            temp_dict.update({'to_addr': _dict['to_address']})
            temp_dict.update({'contract_address': _dict['contract_address']})
            temp_dict.update({'transaction': _dict['transaction']})
            temp_dict.update({'log_index': _dict['log_index']})
            temp_dict.update({'time': _dict['timestamp']})
            file.write(json.dumps(temp_dict))
            file.write("\n")
            contract_transfers.append(temp_dict)
    
    return contract_transfers

# pprint.pprint(get_contract_transfers(bored_ape, headers))


# get the owners of tokens in BAYC
# get the tokens owned by those owners in BAYC


def owners_for_token(contract_address, headers):
    request_url = f'https://api.simplehash.com/api/v0/nfts/owners/ethereum/{contract_address}'
    api_response = requests.get(request_url, headers=headers)
    cursor = api_response.json()['next']

    temp_dict = {}
    for _dict in api_response.json()['owners']:
        if _dict['owner_address'] in temp_dict:
            tokens_owned = temp_dict.get(_dict['owner_address'])
            tokens_owned.append(_dict['token_id'])
        else:
            temp_dict.update({_dict['owner_address']: [_dict['token_id']]})
    
    while cursor:
        new_set = requests.get(cursor, headers=headers)
        cursor = new_set.json()['next']
        
        for _dict in new_set.json()['owners']:
            if _dict['owner_address'] in temp_dict:
                tokens_owned = temp_dict.get(_dict['owner_address'])
                tokens_owned.append(_dict['token_id'])
            else:
                temp_dict.update({_dict['owner_address']: [_dict['token_id']]})
    
    
    return temp_dict

owners = owners_for_token(bored_ape, headers)
pprint.pprint(owners_for_token(bored_ape, headers))