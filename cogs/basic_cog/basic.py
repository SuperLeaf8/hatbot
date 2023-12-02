import discord
from discord.ext import commands
import requests
import random

# Define categories
categories = {
    "Fun": ["cat", "dog", "flip"],
    "Games": ["capitalguess", "flagguess", "unscramble"],
    "Moderation": ["ban", "kick", "mute", "unmute", "purge", "deafen", "undeafen", "voicemute", "unvoicemute", "whois", "slowmode"],
    "Voice": ["join", "leave", "testplay"],
    "Music": ["play", "queue", "queuels", "clearqueue", "loop", "pause", "resume", "setvolume", "volume"],
}

# Define help messages for each command
help_messages = {
    "cat": "Displays a random cat image.",
    "dog": "Displays a random dog image.",
    "flip": "Flips a coin.",
    "capitalguess": "Initiates a capital guessing game.",
    "flagguess": "Initiates a flag guessing game.",
    "unscramble": "Initiates a word unscrambling game.",
    "ban": "Bans a user.",
    "kick": "Kicks a user.",
    "mute": "Chat mutes a user.",
    "unmute": "Removes chat mute from a user.",
    "purge": "Purges a set number of messages.",
    "deafen": "Deafens a user's voice.",
    "undeafen": "Undeafens a user's voice.",
    "voicemute": "Voice mutes a user.",
    "unvoicemute": "Unvoice mutes a user.",
    "whois": "Displays various information regarding a profile.",
    "slowmode": "Enables slowmode for a designated channel.",
    "join": "Summons the bot to a voice channel.",
    "leave": "Removes the bot from the current voice channel.",
    "testplay": "Summons bot to voice channel and plays a test tune.",
    "play": "Plays a specified song.",
    "queue": "Displays the song queue.",
    "queuels": "Displays the queue list.",
    "clearqueue": "Clears the queue.",
    "loop": "Loops the current song.",
    "pause": "Pauses the current song.",
    "resume": "Resumes the current song.",
    "setvolume": "Sets the volume to a certain amount.",
    "volume": "Displays the current volume."
}

# Define arguments for each command
help_arguments = {
    "cat": "No Arguments",
    "dog": "No Arguments",
    "flip": "No Arguments",
    "capitalguess": "No Arguments",
    "flagguess": "No Arguments",
    "unscramble": "No Arguments",
    "ban": "Required: Member\nOptional: Duration (integer), Reason (string)",
    "kick": "Required: Member\nOptional: Reason (string)",
    "mute": "Required: Member\nOptional: Duration (integer), Reason (string)",
    "unmute": "Required: Member",
    "purge": "Required: Amount (integer)",
    "deafen": "Required: Member",
    "undeafen": "Required: Member",
    "voicemute": "Required: Member",
    "unvoicemute": "Required: Member",
    "whois": "Required: Member",
    "slowmode": "Required: Channel, Interval (integer)",
    "join": "No Arguments",
    "leave": "No Arguments",
    "testplay": "No Arguments",
    "play": "Required: Song (string, link)",
    "queue": "Required: Song (string, link)",
    "queuels": "No Arguments",
    "clearqueue": "No Arguments",
    "loop": "No Arguments",
    "pause": "No Arguments",
    "resume": "No Arguments",
    "setvolume": "Required: Volume (integer)",
    "volume": "No Arguments",
}


class BasicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot # gives the cog a bot instance so we can do bot stuff LOL! ex:    self.bot.name returns bot name
    
    @commands.slash_command()
    async def test(self, ctx: discord.ApplicationContext, bollocks):
        await ctx.respond('test')
        await ctx.send(bollocks)
    
    @commands.command()
    async def get_avatar(self, ctx, user: discord.User):
        avatar_url = user.avatar_url

        embed = discord.Embed(title=f"Avatar of {user.display_name}", color=user.color)
        embed.set_image(url=avatar_url)

        await ctx.send(embed=embed)
    
    @commands.command()
    async def cat(self, ctx):
        response = requests.get("https://api.thecatapi.com/v1/images/search")
        data = response.json()

        if data:
            cat_image_url = data[0]["url"]

            embed = discord.Embed(title="Random Cat Image", color=discord.Color.random())
            embed.set_image(url=cat_image_url)

            await ctx.send(embed=embed)
        else:
            await ctx.send("Failed to fetch cat image.")
    
    @commands.command()
    async def dog(self, ctx):
        response = requests.get("https://random.dog/woof.json")
        data = response.json()

        if data and "url" in data:
            dog_image_url = data["url"]

            embed = discord.Embed(title="Random Dog Image", color=discord.Color.random())
            embed.set_image(url=dog_image_url)

            await ctx.send(embed=embed)
        else:
            await ctx.send("Failed to fetch dog image.")
    
    @commands.command()
    async def flip(self, ctx):
        result = random.choice(["Heads", "Tails"])
        await ctx.send(f"The coin landed on: {result}")
    

    #test you can delete when finished
    class MyView(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
        @discord.ui.button(label="Click me!", style=discord.ButtonStyle.primary, emoji="😎") # Create a button with the label "😎 Click me!" with color Blurple
        async def button_callback(self, button, interaction):
            await interaction.response.send_message("You clicked the button!") # Send a message when the button is clicked
    
    @commands.command()
    async def button(self, ctx):
        await ctx.send("hello",view=self.MyView())
    
    @commands.command()
    async def help(self, ctx, command=None):
        if command is None:
            # If no specific command is provided, display help for all categories
            embed = discord.Embed(title="Bot Commands", color=discord.Color.blue())
            for category, commands_list in categories.items():
                embed.add_field(name=category, value=", ".join(commands_list), inline=False)
            await ctx.send(embed=embed)
        else:
            # If a specific command is provided, display help for that command
            if command in help_messages:
                # Include the command's help message
                embed = discord.Embed(title=f"Help for {command}", description=help_messages[command], color=discord.Color.green())

                # Include the command's argument requirements, if available
                if command in help_arguments:
                    embed.add_field(name="Argument Requirements", value=help_arguments[command], inline=False)

                await ctx.send(embed=embed)
            else:
                await ctx.send("Command not found.")
