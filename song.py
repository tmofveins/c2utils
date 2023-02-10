from bs4 import BeautifulSoup
from pony.orm import * 

import pykakasi

import utils
from chart import Chart
from database import *

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
            return ""

        td = next(iterator)
        artist = td.text

        td = next(iterator)
        bpm = td.text

        td = next(iterator)
        _, (easy_name, easy_diff, easy_link) = Chart.create_chart_from_td(td, "EASY")

        td = next(iterator)
        _, (hard_name, hard_diff, hard_link) = Chart.create_chart_from_td(td, "HARD")

        # song_id is only guaranteed obtainable from the chaos chart
        td = next(iterator)
        song_id, (chaos_name, chaos_diff, chaos_link) = Chart.create_chart_from_td(td, "CHAOS")

        td = next(iterator)
        _, (glitch_name, glitch_diff, glitch_link) = Chart.create_chart_from_td(td, "GLITCH")

        td = next(iterator)
        _, (sp_name, sp_diff, sp_link) = Chart.create_chart_from_td(td, "SPECIAL")

        add_song_to_db(song_id, curr_character, title, artist, bpm)
        add_chart_to_db(song_id, easy_name, easy_diff, easy_link)
        add_chart_to_db(song_id, hard_name, hard_diff, hard_link)
        add_chart_to_db(song_id, chaos_name, chaos_diff, chaos_link)

        if glitch_diff is not None:
            add_chart_to_db(song_id, glitch_name, glitch_diff, glitch_link)

        if sp_diff is not None:
            add_chart_to_db(song_id, sp_name, sp_diff, sp_link)

        #song = cls(song_id, curr_character, title, "", artist, bpm, charts)

        return curr_character


@db_session
def add_song_to_db(song_id, character, title, artist, bpm):
    print(
            f"ID: {song_id}\nCharacter: {character}\n"
            f"Song: {title}\n"
            f"Artist: {artist}\nBPM: {bpm}\n"
        )

    Song(song_id = song_id, character = character, title = title, artist = artist, bpm = bpm)

    print("success!\n")

@db_session
def add_chart_to_db(song_id, diff_name, diff_level, diff_link):
    print(f'{diff_name} {diff_level} => {diff_link}\n')
    Chart(song = Song[song_id], diff_name = diff_name, diff_level = diff_level, diff_link = diff_link)
    print("success!\n")