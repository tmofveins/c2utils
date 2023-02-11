import discord
from discord.ext import commands

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

@bot.command
async def c2s(ctx, arg):
    pass

@c2s.error
async def c2s_error(ctx, error):
    pass

#################################################