import re
import asyncio
import PicImageSearch


class Sauce:
    def __init__(self):
        super().__init__()
        self.client = PicImageSearch.Search()

    async def sauce_anime(self, name):
        async with asyncio.Semaphore(4):
            tMoetask = await self.client.tracemoe(url=name)
            try:
                tMoe = tMoetask.raw
            except:
                raise Exception("Source TraceMoe Down")
            similiar = tMoe[0].similarity
            res = {
                'title': tMoe[0].title_english or tMoe[0].title,
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
        async with asyncio.Semaphore(4):
            Googletask, sNaotask, A2dtask, Iqtask, Iq3dtask = await asyncio.gather(self.client.google(url=name), self.client.saucenao(url=name, api_key=open("API_sauceNao").readline()), self.client.ascii2d(url=name), self.client.iqdb(url=name), self.client.iqdb_3d(url=name))

            try:
                A2d = A2dtask.raw
                A2ddata = True
            except:
                A2ddata = None

            try:
                Iq = Iqtask.raw
                Iqsimilar = Iq[0].similarity
            except:
                Iqsimilar = float(0)

            try:
                Iq3d = Iq3dtask.raw
                Iq3dsimilar = Iq3d[0].similarity
            except:
                Iq3dsimilar = float(0)

            try:
                Google = Googletask.raw
                if Google[2].thumbnail == "" or  Google[2].title == "Description" or Google[2].title == "Description":
                    Googledata = None
                else:
                    Googledata = True
            except:
                Googledata = None

            try:
                sNao = sNaotask.raw
                sNaosimilar = sNao[0].similarity
            except:
                sNaosimilar = float(0)
            
            if sNaosimilar <= 80 and Iqsimilar <= 80 and Iq3dsimilar <= 80 and Googledata:
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

            elif sNaosimilar <= 80 and Iqsimilar <= 80 and Iq3dsimilar <= 80 and Googledata == None and A2ddata == True:
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

            elif sNaosimilar >= Iqsimilar and sNaosimilar >= Iq3dsimilar and sNaosimilar >= 80:
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
            elif Iq3dsimilar == 0.0 and Iqsimilar == 0.0 and sNaosimilar == 0.0 and A2ddata is None and Googledata is None:
                raise Exception("All source down")
            else:
                raise Exception("Source not found")