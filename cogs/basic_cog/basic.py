import discord
from discord.ext import commands

class BasicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot # gives the cog a bot instance so we can do bot stuff LOL! ex:    self.bot.name returns bot name
    
    @commands.slash_command()
    async def test(self, ctx, bollocks):
        await ctx.respond('test')
        await ctx.send(bollocks)
    
