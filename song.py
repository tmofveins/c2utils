from chart import Chart
from bs4 import BeautifulSoup

class Song:

    def __init__(self, id: str, character: str, title: str, artist: str,
                 bpm: str, charts: [Chart]):
        self.id = id
        self.character = character
        self.title = title
        self.artist = artist
        self.bpm = bpm
        self.charts = charts

    def __repr__(self):
        return (
                f"ID: {self.id}\nCharacter: {self.character}\n"
                f"Song: {self.title}\nArtist: {self.artist}\nBPM: {self.bpm}\n"
                f"Charts: {[chart for chart in self.charts]}"
                )

    @classmethod
    def create_song_from_tr(cls, tr, curr_character):
        iterator = iter(tr.find_all("td"))
        
        td = next(iterator)

        if td.has_attr("rowspan"):
            curr_character = td.text 
            
            # another iteration to also get the song title
            td = next(iterator)
            title = td.text

        else:
            title = td.text

        if title == "":
            return None, curr_character

        td = next(iterator)
        artist = td.text

        td = next(iterator)
        bpm = td.text

        charts = []

        td = next(iterator)
        easy_lv = td.text
        easy_link = ""
        if td.find('a'):
            easy_link = td.a.get('href')
        easy_chart = Chart("EASY", easy_lv, easy_link)
        charts.append(easy_chart)

        td = next(iterator)
        hard_lv = td.text
        hard_link = ""
        if td.find('a'):
            hard_link = td.a.get('href')
        hard_chart = Chart("HARD", hard_lv, hard_link)
        charts.append(hard_chart)

        td = next(iterator)
        chaos_lv = td.text
        chaos_link = ""
        if td.find('a'):
            chaos_link = td.a.get('href')
        chaos_chart = Chart("CHAOS", chaos_lv, chaos_link)
        charts.append(chaos_chart)

        #song_id = chaos_link.split("/")[-2]

        song = cls("", curr_character, title, artist, bpm, charts)

        return song, curr_character
        
        """
        # check for glitch chart
        td = next(iterator)
        if
        glitch_lv = td.text
        glitch_link = ""
        if td.find('a'):
            glitch_link = td.a.text
        glitch_chart = chart.Chart("GLITCH", glitch_lv, glitch_link)

        # check for special chart (i.e. crash/drop/dream)
        td = next(iterator)
        sp_lv = td.text
        sp_link = ""
        if td.find('a'):
            sp_link = td.a.text
        easy_chart = chart.Chart("EASY", easy_lv, easy_link)"""
