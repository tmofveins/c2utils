import os

from bot import bot
import database
import scraper
import secret

if __name__ == "__main__":
    database.database_setup()
    bot.run(secret.TOKEN)

    if not os.path.exists("c2songs.sqlite"):
        table = scraper.get_table_from_soup()
        scraper.parse_table_into_songs(table)        