import discord
from discord.ext import commands
from discord.utils import get
import pytube
###
import json
from configparser import ConfigParser
import random
import requests, os, asyncio
from traceback import print_exc


class MusicCommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	loops = []
	conts = []
	volumes = {}
	queues = {}

	config = ConfigParser()
	config.read("options.cfg")

	# getter functions
	def get_loops(self):
		return self.loops
	def get_queues(self):
		return self.queues

	# queue functions for ease
	def queue_skip(self,server): # updates queue and index, will return the next index
		try:
			queue = self.queues[str(server.id)]["queue"] # queue is a list, index is an int
			index = self.queues[str(server.id)]["index"]
			if not len(queue):
				raise Exception
		except:
			return None
		if (index + 1) < len(queue):
			index += 1
		else:
			index = 0
		self.queues[str(server.id)]["queue"] = queue
		self.queues[str(server.id)]["index"] = index
		return index
	def queue_back(self,server): # updates queue and index, will return the previous index
		try:
			queue = self.queues[str(server.id)]["queue"] # queue is a list, index is an int
			index = self.queues[str(server.id)]["index"]
			if not len(queue):
				raise Exception
		except:
			return None
		if (index + 1) > 0:
			index -= 1
		else:
			index = len(queue) - 1
		self.queues[str(server.id)]["queue"] = queue
		self.queues[str(server.id)]["index"] = index
		return index
	def queue_reinit(self,server): # reinitialize queues to prevent key errors, or to create one when adding songs
		try:
			queue = self.queues[str(server.id)]["queue"] # queue is a list, index is an int
			index = self.queues[str(server.id)]["index"]
		except: # there is no queue for the server, initialize one
			self.queues[str(server.id)] = {}
			self.queues[str(server.id)]["queue"] = []
			self.queues[str(server.id)]["index"] = 0
		# reset queue, we could make this be skipped if except block is ran (effeciency)
		self.queues[str(server.id)]["queue"] = []
		self.queues[str(server.id)]["index"] = 0
	def queue_shuffle(self,server):
		try:
			queue = self.queues[str(server.id)]["queue"] # queue is a list, index is an int
			index = self.queues[str(server.id)]["index"]
		except:
			return None
		queue = random.shuffle(queue)
		self.queues[str(server.id)]["queue"] = queue
		return queue

	# music commands
	# def play() . . .
	
	class MusicSelect(discord.ui.View): # view for selecting which song to play/add
		def __init__(self, outer, options):
			discord.ui.View.__init__(self)
			self.options = options
			self.index = 0
			self.outer = outer
		@discord.ui.button(
			label="Previous", style=discord.ButtonStyle.success
		)
		async def previous_button(self, button, interaction):
			if self.index > 0:
				self.index = len(self.options) - 1
			else:
				self.index -= 1
			await interaction.message.edit(content=f"song: {self.options[self.index].title}")
			await interaction.response.defer()
		
		@discord.ui.button(
			label="Select", style=discord.ButtonStyle.success
		)
		async def select_button(self, button, interaction):
			try:
				self.outer.queues[str(interaction.guild.id)]["queue"].append(self.options[self.index])
			except:
				self.outer.queue_reinit(interaction.guild)
				self.outer.queues[str(interaction.guild.id)]["queue"].append(self.options[self.index])
			self.disable_all_items()
			await interaction.response.edit_message(view=self)
			await interaction.followup.send("queued this song")

		@discord.ui.button(
			label="Next", style=discord.ButtonStyle.primary
		)
		async def next_button(self, button, interaction):
			if self.index < len(self.options):
				self.index += 1
			else:
				self.index = 0
			await interaction.message.edit(content=f"song: {self.options[self.index].title}")
			await interaction.response.defer()
	
	class MusicControl(discord.ui.View): # view object for controlling music while it is playing
		def __init__(self, outer): # oh my GOD this is terrible, i dont even want to look at this, i know this is bad but i dont know how else to make it work
			discord.ui.View.__init__(self,timeout=None)
			self.outer = outer # please have sympathy for me
		@discord.ui.button(
			label="Back", style=discord.ButtonStyle.secondary
		)
		async def back_button(self, button, interaction):
			music = get(interaction.client.voice_clients,guild=interaction.guild)
			self.outer.queue_back(interaction.guild)
			index = self.outer.queues[str(interaction.guild.id)]["index"]
			# await interaction.message.edit(content=f"playing {self.outer.queues[str(interaction.guild.id)]['queue'][index].name}") # redundant i think
			await interaction.response.defer()
			music.stop()

		@discord.ui.button(
			label="Pause/Resume", style=discord.ButtonStyle.primary
		)
		async def pause_button(self, button, interaction): # pause using bot object commands
			music = get(interaction.client.voice_clients,guild=interaction.guild)
			if music.is_playing():
				music.pause()
				msg = await interaction.response.send_message("paused")
			else:
				music.resume()
				msg = await interaction.response.send_message("resumed")
			await asyncio.sleep(1)
			await msg.delete_original_message()
			
		@discord.ui.button(
			label="Stop", style=discord.ButtonStyle.red
		)
		async def stop_button(self, button, interaction):
			music = get(interaction.client.voice_clients,guild=interaction.guild)
			if not music:
				self.disable_all_items()
				return
			if music.is_playing():
				if str(interaction.guild.id) in self.outer.conts:
					self.outer.conts.remove(str(interaction.guild.id))
				music.stop()
				self.disable_all_items()
				await interaction.response.edit_message(view=self) # after interaction has been responded to, use followup.send()
				await interaction.followup.send("stopped")
			else:
				self.disable_all_items()
				await interaction.response.edit_message(view=self)
				await interaction.followup.send("no music playing")

		@discord.ui.button(
			label="Forward", style=discord.ButtonStyle.secondary
		)
		async def forward_button(self, button, interaction):
			music = get(interaction.client.voice_clients,guild=interaction.guild)
			self.outer.queue_skip(interaction.guild) # dont include self.outer argument
			index = self.outer.queues[str(interaction.guild.id)]["index"]
			# await interaction.message.edit(content=f"playing {self.outer.queues[str(interaction.guild.id)]['queue'][index].name}") # redundant too
			await interaction.response.defer()
			music.stop()
		
		@discord.ui.button(
			label="Shuffle", style=discord.ButtonStyle.primary
		)
		async def shuffle_button(self, button, interaction):
			self.outer.queue_shuffle(self.outer, interaction.guild)
		
		@discord.ui.button(
			label="Loop", style=discord.ButtonStyle.secondary
		)
		async def loop_button(self, button, interaction):
			music = get(interaction.client.voice_clients,guild=interaction.guild)
			channel = interaction.user.voice.channel
			if music and channel and (music.is_playing or music.is_paused):
				if not str(interaction.guild.id) in self.outer.loops: # ew ew ew ew ew ew
					self.outer.loops.append(str(interaction.guild.id))
					button.style = discord.ButtonStyle.primary
					# msg = await interaction.response.send_message("loop enabled")
				else:
					self.outer.loops.remove(str(interaction.guild.id))
					button.style = discord.ButtonStyle.secondary
					# msg = await interaction.response.send_message("loop disabled")
				# await asyncio.sleep(1)
				# await msg.delete_original_message()
				await interaction.response.edit_message(view=self)
			else:
				await interaction.response.send_message("not playing music")

	
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
	async def play(self,ctx,*,song=""):
		if not os.path.exists("./cogs/music_cog/music_cache"):
			os.mkdir("./cogs/music_cog/music_cache")
		
		if not str(ctx.guild.id) in self.conts:
			self.conts.append(str(ctx.guild.id))

		music = get(self.bot.voice_clients,guild=ctx.guild)
		channel = ctx.author.voice.channel

		if not channel:
			await ctx.send("youre not in a channel")
			return
		if not music:
			await ctx.send("am not in channel")
			return
		if song:
			try:
				requests.get(song)
				yt = pytube.YouTube(song)
			except:
				yt = pytube.Search(song).results[0]
			try:
				self.queues[str(ctx.guild.id)]["queue"].append(yt)
				index = self.queue_skip(ctx.guild)
			except KeyError:
				self.queue_reinit(ctx.guild)
				self.queues[str(ctx.guild.id)]["queue"].append(yt)
				index = self.queue_skip(ctx.guild)
		
		else:
			try:
				yt = self.queues[str(ctx.guild.id)]["queue"][0]
			except KeyError:
				await ctx.send("no songs in queue")
				return
		
		stream = yt.streams.filter(only_audio=True).first()
		destiny = stream.download(filename=f".\\cogs\\music_cog\\music_cache\\{str(ctx.guild.id)}")
		audio = discord.FFmpegPCMAudio(source=destiny)

		

		def replay(pre_index,file,msg): # get previouis index so we can tell if we screwed with the indexes using queue control
			if str(ctx.guild.id) in self.loops:
				source = discord.FFmpegPCMAudio(source=file)
				nindex = pre_index
			elif str(ctx.guild.id) in self.conts: # go next in queue
				nindex = self.queues[str(ctx.guild.id)]["index"] # new index
				if nindex == pre_index:
					nindex = self.queue_skip(ctx.guild)
				yt = self.queues[str(ctx.guild.id)]["queue"][nindex]
				stream = yt.streams.filter(only_audio=True).first()
				destiny = stream.download(filename=f"./cogs/music_cog/music_cache/{str(ctx.guild.id)}")
				source = discord.FFmpegPCMAudio(source=destiny)
				# edit_coro = msg.edit(content=f"playing {stream.title}",view=self.MusicControl(outer=self))
				async def edit():
					await msg.edit(content=f"playing {stream.title}")
				asyncio.run_coroutine_threadsafe(edit(), self.bot.loop)
			music.play(source,after=lambda bruh: replay(nindex,destiny,msg))
			music.source = discord.PCMVolumeTransformer(music.source,volume=self.volumes.get(ctx.guild.id,float(self.config["MUSIC"]["volume"])))

		if music.is_playing():
			music.stop()
		msg = await ctx.send(f"playing {stream.title}",view=self.MusicControl(outer=self))
		music.play(audio,after=lambda check: replay(index,destiny,msg))
		music.source = discord.PCMVolumeTransformer(music.source,volume=self.volumes.get(ctx.guild.id,float(self.config["MUSIC"]["volume"])))
	
	@commands.command()
	async def queue(self, ctx, *, song): # add yt object to queues
		music = get(self.bot.voice_clients,guild=ctx.guild)
		channel = ctx.author.voice.channel

		try:
			requests.get(song)
			yt = list(pytube.YouTube(song))
		except:
			yt = pytube.Search(song).results
		
		if len(yt) > 1:
			options = [yt[i] for i in range(min(5,len(yt)))] # when searching queue with words using pytube.Search, return first 5 yt objects
			await ctx.send(f"song: {options[0].title}",view=self.MusicSelect(outer=self,options=options))
		else:
			try:
				self.loops[str(ctx.guild.id)]["queue"].append(yt[0])
			except:
				self.queue_reinit(MusicCommands,ctx.guild)
				self.loops[str(ctx.guild.id)]["queue"].append(yt[0])
			await ctx.send(f"song: {yt[0].title}")

	@commands.command()
	async def queuels(self, ctx):
		msg = ""
		try:
			for song in self.queues[str(ctx.guild.id)]["queue"]:
				msg += f"{song.title} - {song.author}\n"
		except:
			return
		if not msg:
			await ctx.send("none")
			return
		await ctx.send(msg)

	@commands.command() # debug command
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
		x = self.volumes.get(ctx.guild.id,float(self.config["MUSIC"]["volume"]))
		await ctx.send(f"volume is currently {x*100}%")
