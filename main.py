import os

import database
import scraper

if __name__ == "__main__":
    database.database_setup()

    if not os.path.exists("c2songs.sqlite"):
        table = get_table_from_soup()
        parse_table_into_songs(table)        