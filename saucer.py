from fileinput import close
import os
import ffmpeg
import asyncio
import PicImageSearch

class Sauce:
    def __init__(self):
        super().__init__()
        self.ascii2d = PicImageSearch.Ascii2D()
        self.baidu = PicImageSearch.BaiDu()
        self.ehentai = PicImageSearch.EHentai()
        self.google = PicImageSearch.Google()
        self.iqdb = PicImageSearch.Iqdb()
        self.saucenao = PicImageSearch.SauceNAO(os.environ.get('SAUCENAO_TOKEN') or open("SAUCENAO_TOKEN").readline())
        self.tracemoe = PicImageSearch.TraceMoe()

    @staticmethod
    async def image_exporter(url: str, name: str):
        proc = (
        ffmpeg
        .input(url, ss=0)
        .output(name, vframes=1)
        .overwrite_output()
        .run_async(quiet=True)
        )
        proc.wait()

    async def sauce_anime(self, name, isVideo: bool):
        async with asyncio.Semaphore(4):
            try:
                if(isVideo):
                    id: str = str(abs(hash(name)) % (10 ** 8)) + ".png"
                    await self.image_exporter(name, id)
                    tMoetask = await self.tracemoe.search(url=id)
                else:
                    tMoetask = await self.tracemoe.search(url=name)

                tMoe = tMoetask.raw
            except:
                raise Exception("Source TraceMoe Down")

            similiar = tMoe[0].similarity
            if(similiar >= 80):
                res = {
                    'title': tMoe[0].title_english or tMoe[0].title,
                    'similiar': similiar,
                    'source': ["https://i.imgur.com/aXJEPmD.png", "TraceMoe"],
                    'thumbnail': tMoe[0].image,
                    'url': tMoe[0].video,
                    'another_titles': list(),
                    'another_urls': list()
                }
                for x in range(1, len(tMoe)):
                    try:
                        res['another_titles'].append(tMoe[x].title_romaji or tMoe[x].title_native)
                        res['another_urls'].append(tMoe[x].video)
                    except:
                        continue
            else:
                raise Exception("Source not found")
            return res

    async def sauce_image(self, name):
        # Request
        async with asyncio.Semaphore(4):
            try:
                GoogleTask, sNaoTask, A2dTask, IqTask, Iq3dTask, EhentaiTask = await asyncio.gather(
                    self.google.search(url=name), 
                    self.saucenao.search(url=name), 
                    self.ascii2d.search(url=name), 
                    self.iqdb.search(url=name, ), 
                    self.iqdb.search(url=name, is_3d=True),
                    self.ehentai.search(url=name),
                    return_exceptions=True)
            except Exception as e:
                raise e
            
            try:
                A2d = A2dTask.raw
                A2ddata = True
            except:
                A2ddata = None

            try:
                Iq = IqTask.raw
                Iqsimilar = Iq[0].similarity
            except:
                Iqsimilar = float(0)

            try:
                Iq3d = Iq3dTask.raw
                Iq3dsimilar = Iq3d[0].similarity
            except:
                Iq3dsimilar = float(0)

            try:
                Google = GoogleTask.raw
                if Google[2].thumbnail == "" or "description" in Google[2].title.lower():
                    Googledata = None
                else:
                    Googledata = True
            except:
                Googledata = None

            try:
                sNao = sNaoTask.raw
                sNaosimilar = sNao[0].similarity
            except:
                sNaosimilar = float(0)

            try: 
                Ehen = EhentaiTask.raw
                Ehendata = True
            except: 
                Ehendata = False

            
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
                        if "description" in Google[2].title.lower():
                            continue
                        else:
                            res['another_titles'].append(Google[x].title) 
                        res['another_urls'].append(Google[x].url)
                    except:
                        continue
                return res

            elif sNaosimilar <= 80 and Iqsimilar <= 80 and Iq3dsimilar <= 80 and Googledata == None and A2ddata == False and Ehendata == True:
                # Ehentai
                res = {
                    'title': Ehen[0].title,
                    'thumbnail': Ehen[0].thumbnail,
                    'similiar': None,
                    'source': ["https://i.imgur.com/IXSFiax.png", "Ehentai"],
                    'url': Ehen[0].url,
                    'another_titles': list(),
                    'another_urls': list()
                }
                for x in range(1, len(Ehen)):
                    try:
                        res['another_titles'].append(Ehen[x].title)
                        res['another_urls'].append(Ehen[x].url)
                    except:
                        continue
                return res

            elif sNaosimilar <= 80 and Iqsimilar <= 80 and Iq3dsimilar <= 80 and Googledata == None and A2ddata == True and Ehendata == False:
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
                    'title': Iq[0].content[:180 - len(Iq[0].content)],
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
                            Iq[x].content[:180 - len(Iq[0].content)])
                        res['another_urls'].append(Iq[x].url)
                    except:
                        continue
                return res

            elif Iq3dsimilar >= sNaosimilar and Iq3dsimilar >= Iqsimilar:
                # Iqdb 3D
                res = {
                    'title': Iq3d[0].content[:180 - len(Iq3d[0].content)],
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
                            Iq3d[x].content[:180 - len(Iq3d[0].content)])
                        res['another_urls'].append(Iq3d[x].url)
                    except:
                        continue
                return res
            elif Iq3dsimilar == 0.0 and Iqsimilar == 0.0 and sNaosimilar == 0.0 and A2ddata is None and Googledata is None:
                raise Exception("All source down")
            else:
                raise Exception("Source not found")