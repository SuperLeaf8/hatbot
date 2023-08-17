import discord
from discord.ext import commands
import json
import traceback

# import cogs from the cogs module because i love organization
from cogs import basic_cog, mod_cog, games_cog, music_cog

# initial bot stuff
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="d/",intents=intents)

# barebone events
@bot.event
async def on_ready():
    print(f"online in {[x.name for x in bot.guilds]}")

    # cogs
    cogs = [
        basic_cog.cog,
        mod_cog.cog,
        games_cog.cog,
        music_cog.cog
        ]
    for cog in cogs:
        bot.add_cog(cog(bot))

@bot.event
async def on_command_error(ctx, error):
    form = f"```diff\n-{error}\n```"
    await ctx.send(form)
    traceback.print_exception(error)

with open("token.json","r") as token_file:
    token = json.load(token_file)
bot.run(token)