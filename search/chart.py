from bs4 import BeautifulSoup
from pony.orm import * 

from database import db
from .song import Song

class Chart(db.Entity):
    song = Required("Song")
    diff_id = Required(str, unique = True)
    diff_name = Required(str)
    diff_level = Required(str)
    diff_link = Optional(str)

@db_session
def add_chart_to_db(song_id, diff_name, diff_level, diff_link):
    diff_id = f"{song_id}_{diff_name}"

    if Chart.get(diff_id = diff_id) is None:
        Chart(song = Song[song_id], diff_id = diff_id,
                diff_name = diff_name.upper(), diff_level = diff_level, diff_link = diff_link)

@db_session
def retrieve_charts_for_song(song):
    _id = song.song_id

    charts = []
    for c in Chart.select(lambda c : c.song.song_id == _id):
        charts.append(c)
    
    return charts