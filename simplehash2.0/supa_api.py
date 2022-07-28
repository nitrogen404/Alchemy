import os
from supabase import create_client, Client
# from api_parser import wallet_activity_table
from moralis import transfers_

def insert_row(supabase, json_list, table_name):
    for value in json_list:
        supabase.table(table_name).insert(value).execute()

def main():
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    insert_row(supabase, transfers_, "transfers_")
    

main()
