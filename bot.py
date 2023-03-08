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
async def c2s(ctx, search_key):
    # emote/channel/mention
    is_invalid_input = re.search(utils.INVALID_INPUT_REGEX, search_key)    

    if is_invalid_input:
        await ctx.send(embed = utils.generate_embed(
                status = 'Error',
                msg = 'Invalid input. Ping, emote, or channel name detected.'
            ))
        return

    matches = search.search_song(search_key)
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
            status = "OK",
            msg = ("No new songs added.")
        ))

#################################################

@bot.command()
async def addtl(ctx, song_id, trans_title):
    if re.search(utils.INVALID_INPUT_REGEX, song_id) or re.search(utils.INVALID_INPUT_REGEX, trans_title):
        await ctx.send(embed = utils.generate_embed(
                status = 'Error',
                msg = 'Invalid input. Ping, emote, or channel name detected.'
            ))
        return

    if scraper.add_trans_title(song_id, trans_title):
        await ctx.send(embed = utils.generate_embed(
                status = "Success",
                msg = f"Translated title {trans_title} added for song {song_id}"
            ))
    else:
        await ctx.send(embed = utils.generate_embed(
                status = "Error",
                msg = "Invalid song ID."
            ))

@addtl.error
async def addtl_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):    
        await ctx.send(embed = utils.generate_embed(
                status = 'Error',
                msg = "Please specify both a valid song_id and alias."
            ))

#################################################

@bot.command()
async def ocr(ctx, msg):
    pass

@ocr.error
async def ocr_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):    
        await ctx.send(embed = utils.generate_embed(
                status = 'Error',
                msg = "Please send a valid score screenshot."
            ))

#################################################

@bot.command()
async def bp(ctx, tp, perfect, good, bad, miss):
    pass

@bp.error
async def bp_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):    
        await ctx.send(embed = utils.generate_embed(
                status = 'Error',
                msg = (
                    "Please make sure you entered the correct values.\n"
                    "Format: `tp perfect good bad miss`\n"
                    "e.g. `100 1000 0 0 0`"
                )
            ))