import re
import asyncio
from PicImageSearch import SauceNAO, TraceMoe, Ascii2D, Iqdb, Google


class Sauce:
    def __init__(self):
        super().__init__()

    @staticmethod
    def arrange_data(data, similiar, source):
        res = {
            'similiar': similiar,
            'source': source,
            'another_titles': list(),
            'another_urls': list()
        }
        if source[1] == "TraceMoe":
            res.update({
                'title': data[0].title_english,
                'thumbnail': data[0].thumbnail,
                'url': data[0].video_thumbnail
            })
            for x in range(1, len(data)):
                try:
                    res['another_titles'].append(data[x].title)
                    res['another_urls'].append(data[x].video_thumbnail)
                except:
                    continue
        elif source[1] == "Google":
            res.update({
                'title': data[2].titles[0],
                'thumbnail': data[2].thumbnail[0],
                'url': data[2].urls[0]
            })
            for x in range(3, len(data)):
                try:
                    res['another_titles'].append(data[x].titles[0])
                    res['another_urls'].append(data[x].urls[0])
                except:
                    continue
        elif source[1] == "Ascii2d":
            res.update({
                'title': data[1].titles[0],
                'thumbnail': data[1].thumbnail[0],
                'url': data[1].urls[0]
            })
            for x in range(2, len(data)):
                try:
                    res['another_titles'].append(data[x].titles[0])
                    res['another_urls'].append(data[x].urls[0])
                except:
                    continue
        elif source[1] == "SauceNao":
            res.update({
                'title': data[0].title,
                'thumbnail': data[0].thumbnail,
                'url': data[0].url
            })
            for x in range(1, len(data)):
                try:
                    res['another_titles'].append(data[x].title)
                    res['another_urls'].append(data[x].url)
                except:
                    continue
        elif source[1] == "Iqdb" or source[1] == "Iqdb 3D":
            res.update({
                'title': data[0].title[:180 - len(data[0].title)] + "...",
                'thumbnail': data[0].thumbnail,
                'url': data[0].url if data[0].url[:4] == "http" else f"https:{data[0].url}"
            })
            for x in range(1, len(data)):
                try:
                    res['another_titles'].append(
                        data[x].title[:180 - len(data[0].title)] + "...")
                    res['another_urls'].append(
                        data[x].url if data[0].url[:4] == "http" else f"https:{data[0].url}")
                except:
                    continue
        
        return res

    @staticmethod
    async def saucer_sauceNao(name):
        b = open("API_sauceNao")
        saucer = SauceNAO(b.readline())
        sauce = saucer.search(name)
        return sauce

    @staticmethod
    async def saucer_TraceMoe(name):
        saucer = TraceMoe()
        sauce = saucer.search(name)
        return sauce

    @staticmethod
    async def saucer_Ascii2D(name):
        saucer = Ascii2D()
        sauce = saucer.search(name)
        return sauce

    @staticmethod
    async def saucer_Iqdb(name):
        saucer = Iqdb()
        try:
            sauce = saucer.search(name)
            return sauce
        except:
            return None

    @staticmethod
    async def saucer_Iqdb3d(name):
        saucer = Iqdb()
        try:
            sauce = saucer.search_3d(name)
            return sauce
        except:
            return None

    @staticmethod
    async def saucer_Google(name):
        saucer = Google()
        sauce = saucer.search(name)
        return sauce

    async def sauce_anime(self, name):
        tMoetask = await asyncio.create_task(self.saucer_TraceMoe(name))
        tMoe = tMoetask.raw
        similiar = float("{:.2f}".format(tMoe[0].similarity * 100))

        return self.arrange_data(
            tMoe, similiar, ["https://i.imgur.com/aXJEPmD.png", "TraceMoe"])

    async def sauce_image(self, name):
        REGEXIQ = re.compile("[0-9]+")
        # Request
        Googletask, sNaotask, A2dtask, Iqtask, Iq3dtask = await asyncio.gather(self.saucer_Google(name), self.saucer_sauceNao(name), self.saucer_Ascii2D(name), self.saucer_Iqdb(name), self.saucer_Iqdb3d(name))
        Google, sNao, A2d = Googletask.raw, sNaotask.raw, A2dtask.raw

        try:
            Iq = Iqtask.raw
            Iqs = REGEXIQ.search(Iq[0].similarity)
            Iqsimilar = float(Iqs.group(0))
        except:
            Iqsimilar = float(0)

        try:
            Iq3d = Iq3dtask.raw
            Iq3D = REGEXIQ.search(Iq3d[0].similarity)
            Iq3dsimilar = float(Iq3D.group(0))
        except:
            Iq3dsimilar = float(0)

        try:
            Googledata = Google[2].titles[0]
            self.thumbnail = Google[2].thumbnail[0]
        except IndexError:
            Googledata = None

        sNaosimilar = float(sNao[0].similarity)

        if sNaosimilar <= 80 and Iqsimilar <= 80 and Iq3dsimilar <= 80 and Googledata is not None:
            # Google
            return self.arrange_data(
                Google, None, ["https://i.imgur.com/Z9OLjXS.png", "Google"])

        elif sNaosimilar <= 80 and Iqsimilar <= 80 and Iq3dsimilar <= 80 and Googledata is None:
            # Ascii2d
            return self.arrange_data(
                A2d, None, ["https://i.imgur.com/BA7hWTm.png", "Ascii2d"])

        elif sNaosimilar >= Iqsimilar and sNaosimilar >= Iq3dsimilar:
            # SauceNao
            return self.arrange_data(sNao, sNaosimilar, [
                              "https://i.imgur.com/FhsgOiv.png", "SauceNao"])

        elif Iqsimilar >= sNaosimilar and Iqsimilar >= Iq3dsimilar:
            # Iqdb
            return self.arrange_data(
                Iq, Iqsimilar, ["https://i.imgur.com/r3kJwPF.png", "Iqdb"])

        elif Iq3dsimilar >= sNaosimilar and Iq3dsimilar >= Iqsimilar:
            # Iqdb 3D
            return self.arrange_data(Iq3d, Iq3dsimilar, [
                              "https://i.imgur.com/r3kJwPF.png" "Iqdb 3D"])
