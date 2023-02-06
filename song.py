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

        # no title, no song
        if title == "":
            return None, ""

        td = next(iterator)
        artist = td.text

        td = next(iterator)
        bpm = td.text

        charts = []

        td = next(iterator)
        easy_chart, _ = Chart.create_chart_from_td(td, "EASY")
        charts.append(easy_chart)

        td = next(iterator)
        hard_chart, _ = Chart.create_chart_from_td(td, "HARD")
        charts.append(hard_chart)

        # song_id is only guaranteed obtainable from the chaos chart
        td = next(iterator)
        chaos_chart, song_id = Chart.create_chart_from_td(td, "CHAOS")
        charts.append(chaos_chart)

        td = next(iterator)
        glitch_chart, _ = Chart.create_chart_from_td(td, "GLITCH")
        if glitch_chart is not None:
            charts.append(glitch_chart)

        td = next(iterator)
        sp_chart, _ = Chart.create_chart_from_td(td, "SPECIAL")
        if sp_chart is not None:
            charts.append(sp_chart)

        song = cls(song_id, curr_character, title, artist, bpm, charts)

        return song, curr_character
