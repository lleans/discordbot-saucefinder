import discord
import os
import saucer
import re
import kadal

class MaidOurdick(discord.Client):
    def __init__(self):
        super().__init__()
        self.regex = re.compile(r'"(.*?)"')
        self.klient = kadal.Klient()
        print("start")

    async def on_ready(self):
        print('Logged as', maid.user.name, ",", maid.user.id)

    async def format_embed(self, sauce):
        try:
            media = await self.klient.search_manga(sauce[0].title, popularity=True)
            desc = "Likely **" + str(sauce[0].similarity) + f"%**\n\n***" + ", ".join(media.genres) + "***\n"
            if media.description is not None:
                desc += media.description[:256 - len(desc)] + f"... [(more)]({media.site_url})\n\nAnother Results \n"
                desc = desc.replace("<br>", "").replace("<i>", "").replace("</i>", "")
            else:
                desc += "\n\nAnother Results \n"
        except kadal.MediaNotFound:
            desc = "Likely **" + str(sauce[0].similarity) + f"%**\n\nAnother Results \n"
        for another in sauce:
            data = another.title
            desc += f"**{data}**\n"
        footer = "If the search result is below 50% then do a manual search"
        e = discord.Embed(title=sauce[0].title, description=desc, color=discord.Color.random())
        e.set_image(url=sauce[0].thumbnail)
        e.url = sauce[0].urls[0]
        e.set_footer(text=footer)
        return e

    async def on_message(self, message):
        if message.author == self.user:  # Ignore own messages
            return
        m = self.regex.findall(message.clean_content)
        m_clean = list(filter(bool, m))
        if m_clean:
            sauce = saucer.saucer_sauceNao(m_clean[0])
            await message.channel.send(m_clean[0])
            embed = await self.format_embed(sauce)
            await message.channel.send(embed=embed)


maid = MaidOurdick()
f = open("TOKEN")
token = f.readline()
maid.run(token)
