import os
import json
import pprint
import requests
from dotenv import load_dotenv
from supabase import create_client, Client
from alchemy_fetch import contractMedata, tokens, nfts_in_wallet, base_url, bored_ape

load_dotenv()

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
    # tokens_inCollection = get_tokenData(nfts_for_collection(base_url, bored_ape))
    
    # insertData(supabase, contractMedata, "NFT_collections")
    # insertData(supabase, tokens, "collection_items")
    insertData(supabase, nfts_in_wallet, "Owners")

    print("\n")
    # displayRows(supabase, "NFT_collections")
    # displayRows(supabase, "collection_items")
    displayRows(supabase, "Owners")
    
main()