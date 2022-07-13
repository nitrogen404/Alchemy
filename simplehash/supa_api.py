import os
from supabase import create_client, Client
from simple_hash import owners

def insert_row(supabase, json_data, table_name):
    for key in json_data:
        temp_dict = {}
        temp_dict.update({'owner': key, 'tokens': json_data[key]})
        supabase.table(table_name).insert(temp_dict).execute()


def main():
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    insert_row(supabase, owners, "sh_owners")
    

main()
