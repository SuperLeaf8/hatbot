import discord
from discord.ext import commands
import json

# import cogs from the cogs module because i love organization
from cogs import basic_cog

# initial bot stuff
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="d/",intents=intents)

# barebone events
@bot.event
async def on_ready():
    print(f"online in {[x.name for x in bot.guilds]}")

    # cogs
    cogs = [basic_cog.cog]
    for cog in cogs:
        bot.add_cog(cog(bot))

@bot.slash_command()
async def ping(ctx):
    await ctx.respond("hello")

with open("token.json","r") as token_file:
    token = json.load(token_file)
bot.run(token)