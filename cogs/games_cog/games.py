import discord
from discord.ext import commands
import random
import asyncio
import json
import os
import requests

class GamesCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # capital guesser ##########################################################################
    @commands.command()
    async def capitalguess(self, ctx):
        with open("./cogs/games_cog/capitals.json","r") as capitals_file: # json file containing dictionary of all countries and their capital(s)
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
    ############################################################################################

    # flag guesser #############################################################################
    @commands.command()
    @commands.cooldown(rate=1,per=65,type=commands.BucketType.channel)
    async def flagguess(self, ctx):
        with open("./cogs/games_cog/flags.json", "r", encoding="utf-8") as json_file:
            data = json.load(json_file)


        # URL template for flag images
        flag_url_template = "https://flagcdn.com/256x192/{0}.png"
        
        # Check if the url is valid, for the website has the flag
        ## if not, just reroll the index

        valid_url = False
        while not valid_url:
            rand_index = random.randint(0,len(data)-1) # get random index of countries
            country_code = data[rand_index]["code2l"] # get the country code (2 letters)
            flag_url = flag_url_template.format(country_code.lower()) # actual url of the flag
            if not requests.get(flag_url).status_code == 404:
                valid_url = True

        # print("Country Code:", country_code)
        # print("Flag URL:", flag_url)

        # Send an embed message
        embed = discord.Embed(title="Guess the Country", description=f"What country does this flag belong to?", color=discord.Color.magenta())
        embed.set_image(url=flag_url)
        await ctx.send(embed=embed)

        # Function to check if the user's response is correct
        def check(m):
            return m.content.lower() in (data[rand_index]['name'].lower()).split(" ") # and m.author == ctx.author

        try:
            user_response = await self.bot.wait_for('message', check=check, timeout=60)
            await ctx.send(f"Correct! The flag belongs to {data[rand_index]['name']}.")
            self.flagguess.reset_cooldown(ctx)
        except asyncio.TimeoutError:
            await ctx.send(f"60 second timer's up! The correct answer was {data[rand_index]['name']}.")
        
    @commands.command()
    async def unscramble(self, ctx):
        # Open the "words.json" JSON file and load the words
        with open("./cogs/games_cog/words.json", "r") as json_file:
            words = json.load(json_file)
        
        # Choose a random word from the loaded list of words
        chosen_word = random.choice(words)
        # Scramble the letters of the chosen word
        scrambled_word = ''.join(random.sample(chosen_word, len(chosen_word)))

        # Create an embed to send to the user
        embed = discord.Embed(
            title="Unscramble the Word!",
            description=f"Unscramble the letters to form a word: **{scrambled_word}**",
            color=discord.Color.blue()
        )
        # Send the embed to the user
        await ctx.send(embed=embed)

        # Define a function to check if the user's response matches the chosen word
        def check(message):
            return message.author == ctx.author and message.content.lower() == chosen_word

        try:
            # Wait for the user's response using the defined check function, with a timeout of 30 seconds
            response_message = await self.bot.wait_for("message", check=check, timeout=30)
            # Send a congratulatory message if the user's response is correct
            await ctx.send(f"Congratulations! {response_message.author.mention} unscrambled the word!")
        except asyncio.TimeoutError:
            # If the user doesn't respond within the timeout, send the correct word
            await ctx.send("Time's up! The correct word was: **" + chosen_word + "**")