import re
import asyncio
import PicImageSearch


class Sauce:
    def __init__(self):
        super().__init__()
        self.client = PicImageSearch.Search()
        self.Googletask = None
        self.sNaotask = None
        self.A2dtask = None
        self.Iqtask = None
        self.Iq3dtask = None
        self.tMoetask = None

    
    async def saucer_sauceNao(self, name):
        b = open("API_sauceNao")
        self.sNaotask = await self.client.saucenao(url=name, api_key=b.readline())
        return 

    async def saucer_TraceMoe(self, name):
        self.tMoetask = await self.client.tracemoe(name)
        return 

    async def saucer_Ascii2D(self, name):
        self.A2dtask = await self.client.ascii2d(name)
        return

    async def saucer_Iqdb(self, name):
        self.Iqtask = await self.client.iqdb(name)
        return

    async def saucer_Iqdb3d(self, name):
        self.Iq3dtask = await self.client.iqdb_3d(name)
        return

    async def saucer_Google(self, name):
        self.Googletask = await self.client.google(name)
        return

    async def sauce_anime(self, name):
        await self.saucer_TraceMoe(name)
        tMoe = self.tMoetask.raw
        similiar = tMoe[0].similarity
        res = {
            'title': tMoe[0].title_english,
            'similiar': similiar,
            'source': ["https://i.imgur.com/aXJEPmD.png", "TraceMoe"],
            'thumbnail': tMoe[0].thumbnail,
            'url': tMoe[0].video_thumbnail,
            'another_titles': list(),
            'another_urls': list()
        }
        for x in range(1, len(tMoe)):
            try:
                res['another_titles'].append(tMoe[x].title)
                res['another_urls'].append(tMoe[x].video_thumbnail)
            except:
                continue
        return res

    async def sauce_image(self, name):
        # Request
        await asyncio.wait([self.saucer_Ascii2D(name), self.saucer_Google(name), self.saucer_Iqdb(name), self.saucer_Iqdb3d(name), self.saucer_sauceNao(name)])
        Google, sNao, A2d = self.Googletask.raw, self.sNaotask.raw, self.A2dtask.raw

        try:
            Iq = self.Iqtask.raw
            Iqsimilar = Iq[0].similarity
        except:
            Iqsimilar = float(0)

        try:
            Iq3d = self.Iq3dtask.raw
            Iq3dsimilar = Iq3d[0].similarity
        except:
            Iq3dsimilar = float(0)

        try:
            Googledata = Google[2].title
            if Google[2].thumbnail == "":
                Googledata = None
        except:
            Googledata = None

        sNaosimilar = sNao[0].similarity

        if sNaosimilar <= 80 and Iqsimilar <= 80 and Iq3dsimilar <= 80 and Googledata is not None:
            # Google
            res = {
                'title': Google[2].title,
                'thumbnail': Google[2].thumbnail,
                'similiar': None,
                'source': ["https://i.imgur.com/Z9OLjXS.png", "Google"],
                'url': Google[2].url,
                'another_titles': list(),
                'another_urls': list()
            }
            for x in range(3, len(Google)):
                try:
                    res['another_titles'].append(Google[x].title)
                    res['another_urls'].append(Google[x].url)
                except:
                    continue
            return res

        elif sNaosimilar <= 80 and Iqsimilar <= 80 and Iq3dsimilar <= 80 and Googledata is None:
            # Ascii2d
            res = {
                'title': A2d[1].title,
                'thumbnail': A2d[1].thumbnail,
                'similiar': None,
                'source': ["https://i.imgur.com/BA7hWTm.png", "Ascii2d"],
                'url': A2d[1].url,
                'another_titles': list(),
                'another_urls': list()
            }
            for x in range(2, len(A2d)):
                try:
                    res['another_titles'].append(A2d[x].title)
                    res['another_urls'].append(A2d[x].url)
                except:
                    continue
            return res

        elif sNaosimilar >= Iqsimilar and sNaosimilar >= Iq3dsimilar:
            # SauceNao
            res = {
                'title': sNao[0].title,
                'thumbnail': sNao[0].thumbnail,
                'similiar': sNaosimilar,
                'source': ["https://i.imgur.com/FhsgOiv.png", "SauceNao"],
                'url': sNao[0].url,
                'another_titles': list(),
                'another_urls': list()
            }
            for x in range(1, len(sNao)):
                try:
                    res['another_titles'].append(sNao[x].title)
                    res['another_urls'].append(sNao[x].url)
                except:
                    continue
            return res

        elif Iqsimilar >= sNaosimilar and Iqsimilar >= Iq3dsimilar:
            # Iqdb
            res = {
                'title': Iq[0].title[:180 - len(Iq[0].title)] + "...",
                'thumbnail': Iq[0].thumbnail,
                'similiar': Iqsimilar,
                'source': ["https://i.imgur.com/r3kJwPF.png", "Iqdb"],
                'url': Iq[0].url,
                'another_titles': list(),
                'another_urls': list()
            }
            for x in range(1, len(Iq)):
                try:
                    res['another_titles'].append(
                        Iq[x].title[:180 - len(Iq[0].title)] + "...")
                    res['another_urls'].append(Iq[x].url)
                except:
                    continue
            return res

        elif Iq3dsimilar >= sNaosimilar and Iq3dsimilar >= Iqsimilar:
            # Iqdb 3D
            res = {
                'title': Iq3d[0].title[:180 - len(Iq3d[0].title)] + "...",
                'thumbnail': Iq3d[0].thumbnail,
                'similiar': Iq3dsimilar,
                'source': ["https://i.imgur.com/r3kJwPF.png", "Iqdb 3D"],
                'url': Iq3d[0].url,
                'another_titles': list(),
                'another_urls': list()
            }
            for x in range(1, len(Iq3d)):
                try:
                    res['another_titles'].append(
                        Iq3d[x].title[:180 - len(Iq3d[0].title)] + "...")
                    res['another_urls'].append(Iq3d[x].url)
                except:
                    continue
            return res
