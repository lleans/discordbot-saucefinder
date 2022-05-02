import traceback

from io import BytesIO
from random import choice
from os import environ, remove as rm
from re import compile, search, sub, IGNORECASE

from discord import Client, Embed, Activity, ActivityType, File
from urllib.request import urlopen, Request
from colorthief import ColorThief
from kadal import Klient
from saucer import Sauce


class MaidHayasaka(Client):

    RANDOM_EXPRESSION = [
        "nice cock bruh",
        "are you horny ?",
        "just another degenerate weeb doing the stuff",
        "Peter Piper picked a peck of pickled peppers\nA peck of pickled peppers Peter Piper picked\nIf Peter Piper picked a peck of pickled peppers\nWhere’s the peck of pickled peppers Peter Piper picked?",
        "Hi cunt",
        "The coconut nut is a giant nut\nIf you eat too much you'll get very fat\nNow the coconut nut is a big-big nut\nBut it's delicious nut is not a nut\nIt's the coco fruit (it's the coco fruit)\nOf the coco tree (of the coco tree)\nFrom the coco palm family"]
    HAYASAKA_COLOR = {
        "accent":  "ffe063",
        "random": ["ff5c5c", "ffae5c", "ffd45c", "ff5c6c", "ff5c5c", "5cb3ff"],
        "error": "ff6038",
        "wait": "ffc96b"
    }
    HAYASAKA_THUMBNAIL = {
        "help": "https://i.imgur.com/38MpUXM.gif",
        "error": "https://i.imgur.com/foNFxKu.gif",
        "wait": "https://i.imgur.com/GE8uaS4.gif",
        "img_not_found": "https://i.imgur.com/1CzcRfk.gif"
    }

    def __init__(self):
        super().__init__()

        self.regex_command = {
            "image": compile(r'"(.*?)"'),
            "video": compile(r',(.*?),')
        }
        self.video = compile(
            r'(.*avi)|(.*m4v)|(.*mpeg)|(.*mpg)|(.*webm)|(.*mp4)')
        self.image = compile(
            r'(.*png)|(.*jpg)|(.*jpeg)|(.*webp)|(.*bmp)|(.*tiff)|(.*gif)')

        self.kadal = Klient()
        self.sauce = Sauce()
        print("start")

    @staticmethod
    def _help(message):
        e = Embed(
            title="Help Commands",
            description="So this is my first time with you\nso please be gentle with me....\n\n\n**Anyway here the command list**",
            color=int(MaidHayasaka.HAYASAKA_COLOR['accent'].lstrip('#'), 16)
        ).set_thumbnail(url=MaidHayasaka.HAYASAKA_THUMBNAIL['help']
                        ).add_field(
            name="Basic Command",
            value='If you find a picture or video, just right click and click copy link, then enter it like the command above\n\ne.g `"https: //i.imgur.com/1Czc ..."`'
        ).add_field(
            name="Override Command",
            value='For this case, when you found some anime screenshot or gif anything that you think it is anime, you can use this command to search for it\n\ne.g `,https: //i.imgur.com/F7ed ...,`'
        ).set_author(
            name=maid.user.name,
            icon_url=maid.user.avatar_url
        ).set_footer(text=f"© {maid.user.name} | {message.created_at.strftime('%x')}")
        return e

    @staticmethod
    def _error(message, error):
        e = Embed(
            title="404 not found..." if Exception(
                "Source not found") else "Whoopsss...",
            description="Looks like i couldn't find the sauce, maybe god doesn't like it\n\n**What should i do ?**\nYou can use these website to reverse image manually\n" if Exception(
                "Source not found") else "Looks like the source is down, maybe god doesn't like it\n\n**What should i do ?**\nYou can use these website to reverse image manually\n",
            color=int(MaidHayasaka.HAYASAKA_COLOR['error'].lstrip('#'), 16)
        ).set_thumbnail(url=MaidHayasaka.HAYASAKA_THUMBNAIL['error']
                        ).add_field(
            name='Multi Service',
            value=f"[Iqdb]({'https://iqdb.org/'})\n[ImgOps]({'https://imgops.com/'})"
        ).add_field(
            name='Manga, anime & art',
            value=f"[SauceNao]({'https://saucenao.com/'})\n[Ascii2D]({'https://ascii2d.net/'})\n[TraceMoe]({'https://trace.moe/'})\n[E-Hentai]({'https://e-hentai.org/?f_shash=nofile&fs_from='})"
        ).add_field(
            name='Everything',
            value=f"[Google Images]({'https://images.google.com/'})\n[TinEye]({'https://tineye.com/'})\n[Yandex]({'https://yandex.com/images/'})\n[Baidu]({'https://image.baidu.com/'})"
        ).set_author(
            name=maid.user.name,
            icon_url=maid.user.avatar_url
        ).set_footer(text=f"© {maid.user.name} | {message.created_at.strftime('%x')} | {error}")
        return e

    @staticmethod
    def _wait(message):
        e = Embed(
            title="Looking for the sauce...",
            description=f"{choice(MaidHayasaka.RANDOM_EXPRESSION)}\n\n**It may takes a while to complete because a lot of request**",
            color=int(MaidHayasaka.HAYASAKA_COLOR['wait'].lstrip('#'), 16)
        ).set_thumbnail(url=MaidHayasaka.HAYASAKA_THUMBNAIL['wait']
                        ).set_author(
            name=maid.user.name,
            icon_url=maid.user.avatar_url
        ).set_footer(text=f"© {maid.user.name} | {message.created_at.strftime('%x')}")
        return e

    async def format_embed(self, sauce, *, type, message, original, isVideo):
        anilist = False
        footer = f"© {maid.user.name} | {message.created_at.strftime('%x')}"

        try:
            media = await type(sauce['title'], popularity=True, allow_adult=True)
            if media.description is not None and not search(r"ascii2d|iqdb|baidu", sauce['source'][0], flags=IGNORECASE):
                anilist = True
                thumbnail_anilist = f"https://img.anili.st/media/{media.id}"
                hex_color = media.cover_color or choice(
                    self.HAYASAKA_COLOR['random'])
                desc = f"Likely **{sauce['similar']}%**\n\n***{', '.join(media.genres)}***\n"
                anilist_desc = sub(r"<br>|</br>|<b>|</b>|<i>|</i>",
                                   "", media.description, flags=IGNORECASE)
                desc += anilist_desc[:256 - len(
                    desc)] + f"... [(more)]({media.site_url})\n\nAnother Results: \n"
            else:
                desc = f"Likely **{sauce['similar']}%**\n\nAnother Results: \n"
        except:
            desc = f"Likely **{sauce['similar']}%**\n\nAnother Results: \n"

        if not sauce['another_titles']:
            desc += "**Unfortunately there is no other results**\n"
        else:
            for x in range(3):
                try:
                    desc += f"** • [{sauce['another_titles'][x][:150 - len(sauce['another_titles'][x])]}...]({sauce['another_urls'][x]})**\n"
                except:
                    continue

        if anilist:
            e = Embed(title=sauce['title'],
                      description=desc, color=int(hex_color.lstrip('#'), 16))
            e.set_image(url=thumbnail_anilist)
        else:
            try:
                req = Request(sauce['thumbnail'], headers={
                              'User-Agent': 'Mozilla/5.0'})
                f = BytesIO(urlopen(req).read())
                e = Embed(title=sauce['title'], description=desc, color=int(
                    ('%02x%02x%02x' % ColorThief(f).get_color(quality=1)).lstrip('#'), 16))
                e.set_image(url=sauce['thumbnail'])
            except:
                e = Embed(title=sauce['title'], description=desc, color=int(
                    choice(self.HAYASAKA_COLOR['random']).lstrip('#'), 16))

                if sauce['thumbnail'].startswith('http'):
                    desc += f"\nLooks like the image doesn't show up, [click here]({sauce['thumbnail']}) to open it"
                else:
                    desc += "\nLooks like there is no thumbnail for this, try click one of the results to open it"
                e.set_image(url=self.HAYASAKA_THUMBNAIL['img_not_found'])
                footer += " | Image not found 404"
        e.url = sauce['url']
        if isVideo:
            e.set_thumbnail(url="attachment://image.png")
        else:
            e.set_thumbnail(url=original)
        e.set_author(name=sauce['source'][0], icon_url=sauce['source'][1])
        e.set_footer(icon_url=message.author.avatar_url, text=footer)
        return e

    async def search(self, url, message, video):
        temp = await message.channel.send(embed=self._wait(message))
        isVideo = self.video.search(url)
        isImage = self.image.search(url)
        try:
            if video or isVideo:
                sauce = await self.sauce.sauce_anime(url=url, isVideo=isVideo)
                embed = await self.format_embed(sauce, type=self.kadal.search_anime, message=message, original=url, isVideo=isVideo)
                await temp.delete()
                if isVideo:
                    image_file = File(sauce['thumbnail'], filename='image.png')
                    await message.channel.send(file=image_file, embed=embed)
                    rm(sauce['thumbnail'])
                else:
                    await message.channel.send(embed=embed)
                await message.channel.send(sauce['url'])
            elif isImage and not (video or isVideo):
                sauce = await self.sauce.sauce_image(url=url)
                embed = await self.format_embed(sauce, type=self.kadal.search_manga, message=message, original=url, isVideo=isVideo)
                await temp.delete()
                await message.channel.send(embed=embed)
            else:
                await temp.delete()
                await message.channel.send(embed=self._error(message, Exception("Image or Video format not supported !")))
        except Exception as catch:
            await temp.delete()
            traceback.print_exc()
            await message.channel.send(embed=self._error(message, catch))

    async def filter(self, message, regex, method):
        m = regex.findall(message.clean_content)
        m_clean = list(filter(bool, m))
        if m_clean and len(m_clean) > 1:
            for url in m_clean:
                if url.startswith("http"):
                    await self.search(url, message, method)
        elif m_clean and m_clean[0].lower() in "help":
            await message.channel.send(embed=self._help(message))
        elif m_clean and m_clean[0].startswith("http"):
            await self.search(m_clean[0], message, method)

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return
        elif maid.user in message.mentions and message.clean_content == f"@{maid.user.name}":
            await message.channel.send(embed=self._help(message))

        for type, regex in self.regex_command.items():
            method = True if type == "video" else False
            await self.filter(message, regex, method)

    async def on_ready(self):
        print('Logged as', maid.user.name, ",", maid.user.id)
        await maid.change_presence(activity=Activity(type=ActivityType.listening, name=f"@{maid.user.name}"))


maid = MaidHayasaka()
token = environ.get('BOT_TOKEN') or open("BOT_TOKEN").readline()
maid.run(token)
