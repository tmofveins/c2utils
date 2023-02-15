import os

from bot import bot
import database
import search.scraper as scraper
import secret

if __name__ == "__main__":
    database.database_setup()

    #table = scraper.get_table_from_soup()
    #scraper.parse_table_into_songs(table)        

    #bot.run(secret.TOKEN)
    matches = scraper.search_song("001_004")
    embed = scraper.show_search_results_embed(matches)