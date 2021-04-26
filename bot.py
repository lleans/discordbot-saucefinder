import discord
import io
import re
import kadal
import random
import traceback
import saucer

from aiohttp import ClientSession
from colorthief import ColorThief


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

        self.kadal = kadal.Klient()
        self.sauce = saucer.Sauce()
        print("start")

    @staticmethod
    def help(message):
        e = discord.Embed(title="Help Commands", description="So this is my first time with you\nso please be gentle with me....\n\n\nAnyway here the command list", color=discord.Color.from_rgb(255, 224, 99)).set_thumbnail(url="https://i.imgur.com/38MpUXM.gif").add_field(name="Basic Command", value='If you find a picture or video, just right click and click copy link, then enter it like the command above\n\ne.g `"https: //i.imgur.com/1Czc ..."`').add_field(
            name="Override Command", value='For this case, when you found some anime screenshot or gif anything that you think it is anime, you can use this command to search for it\n\ne.g `,https: //i.imgur.com/F7ed ...,`').set_author(name=maid.user.name, icon_url=maid.user.avatar_url).set_footer(text=f"© {maid.user.name} | {message.created_at.strftime('%x')}")
        return e

    @staticmethod
    def error(message, error):
        e = discord.Embed(title="Whoopsss.....", description="Looks like i couldn't find the sauce or there is something went wrong, maybe API down or even god doesn't like it\n\n**What should i do ?**\nYou can use these website to reverse image manually\n", color=discord.Color.from_rgb(255, 96, 56)).set_thumbnail(url="https://i.imgur.com/foNFxKu.gif").add_field(name='Multi Service', value=f"[Iqdb]({'https://iqdb.org/'})\n[ImgOps]({'https://imgops.com/'})").add_field(
            name='Manga, anime & art', value=f"[SauceNao]({'https://saucenao.com/'})\n[Ascii2D]({'https://ascii2d.net/'})\n[TraceMoe]({'https://trace.moe/'})").add_field(name='Everything', value=f"[Google Images]({'https://images.google.com/'})\n[TinEye]({'https://tineye.com/'})\n[Yandex]({'https://yandex.com/images/'})").set_author(name=maid.user.name, icon_url=maid.user.avatar_url).set_footer(text=f"© {maid.user.name} | {message.created_at.strftime('%x')} | {error}")
        return e

    @staticmethod
    def wait(message):
        rand = random.choice(["nice cock bruh",
                              "are you horny ?",
                              "just another degenerate weeb doing the stuff",
                              "Peter Piper picked a peck of pickled peppers\nA peck of pickled peppers Peter Piper picked\nIf Peter Piper picked a peck of pickled peppers\nWhere’s the peck of pickled peppers Peter Piper picked?",
                              "Hi cunt",
                              "The coconut nut is a giant nut\nIf you eat too much you'll get very fat\nNow the coconut nut is a big-big nut\nBut it's delicious nut is not a nut\nIt's the coco fruit (it's the coco fruit)\nOf the coco tree (of the coco tree)\nFrom the coco palm family"])
        e = discord.Embed(title="Looking for the sauce....", description=rand, color=discord.Color.from_rgb(255, 201, 107)).set_thumbnail(
            url="https://i.imgur.com/GE8uaS4.gif").set_author(name=maid.user.name, icon_url=maid.user.avatar_url).set_footer(text=f"© {maid.user.name} | {message.created_at.strftime('%x')}")
        return e

    async def format_embed(self, sauce, *, type, message, original, anilist=False):
        footer = f"© {maid.user.name} | {message.created_at.strftime('%x')}"
        # Anilist
        try:
            media = await type(sauce['title'], popularity=True, allow_adult=True)
            if media.description is not None:
                anilist = True
                thumbnail_anilist = f"{self.ANILIST_URL}{media.id}"
                hex_color = media.cover_color or random.choice(
                    self.RANDOM_COLOR)
                color_anilist = int(hex_color.lstrip('#'), 16)
                desc = f"Likely **{sauce['similiar']}%**\n\n***{', '.join(media.genres)}***\n"
                anilist_description = media.description.replace("<br>", "").replace("<i>", "").replace("<b>", "").replace("</br>", "").replace("/<i>", "").replace("</b>", "")
                desc += anilist_description[:256 - len(desc)] + f"... [(more)]({media.site_url})\n\nAnother Results: \n"
            else:
                desc = "\nAnother Results: \n"
        except:
            desc = f"Likely **{sauce['similiar']}%**\n\nAnother Results: \n"

        # Another Resulta
        for x in range(3):
            try:
                desc += f"** • [{sauce['another_titles'][x][:150 - len(sauce['another_titles'][x])]} ...]({sauce['another_urls'][x]})**\n"
            except:
                continue

        # Embed
        if anilist == True:
            e = discord.Embed(title=sauce['title'],
                              description=desc, color=color_anilist)
            e.set_image(url=thumbnail_anilist)
        else:
            try:
                async with ClientSession() as Session:
                    async with Session.get(sauce['thumbnail'], allow_redirects=True, headers={'User-Agent': 'Mozilla/5.0'}) as data:
                        f = io.BytesIO(await data.read())
                        e = discord.Embed(title=sauce['title'], description=desc, color=int(('%02x%02x%02x' % ColorThief(f).get_color(quality=1)).lstrip('#'), 16))
                        e.set_image(url=sauce['thumbnail'])
            except:
                if sauce['thumbnail'][:4] == 'http':
                    desc += f"\nLooks like the image doesn't show up, [click here]({sauce['thumbnail']}) to open it"
                else:
                    desc += "\nLooks like there is no thumbnail for this, try click one of the results to open it"
                e = discord.Embed(title=sauce['title'], description=desc, color=int(
                    random.choice(self.RANDOM_COLOR).lstrip('#'), 16))
                e.set_image(url="https://i.imgur.com/1CzcRfk.gif")
                footer += " | Image not found 404"
        e.url = sauce['url']
        e.set_thumbnail(url=original)
        e.set_author(name=sauce['source'][1], icon_url=sauce['source'][0])
        e.set_footer(icon_url=message.author.avatar_url, text=footer)
        return e

    async def on_ready(self):
        print('Logged as', maid.user.name, ",", maid.user.id)
        await maid.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"@{maid.user.name}"))

    async def search(self, name, message, video):
        temp = await message.channel.send(embed=self.wait(message))
        if video or self.video.findall(name):
            try:
                sauce = await self.sauce.sauce_anime(name=name)
                embed = await self.format_embed(sauce, type=self.kadal.search_anime, message=message, original=name)
                await temp.delete()
                if self.video.findall(name):
                    await message.channel.send(name)
                await message.channel.send(embed=embed)
                await message.channel.send(sauce['url'])
            except Exception as catch:
                await temp.delete()
                traceback.print_exc()
                await message.channel.send(embed=self.error(message, catch))
        else:
            try:
                sauce = await self.sauce.sauce_image(name=name)
                embed = await self.format_embed(sauce, type=self.kadal.search_manga, message=message, original=name)
                await temp.delete()
                await message.channel.send(embed=embed)
            except Exception as catch:
                await temp.delete()
                traceback.print_exc()
                await message.channel.send(embed=self.error(message, catch))

    async def filter(self, message, regex, method):
        m = regex.findall(message.clean_content)
        m_clean = list(filter(bool, m))
        if m_clean:
            if len(m_clean) > 1:
                for name in m_clean:
                    if name[:4] == "http":
                        await self.search(name, message, method)
            elif m_clean[0] == "help":
                await message.channel.send(embed=self.help(message))
            else:
                if m_clean[0][:4] == "http":
                    await self.search(m_clean[0], message, method)

    async def on_message(self, message):
        if message.author == self.user:
            return
        if maid.user in message.mentions and message.clean_content == f"@{maid.user.name}":
            await message.channel.send(embed=self.help(message))
        # ignore her own message
        for type, regex in self.regex_command.items():
            method = True if type == "video" else False
            await self.filter(message, regex, method)
        # check regex


maid = MaidHayasaka()
token = open("TOKEN").readline()
maid.run(token)
