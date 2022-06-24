import os
import json
import requests
from dotenv import load_dotenv
from supabase import create_client, Client
import os
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


def insertData(supabase, jsonList, table_name):
    data = supabase.table(str(table_name)).insert(jsonList).execute()


def displayRows(supabase, table):
    pprint.pprint(supabase.table(str(table)).select("*").execute())
    


def deleteRow(supabase): # remove the address!!!!!!
    data = supabase.table("NFT_collections").delete().eq("address", "0xED5AF388653567Af2F388E6224dC7C4b3241C544").execute()


def main():
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)

    # collection_data = nftCollections(base_url, azuki)
    tokens_inCollection = get_tokenData(nfts_for_collection(base_url, bored_ape))
    
    # insertData(supabase, collection_data)
    insertData(supabase, tokens_inCollection, "collection_items")
    # deleteRow(supabase)
    displayRows(supabase, "NFT_collections")
    print("\n")
    displayRows(supabase, "collection_items")
    
main()
