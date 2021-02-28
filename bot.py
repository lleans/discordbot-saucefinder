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


class MaidOurdick(discord.Client):
    def __init__(self):
        super().__init__()
        self.regex_sauce_image = re.compile(r'"(.*?)"')
        self.regex_sauce_video = re.compile(
            r'(.*avi)|(.*m4v)|(.*mpeg)|(.*mpg)|(.*webm)|(.*mp4)|<(.*?)>')
        self.klient = kadal.Klient()
        self.anilist_cover_url = "https://img.anili.st/media/"
        self. random_color = ["ffd663", "ff7363",
                              "2f3136", "ff63c8", "ff636d", "faf67a"]
        print("start")

    async def on_ready(self):
        print('Logged as', maid.user.name, ",", maid.user.id)

    async def format_embed(self, sauce, type, message, thumbnail):
        anilist = None
        if type == "manga":
            try:
                media = await self.klient.search_manga(sauce.title, popularity=True, allow_adult=True)
                thumbnail_anilist = f"{self.anilist_cover_url}{media.id}"
                hex_color = media.cover_color or random.choice(
                    self.random_color)
                color_embed = int(hex_color.lstrip('#'), 16)
                desc = "Likely **" + \
                    str(sauce.similiar) + f"%**\n\n***" + \
                    ", ".join(media.genres) + "***\n"
                if media.description is not None:
                    anilist = True
                    desc += media.description[:256 - len(
                        desc)] + f"... [(more)]({media.site_url})\n\nAnother Results: \n"
                    desc = desc.replace("<br>", "").replace(
                        "<i>", "").replace("</i>", "")
                else:
                    desc += "\nAnother Results: \n"
            except:
                desc = "Likely **" + str(sauce.similiar) + \
                    f" %**\n\nAnother Results: \n"

        if type == "anime":
            try:
                media = await self.klient.search_anime(sauce.title, popularity=True, allow_adult=True)
                thumbnail_anilist = f"{self.anilist_cover_url}{media.id}"
                hex_color = media.cover_color or random.choice(
                    self.random_color)
                color_embed = int(hex_color.lstrip('#'), 16)
                desc = "Likely **" + \
                    str(sauce.similiar) + f"%**\n\n***" + \
                    ", ".join(media.genres) + "***\n"
                if media.description is not None:
                    anilist = True
                    desc += media.description[:256 - len(
                        desc)] + f"... [(more)]({media.site_url})\n\nAnother Results: \n"
                    desc = desc.replace("<br>", "").replace(
                        "<i>", "").replace("</i>", "")
                else:
                    desc += "\nAnother Results: \n"
            except:
                desc = "Likely **" + str(sauce.similiar) + \
                    f" %**\n\nAnother Results: \n"
        for x in range(4):
            try:
                desc += f"** • [{sauce.another_titles[x][:150 - len(sauce.another_titles[x])]}...]({sauce.another_urls[x]})**\n"
            except:
                continue
        if anilist:
            e = discord.Embed(title=sauce.title, description=desc,
                              color=color_embed)
            e.set_image(url=thumbnail_anilist)
            footer = f"{sauce.source}  •  {message.created_at.strftime('%x')}"
        else:
            try:
                req = Request(sauce.thumbnail, headers={
                    'User-Agent': 'Mozilla/5.0'})
                f = io.BytesIO(urlopen(req).read())
                color_thief = ColorThief(f)
                e = discord.Embed(title=sauce.title, description=desc,
                                color=discord.Color.from_rgb(color_thief.get_color(quality=1)[0], color_thief.get_color(quality=1)[1], color_thief.get_color(quality=1)[2]))
                e.set_image(url=sauce.thumbnail)
                footer = f"{sauce.source}  •  {message.created_at.strftime('%x')}"
            except:
                if sauce.thumbnail[:4] == 'http':
                    desc += f"\nLooks like the image doesn't show up, [click here]({sauce.thumbnail}) to open it"
                else:
                    desc += "\nLooks like the image doesn't show up, try click one of the results to open it"
                e = discord.Embed(title=sauce.title, description=desc,
                                color=int(random.choice(self.random_color).lstrip('#'), 16))
                e.set_image(url="https://i.imgur.com/1CzcRfk.gif")
                footer = f"{sauce.source}  •  {message.created_at.strftime('%x')} | Image not found 404"
        e.url = sauce.url
        e.set_thumbnail(url=thumbnail)
        e.set_footer(icon_url=message.author.avatar_url,
                     text=footer)
        return e

    async def on_message(self, message):
        if message.author == self.user:
            return
        m = self.regex_sauce_image.findall(message.clean_content)
        m_clean = list(filter(bool, m))
        if m_clean:
            ver = m_clean[0]
            if re.findall('http', ver):
                vid = self.regex_sauce_video.findall(m_clean[0])
                embedwait = self.wait_please(message)
                if vid:
                    try:
                        temp = await message.channel.send(embed=embedwait)
                        sauce = saucer.Sauce(m_clean[0], type="anime")
                        embed = await self.format_embed(sauce, type="anime", message=message, thumbnail=sauce.thumbnail)
                        await temp.delete()
                        await message.channel.send(m_clean[0])
                        await message.channel.send(embed=embed)
                        await message.channel.send(sauce.url)
                    except Exception as catch:
                        await temp.delete()
                        traceback.print_exc()
                        error = self.error(message, catch)
                        await message.channel.send(embed=error)
                else:
                    try:
                        temp = await message.channel.send(embed=embedwait)
                        sauce = saucer.Sauce(m_clean[0], type="image")
                        embed = await self.format_embed(sauce, type="manga", message=message, thumbnail=m_clean[0])
                        await temp.delete()
                        await message.channel.send(embed=embed)
                    except Exception as catch:
                        await temp.delete()
                        traceback.print_exc()
                        error = self.error(message, catch)
                        await message.channel.send(embed=error)

    def wait_please(self, message):
        des = ["nice cock bruh",
               "are you horny ?",
               "just another degenerate weeb doing the stuff",
               "Peter Piper picked a peck of pickled peppers\nA peck of pickled peppers Peter Piper picked\nIf Peter Piper picked a peck of pickled peppers\nWhere’s the peck of pickled peppers Peter Piper picked?",
               "Hi cunt",
               "The coconut nut is a giant nut\nIf you eat too much you'll get very fat\nNow the coconut nut is a big-big nut\nBut it's delicious nut is not a nut\nIt's the coco fruit (it's the coco fruit)\nOf the coco tree (of the coco tree)\nFrom the coco palm family"]
        a = discord.Embed(title="Looking for the sauce ...", description=random.choice(
            des), color=discord.Color.from_rgb(255, 201, 107))
        a.set_footer(icon_url=message.author.avatar_url,
                     text=f"Requested by {message.author.name} | {message.created_at.strftime('%x')}")
        a.set_thumbnail(url="https://i.imgur.com/GE8uaS4.gif")
        return a

    def error(self, message, eror):
        des = "Looks like, there is something went wrong in the backend, maybe API down or anything else, or even god doesn't like it\n\n**What should i do ?**\nYou can use these website to reverse image manually\n "
        a = discord.Embed(title="Whoopsss.....", description=des,
                          color=discord.Color.from_rgb(255, 96, 56))
        a.add_field(name="Multi Service",
                    value=f"[Iqdb]({'https://iqdb.org/'})\n[ImgOps]({'https://imgops.com/'})", inline=True)
        a.add_field(name="Manga, anime & art",
                    value=f"[SauceNao]({'https://saucenao.com/'})\n[Ascii2D]({'https://ascii2d.net/'})\n[TraceMoe]({'https://trace.moe/'})", inline=True)
        a.add_field(
            name="Everything", value=f"[Google Images]({'https://images.google.com/'})\n[TinEye]({'https://tineye.com/'})\n[Yandex]({'https://yandex.com/images/'})", inline=True)
        a.set_footer(icon_url=message.author.avatar_url,
                     text=f"{eror.args[0]} | {message.created_at.strftime('%x')}")
        a.set_thumbnail(url="https://i.imgur.com/foNFxKu.gif")
        return a


maid = MaidOurdick()
f = open("TOKEN")
token = f.readline()
maid.run(token)
