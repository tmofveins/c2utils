from bs4 import BeautifulSoup
from pony.orm import * 

from database import db

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
    if Song.get(song_id = song_id) is None:
        Song(song_id = song_id, character = character, title = title, artist = artist, bpm = bpm)