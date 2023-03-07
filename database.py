from pony.orm import *

db = Database()

def database_setup():
    db.bind(provider = "sqlite", filename = "c2songs.sqlite", create_db = True)
    db.generate_mapping(create_tables = True)