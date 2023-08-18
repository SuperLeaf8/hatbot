import discord
from discord.ext import commands
from discord.utils import get
import pytube
###
import json
import requests, os, asyncio
from traceback import print_exc


# ydl_opts = {
# 	'format': 'bestaudio/best',
# 	'quiet': True,
# 	'outtmpl': u'song.%(ext)s',
# 	'postprocessors': [{
# 		'key': 'FFmpegExtractAudio',
# 		'preferredcodec': 'mp3',
# 		'preferredquality': '192',
# 		}],
# }

# def search(arg):
# 	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
# 		try:
# 			requests.get(arg)
# 			video = ydl.extract_info(arg, download=False) 
# 		except:
# 			video = ydl.extract_info(f"ytsearch: {[arg]}", download=False)['entries'][0]
# 	return video['webpage_url'], video['title']



class MusicCommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.loops = []
		self.volumes = {}

	#### TEST FUNCTIONs
	def check_channel(self,ctx):
		channel = ctx.author.voice.channel
		return channel
	def check_bot_channel(self,ctx):
		voice = get(self.bot.voice_clients,guild=ctx.guild)
		return voice

	@commands.command()
	async def join(self, ctx):
		channel = self.check_channel(ctx)
		bot_voice = self.check_bot_channel(ctx)
		if not channel:
			await ctx.send("youre not in a channel")
			return
		if not bot_voice:
			await channel.connect()
			await ctx.send("joined")
		else:
			await ctx.send("im already in the channel idiot")

	@commands.command()
	async def leave(self, ctx):
		voice = get(self.bot.voice_clients,guild=ctx.guild)
		if not voice:
			await ctx.send("am not in channel")
			return
		if str(ctx.guild.id) in self.loops:
			self.loops.remove(str(ctx.guild.id))
		await voice.disconnect()
		await ctx.send("left")
		

	@commands.command()
	async def testplay(self,ctx,name:str):
		music = get(self.bot.voice_clients,guild=ctx.guild) # voice object
		channel = ctx.author.voice.channel # channel object
		audio = discord.FFmpegPCMAudio(f"./cogs/music_cog/{name}.mp3") # audiosource object
		if not channel:
			await ctx.send("youre not in a channel")
			return
		if not music:
			await ctx.send("am not in channel")
			return
		# def replay():
		# 	source = discord.FFmpegPCMAudio(f"{name}.mp3")
		# 	if str(ctx.guild.id) in self.loops:
		# 		music.play(source,after=lambda bruh: replay()) # THIS IS FUCKING CRASHING
		# 		# music.source = discord.PCMVolumeTransformer(music.source,volume=self.volumes.get(ctx.guild.id,1.0))
		try:

			# music.play(audio,after=lambda check: replay())
			music.play(audio)
			# music.source = discord.PCMVolumeTransformer(music.source,volume=self.volumes.get(ctx.guild.id,1.0))
			await ctx.send("vibe time")
		except:
			print_exc()

	@commands.command() # for fun
	async def play(self,ctx,*,song):
		music = get(self.bot.voice_clients,guild=ctx.guild)
		channel = ctx.author.voice.channel

		try:
			requests.get(song)
			yt = pytube.YouTube(song)
		except:
			yt = pytube.Search(song).results[0]
		
		stream = yt.streams.filter(only_audio=True).first()
		destiny = stream.download(filename=f"./cogs/music_cog/music_cache/{str(ctx.guild.id)}")
		
		audio = discord.FFmpegPCMAudio(source=destiny)

		if not channel:
			await ctx.send("youre not in a channel")
			return
		if not music:
			await ctx.send("am not in channel")
			return

		def replay():
			source = discord.FFmpegPCMAudio(source=destiny)
			if str(ctx.guild.id) in self.loops:		
				music.play(source,after=lambda bruh: replay()) # THIS IS FUCKING CRASHING
				music.source = discord.PCMVolumeTransformer(music.source,volume=self.volumes.get(ctx.guild.id,1.0))
		
		if music.is_playing():
			music.stop()
		music.play(audio,after=lambda check: replay())
		music.source = discord.PCMVolumeTransformer(music.source,volume=self.volumes.get(ctx.guild.id,1.0))
		await ctx.send("playing")
	
	def play_music(self,ctx,src_name):
		channel = self.check_channel(ctx)
		voice = self.check_bot_channel(ctx)
		# here, check if voice and channel are valid

		#

		if str(ctx.guild.id) in self.loops:
			self.loops.remove(str(ctx.guild.id))
		src = discord.FFmpegPCMAudio(source=src_name)
		voice.source = discord.PCMVolumeTransformer(voice.source,volume=1.0)
		def replay():
			src = discord.FFmpegPCMAudio(source=src_name)
			if str(ctx.guild.id) in self.loops:		
				voice.play(src,after=lambda after: replay())
				voice.source = discord.PCMVolumeTransformer(voice.source,volume=self.volumes.get(ctx.guild.id,1.0))
		voice.play(src,after=lambda after: replay())
		
		

	@commands.command()
	async def testfile(self,ctx):
		music = get(self.bot.voice_clients,guild=ctx.guild)
		channel = ctx.author.voice.channel
		music.play(source = discord.FFmpegPCMAudio(source=f"music_files/{ctx.guild.id}_music.mp3"))
		music.source = discord.PCMVolumeTransformer(music.source,volume=1.0)
		
	@commands.command()
	async def loop(self, ctx): # can only loop when music play
		music = get(self.bot.voice_clients,guild=ctx.guild)
		channel = ctx.author.voice.channel
		if not channel:
			await ctx.send("youre not in a channel")
			return
		if not music:
			await ctx.send("am not in channel")
			return
		if music.is_playing() or music.is_paused(): # if music is playing or music is PAUSED
			if not str(ctx.guild.id) in self.loops:
				self.loops.append(str(ctx.guild.id))
				await ctx.send("loop enabled")
			else:
				self.loops.remove(str(ctx.guild.id))
				await ctx.send("loop disabled")
		else:
			await ctx.send("music not playing")
			return
	
	@commands.command()
	async def pause(self,ctx):
		music = get(self.bot.voice_clients,guild=ctx.guild)
		channel = ctx.author.voice.channel
		if not channel:
			await ctx.send("youre not in a channel")
			return
		if not music:
			await ctx.send("am not in channel")
			return
		if music.is_playing():
			music.pause()
			await ctx.send("paused")
		else:
			await ctx.send("music already paused")
	
	@commands.command()
	async def stop(self,ctx):
		music = get(self.bot.voice_clients,guild=ctx.guild)
		channel = ctx.author.voice.channel
		if not channel:
			await ctx.send("youre not in a channel")
			return
		if not music:
			await ctx.send("am not in channel")
			return
		if music.is_playing() or music.is_paused():
			if str(ctx.guild.id) in self.loops:
				self.loops.remove(str(ctx.guild.id))
			music.stop()
			await ctx.send("stopped")
		else:
			await ctx.send("music not playing")
	
	@commands.command()
	async def resume(self, ctx):
		music = get(self.bot.voice_clients,guild=ctx.guild)
		channel = ctx.author.voice.channel
		if not channel:
			await ctx.send("youre not in a channel")
			return
		if not music:
			await ctx.send("am not in channel")
			return
		if music.is_paused():
			music.resume()
			await ctx.send("resumed")
		else:
			await ctx.send("music not paused")

	@commands.command()
	async def setvolume(self,ctx,number:int):
		voice = get(self.bot.voice_clients,guild=ctx.guild)
		channel = ctx.author.voice.channel
		if not channel:
			await ctx.send("you are not in a channel")
			return
		if not voice:
			await ctx.send("im not in a channel")
		if not voice.is_playing():
			await ctx.send("im not playing anything")
			return
		vol = float(number/100)
		if ctx.guild.id not in self.volumes.keys():
			self.volumes.update({ctx.guild.id:vol})
		else:
			self.volumes[ctx.guild.id] = vol
		voice.source.volume = vol
		await ctx.send(f"set volume to {vol*100}%")
	
	@commands.command()
	async def volume(self,ctx):
		x = self.volumes.get(ctx.guild.id,1.0)
		await ctx.send(f"volume is currently {x*100}%")
