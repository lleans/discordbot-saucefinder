import discord
import os
import io
import saucer
import re
import kadal
import random
import traceback

from colorthief import ColorThief
from urllib.request import urlopen, Request


class MaidHayasaka(discord.Client):
    ANILIST_URL = "https://img.anili.st/media/"
    RANDOM_COLOR = ["ff5c5c", "ffae5c", "ffd45c", "ff5c6c", "ff5c5c", "5cb3ff"]

    def __init__(self):
        super().__init__()
        # Command REGEX
        self.regex_command = {
            "image": re.compile(r'"(.*?)"'),
            "video": re.compile(r',(.*?),')
        }
        # Detect video using REGEX
        self.video = re.compile(
            r'(.*avi)|(.*m4v)|(.*mpeg)|(.*mpg)|(.*webm)|(.*mp4)')

        # Discord embed system message
        url_eg = {
            "url_eg": '`"https: //i.imgur.com/1Czc ..."`',
            "override_eg": '`,https: //i.imgur.com/F7ed ...,`'
        }
        self.help_message = {
            'title': "Help Commands",
            'desc': "So this is my first time with you\nso please be gentle with me....\n\n\nAnyway here the command list",
            'image': "https://i.imgur.com/38MpUXM.gif",
            'field_title': ['Basic Command', 'Override Command'],
            'color': [255, 224, 99],
            'field_value': [f"If you find a picture or video, just right click and click copy link, then enter it like the command above\n\ne.g {url_eg['url_eg']}", f"For this case, when you found some anime screenshot or gif anything that you think it is anime, you can use this command to search for it\n\ne.g {url_eg['override_eg']}"]
        }
        self.error_message = {
            'title': "Whoopsss.....",
            'desc': "Looks like i couldn't find the sauce or there is something went wrong, maybe API down or anything else, or even god doesn't like it\n\n**What should i do ?**\nYou can use these website to reverse image manually\n",
            'image': 'https://i.imgur.com/foNFxKu.gif',
            'field_title': ['Multi Service', 'Manga, anime & art', 'Everything'],
            'color': [255, 96, 56],
            'field_value': [f"[Iqdb]({'https://iqdb.org/'})\n[ImgOps]({'https://imgops.com/'})", f"[SauceNao]({'https://saucenao.com/'})\n[Ascii2D]({'https://ascii2d.net/'})\n[TraceMoe]({'https://trace.moe/'})", f"[Google Images]({'https://images.google.com/'})\n[TinEye]({'https://tineye.com/'})\n[Yandex]({'https://yandex.com/images/'})"]
        }
        self.wait_message = {
            'title': "Looking for the sauce....",
            'desc': ["nice cock bruh",
               "are you horny ?",
               "just another degenerate weeb doing the stuff",
               "Peter Piper picked a peck of pickled peppers\nA peck of pickled peppers Peter Piper picked\nIf Peter Piper picked a peck of pickled peppers\nWhere’s the peck of pickled peppers Peter Piper picked?",
               "Hi cunt",
               "The coconut nut is a giant nut\nIf you eat too much you'll get very fat\nNow the coconut nut is a big-big nut\nBut it's delicious nut is not a nut\nIt's the coco fruit (it's the coco fruit)\nOf the coco tree (of the coco tree)\nFrom the coco palm family"],
            'image': 'https://i.imgur.com/GE8uaS4.gif',
            'field_title': None,
            'color': [255, 201, 107],
             'field_value': None
        }
        self.kadal = kadal.Klient()
        print("start")

    def embed_builder(self, message, type, error=None):
        if type == "wait":
            data = self.wait_message
        elif type == "help":
            data = self.help_message
        else:
            data = self.error_message
        
        e = discord.Embed(title=data['title'], description=data['desc'] if type != "wait" else random.choice(data['desc']), color=discord.Color.from_rgb(data['color'][0], data['color'][1], data['color'][2])).set_author(name=maid.user.name, icon_url=maid.user.avatar_url).set_thumbnail(url=data['image'])
        if data['field_title'] is not None:
            for index, a in enumerate(data['field_title']):
                e.add_field(name=a,value=data['field_value'][index], inline=True)
        e.set_footer(text=f"© HayasakaMaid | {message.created_at.strftime('%x')}" if error == None else f"© HayasakaMaid | {message.created_at.strftime('%x')} | {error}")
        return e

    async def format_embed(self, sauce, type, message, original):
        method = self.kadal.search_manga if type == "manga" else self.kadal.search_anime
        try:
            nsfw = message.channel.is_nsfw()
        except:
            nsfw = False
        anilist = ""
        try:
            media = await method(sauce.title, popularity=True, allow_adult=nsfw)
            if media.description is not None:
                anilist = True
                thumbnail_anilist = f"{self.ANILIST_URL}{media.id}"
                hex_color = media.cover_color or random.choice(
                    self.RANDOM_COLOR)
                color_anilist = int(hex_color.lstrip('#'), 16)
                desc = "Likely **" + \
                    str(sauce.similiar) + f"%**\n\n***" + \
                    ", ".join(media.genres) + "***\n"
                desc += media.description[:256 - len(
                    desc)] + f"... [(more)]({media.site_url})\n\nAnother Results: \n"
                desc = desc.replace("<br>", "").replace(
                    "<i>", "").replace("/n", "")
            else:
                desc = "\nAnother Results: \n"
        except:
            desc = "Likely **" + str(sauce.similiar) + \
                f"%**\n\nAnother Results: \n"
        # find title at anilist, if exist

        for x in range(5):
            try:
                desc += f"** • [{sauce.another_titles[x][:150 - len(sauce.another_titles[x])]}...]({sauce.another_urls[x]})**\n"
            except:
                continue
        # give another results
        footer = f"Requested by {message.author.name}  •  {message.created_at.strftime('%x')}"
        if anilist == True:
            e = discord.Embed(title=sauce.title,
                              description=desc, color=color_anilist)
            e.set_image(url=thumbnail_anilist)
            e.set_thumbnail(url=original)
        else:
            try:
                req = Request(sauce.thumbnail, headers={
                              'User-Agent': 'Mozilla/5.0'})
                f = io.BytesIO(urlopen(req).read())
                e = discord.Embed(title=sauce.title,
                                  description=desc, color=int(('%02x%02x%02x' % ColorThief(f).get_color(quality=1)).lstrip('#'), 16))
                e.set_thumbnail(url=original)
                e.set_image(url=sauce.thumbnail)
            except:
                if sauce.thumbnail[:4] == 'http':
                    desc += f"\nLooks like the image doesn't show up, [click here]({sauce.thumbnail}) to open it"
                else:
                    desc += "\nLooks like there is no thumbnail for this, try click one of the results to open it"
                e = discord.Embed(title=sauce.title,
                                  description=desc, color=int(random.choice(self.RANDOM_COLOR).lstrip('#'), 16))
                e.set_thumbnail(url=original)
                e.set_image(url="https://i.imgur.com/1CzcRfk.gif")
                footer += " | Image not found 404"
        e.url = sauce.url
        e.set_footer(icon_url=sauce.source, text=footer)
        return e

    async def on_ready(self):
        print('Logged as', maid.user.name, ",", maid.user.id)
        await maid.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="@HayasakaMaid"))

    async def search(self, name, message, video):
        if name[:4] == "http":
            if video or self.video.findall(name):
                try:
                    temp = await message.channel.send(embed=self.embed_builder(message, "wait"))
                    sauce = saucer.Sauce(name, type="anime")
                    embed = await self.format_embed(sauce, type="anime", message=message, original=name)
                    await temp.delete()
                    await message.channel.send(name)
                    await message.channel.send(embed=embed)
                    await message.channel.send(sauce.url)
                except Exception as catch:
                    await temp.delete()
                    traceback.print_exc()
                    await message.channel.send(embed=self.embed_builder(message, "error", catch))
            else:
                try:
                    temp = await message.channel.send(embed=self.embed_builder(message, "wait"))
                    sauce = saucer.Sauce(name, type="image")
                    embed = await self.format_embed(sauce, type="manga", message=message, original=name)
                    await temp.delete()
                    await message.channel.send(embed=embed)
                except Exception as catch:
                    await temp.delete()
                    traceback.print_exc()
                    await message.channel.send(embed=self.embed_builder(message, "error", catch))

    async def filter(self, message, regex, method):
        m = regex.findall(message.clean_content)
        m_clean = list(filter(bool, m))
        if m_clean:
            if len(m_clean) > 1:
                for name in m_clean:
                    await self.search(name, message, method)
            if m_clean[0] == "help":
                await message.channel.send(embed=self.embed_builder(message, "help"))
            else:
                await self.search(m_clean[0], message, method)

    async def on_message(self, message):
        if message.author == self.user:
            return
        if maid.user in message.mentions:
            await message.channel.send(embed=self.embed_builder(message, "help"))
        # ignore her own message
        for type, regex in self.regex_command.items():
            method = True if type == "video" else False
            await self.filter(message, regex, method)
        # check regex


maid = MaidHayasaka()
token = open("TOKEN").readline()
maid.run(token)
