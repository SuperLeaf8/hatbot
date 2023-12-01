import discord
from discord.ext import commands
import datetime
import asyncio
import aiohttp
from modules import async_json

import random

class ModCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.modmails = [] # if used as public bot, make this a dict with keys being server ids, and values being lists of modmailmessage objects
    
    class ModmailMessage:
        def __init__(self, modmsg, usermsg):
            self.modmsg = modmsg
            self.usermsg = usermsg

    async def modmail_dm(self, msg: discord.Message):
        channelid = 1143930181099212921 # hat nation modmail channel, you will want to use a different method if bot is used in other servers
        channel = self.bot.get_channel(channelid)
        msg = await channel.send(f"{msg.author.name} to HatBot:\n\n \"{msg.content}\"")
        return msg
    
    class ModmailModal(discord.ui.Modal):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.add_item(discord.ui.InputText(label="Message",style=discord.InputTextStyle.long))
            self.response = None

        async def callback(self, interaction: discord.Interaction):
            # respond to dm using self.modmails and modmailmessage class
            self.response = self.children[0].value
            await interaction.response.defer()
            

    @commands.message_command()
    async def reply(self,ctx,msg):
        for modmail in self.modmails:
            if modmail.modmsg == msg:
                modal = self.ModmailModal(title="Modal via Slash Command")
                channel = self.bot.get_channel(1143930181099212921)
                await ctx.send_modal(modal)
                await modal.wait()
                await channel.send(f"HatBot (mod: {ctx.author.name}) to {modmail.usermsg.author.name}:\n\n \"{modal.response}\"")
                await modmail.usermsg.channel.send(modal.response)

    @commands.Cog.listener()
    async def on_message(self,msg):
        # mod mail
        if (not msg.guild) and (msg.author != self.bot.user):
            modmsg = await self.modmail_dm(msg)
            self.modmails.append(self.ModmailMessage(modmsg,msg))
        # bad word
        leetdict = { # update with leet letters, syntax being {"letter": ["leetletter1","leetletter2",. . ."leetletter"]}
            "a": ["4","&","@"],
            "i": ["!","1"],
            "e": ["3"],
            "h": ["#","4"],
            "t": ["+","7"],
            "o": ["0"],
            "g": ["6","9"],
            "s": ["$"]
        }
        rawmsg = ""
        bads = await async_json.async_read_json("bad.json",[])
        for i in msg.content.lower(): # this converts leet speek letters into regular to avoid bypasses
            convert = False
            for letter, leet in leetdict.items():
                if i in leet:
                    convert = True
                    rawmsg += letter
            if not convert:
                rawmsg += i
        for bad in bads: # also make it to detect leet speak
            if bad in rawmsg:
                await msg.delete()
                rmsg = await msg.channel.send(f"{msg.author.mention} bad")
                await asyncio.sleep(2)
                await rmsg.delete()

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if ctx.author.top_role <= member.top_role:
            raise commands.errors.MissingPermissions
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member.mention}')

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def unban(self, ctx, user_id: int, *, reason="No reason provided."):
        #Unban a user by ID
        user = await self.bot.fetch_user(user_id)
        if user:
            await ctx.guild.unban(user, reason=reason)
            await ctx.send(f"{user.name} has been unbanned.")
        else:
            await ctx.send("User not found.")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if ctx.author.top_role <= member.top_role:
            raise commands.errors.MissingPermissions
        await member.kick(reason=reason)
        await ctx.send(f'Kicked {member.mention}')

    @commands.command(aliases=["timeout"])
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, duration="1d", *, reason="No reason lol"):
        # time = duration.split(" ")[0] # get the FIRST time duration
        if ctx.author.top_role <= member.top_role:
            raise commands.errors.MissingPermissions
        time = duration
        timedeltas = {
            "weeks": 0,
            "days": 0,
            "hours": 0,
            "minutes": 0
        }

        try: # check if duration format is proper
            magnitude = int(time[:-1])
        except ValueError:
            await ctx.respond("Not valid duration format")
            return
        
        match time[-1]:
            case "w":
                timedeltas["weeks"] = magnitude
            case "d":
                timedeltas["months"] = magnitude
            case "h":
                timedeltas["hours"] = magnitude
            case "m":
                timedeltas["minutes"] = magnitude
            case _:
                await ctx.respond("Not valid duration unit")
                return
        try:
            await member.timeout_for(
                duration=datetime.timedelta(
                    weeks=timedeltas["weeks"],
                    days=timedeltas["days"],
                    hours=timedeltas["hours"],
                    minutes=timedeltas["minutes"],
                    ),
                reason=reason
                )
            await ctx.send(f'{member.mention} has been muted.')
        except:
            await ctx.send(f'{member.mention} is not muted.')

    @commands.command(aliases=["untimeout"])
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx, member: discord.Member):
        if ctx.author.top_role <= member.top_role:
            raise commands.errors.MissingPermissions
        try:
            await member.remove_timeout()
            await ctx.send(f'{member.mention} has been unmuted.')
        except:
            await ctx.send('User is not muted.')
    
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amt:int):
        await ctx.channel.purge(limit = int(amt) + 1)
        msg = await ctx.send(f"Purged {amt} messages.")
        await asyncio.sleep(4)
        await msg.delete()
    
    @commands.command()
    async def deafen(self, ctx, member: discord.Member):
        if ctx.author.top_role <= member.top_role:
            raise commands.errors.MissingPermissions
        if not member.voice:
            await ctx.send("The mentioned user is not in a voice channel.")
            return
        await member.edit(deafen=True)
        await ctx.send(f"{member.display_name} has been deafened in the voice channel.")
    
    @commands.command()
    async def undeafen(self, ctx, member: discord.Member):
        if ctx.author.top_role <= member.top_role:
            raise commands.errors.MissingPermissions
        if not member.voice:
            await ctx.send("The mentioned user is not in a voice channel.")
            return
        await member.edit(deafen=False)
        await ctx.send(f"{member.display_name} has been undeafened in the voice channel.")
    
    @commands.command()
    async def voicemute(self, ctx, member: discord.Member):
        if ctx.author.top_role <= member.top_role:
            raise commands.errors.MissingPermissions
        if not member.voice:
            await ctx.send("The mentioned user is not in a voice channel.")
            return

        await member.edit(mute=True)
        await ctx.send(f"{member.display_name} has been muted in the voice channel.")

    @commands.command()
    async def unvoicemute(self, ctx, member: discord.Member):
        if ctx.author.top_role <= member.top_role:
            raise commands.errors.MissingPermissions
        if not member.voice:
            await ctx.send("The mentioned user is not in a voice channel.")
            return

        await member.edit(mute=False)
        await ctx.send(f"{member.display_name} has been unmuted in the voice channel.")
    
    @commands.command()
    async def whois(self, ctx, member: discord.Member = None):
        member = member or ctx.author

        embed = discord.Embed(title="User Information", color=member.color)
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="Profile Name", value=member.name, inline=True)
        embed.add_field(name="Server Nickname", value=member.nick, inline=True)
        embed.add_field(name="ID", value=member.id, inline=False)
        embed.add_field(name="Account Created", value=member.created_at.strftime("%b %d, %Y %H:%M:%S"), inline=False)
        embed.add_field(name="Joined Guild", value=member.joined_at.strftime("%b %d, %Y %H:%M:%S"), inline=False)

        roles = [role.mention for role in member.roles if role != ctx.guild.default_role]
        roles_str = " ".join(roles) if roles else "None"
        embed.add_field(name="Roles", value=roles_str, inline=False)

        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, channel: discord.TextChannel, interval: int=0):
        if interval == 0:
            await ctx.send(f"Slowmode has been removed in {channel.mention}.")
        
        if interval < 0:
            await ctx.send("Please provide a positive interval.")
            return

        if interval > 21600:  # Maximum slowmode interval is 6 hours (21600 seconds)
            await ctx.send("Maximum slowmode interval is 6 hours (21600 seconds).")
            return

        await channel.edit(slowmode_delay=interval)
        if interval != 0:
            await ctx.send(f"Slowmode has been set to {interval} seconds in {channel.mention}.")
    