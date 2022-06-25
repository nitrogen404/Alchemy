import os
import json
import requests
from dotenv import load_dotenv
import pprint
import time
load_dotenv()


base_url = "https://eth-mainnet.g.alchemy.com/nft/v2/" + os.environ.get("ALCHEMY_API_KEY")
bored_ape = "0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d"  # bored ape contains some empty fields

def nfts_for_collection(base_url, contractAddr):  # returns a list of dictionaries
    request_url = base_url + "/getNFTsForCollection/?contractAddress=" + contractAddr + "&start=0&withMetadata=true&limit=10"
    nfts_data = requests.get(request_url)
    data = nfts_data.json()
    data.pop("nextToken")
    return data['nfts']

# json_file = nfts_for_collection(base_url, bored_ape)
# pprint.pprint(json_file)

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

wallets = getOwnersfor_collection(bored_ape)

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

# pprint.pprint(wallet_info(wallets))
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

pprint.pprint(NFT_owned_by_wallet(wallet_info(wallets)))

def get_tokenData(data_list):
    token_list = []
    for dictionary in data_list:
        temp_dict = dict()
        temp_dict.update({'tokenID': int(dictionary['id']['tokenId'], 16)})
        temp_dict.update({'tokenType': dictionary['id']['tokenMetadata']['tokenType']})
        temp_dict.update({'title': dictionary['title']})
        temp_dict.update({'description': dictionary['description']})
        temp_dict.update({'timestamp': dictionary['timeLastUpdated']})
        metadata_dict = dictionary['metadata']
        temp_dict.update({'metadata': metadata_dict['attributes']})
        mediaDict = dictionary['media'][0]
        temp_dict.update({'imageURL': mediaDict['gateway']})
        token_list.append(temp_dict)

    return token_list


# pprint.pprint(get_tokenData(nfts_for_collection(base_url, bored_ape)))


