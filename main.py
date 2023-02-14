import os

from bot import bot
import database
import search.scraper as scraper
import secret

if __name__ == "__main__":
    database.database_setup()

    if not os.path.exists("c2songs.sqlite"):
        table = scraper.get_table_from_soup()
        scraper.parse_table_into_songs(table)        

    #bot.run(secret.TOKEN)
    matches = scraper.search_song("body")
    scraper.show_search_results_embed(matches)