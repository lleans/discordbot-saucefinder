import discord
import os
import io
import saucer
import re
import kadal

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

    async def format_embed(self, sauce, type):
        if type == "manga":
            try:
                media = await self.klient.search_manga(sauce.title, popularity=True)
                desc = "Likely **" + \
                    str(sauce.similiar) + f"%**\n\n***" + \
                    ", ".join(media.genres) + "***\n"
                if media.description is not None:
                    desc += media.description[:256 - len(
                        desc)] + f"... [more]({media.site_url})\n\nAnother Results \n"
                    desc = desc.replace("<br>", "").replace(
                        "<i>", "").replace("</i>", "")
                else:
                    desc += "\n\nAnother Results \n"
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
                        desc)] + f"... [more]({media.site_url})\n\nAnother Results: \n"
                    desc = desc.replace("<br>", "").replace(
                        "<i>", "").replace("</i>", "")
                else:
                    desc += "\n\nAnother Results: \n"
            except kadal.MediaNotFound:
                desc = "Likely **" + str(sauce.similiar) + \
                    f"%**\n\nAnother Results: \n"
        for another in islice(sauce.another, 0, 5):
            try:
                desc += f"** • [{another.title[:240 - len(another.title)]}...]({another.url})**\n"
            except:
                pass
            try:
                desc += f"** • [{another.title[:240 - len(another.title)]}...]({another.thumbnail})**\n"
            except:
                pass
            try:
                desc += f"** • [{another.titles[:240 - len(another.titles)]}...]({another.urls})**\n"
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
        except IndexError:
            pass
        e.set_footer(text=f"Source from {sauce.frm}")
        return e

    async def on_message(self, message):
        if message.author == self.user:
            return
        m = self.regex_sauce_image.findall(message.clean_content)
        m_clean = list(filter(bool, m))
        if m_clean:
            vid = self.regex_sauce_video.findall(m_clean[0])    
            if vid:
                embedwait = await self.wait_please()
                temp = await message.channel.send(embed=embedwait)
                sauce = saucer.sauce(m_clean[0], type="anime")
                embed = await self.format_embed(sauce, type="anime")
                await temp.delete()
                await message.channel.send(m_clean[0])
                await message.channel.send(embed=embed)
                await message.channel.send(sauce.url)
            else:
                embedwait = await self.wait_please()
                temp = await message.channel.send(embed=embedwait)
                sauce = saucer.sauce(m_clean[0], type="image")
                embed = await self.format_embed(sauce, type="manga")
                await temp.delete()
                await message.channel.send(m_clean[0])
                await message.channel.send(embed=embed)

    async def wait_please(self):
        a = discord.Embed(title="Searching the sauce ...", description="Wait a second plzz", color=discord.Color.from_rgb(255, 201, 107))
        a.set_image(url="https://i.imgur.com/GE8uaS4.gif")
        return a

maid = MaidOurdick()
f = open("TOKEN")
token = f.readline()
maid.run(token)