import os
import json
import requests
from dotenv import load_dotenv
import pprint
load_dotenv()

base_url = "https://eth-mainnet.g.alchemy.com/nft/v2/" + os.environ.get("ALCHEMY_API_KEY")
bored_ape = "0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d"
azuki = "0xED5AF388653567Af2F388E6224dC7C4b3241C544"


# fetching the contract Metadata
def nftCollections(url, address):  
    request_url = url + "/getContractMetadata/?contractAddress=" + address
    collection_data = requests.get(request_url)
    api_response_dict = collection_data.json()
    contractMetadata = dict()
    
    for key in api_response_dict:
        if type(api_response_dict[key]) == type(dict()):
            for subkey in api_response_dict[key]:
                contractMetadata.update({subkey: api_response_dict[key][subkey]})
        else:
            contractMetadata.update({key: api_response_dict[key]})    
    
    return [contractMetadata]


# # fetching tokens for a collection (not scaled)
def nfts_for_collection(base_url, contractAddr, startToken):  # returns a list of dictionaries
    request_url = f'{base_url}/getNFTsForCollection/?contractAddress={contractAddr}&withMetadata=true&startToken={startToken}'
    nfts_data = requests.get(request_url)
    return nfts_data.json()


# fetching all tokens from a collection
def scale_nft_collection(url, contractAddr):
    token_collection = []
    total_supply_request = requests.get(url + "/getContractMetadata/?contractAddress=" + contractAddr) 
    total_supply = total_supply_request.json()['contractMetadata']['totalSupply']
    start_token = 0
    while start_token < int(total_supply):
        api_requests = nfts_for_collection(url, contractAddr, start_token)
        nfts = api_requests['nfts']
        token_collection = token_collection + nfts
        start_token += 100
        
    return token_collection 

# fetching owners for each token in a collection
def getOwners_fortoken(url, contractAddr, raw_token_response):
    owners_dict = []
    more_tokens = raw_token_response
    for dictionary in more_tokens:
        token_number = dictionary['id']['tokenId']
        print(int(token_number, 16))
        try:
            request_url = requests.get(f'{url}/getOwnersForToken?contractAddress={contractAddr}&tokenId={token_number}')
            api_response = request_url.json()
            owners_dict.append({'tokenNumber': int(token_number, 16), 'wallet_addr': api_response['owners'][0]})
        except:
            owners_dict.append({'tokenNumber': int(token_number, 16), 'wallet_addr': " "})
    
    return owners_dict


# structuring the raw data from scaling tokens funciton 
def get_tokenData(raw_token_response, owners_data):
    token_list = []
    for i in range(len(raw_token_response)):
        
        temp_dict = dict()
        dictionary = raw_token_response[i]
        temp_dict.update({'collection_addr': dictionary['contract']['address']})
        temp_dict.update({'tokenID': int(dictionary['id']['tokenId'], 16)})
        temp_dict.update({'owner_addr': owners_data[i]['wallet_addr']})
        temp_dict.update({'tokenType': dictionary['id']['tokenMetadata']['tokenType']})
        temp_dict.update({'title': dictionary['title']})
        temp_dict.update({'description': dictionary['description']})
        temp_dict.update({'timestamp': dictionary['timeLastUpdated']})
        metadata_dict = dictionary['metadata']
        
        temp_dict.update({'traits': metadata_dict['attributes']})
        mediaDict = dictionary['media'][0]
        temp_dict.update({'imageURL': mediaDict['gateway']})
        token_list.append(temp_dict)
    return token_list


# fetching owners of a collection (not tokens in that collection)
def getOwnersfor_collection(contractAddr):  # returns a list 
    request_url = base_url + "/getOwnersForCollection/?contractAddress=" + contractAddr
    api_data = requests.get(request_url)
    data = api_data.json()
    return data['ownerAddresses']


# fetching all nfts owned by a wallet 
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


# structuring the wallets_info data
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
    cleaned_list.pop(4)  # insanely large number removed 
    return cleaned_list


# traits and their values (collection_trait table)
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


# data for NFT_collection table
# contractMedata = nftCollections(base_url, bored_ape)
# pprint.pprint(contractMedata)

# data for collection_items table 
raw_token_response = scale_nft_collection(base_url, bored_ape)
# ownerof_token = getOwners_fortoken(base_url, bored_ape, raw_token_response)
# structured_token_data = get_tokenData(raw_token_response, ownerof_token)


traits_and_values = traits(base_url, bored_ape, raw_token_response)
pprint.pprint(traits_and_values)
# 1 eye
# 4 fur


