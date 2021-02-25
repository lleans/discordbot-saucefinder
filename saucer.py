import re
from PicImageSearch import SauceNAO, TraceMoe, Ascii2D, Iqdb, Google


class Sauce:

    def __init__(self, name, type):
        self.title = ""
        self.similiar = ""
        self.thumbnail = ""
        self.url = ""
        self.source = ""
        self.another_titles: list = list()
        self.another_urls: list = list()
        self._getsauce(name=name, type=type)

    def _getsauce(self, name, type):
        if type == "anime":
            self.sauce_anime(name)

        if type == "image":
            self.sauce_image(name)

    def sauce_anime(self, name):
        tMoe = Saucer.saucer_TraceMoe(name).raw
        tMoesimilar = float("{:.2f}".format(tMoe[0].similarity * 100))

        self.title = tMoe[0].title_english
        self.similiar = tMoesimilar
        self.thumbnail = tMoe[0].thumbnail
        self.url = tMoe[0].video_thumbnail
        self.source = "TraceMoe"
        for x in tMoe:
            self.another_titles.append(x.title)
            self.another_urls.append(x.video_thumbnail)

    def sauce_image(self, name):
        Google = Saucer.saucer_Google(name).raw
        sNao = Saucer.saucer_sauceNao(name).raw
        A2d = Saucer.saucer_Ascii2D(name).raw

        try:
            Iq = Saucer.saucer_Iqdb(name).raw
            regexIq = re.compile("[0-9]+")
            Iqs = regexIq.search(Iq[0].similarity)
            Iqsimilar = float(Iqs.group(0))
        except AttributeError:
            Iqsimilar = float(0)

        try:
            Iq3d = Saucer.saucer_Iqdb3d(name).raw
            regexIqs = re.compile("[0-9]+")
            Iq3D = regexIqs.search(Iq3d[0].similarity)
            Iq3dsimilar = float(Iq3D.group(0))
        except AttributeError:
            Iq3dsimilar = float(0)

        try:
            Googledata = Google[2].titles[0]
        except IndexError:
            Googledata = None

        sNaosimilar = float(sNao[0].similarity)

        if sNaosimilar <= 80 and Iqsimilar <= 80 and Iq3dsimilar <= 80 and Googledata is not None:
            # Google
            self.title = Google[2].titles[0]
            self.similiar = None
            self.thumbnail = Google[2].thumbnail[0]
            self.url = Google[2].urls[0]
            self.source = "Google"
            for x in Google:
                try:
                    self.another_titles.append(x.titles[0])
                    self.another_urls.append(x.urls[0])
                except:
                    continue
        elif sNaosimilar <= 80 and Iqsimilar <= 80 and Iq3dsimilar <= 80 and Googledata is None:
            # Ascii2d
            self.title = A2d[1].titles[0]
            self.similiar = None
            self.thumbnail = A2d[1].thumbnail[0]
            self.url = A2d[1].urls[0]
            self.source = "Ascii2D"
            for x in A2d:
                try:
                    self.another_titles.append(x.titles[0])
                    self.another_urls.append(x.urls[0])
                except:
                    continue
        elif sNaosimilar >= Iqsimilar and sNaosimilar >= Iq3dsimilar:
            # SauceNao
            self.title = sNao[0].title
            self.similiar = sNaosimilar
            self.thumbnail = sNao[0].thumbnail
            self.url = sNao[0].url
            self.source = "SauceNao"
            for x in sNao:
                try:
                    self.another_titles.append(x.title)
                    self.another_urls.append(x.url)
                except:
                    continue
        elif Iqsimilar >= sNaosimilar and Iqsimilar >= Iq3dsimilar:
            # Iqdb
            self.title = Iq[0].title[:180 - len(Iq[0].title)] + "..."
            self.similiar = Iqsimilar
            self.thumbnail = Iq[0].thumbnail
            if Iq[0].url[:4] == 'http':
                self.url = Iq[0].url
            else:
                self.url = f"https:{Iq[0].url}"
            self.source = "Iqdb"
            for x in Iq:
                try:
                    self.another_titles.append(x.title)
                    if x.url[:4] == 'http':
                        self.another_urls.append(x.url)
                    else:
                        self.another_urls.append(f"https:{x.url}")
                except:
                    continue
        elif Iq3dsimilar >= sNaosimilar and Iq3dsimilar >= Iqsimilar:
            # Iqdb 3D
            self.title = Iq3d[0].title[:180 - len(Iq[0].title)] + "..."
            self.similiar = Iq3dsimilar
            self.thumbnail = Iq3d[0].thumbnail
            if Iq3d[0].url[:4] == 'http':
                self.url = Iq3d[0].url
            else:
                self.url = f"https:{Iq3d[0].url}"
            self.source = "Iqdb 3D"
            for x in Iq3d:
                try:
                    self.another_titles.append(x.title)
                    if x.url[:4] == 'http':
                        self.another_urls.append(x.url)
                    else:
                        self.another_urls.append(f"https:{x.url}")
                except:
                    continue


class Saucer:

    def saucer_sauceNao(name):
        b = open("API_sauceNao")
        saucer = SauceNAO(b.readline())
        sauce = saucer.search(name)
        return sauce

    def saucer_TraceMoe(name):
        saucer = TraceMoe()
        sauce = saucer.search(name)
        return sauce

    def saucer_Ascii2D(name):
        saucer = Ascii2D()
        sauce = saucer.search(name)
        return sauce

    def saucer_Iqdb(name):
        saucer = Iqdb()
        sauce = saucer.search(name)
        return sauce

    def saucer_Iqdb3d(name):
        saucer = Iqdb()
        sauce = saucer.search_3d(name)
        return sauce

    def saucer_Google(name):
        saucer = Google()
        sauce = saucer.search(name)
        return sauce
