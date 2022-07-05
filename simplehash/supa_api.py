import os
from supabase import create_client, Client
from simple_hash import collection_field

def insert_row(supabase, json_data, table_name):
    supabase.table(table_name).insert(json_data).execute()


def main():
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    insert_row(supabase, collection_field, "sh_collections")

main()