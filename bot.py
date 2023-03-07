import discord
from discord.ext import commands
import re

import utils
from search import scraper
from search import search

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
    num_songs_added, songs_added_blurb = scraper.update_database()

    if num_songs_added >= 1:
        await ctx.send(embed = utils.generate_embed(
            status = "Success",
            msg = (
                f"{num_songs_added} songs added:\n"
                f"{songs_added_blurb}"
            )
        ))
    else:
        await ctx.send(embed = utils.generate_embed(
            status = "Neutral",
            msg = ("No new songs added.")
        ))

@bot.command()
async def alias(ctx, arg1, arg2s):
    pass 

@alias.error
async def alias_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):    
        await ctx.send(embed = utils.generate_embed(
                status = 'Error',
                msg = "Please specify both a valid song_id and alias."
            ))

#################################################