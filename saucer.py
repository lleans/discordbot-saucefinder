import ffmpeg

from io import BytesIO
from re import IGNORECASE, search
from random import choice
from os import environ
from asyncio import gather, Semaphore

from PIL.Image import open as openImage
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
            'SAUCENAO_TOKEN') or open("SAUCENAO_TOKEN").readline().strip())
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
    async def extract_image(url):
        ss = 0
        isBlank = True

        while isBlank:
            ffmpeg_proc = (
                        ffmpeg
                        .input(url, ss=ss)
                        .filter("cropdetect")
                        .output('pipe: ', format='image2', vframes=1)
                        .overwrite_output()
                        .run_async(pipe_stdout=True, pipe_stderr=True)
                    )
            img = ffmpeg_proc.communicate()[0]
            extrema = openImage(BytesIO(img)).convert("L").getextrema()
            isBlank = extrema[0] == extrema[1]
            ss += 1
        else:
            return img 


    async def sauce_anime(self, url, isVideo):
        async with Semaphore(4):
            try:
                if(isVideo):
                    img = await self.extract_image(url=url)
                    tMoetask = await self.tracemoe.search(file=img)
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
                return self._value_assigment(tMoe[0].title_english or tMoe[0].title_romaji, tMoe[0].video, img if isVideo else tMoe[0].image, similar, ["TraceMoe", self.SOURCE_DICT['TraceMoe']], another_titles, another_urls)
            else:
                raise Exception("Source not found")

    async def sauce_image(self, url):
        async with Semaphore(4):
            GoogleTask = sNaoTask = A2dTask = IqTask = Iq3dTask = EhentaiTask = BaiduTask = None
            task = [
                self.google.search(url=url),
                self.saucenao.search(url=url),
                self.ascii2d.search(url=url),
                self.iqdb.search(url=url, ),
                self.iqdb.search(url=url, is_3d=True),
                self.ehentai.search(url=url),
                self.baidu.search(url=url)
            ]
            GoogleTask, sNaoTask, A2dTask, IqTask, Iq3dTask, EhentaiTask, BaiduTask = await gather(
                *task,
                return_exceptions=True)
            
            try:
                isGoogleExist = (True, choice(range(90, 100))) if GoogleTask is not None and (
                    GoogleTask.raw[2].thumbnail != "" or not search(r"description", GoogleTask.raw[2].title, flags=IGNORECASE)) else (False, 0)
            except:
                isGoogleExist = (False, 0)

            try:
                isSNaoExist = (
                    True, sNaoTask.raw[0].similarity) if sNaoTask is not None and sNaoTask.raw[0].title != "" else (False, 0)
            except:
                isSNaoExist = (False, 0)

            try:
                isA2DExist = (
                    True, None) if A2dTask is not None and A2dTask.raw[1].title != "" else (False, 0)
            except:
                isA2DExist = (False, 0)

            try:
                isIqdbExist = (
                    True, IqTask.raw[0].similarity) if IqTask is not None and IqTask.raw[0].title != "" and IqTask.raw[0].title != 'No relevant matches' else (False, 0)
            except:
                isIqdbExist = (False, 0)

            try:
                isIqdb3DExist = (
                    True, Iq3dTask.raw[0].similarity) if Iq3dTask is not None and Iq3dTask.raw[0].title != "" and Iq3dTask.raw[0].title != 'No relevant matches' else (False, 0)
            except:
                isIqdb3DExist = (False, 0)

            try:
                isEhenExist = (
                    True, None) if EhentaiTask is not None and EhentaiTask.raw[0].title != "" else (False, 0)
            except:
                isEhenExist = (False, 0)

            try:
                isBaiduExist = (
                    True, None) if BaiduTask is not None and BaiduTask.raw[0].title != "" else(False, 0)
            except:
                isBaiduExist = (False, 0)

            if isGoogleExist[0] and isSNaoExist[1] <= 80 and isIqdbExist[1] <= 80 and isIqdb3DExist[1] <= 80:
                another_titles = list()
                another_urls = list()
                for x in GoogleTask.raw[3:]:
                    try:
                        another_titles.append(x.title)
                        another_urls.append(x.url)
                    except:
                        continue
                return self._value_assigment(GoogleTask.raw[2].title, GoogleTask.raw[2].url, GoogleTask.raw[2].thumbnail, isGoogleExist[1], ["Google", self.SOURCE_DICT['Google']], another_titles, another_urls)

            elif isBaiduExist[0] and isSNaoExist[1] <= 80 and isIqdbExist[1] <= 80 and isIqdb3DExist[1] <= 80:
                another_titles = list()
                another_urls = list()
                for x in BaiduTask.raw[1:]:
                    try:
                        another_titles.append(x.title)
                        another_urls.append(x.url)
                    except:
                        continue
                return self._value_assigment(BaiduTask.raw[0].title, BaiduTask.raw[0].url, BaiduTask.raw[0].img_src, isBaiduExist[1], ["Baidu", self.SOURCE_DICT['Baidu']], another_titles, another_urls)

            elif isEhenExist[0] and isSNaoExist[1] <= 80 and isIqdbExist[1] <= 80 and isIqdb3DExist[1] <= 80:
                another_titles = list()
                another_urls = list()
                for x in EhentaiTask.raw[1:]:
                    try:
                        another_titles.append(x.title)
                        another_urls.append(x.url)
                    except:
                        continue
                return self._value_assigment(EhentaiTask.raw[0].title, EhentaiTask.raw[0].url, EhentaiTask.raw[0].thumbnail, isEhenExist[1], ["E-Hentai", self.SOURCE_DICT['E-Hentai']], another_titles, another_urls)

            elif isA2DExist[0] and isSNaoExist[1] <= 80 and isIqdbExist[1] <= 80 and isIqdb3DExist[1] <= 80:
                another_titles = list()
                another_urls = list()
                for x in A2dTask.raw[2:]:
                    try:
                        another_titles.append(x.title)
                        another_urls.append(x.url)
                    except:
                        continue
                return self._value_assigment(A2dTask.raw[1].title, A2dTask.raw[1].url, A2dTask.raw[1].thumbnail, isA2DExist[1], ["Ascii2D", self.SOURCE_DICT['Ascii2D']], another_titles, another_urls)

            elif isSNaoExist[1] >= isIqdbExist[1] and isSNaoExist[1] >= isIqdb3DExist[1] and isSNaoExist[1] >= 80:
                another_titles = list()
                another_urls = list()
                for x in sNaoTask.raw[1:]:
                    try:
                        another_titles.append(x.title)
                        another_urls.append(x.url)
                    except:
                        continue
                return self._value_assigment(sNaoTask.raw[0].title, sNaoTask.raw[0].url, sNaoTask.raw[0].thumbnail, isSNaoExist[1], ["SauceNao", self.SOURCE_DICT['SauceNao']], another_titles, another_urls)

            elif isIqdbExist[1] >= isSNaoExist[1] and isIqdbExist[1] >= isIqdb3DExist[1]:
                another_titles = list()
                another_urls = list()
                for x in IqTask.raw[1:]:
                    try:
                        another_titles.append(x.content[:180 - len(x.content)])
                        another_urls.append(x.url)
                    except:
                        continue
                return self._value_assigment(IqTask.raw[0].content[:180 - len(IqTask.raw[0].content)], IqTask.raw[0].url, IqTask.raw[0].thumbnail, isIqdbExist[1], ["Iqdb", self.SOURCE_DICT['Iqdb']], another_titles, another_urls)

            elif isIqdb3DExist[1] >= isSNaoExist[1] and isIqdb3DExist[1] >= isIqdbExist[1]:
                another_titles = list()
                another_urls = list()
                for x in Iq3dTask.raw[1:]:
                    try:
                        another_titles.append(x.content[:180 - len(x.content)])
                        another_urls.append(x.url)
                    except:
                        continue
                return self._value_assigment(Iq3dTask.raw[0].content[:180 - len(Iq3dTask.raw[0].content)], Iq3dTask.raw[0].url, Iq3dTask.raw[0].thumbnail, isIqdb3DExist[1], ["Iqdb 3D", self.SOURCE_DICT['Iqdb']], another_titles, another_urls)

            elif not (isSNaoExist[0] and isIqdbExist[0] and isSNaoExist[0] and isA2DExist[0] and isGoogleExist[0] and isEhenExist[0] and isBaiduExist[0]):
                raise Exception("Source not found")
            else:
                raise Exception("All source down")
