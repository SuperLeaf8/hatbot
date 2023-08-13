import discord
from discord.ext import commands

class ModCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # commands here