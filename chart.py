from bs4 import BeautifulSoup
from pony.orm import * 

from database import db
#from song import Song

class Chart(db.Entity):
    song = Required("Song")
    diff_name = Required(str)
    diff_level = Required(str)
    diff_link = Optional(str)

    """def __init__(self, diff_name: str, diff_level: str, diff_link: str):
        self.diff_name = diff_name
        self.diff_level = diff_level
        self.diff_link = diff_link"""

    @classmethod
    def create_chart_from_td(cls, td, diff_name):
        chart_lv = td.text

        # no level, no chart
        if chart_lv == "":
            return "", (None, None, None)

        chart_link = ""
        if td.find('a'):
            chart_link = td.a.get('href')

        song_id = ""

        # chaos chart is always present, hence song_id only obtainable from here
        if diff_name == "CHAOS":
            song_id = chart_link.split("/")[-2]
        # crash/drop/dream is stored in the same table space, so we use url to determine which it is
        elif diff_name == "SPECIAL":
            diff_name = chart_link.split("/")[-1]

        return song_id, (diff_name, chart_lv, chart_link)
        #return cls(diff_name, chart_lv, chart_link), song_id