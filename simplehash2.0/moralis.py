import os
import json 
import pprint
import requests
from dotenv import load_dotenv

load_dotenv()
headers = {
    "Accept": "application/json",
    "X-API-KEY": os.environ.get("moralis_key"), 
}


contracts = ["0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"]

def create_row_transfers(dict_obj, token_id):
    temp_dict = {}
    temp_dict.update({'block_hash': dict_obj['block_hash']})
    temp_dict.update({'block_number': dict_obj['block_number']})
    temp_dict.update({'block_timestamp': dict_obj['block_timestamp']})
    temp_dict.update({'to_address': dict_obj['buyer_address']})
    temp_dict.update({'from_address': dict_obj['seller_address']})
    temp_dict.update({'marketplace_address': dict_obj['marketplace_address']})
    temp_dict.update({'price': int(dict_obj['price']) / (10 ** 18)})
    temp_dict.update({'price_token_address': dict_obj['price_token_address']})
    temp_dict.update({'contract_address': dict_obj['token_address']})
    temp_dict.update({'token_id': token_id})
    temp_dict.update({'transaction_hash': dict_obj['transaction_hash']})
    temp_dict.update({'transaction_index': dict_obj['transaction_index']})
    return temp_dict
    
    
def get_contract_transfers(contract_addr_list, headers):
    transfers = []
    for address in contract_addr_list:
        url = f'https://deep-index.moralis.io/api/v2/nft/{address}/trades?chain=eth&marketplace=opensea'
        api_response = requests.get(url, headers=headers)
        cursor = api_response.json()['cursor']
        for value in api_response.json()['result']:
            if len(value['token_ids']) > 1:
                for token in value['token_ids']:
                    transfers.append(create_row_transfers(value, token))
            else:
                transfers.append(create_row_transfers(value, value['token_ids'][0]))
        
        while cursor:
            new_set = requests.get(url, params={'cursor': cursor}, headers=headers)
            cursor = new_set.json()['cursor']
            
            for value in new_set.json()['result']:
                if len(value['token_ids']) > 1:
                    for token in value['token_ids']:
                        transfers.append(create_row_transfers(value, token))
                else:
                    transfers.append(create_row_transfers(value, value['token_ids'][0]))
        
    return transfers
    

transfers_ = get_contract_transfers(contracts, headers)
