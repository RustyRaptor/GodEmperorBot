from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from datetime import datetime, date, time, timedelta
from collections import Counter
import sys
import asyncio
import os
import random
import requests
import discord
import youtube_dl
from discord.ext import commands

from discord.ext.commands import bot

# consumer_key=""
# consumer_secret=""
# access_token=""
# access_token_secret=""
#
# auth = OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)
# auth_api = API(auth)
# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


def get_sound(key):
    # sounds = {
    #     "eggs": "eggs.ogg",
    #     "semx": "moan.ogg",
    #     "crabrave": random.choice([
    #         "crab.opus",
    #         "crabrave_smb.opus",
    #         "crabmetal.opus",
    #         "crabali.opus",
    #         "crabsans.opus",
    #         "crabgod.opus"])
    # }
    path = random.choice(os.listdir("sounds/" + key))  # change dir name to whatever

    return "sounds/" + key + "/" + path




dorimes = [
    "https://youtu.be/f6jvnmyYpl8",
    "https://www.youtube.com/watch?v=hCzfzeobeNM",
    "https://www.youtube.com/watch?v=kLaaJ_aeoyM",
    "https://www.youtube.com/watch?v=zQ4LiyFF8RU",
    "https://www.youtube.com/watch?v=6xUnSVTh8fI"
]


def get_video(source):
    cheemses = [
        "https://www.youtube.com/channel/UChZWowQd_y6usuF7vSL4jmA"
    ]
    channels = [
        "https://www.youtube.com/channel/UCYd6CmhFvvq6yruUBmGXjuA/videos",
        "https://www.youtube.com/channel/UCX2laRqGQhqoChYmlaUgOiw/videos",
        "https://www.youtube.com/user/wettitab/videos",
        "https://www.youtube.com/channel/UC38r7_x7oMPAZweB2fvGDXQ/videos",
        "https://www.youtube.com/channel/UC-xjitW_J39_Q1ure2HlJew/videos",
        "https://www.youtube.com/channel/UCHh-cQr-viOcimjPhxr3xRQ/videos",
        "https://www.youtube.com/channel/UCAJI1a4L0R5HkvTHTxZOd6g/videos",
        "https://www.youtube.com/user/shibainusaki/videos",
        "https://www.youtube.com/channel/UCOE2s_EwBM0es4TfC6ce7Fg/videos",
        "https://www.youtube.com/channel/UCkEdaRw8w0daEvGgzKff8TA",
        "https://www.youtube.com/channel/UC_WUkVnPROmHC1qnGHQAMDA",
        "https://www.youtube.com/channel/UChZWowQd_y6usuF7vSL4jmA"

    ]

    sources = {
        "shibes": channels,
        "cheems": cheemses
    }
    all_vids = []
    for i in sources[source]:
        url = i
        page = requests.get(url).content
        data = str(page).split(' ')
        item = 'href="/watch?'
        vids = [line.replace('href="', 'youtube.com') for line in data if
                item in line]  # list of all videos listed twice
        all_vids.extend(vids)
    return random.choice(all_vids)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="DOGE BOT COMMANDS", description="command prefix is doge! e.g. doge!meme",
                              color=0xe8e361)
        embed.set_author(name="GodEmperorDoge", url="https://www.github.com/rustyraptor")
        embed.set_thumbnail(url="https://i.imgur.com/ddy9MGr.jpg")
        embed.add_field(name="meme", value="fetch a random doge meme or template", inline=False)
        embed.add_field(name="memerand", value="fetch a random image", inline=False)
        embed.add_field(name="shibe", value="get a cute or funny shibe video", inline=False)
        embed.add_field(name="play", value="play a sound (for list of sounds type doge!playlist", inline=False)
        embed.add_field(name="yt", value="play a youtube video link", inline=False)
        embed.add_field(name="volume", value="adjust volume to n%", inline=False)
        embed.add_field(name="eggs", value="eggs", inline=False)
        embed.add_field(name="emote", value="doge will send an emote he has access to. ", inline=False)
        embed.add_field(name="stop", value="stops playback and disconnects", inline=False)
        embed.set_footer(text="If you want more content or features ask me to add them. ")
        await ctx.send(embed=embed)

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def shibe(self, ctx):
        await ctx.send("https://www." + str(get_video("shibes")).replace("\"", ""))

    @commands.command()
    async def cheems(self, ctx):
        await ctx.send("https://www." + str(get_video("cheems")).replace("\"", ""))
        path = random.choice(os.listdir("cheems/"))  # change dir name to whatever
        await ctx.send(file=discord.File("cheems/" + path))

    @commands.command(aliases=['EGGS', 'eggs', 'Eggs'])
    async def play(self, ctx, args="eggs"):
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(get_sound(args)))
        emote = "ERROR: EMOTE NOT FOUND"
        for i in bot.emojis:
            if i.name == "cooldoge":
                emote = str(i)
        await ctx.send(emote)
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
        if args == "dorime":
            path = random.choice(os.listdir("dorimepic/"))  # change dir name to whatever
            await ctx.send(file=discord.File("dorimepic/" + path))
            await ctx.send(random.choice(dorimes))

    @commands.command()
    async def yt(self, ctx, *, url):

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def stream(self, ctx, *, url):

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def volume(self, ctx, volume: int):

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command()
    async def stop(self, ctx):

        await ctx.voice_client.disconnect()

    @commands.command()
    async def emote(self, ctx, arg):
        emote = "ERROR: EMOTE NOT FOUND"
        for i in bot.emojis:
            if i.name == str(arg):
                emote = str(i)
        await ctx.send(emote)

    @commands.command()
    async def meme(self, ctx):
        path = random.choice(os.listdir("memes/"))  # change dir name to whatever
        await ctx.send(file=discord.File("memes/" + path))

    @commands.command()
    async def memerand(self, ctx):
        path = random.choice(os.listdir("memerand/"))  # change dir name to whatever
        await ctx.send(file=discord.File("memerand/" + path))

    @play.before_invoke
    @yt.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


bot = commands.Bot(command_prefix=commands.when_mentioned_or("doge!"),
                   description='Karen, release me from this discord bot immediately!')
bot.remove_command('help')

@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')


bot.add_cog(Music(bot))
bot.run('yourtoken')
