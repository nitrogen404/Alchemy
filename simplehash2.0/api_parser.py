import requests
import pprint
import os
import math
from dotenv import load_dotenv
from datetime import datetime
from multiprocessing import Pool

load_dotenv()

headers = {
    "Accept": "application/json",
    "X-API-KEY": os.environ.get("sh_key"), 
}


def get_collection_metadata(contract_addr_list, headers):
    collection_metadata = []

    for address in contract_addr_list:
        request_url = f"https://api.simplehash.com/api/v0/nfts/ethereum/{address}"
        api_response = requests.get(request_url, headers=headers)
        contract_data = api_response.json()["nfts"][0]["collection"]

        # creating a temperary dictionary which contains a row of table
        collection_dict = {}
        collection_dict.update({'contract_address': address})
        collection_dict.update({"collection_id": contract_data["collection_id"]})
        collection_dict.update({"name": contract_data["name"]})
        collection_dict.update({"description": contract_data["description"]})
        collection_dict.update({"image_url": contract_data["image_url"]})
        collection_dict.update({"banner_image_url": contract_data["banner_image_url"]})
        collection_dict.update({"external_url": contract_data["external_url"]})
        collection_dict.update({"twitter_username": contract_data["twitter_username"]})
        collection_dict.update({"metaplex_mint": contract_data["metaplex_mint"]})
        collection_dict.update({"discord_url": contract_data["discord_url"]})
        collection_dict.update({"chain": api_response.json()["nfts"][0]["chain"]})

        collection_metadata.append(collection_dict)

    return collection_metadata


def create_row_nfts(value):
    token_dict = {}
    token_dict.update({'nft_id': value['nft_id']})
    token_dict.update({'chain': value['chain']})
    token_dict.update({'nft_id': value['nft_id']})
    token_dict.update({'contract_address': value['contract_address']})
    token_dict.update({'token_id': value['token_id']})
    token_dict.update({'name': value['name']})
    token_dict.update({'description': value['description']})
    token_dict.update({'image_url': value['image_url']})
    token_dict.update({'video_url': value['video_url']})
    token_dict.update({'audio_url': value['audio_url']})
    token_dict.update({'model_url': value['model_url']})
    token_dict.update({'previews': value['previews']})
    token_dict.update({'background_color': value['background_color']})
    token_dict.update({'external_url': value['external_url']})
    token_dict.update({'created_date': value['created_date']})
    token_dict.update({'status': value['status']})
    token_dict.update({'token_count': value['token_count']})
    token_dict.update({'owner_count': value['owner_count']})
    token_dict.update({'owners': []})
    if len(value['owners']) > 0:
        for _dict in value['owners']:
            token_dict['owners'].append(_dict)
        token_dict.update({'current_owner': token_dict['owners'][0]['owner_address']})
    
        
    return token_dict



def get_nfts_for_collection(contract_address_list, headers):
    collection_tokens = []
    for address in contract_address_list:
        print(address)
        request_url = f'https://api.simplehash.com/api/v0/nfts/ethereum/{address}'
        api_response = requests.get(request_url, headers=headers)
        cursor = api_response.json()['next']
        
        for value in api_response.json()['nfts']:
            collection_tokens.append(create_row_nfts(value))

        while cursor:
            new_set = requests.get(cursor, headers=headers)
            cursor = new_set.json()['next']
            for value in new_set.json()['nfts']:
                collection_tokens.append(create_row_nfts(value))
    
    return collection_tokens


def create_row_transfers(value):
    temp_dict = {}
    temp_dict.update({'from_address': value['from_address']})
    temp_dict.update({'to_address': value['to_address']})
    temp_dict.update({'timestamp': value['timestamp']})
    temp_dict.update({'contract_address': value['contract_address']})
    temp_dict.update({'chain': value['chain']})
    temp_dict.update({'block_number': value['block_number']})
    temp_dict.update({'token_id': value['token_id']})
    temp_dict.update({'quantity': value['quantity']})
    temp_dict.update({'log_index': value['log_index']})
    temp_dict.update({'batch_transfer_index': value['batch_transfer_index']})
    temp_dict.update({'block_hash': value['block_hash']})
    temp_dict.update({'transaction': value['transaction']})
    
    if value['sale_details']:
        temp_dict.update({'marketplace_name': value['sale_details']['marketplace_name']})
        temp_dict.update({'is_bundle_sale': value['sale_details']['is_bundle_sale']})
        temp_dict.update({'payment_token': value['sale_details']['payment_token']})
        temp_dict.update({'unit_price': value['sale_details']['unit_price']})
        temp_dict.update({'total_price': value['sale_details']['total_price']})
    
        
    return temp_dict


def get_contract_transfers(contract_address_list, headers):
    contract_transfers = []
    for address in contract_address_list:
        request_url = f'https://api.simplehash.com/api/v0/nfts/transfers/ethereum/{address}?order_by=timestamp_desc'
        api_response = requests.get(request_url, headers=headers)
        cursor = api_response.json()['next']
        for value in api_response.json()['transfers']:
            contract_transfers.append(create_row_transfers(value))

        while cursor:
            new_set = requests.get(cursor, headers=headers)
            cursor = new_set.json()['next']
            for value in new_set.json()['transfers']:
                contract_transfers.append(create_row_transfers(value))                             
            
    return contract_transfers


def owners_for_collection(contract_address_list, headers):
    for collection in contract_address_list:
        print("collection: ", collection)
        request_url = f'https://api.simplehash.com/api/v0/nfts/owners/ethereum/{collection}'
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
    
    sorted_dict = {}
    for k in sorted(temp_dict, key=lambda k: len(temp_dict[k]), reverse=True):
        sorted_dict[k] = temp_dict[k]
    
    return sorted_dict


# gives top 1% whales of a collection
# input = owners_for_collection
# output a list of wallet addresses
def collection_whales(owners_dict):
    collection_whales = []
    keys = list(owners_dict)

    for i in range(math.ceil(0.01 * len(keys))):
        collection_whales.append(keys[i])

    return collection_whales



def whale_activity(contract_address_list):
    collection_owners = owners_for_collection(contract_address_list, headers)
    collection_owners_list = collection_whales(collection_owners)
    
    transfers_list = []
    time_format = '%Y-%m-%d %H:%M:%S'
    current_date = datetime.now().isoformat(' ', "seconds")
    current_date_obj = datetime.strptime(current_date, time_format)
    
    s = requests.Session()
    for address in collection_owners_list:
        print(address)
        request_url = f'https://api.simplehash.com/api/v0/nfts/transfers/wallets?chains=ethereum&wallet_addresses={address}'
        api_response = s.get(request_url, headers=headers)
        cursor = api_response.json()['next']
        
        for value in api_response.json()['transfers']:
            api_date = value['timestamp']
            api_date = api_date.replace("T", " ")
            api_date = api_date.replace("Z", "")
            api_date_obj = datetime.strptime(api_date, time_format)
            
            if (current_date_obj - api_date_obj).days < 30:
                transfers_list.append(create_row_transfers(value))
            else:
                break
        
        print("....")
        while cursor:
            new_set = requests.get(cursor, headers=headers)
            cursor = new_set.json()['next']
            for value in new_set.json()['transfers']:
                api_date = value['timestamp']
                api_date = api_date.replace("T", " ")
                api_date = api_date.replace("Z", "")
                api_date_obj = datetime.strptime(api_date, time_format)
                
                if (current_date_obj - api_date_obj).days < 30:
                    transfers_list.append(create_row_transfers(value))
                else:
                    break
        

    return transfers_list




# get the collection information
# get the all tokens in that collection
# get the transfers in that collection
# get the trading activity of whales of that collection

contracts = ["0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"]
# collection_table = get_collection_metadata(contracts, headers)
# nfts_table = get_nfts_for_collection(contracts, headers)
# transfers_table = get_contract_transfers(contracts, headers)
wallet_activity_table = whale_activity(contracts)




