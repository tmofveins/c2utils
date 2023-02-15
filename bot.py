import discord
from discord.ext import commands
import re

import search.scraper as scraper
import search.search as search
import utils

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = "!", intents = intents)

@bot.event
async def on_ready():
    print("Bot is ready. Logged in as:")
    print(bot.user.name)
    print(bot.user.id)
    print("------")

#################################################

@bot.command()
async def test(ctx):
    await ctx.send("hi")

@bot.command()
async def c2s(ctx, arg):
    # emote/channel/mention
    is_invalid_input = re.search(utils.INVALID_INPUT_REGEX, arg)    

    if is_invalid_input:
        await ctx.send(embed = utils.generate_embed(
                status = 'Error',
                msg = 'Invalid input. Ping, emote, or channel name detected.'
            ))
        return

    matches = search.search_song(arg)
    result = search.display_search_result_as_embed(matches)

    await ctx.send(embed = result)

@c2s.error
async def c2s_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):    
        await ctx.send(embed = utils.generate_embed(
                status = 'Error',
                msg = "Please specify a search key."
            ))

#################################################

@bot.command()
async def update(ctx):
    table = scraper.get_table_from_soup()
    scraper.parse_table_into_songs(table)

    songs_added_blurb = "\n".join(s for s in utils.SONGS_ADDED_THIS_UPDATE)

    await ctx.send(embed = utils.generate_embed(
        status = "Success",
        msg = (
            f"{len(utils.SONGS_ADDED_THIS_UPDATE)} new songs added.\n"
            f"{songs_added_blurb}"
        )
    ))

    utils.SONGS_ADDED_THIS_UPDATE = []