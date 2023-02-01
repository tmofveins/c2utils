class Song:

    def __init__(self, id: str, character: str, title: str, artist: str,
                 bpm: int, charts: [Chart]):
        self.id = id
        self.character = character
        self.title = title
        self.artist = artist
        self.bpm = bpm
        self.charts = charts

    def __repr__(self):
        return f"""
                ID: {self.id}\n Character: {self.character}\n 
                Song: {self.title}\n Artist: {self.artist}\n BPM: {self.bpm}\n
                Charts: {[chart for chart in self.charts]} 
                """

    @classmethod
    def create_song_from_tr(tr):
        pass

    class Chart:

        def __init__(self, diff_name, diff_level, diff_link):
            self.diff_name = diff_name
            self.diff_level = diff_level
            self.diff_link = diff_link

        def __repr__(self):
            return f"""
                    {self.diff_name} {self.diff_level} => {getattr(self, "diff_link", "N/A")}
                    """

        @classmethod
        def create_chart_from_tr(tr):
            pass
