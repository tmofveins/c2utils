from bs4 import BeautifulSoup
from pony.orm import * 

import pykakasi

import utils
from chart import Chart
from database import db

class Song(db.Entity):
    song_id = PrimaryKey(str)
    character = Required(str)
    title = Required(str)
    trans_title = Optional(str)
    artist = Required(str)
    bpm = Required(str)
    charts = Set("Chart")

    """def __init__(self, song_id: str, character: str, title: str, trans_title: str,
                artist: str, bpm: str, charts: [Chart]):
        self.song_id = song_id
        self.character = character
        self.title = title
        self.trans_title = trans_title
        self.artist = artist
        self.bpm = bpm
        self.charts = charts"""

    def __repr__(self):
        return (
                f"ID: {self.song_id}\nCharacter: {self.character}\n"
                f"Song: {self.title}\nTranslated title: {self.trans_title}\n"
                f"Artist: {self.artist}\nBPM: {self.bpm}\n"
                f"Charts: {[chart for chart in self.charts]}"
                )

    @classmethod
    def create_song_from_tr(cls, tr, curr_character):
        kks = pykakasi.kakasi()

        iterator = iter(tr.find_all("td"))
        td = next(iterator)

        if td.has_attr("rowspan"):
            curr_character = td.text 

            # another iteration to also get the song title
            td = next(iterator)
            title = td.text
        else:
            title = td.text

        # no title, no song
        if title == "":
            return None, ""

        td = next(iterator)
        artist = td.text

        td = next(iterator)
        bpm = td.text

        charts = []

        td = next(iterator)
        Chart.create_chart_from_td(td, "EASY")

        td = next(iterator)
        Chart.create_chart_from_td(td, "HARD")

        # song_id is only guaranteed obtainable from the chaos chart
        td = next(iterator)
        Chart.create_chart_from_td(td, "CHAOS")

        td = next(iterator)
        Chart.create_chart_from_td(td, "GLITCH")

        td = next(iterator)
        Chart.create_chart_from_td(td, "SPECIAL")

        #song = cls(song_id, curr_character, title, "", artist, bpm, charts)

        #return song, curr_character
