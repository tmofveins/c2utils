from chart import Chart

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
    def create_song_from_tr(tr):
        pass
