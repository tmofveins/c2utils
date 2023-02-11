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
    print(
            f"ID: {song_id}\nCharacter: {character}\n"
            f"Song: {title}\n"
            f"Artist: {artist}\nBPM: {bpm}\n"
        )
    Song(song_id = song_id, character = character, title = title, artist = artist, bpm = bpm)

@db_session
def print_songs():
    for s in select(s for s in Song):
        print(
                f"ID: {s.song_id}\nCharacter: {s.character}\n"
                f"Song: {s.title}\n"
                f"Artist: {s.artist}\nBPM: {s.bpm}\n"
            )