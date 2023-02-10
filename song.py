from bs4 import BeautifulSoup
from pony.orm import * 

from database import db
#from chart import Chart

class Song(db.Entity):
    song_id = PrimaryKey(str)
    character = Required(str)
    title = Required(str)
    trans_title = Optional(str)
    artist = Required(str)
    bpm = Required(str)
    charts = Set("Chart")

@db_session
def add_song_to_db(song_id, character, title, artist, bpm):
    print(
            f"ID: {song_id}\nCharacter: {character}\n"
            f"Song: {title}\n"
            f"Artist: {artist}\nBPM: {bpm}\n"
        )

    Song(song_id = song_id, character = character, title = title, artist = artist, bpm = bpm)

    print("success!\n")