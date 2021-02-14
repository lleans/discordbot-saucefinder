import discord
import os
import io
import saucer
import re
import kadal
import random

from colorthief import ColorThief
from urllib.request import urlopen, Request
from itertools import islice


class MaidOurdick(discord.Client):
    def __init__(self):
        super().__init__()
        self.regex_sauce_image = re.compile(r'"(.*?)"')
        self.regex_sauce_video = re.compile(r"mp4")
        self.klient = kadal.Klient()
        print("start")

    async def on_ready(self):
        print('Logged as', maid.user.name, ",", maid.user.id)

    async def format_embed(self, sauce, type, message):
        if type == "manga":
            try:
                media = await self.klient.search_manga(sauce.title, popularity=True)
                desc = "Likely **" + \
                    str(sauce.similiar) + f"%**\n\n***" + \
                    ", ".join(media.genres) + "***\n"
                if media.description is not None:
                    desc += media.description[:256 - len(
                        desc)] + f"... [(more)]({media.site_url})\n\nAnother Results \n"
                    desc = desc.replace("<br>", "").replace(
                        "<i>", "").replace("</i>", "")
                else:
                    desc += "\nAnother Results \n"
            except kadal.MediaNotFound:
                desc = "Likely **" + str(sauce.similiar) + \
                    f"%**\n\nAnother Results \n"

        if type == "anime":
            try:
                media = await self.klient.search_anime(sauce.title, popularity=True)
                desc = "Likely **" + \
                    str(sauce.similiar) + f"%**\n\n***" + \
                    ", ".join(media.genres) + "***\n"
                if media.description is not None:
                    desc += media.description[:256 - len(
                        desc)] + f"... [(more)]({media.site_url})\n\nAnother Results: \n"
                    desc = desc.replace("<br>", "").replace(
                        "<i>", "").replace("</i>", "")
                else:
                    desc += "\nAnother Results: \n"
            except kadal.MediaNotFound:
                desc = "Likely **" + str(sauce.similiar) + \
                    f"%**\n\nAnother Results: \n"
        for another in islice(sauce.another, 0, 5):
            try:
                desc += f"** • [{another.title[:256 - len(another.title)]} ...]({another.url})**\n"
            except:
                pass
            try:
                desc += f"** • [{another.title[:256 - len(another.title)]} ...]({another.thumbnail})**\n"
            except:
                pass
            try:
                desc += f"** • [{another.titles[0][:256 - len(another.titles)]} ...]({another.urls[0]})**\n"
            except:
                pass
        req = Request(sauce.thumbnail, headers={'User-Agent': 'Mozilla/5.0'})
        fd = urlopen(req)
        f = io.BytesIO(fd.read())
        color_thief = ColorThief(f)
        e = discord.Embed(title=sauce.title, description=desc,
                          color=discord.Color.from_rgb(color_thief.get_color(quality=1)[0], color_thief.get_color(quality=1)[1], color_thief.get_color(quality=1)[2]))
        e.set_image(url=sauce.thumbnail)
        try:
            e.url = sauce.url
        except:
            e.url = f"https:{sauce.url}"
        e.set_footer(icon_url=message.author.avatar_url,
                     text=f"Requesed by {message.author.name} | {sauce.frm}")
        return e

    async def on_message(self, message):
        if message.author == self.user:
            return
        m = self.regex_sauce_image.findall(message.clean_content)
        m_clean = list(filter(bool, m))
        if m_clean:
            vid = self.regex_sauce_video.findall(m_clean[0])
            if vid:
                embedwait = self.wait_please(message)
                temp = await message.channel.send(embed=embedwait)
                sauce = saucer.sauce(m_clean[0], type="anime")
                embed = await self.format_embed(sauce, type="anime", message=message)
                await temp.delete()
                await message.channel.send(m_clean[0])
                await message.channel.send(embed=embed)
                await message.channel.send(sauce.url)
            else:
                embedwait = self.wait_please(message)
                temp = await message.channel.send(embed=embedwait)
                sauce = saucer.sauce(m_clean[0], type="image")
                embed = await self.format_embed(sauce, type="manga", message=message)
                await temp.delete()
                await message.channel.send(m_clean[0])
                await message.channel.send(embed=embed)

    def wait_please(self, message):
        des = ["nice cock bruh",
               "are you horny ?",
               "just another degenerate weeb doing the stuff",
               "Peter Piper picked a peck of pickled peppers\nA peck of pickled peppers Peter Piper picked\nIf Peter Piper picked a peck of pickled peppers\nWhere’s the peck of pickled peppers Peter Piper picked?",
               "Hi cunt",
               "The coconut nut is a giant nut If you eat too much\n you'll get very fat Now\n the coconut nut is a big-big nut But it's delicious nut is not a nut It's the coco fruit (it's the coco fruit) Of the coco tree (of the coco tree) From the coco palm family"]
        a = discord.Embed(title="Looking for the sauce ...", description=random.choice(
            des), color=discord.Color.from_rgb(255, 201, 107))
        a.set_footer(icon_url=message.author.avatar_url,
                     text=f"Requested by {message.author.name}")
        a.set_thumbnail(url="https://i.imgur.com/GE8uaS4.gif")
        return a


maid = MaidOurdick()
f = open("TOKEN")
token = f.readline()
maid.run(token)
