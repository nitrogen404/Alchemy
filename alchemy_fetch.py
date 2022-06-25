import os
import json
import requests
from dotenv import load_dotenv
import pprint
load_dotenv()

base_url = "https://eth-mainnet.g.alchemy.com/nft/v2/" + os.environ.get("ALCHEMY_API_KEY")
bored_ape = "0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d"
azuki = "0xED5AF388653567Af2F388E6224dC7C4b3241C544"


def nftCollections(url, address):
    request_url = url + "/getContractMetadata/?contractAddress=" + address
    collection_data = requests.get(request_url)
    return [collection_data.json()]


def nfts_for_collection(base_url, contractAddr):  # returns a list of dictionaries
    request_url = base_url + "/getNFTsForCollection/?contractAddress=" + contractAddr + "&start=0&withMetadata=true"
    nfts_data = requests.get(request_url)
    data = nfts_data.json()
    data.pop("nextToken")
    return data['nfts']


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


def getOwnersfor_collection(contractAddr):  # returns a list 
    request_url = base_url + "/getOwnersForCollection/?contractAddress=" + contractAddr
    api_data = requests.get(request_url)
    data = api_data.json()
    return data['ownerAddresses']


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


# collection metadata
contractMedata = nftCollections(base_url, bored_ape)

# tokens in a collection
tokens = get_tokenData(nfts_for_collection(base_url, bored_ape))

# NFTs owned by wallets
wallets = getOwnersfor_collection(bored_ape)
nfts_in_wallet = NFT_owned_by_wallet(wallet_info(wallets))