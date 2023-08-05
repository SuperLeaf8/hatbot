import discord
from discord.ext import commands

class BasicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot # gives the cog a bot instance so we can do bot stuff LOL! ex:    self.bot.name returns bot name
    
    @commands.command()
    async def hello(self, ctx):
        await ctx.channel.send("hello")
        
