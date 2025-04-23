import discord
from discord.ext import commands
import json
import traceback

# import cogs from the cogs module because i love organization
from cogs import basic_cog, mod_cog, games_cog, music_cog

# initial bot stuff
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="h/",intents=intents,help_command=None)

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def fart(self,ctx):
        await ctx.send("hello")

tcog = Test(bot)
print(type(tcog))

# barebone events
@bot.event
async def on_ready():
    print(f"online in {[x.name for x in bot.guilds]}")
    for cog in cogs:
        await bot.add_cog(cog(bot))
        print(type(cog))
    await bot.add_cog(tcog)

cogs = [
    basic_cog.cog,
    mod_cog.cog,
    games_cog.cog,
    music_cog.cog
]
@bot.event
async def on_command_error(ctx, error):
    form = f"```diff\n-{error}\n```"
    await ctx.send(form)
    traceback.print_exception(error)



with open("token.json","r") as token_file:
    token = json.load(token_file)
bot.run(token)