import ffmpeg

from re import search
from random import choice
from os import environ, remove
from asyncio import gather, Semaphore
from PicImageSearch import Ascii2D, BaiDu, EHentai, Google, Iqdb, SauceNAO, TraceMoe


class Sauce:

    SOURCE_DICT = {
        'SauceNao': "https://i.imgur.com/FhsgOiv.png",
        'Google': "https://i.imgur.com/Z9OLjXS.png",
        'TraceMoe': "https://i.imgur.com/aXJEPmD.png",
        'Iqdb': "https://i.imgur.com/r3kJwPF.png",
        'Ascii2D': "https://i.imgur.com/BA7hWTm.png",
        'E-Hentai': "https://i.imgur.com/IXSFiax.png"
    }

    def __init__(self, client):
        super().__init__()
        self.ascii2d = Ascii2D(client=client)
        self.baidu = BaiDu(client=client)
        self.ehentai = EHentai(client=client)
        self.google = Google(client=client)
        self.iqdb = Iqdb(client=client)
        self.saucenao = SauceNAO(client=client, api_key=environ.get(
            'SAUCENAO_TOKEN') or open("SAUCENAO_TOKEN").readline())
        self.tracemoe = TraceMoe(client=client)

    @staticmethod
    def _value_assigment(title, url, thumbnail, similar, source, another_titles, another_urls):
        return {
            'title': title,
            'url': url,
            'thumbnail': thumbnail,
            'similar': similar,
            'source': source,
            'another_titles': another_titles,
            'another_urls': another_urls
        }

    @staticmethod
    async def _image_exporter(url, uri):
        return (ffmpeg
         .input(url, ss=0)
         .output(uri, vframes=1)
         .overwrite_output()
         .run_async(quiet=True)
         ).communicate()

    async def sauce_anime(self, url, isVideo):
        async with Semaphore(4):
            try:
                if(isVideo):
                    uri = f"{abs(hash(url)) % (10 ** 8)}.png"
                    await self._image_exporter(url, uri)
                    with open(uri, "rb") as img:
                        tMoetask = await self.tracemoe.search(file=img)
                        img.close()
                else:
                    tMoetask = await self.tracemoe.search(url=url)

                tMoe = tMoetask.raw
            except:
                raise Exception("All source Down")

            similar = tMoe[0].similarity
            if(similar >= 80):
                another_titles = list()
                another_urls = list()
                for x in tMoe[1:]:
                    try:
                        another_titles.append(
                            x.title_english or x.title_romaji)
                        another_urls.append(x.video)
                    except:
                        continue
                return self._value_assigment(tMoe[0].title_english or tMoe[0].title_romaji, tMoe[0].video, uri if isVideo else tMoe[0].image, similar, ["TraceMoe", self.SOURCE_DICT['TraceMoe']], another_titles, another_urls)
            else:
                if isVideo:
                    remove(uri)
                raise Exception("Source not found")

    async def sauce_image(self, url):
        async with Semaphore(4):
            try:
                GoogleTask, sNaoTask, A2dTask, IqTask, Iq3dTask, EhentaiTask, BaiduTask = await gather(
                    self.google.search(url=url),
                    self.saucenao.search(url=url),
                    self.ascii2d.search(url=url),
                    self.iqdb.search(url=url, ),
                    self.iqdb.search(url=url, is_3d=True),
                    self.ehentai.search(url=url),
                    self.baidu.search(url=url),
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
                if Google[2].thumbnail == "" or search("description", Google[2].title.lower()):
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
                Ehendata = True if Ehen[0].title != "" else None
            except:
                Ehendata = None

            try:
                Baid = BaiduTask.raw
                Baidata = True
            except:
                Baidata = None

            if sNaosimilar <= 80 and Iqsimilar <= 80 and Iq3dsimilar <= 80 and Googledata:
                another_titles = list()
                another_urls = list()
                for x in Google[3:]:
                    try:
                        another_titles.append(x.title)
                        another_urls.append(x.url)
                    except:
                        continue
                return self._value_assigment(Google[2].title, Google[2].url, Google[2].thumbnail, choice(range(90, 100)), ["Google", self.SOURCE_DICT['Google']], another_titles, another_urls)

            if sNaosimilar <= 80 and Iqsimilar <= 80 and Iq3dsimilar <= 80 and Baidata and Googledata is None and A2ddata is None and Ehendata is None:
                another_titles = list()
                another_urls = list()
                for x in Baid[1:]:
                    try:
                        another_titles.append(x.title)
                        another_urls.append(x.url)
                    except:
                        continue
                return self._value_assigment(Baid[0].title, Baid[0].url, Baid[0].img_src, None, ["Baidu", self.SOURCE_DICT['Baidu']], another_titles, another_urls)

            elif sNaosimilar <= 80 and Iqsimilar <= 80 and Iq3dsimilar <= 80 and Ehendata and A2ddata is None and Googledata is None and Baidata is None:
                another_titles = list()
                another_urls = list()
                for x in Ehen[1:]:
                    try:
                        another_titles.append(x.title)
                        another_urls.append(x.url)
                    except:
                        continue
                return self._value_assigment(Ehen[0].title, Ehen[0].url, Ehen[0].thumbnail, None, ["E-Hentai", self.SOURCE_DICT['E-Hentai']], another_titles, another_urls)

            elif sNaosimilar <= 80 and Iqsimilar <= 80 and Iq3dsimilar <= 80 and A2ddata and Ehendata is None and Googledata is None and Baidata is None:
                another_titles = list()
                another_urls = list()
                for x in A2d[2:]:
                    try:
                        another_titles.append(x.title)
                        another_urls.append(x.url)
                    except:
                        continue
                return self._value_assigment(A2d[1].title, A2d[1].url, A2d[1].thumbnail, None, ["Ascii2D", self.SOURCE_DICT['Ascii2D']], another_titles, another_urls)

            elif sNaosimilar >= Iqsimilar and sNaosimilar >= Iq3dsimilar and sNaosimilar >= 80:
                another_titles = list()
                another_urls = list()
                for x in sNao[1:]:
                    try:
                        another_titles.append(x.title)
                        another_urls.append(x.url)
                    except:
                        continue
                return self._value_assigment(sNao[0].title, sNao[0].url, sNao[0].thumbnail, sNaosimilar, ["SauceNao", self.SOURCE_DICT['SauceNao']], another_titles, another_urls)

            elif Iqsimilar >= sNaosimilar and Iqsimilar >= Iq3dsimilar:
                another_titles = list()
                another_urls = list()
                for x in Iq[1:]:
                    try:
                        another_titles.append(x.content[:180 - len(x.content)])
                        another_urls.append(x.url)
                    except:
                        continue
                return self._value_assigment(Iq[0].content[:180 - len(Iq[0].content)], Iq[0].url, Iq[0].thumbnail, Iqsimilar, ["Iqdb", self.SOURCE_DICT['Iqdb']], another_titles, another_urls)

            elif Iq3dsimilar >= sNaosimilar and Iq3dsimilar >= Iqsimilar:
                another_titles = list()
                another_urls = list()
                for x in Iq3d[1:]:
                    try:
                        another_titles.append(x.content[:180 - len(x.content)])
                        another_urls.append(x.url)
                    except:
                        continue
                return self._value_assigment(Iq3d[0].content[:180 - len(Iq3d[0].content)], Iq3d[0].url, Iq3d[0].thumbnail, Iq3dsimilar, ["Iqdb 3D", self.SOURCE_DICT['Iqdb']], another_titles, another_urls)

            elif Iq3dsimilar == 0.0 and Iqsimilar == 0.0 and sNaosimilar == 0.0 and A2ddata is None and Googledata is None and Ehendata is None and Baidata is None:
                raise Exception("All source down")
            else:
                raise Exception("Source not found")
