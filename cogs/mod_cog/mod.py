import discord
from discord.ext import commands
import datetime
import asyncio
import random

class ModCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if ctx.author.guild_permissions.ban_members:
            await member.ban(reason=reason)
            await ctx.send(f'Banned {member.mention}')
        else:
            await ctx.send('You do not have permission to use this command.')

    @commands.command()
    async def unban(self, ctx, user_id: int, *, reason="No reason provided."):
        #Unban a user by ID
        user = await self.bot.fetch_user(user_id)
        if user:
            await ctx.guild.unban(user, reason=reason)
            await ctx.send(f"{user.name} has been unbanned.")
        else:
            await ctx.send("User not found.")

    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if ctx.author.guild_permissions.kick_members:
            await member.kick(reason=reason)
            await ctx.send(f'Kicked {member.mention}')
        else:
            await ctx.send('You do not have permission to use this command.')

    @commands.command()
    async def mute(self, ctx, member: discord.Member, duration="1d", *, reason="No reason lol"):
        # time = duration.split(" ")[0] # get the FIRST time duration
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

        if ctx.author.guild_permissions.administrator:
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

    @commands.command()
    async def unmute(self, ctx, member: discord.Member):
        if ctx.author.guild_permissions.administrator:
            await member.remove_timeout()
            await ctx.send(f'{member.mention} has been unmuted.')
        else:
            await ctx.send('User is not muted.')
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx, amt:int):
        await ctx.channel.purge(limit = int(amt) + 1)
        msg = await ctx.send(f"Purged {amt} messages.")
        await asyncio.sleep(4)
        await msg.delete()
    
    @commands.command()
    async def deafen(self, ctx, member: discord.Member):
        if not member.voice:
            await ctx.send("The mentioned user is not in a voice channel.")
            return
        await member.edit(deafen=True)
        await ctx.send(f"{member.display_name} has been deafened in the voice channel.")
    
    @commands.command()
    async def undeafen(self, ctx, member: discord.Member):
        if not member.voice:
            await ctx.send("The mentioned user is not in a voice channel.")
            return
        await member.edit(deafen=False)
        await ctx.send(f"{member.display_name} has been undeafened in the voice channel.")
    
    @commands.command()
    async def voicemute(self, ctx, member: discord.Member):
        if not member.voice:
            await ctx.send("The mentioned user is not in a voice channel.")
            return

        await member.edit(mute=True)
        await ctx.send(f"{member.display_name} has been muted in the voice channel.")

    @commands.command()
    async def unvoicemute(self, ctx, member: discord.Member):
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
    async def slowmode(self, ctx, channel: discord.TextChannel, interval: int):
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