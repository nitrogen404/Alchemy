import os
import json
import requests
from dotenv import load_dotenv
import pprint
import time
load_dotenv()

base_url = "https://eth-mainnet.g.alchemy.com/nft/v2/" + os.environ.get("ALCHEMY_API_KEY")
bored_ape = "0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d"  # bored ape contains some empty fields

def nftCollections(url, address):
    request_url = url + "/getContractMetadata/?contractAddress=" + address
    collection_data = requests.get(request_url)
    return [collection_data.json()]
# pprint.pprint(nftCollections(base_url, bored_ape))


def nfts_for_collection(base_url, contractAddr, startToken):  # returns a list of dictionaries
    request_url = f'{base_url}/getNFTsForCollection/?contractAddress={contractAddr}&withMetadata=true&startToken={startToken}'
    nfts_data = requests.get(request_url)
    return nfts_data.json()
# pprint.pprint(nfts_for_collection(base_url, bored_ape, startToken=""))


def scale_nft_collection(url, contractAddr):
    token_collection = []
    total_supply_request = requests.get(url + "/getContractMetadata/?contractAddress=" + contractAddr) 
    total_supply = total_supply_request.json()['contractMetadata']['totalSupply'] 
    start_token = 0
    while start_token < 110:
        api_requests = nfts_for_collection(url, contractAddr, start_token)
        nfts = api_requests['nfts']
        token_collection = token_collection + nfts
        start_token += 100
        
    return token_collection 
# pprint.pprint(scale_nft_collection(base_url, bored_ape))


# select the contract address
# select the tokenID 
# use this to call getownersfortoken method 
# append this info in table 
def getOwners_fortoken(url, contractAddr, raw_token_response):
    owners_dict = []
    more_tokens = raw_token_response
    for dictionary in more_tokens:
        token_number = dictionary['id']['tokenId']
        # print(token_number)
        try:
            request_url = requests.get(f'{url}/getOwnersForToken?contractAddress={contractAddr}&tokenId={token_number}')
            api_response = request_url.json()
            owners_dict.append({'tokenNumber': int(token_number, 16), 'wallet_addr': api_response['owners'][0]})
        except:
            owners_dict.append({'tokenNumber': int(token_number, 16), 'wallet_addr': " "})
    
    return owners_dict
# pprint.pprint(getOwners_fortoken(base_url, bored_ape, scale_nft_collection(base_url, bored_ape)))

def get_tokenData(raw_token_response, owners_data):
    token_list = []

    for i in range(len(raw_token_response)):
        temp_dict = dict()
        dictionary = raw_token_response[i]

        temp_dict.update({'collection_addr': dictionary['contract']['address']})
        temp_dict.update({'tokenID': int(dictionary['id']['tokenId'], 16)})
        temp_dict.update({'owner': owners_data[i]['wallet_addr']})
        temp_dict.update({'tokenType': dictionary['id']['tokenMetadata']['tokenType']})
        temp_dict.update({'title': dictionary['title']})
        temp_dict.update({'description': dictionary['description']})
        temp_dict.update({'timestamp': dictionary['timeLastUpdated']})
        metadata_dict = dictionary['metadata']
        
        temp_array = []
        for i in metadata_dict['attributes']:
            temp_array.append(i['value'])

        temp_dict.update({'traits': temp_array})
        temp_dict.update({'metadata': metadata_dict['attributes']})
        mediaDict = dictionary['media'][0]
        temp_dict.update({'imageURL': mediaDict['gateway']})
        token_list.append(temp_dict)

    return token_list

raw_token_response = scale_nft_collection(base_url, bored_ape)
ownerof_token = getOwners_fortoken(base_url, bored_ape, raw_token_response) 
pprint.pprint(get_tokenData(raw_token_response, ownerof_token))
# pprint.pprint(raw_token_response)

def getTokenID(data_list):
    token_list = []
    for dictionary in data_list:
        token_list.append(int(dictionary['id']['tokenId'], 16))
    return token_list

# tokens = getTokenID(json_file)

def NFTMedata(base_url, contractAddr, token_list):
    token_metadata = []
    for token in token_list:
        request_url = base_url + "/getNFTMetadata?contractAddress=" + contractAddr + "&tokenId=" + str(token)
        metadata = requests.get(request_url)
        data = metadata.json()
        token_metadata.append(data)
    return token_metadata
# pprint.pprint(NFTMedata(base_url, bored_ape, tokens))


def getOwnersfor_collection(contractAddr):  # returns a list 
    request_url = base_url + "/getOwnersForCollection/?contractAddress=" + contractAddr
    api_data = requests.get(request_url)
    data = api_data.json()
    return data['ownerAddresses']
# wallets = getOwnersfor_collection(bored_ape)


def wallet_info(wallets):
    list_ = []
    for i in range(1, 10):
        request_url = base_url + "/getNFTs/?owner=" + wallets[i] + "&withMetadata=false" 
        api_data = requests.get(request_url)
        data = api_data.json()
        data.pop('blockHash')
        data.update({'walletAddress': wallets[i]})
        list_.append(data)
    return list_

 #pprint.pprint("wallet_info ", wallet_info(wallets))
# temp_dict.update({'collection_address': obj['contract']['address']})
# temp_dict.update({'tokenID': int(obj['id']['tokenId'], 16)})
# temp_dict.update({'wallet_address': dictionary['walletAddress']}) 

def NFT_owned_by_wallet(list_):
    cleaned_list = []
    for dictionary in list_:
        temp_dict = dict()
        temp_dict.update({'wallet_address': dictionary['walletAddress']})
        sub_list = dictionary['ownedNfts']
        temp_list = []
        for small_dict in sub_list:
            temp_list.append({'collection_addr':small_dict['contract']['address'], 'tokenID': int(small_dict['id']['tokenId'], 16)})
        temp_dict.update({'assets': temp_list})
        cleaned_list.append(temp_dict)

    return cleaned_list
 #pprint.pprint("NFT_owned_by_wallet ", NFT_owned_by_wallet(wallet_info(wallets)))


def traits(url, contractAddr, tokenMetadata):
    traits_and_values = []
    for dictionary in tokenMetadata:
        var_metadata = dictionary['metadata']
        list_of_attribute = var_metadata['attributes'] # list of dictionaries
        temp_dict = {}
        temp_dict.update({'collection_addr': dictionary['contract']['address']})
        for trait_obj in list_of_attribute:
            temp_dict.update({'trait_type': trait_obj['trait_type']})
            temp_dict.update({'trait_value': trait_obj['value']})
        traits_and_values.append(temp_dict)
    return traits_and_values

# raw_token_response = scale_nft_collection(base_url, bored_ape)

# pprint.pprint(get_tokenData(raw_token_response, ))

