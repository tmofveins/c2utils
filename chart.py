from bs4 import BeautifulSoup
from pony.orm import * 

from database import db
from song import Song

class Chart(db.Entity):
    song = Required("Song")
    diff_name = Required(str)
    diff_level = Required(str)
    diff_link = Optional(str)

@db_session
def add_chart_to_db(song_id, diff_name, diff_level, diff_link):
    print(f'{diff_name} {diff_level} => {diff_link}\n')
    Chart(song = Song[song_id], diff_name = diff_name, diff_level = diff_level, diff_link = diff_link)
    print("success!\n")