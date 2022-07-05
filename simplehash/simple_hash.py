import requests
import pprint
import os
from dotenv import load_dotenv
import json
load_dotenv()

# NFT_model = information about the tokens
# collection_model = nft_contract

bored_ape = "0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d"
headers = {
        "Accept": "application/json",
        "X-API-KEY": os.environ.get("sh_key")
    }

# get the basic contract information
def nfts_by_contract(contract_addr, headers):
    list_ = []
    request_url = f'https://api.simplehash.com/api/v0/nfts/ethereum/{contract_addr}'
    
    api_response = requests.get(request_url, headers=headers)
    data = api_response.json()
    collection_field = data['nfts'][0]['collection']
    list_.append(collection_field)
    return list_
# collection_field = nfts_by_contract(bored_ape)  
# pprint.pprint(nfts_by_contract(bored_ape))  


# get tokens for a collection with pagination
def get_collection_tokens(contract_addr, headers):
    tokens_for_collection = []
    request_url = f'https://api.simplehash.com/api/v0/nfts/ethereum/{contract_addr}'
    api_response = requests.get(request_url, headers=headers)
    next_batch = api_response.json()['next']

    for _dict in api_response.json()['nfts']:
        tokens_for_collection.append(_dict)
    
    while next_batch:
        api_response = requests.get(next_batch, headers=headers)
        next_batch = api_response.json()['next']

        for _dict in api_response.json()['nfts']:
            tokens_for_collection.append(_dict)
    
    return tokens_for_collection
    
        
pprint.pprint(get_collection_tokens(bored_ape, headers))


