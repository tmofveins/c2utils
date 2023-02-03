class Chart:

        def __init__(self, diff_name: str, diff_level: str, diff_link: str):
            self.diff_name = diff_name
            self.diff_level = diff_level
            self.diff_link = diff_link

        def __repr__(self):
            return f'{self.diff_name} {self.diff_level} => {getattr(self, "diff_link", "N/A")}'

        @classmethod
        def create_chart_from_tr(tr):
            pass