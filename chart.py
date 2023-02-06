from bs4 import BeautifulSoup

class Chart:

    def __init__(self, diff_name: str, diff_level: str, diff_link: str):
        self.diff_name = diff_name
        self.diff_level = diff_level
        self.diff_link = diff_link

    def __repr__(self):
        return f'{self.diff_name} {self.diff_level} => {getattr(self, "diff_link", "N/A")}'

    @classmethod
    def create_chart_from_td(cls, td, diff_name):
        chart_lv = td.text

        # no level, no chart
        if chart_lv == "":
            return None, ""

        chart_link = ""
        if td.find('a'):
            chart_link = td.a.get('href')

        song_id = ""

        # chaos chart is always present, hence song_id only obtainable from here
        if diff_name == "CHAOS":
            song_id = chart_link.split("/")[-2]
        # crash/drop/dream is stored in the same space, so we use url to determine which it is
        elif diff_name == "SPECIAL":
            diff_name = chart_link.split("/")[-1]

        return cls(diff_name, chart_lv, chart_link), song_id