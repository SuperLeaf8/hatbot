import discord
from discord.ext import commands
import random
import asyncio
import json

class GamesCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# capital guesser #######################################################################################################################################################
@commands.command()
async def capitalguess(self, ctx):
    with open("capitals.json","r") as capitals_file: # json file containing dictionary of all countries and their capital(s)
        countries_capitals = json.load(capitals_file)
    country, capital = random.choice(list(countries_capitals.items()))
    # Send an embed message
    embed = discord.Embed(title="Guess the Capital", description=f"What is the capital of {country}?", color=discord.Color.magenta())
    await ctx.send(embed=embed)
    # Function to check if the user's response is correct
    def check(m):
        return m.author == ctx.author and m.content.lower() == capital.lower()
    try:
        user_response = await self.bot.wait_for('message', check=check, timeout=20)
    except asyncio.TimeoutError:
        await ctx.send(f"Time's up! The correct answer was {capital}.")
    else:
        await ctx.send(f"Correct! {capital} is the capital of {country}.")
#########################################################################################################################################################################

# flag guesser ##########################################################################################################################################################
@commands.command()
async def countryguess(self, ctx):
    with open("flags.json", "r") as flags_file: # json file containing dictionary of all countries and their flag image URLs
        countries_flags = json.load(flags_file)
    country, flag_url = random.choice(list(countries_flags.items()))
    
    # Send an embed message
    embed = discord.Embed(title="Guess the Country", description=f"What country does this flag belong to?", color=discord.Color.magenta())
    embed.set_image(url=flag_url)
    await ctx.send(embed=embed)
    
    # Function to check if the user's response is correct
    def check(m):
        return m.author == ctx.author and m.content.lower() == country.lower()
    
    try:
        user_response = await self.bot.wait_for('message', check=check, timeout=60)
    except asyncio.TimeoutError:
        await ctx.send(f"Sixty second timer's up! The correct answer was {country}.")
    else:
        await ctx.send(f"Correct! The flag belongs to {country}.")