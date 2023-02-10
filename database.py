from pony.orm import *

db = Database()

def database_setup():
    db.bind(provider = "sqlite", filename = "c2songs.sqlite", create_db = True)
    db.generate_mapping(create_tables = True)

@db_session
def add_song_to_db(song_id, character, title, artist, bpm):
    Song(song_id = song_id, character = character, title = title, artist = artist, bpm = bpm)

@db_session
def add_chart_to_db():
    pass