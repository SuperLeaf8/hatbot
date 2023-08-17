import discord
from discord.ext import commands
from discord.utils import get
from traceback import print_exc
from asyncio import sleep
import youtube_dl
import requests
import shutil
import os
from traceback import print_exc
import json


"""
IF YOURE GONNA MAKE THIS BOT PUBLIC YOU NEED TO MAKE SONG FILES FOR EACH SERVER

and that might suck

so lay off the music commands for now

SCREW YOU PAST DENNIS I MADE IT WORK
"""

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
	async def yt_play(self,ctx,*,song):
		music = get(self.bot.voice_clients,guild=ctx.guild)
		channel = ctx.author.voice.channel
		filename = f'{ctx.guild.id}_music.mp3'
		ydl_opts = {
			'format': 'bestaudio/best',
			# 'quiet': True,
			'outtmpl': '{0}.%(ext)s'.format(f"{ctx.guild.id}_music"),
			'noplaylist':True,
			'ignoreerrors':True,
			'postprocessors': [{
				'key': 'FFmpegExtractAudio',
				'preferredcodec': 'mp3',
				'preferredquality': '192',
				}],
		}

		def search(arg):
			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				try:
					requests.get(arg)
					video = ydl.extract_info(arg, download=False) 
				except:
					video = ydl.extract_info(f"ytsearch: {[arg]}", download=False)['entries'][0]
			return video['webpage_url'], video['title']

		link, title = search(song)
		
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			ydl.download([link])
		
		destiny = f"{os.getcwd()}/music_files/{filename}"
		source = f"{os.getcwd()}/{filename}"
		

		shutil.move(source,destiny)

		print("\n\ndownloaded",title)
		
		audio = discord.FFmpegPCMAudio(source=destiny)
		if not channel:
			await ctx.send("youre not in a channel")
			return
		if not music:
			await ctx.send("am not in channel")
			return
		def replay():
			source = discord.FFmpegPCMAudio(source=f"{os.getcwd()}/music_files/{filename}")
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
	
	# @commands.command()
	# async def play(self, ctx,*,name):
	# 	music = get(self.bot.voice_clients,guild=ctx.guild)
	# 	channel = ctx.author.voice.channel
	# 	if str(ctx.guild.id) in self.loops:
	# 		self.loops.remove(str(ctx.guild.id))
	# 	with open("inventory.json","r") as f:
	# 		data = json.load(f)
	# 		uitems = [] # the items the user actually has
	# 		for di in data[str(ctx.author.id)]:
	# 			uitem = item.Item(di["name"],di["type"],di["price"])
	# 			uitems.append(uitem)
			
	# 		exists = False
	# 		is_music = False
	# 		for i in item.all_items:
	# 			if i.name == name:
	# 				exists = True
	# 				if i.itemtype == "music":
	# 					is_music = True
	# 		if not exists:
	# 			await ctx.send("this item doesnt even exist")
	# 			return
	# 		elif not is_music:
	# 			await ctx.send("this isnt a music item")
	# 			return

	# 		if not name in [n.name for n in uitems]:
	# 			await ctx.send("you dont have this song")
	# 			return

	# 	file = f"{os.getcwd()}\\kk_music\\{name}.mp3"
		
	# 	audio = discord.FFmpegPCMAudio(source=file)
	# 	if not channel:
	# 		await ctx.send("youre not in a channel")
	# 		return
	# 	if not music:
	# 		await ctx.send("am not in channel")
	# 		return
	# 	def replay():
	# 		source = discord.FFmpegPCMAudio(source=file)
	# 		if str(ctx.guild.id) in self.loops:		
	# 			music.play(source,after=lambda bruh: replay()) # THIS IS FUCKING CRASHING
	# 			music.source = discord.PCMVolumeTransformer(music.source,volume=self.volumes.get(ctx.guild.id,1.0))
	# 	if music.is_playing():
	# 		music.stop()
	# 	music.play(audio,after=lambda check: replay())
	# 	music.source = discord.PCMVolumeTransformer(music.source,volume=self.volumes.get(ctx.guild.id,1.0))
	# 	await ctx.send(f"playing {name}")
	
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
