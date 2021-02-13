import re
from PicImageSearch import SauceNAO, TraceMoe, Ascii2D, Iqdb

class Sauce:
    title = ""
    similiar = ""
    thumbnail = ""
    url = ""
    frm = ""
    another = ""


def sauce(name, type):
    if type == "anime":
        sauce_anime(name)

    if type == "image":
        sauce_image(name)

    sauce = Sauce()

    return sauce


def sauce_anime(name):
    tMoe = saucer_TraceMoe(name).raw[0]
    tMoesimilar = float("{:.2f}".format(tMoe.similarity * 100))

    setattr(Sauce, 'title', tMoe.title_english)
    setattr(Sauce, 'similiar', tMoesimilar)
    setattr(Sauce, 'thumbnail', tMoe.thumbnail)
    setattr(Sauce, 'url', tMoe.video_thumbnail)
    setattr(Sauce, 'frm', "TraceMoe")
    setattr(Sauce, 'another', saucer_TraceMoe(name).raw)


def sauce_image(name):
    sNao = saucer_sauceNao(name).raw[0]
    A2d = saucer_Ascii2D(name).raw[1]
    try:
        Iq = saucer_Iqdb(name).raw[0]
        regexIq = re.compile("[0-9]+")
        Iqs = regexIq.findall(Iq.similarity)
        Iqsi_clean = list(filter(bool, Iqs))
        Iqsimilar = float(Iqsi_clean[0])
    except AttributeError:
        Iqsimilar = float(0)

    try:
        Iq3d = saucer_Iqdb3d(name).raw[0]
        regexIqs = re.compile("[0-9]+")
        Iq3D = regexIqs.findall(Iq.similarity)
        Iqs3D_clean = list(filter(bool, Iq3D))
        Iq3dsimilar = float(Iqs3D_clean[0])
    except AttributeError:
        Iq3dsimilar = float(0)

    sNaosimilar = float(sNao.similarity)

    if sNaosimilar <= 50 and Iqsimilar <= 50 and Iq3dsimilar <= 50:
        setattr(Sauce, 'title', A2d.titles[0])
        setattr(Sauce, 'similiar', None)
        setattr(Sauce, 'thumbnail', A2d.thumbnail[0])
        setattr(Sauce, 'url', A2d.urls[0])
        setattr(Sauce, 'frm', "Ascii2d")
        setattr(Sauce, 'another', saucer_Ascii2D(name).raw)
    elif sNaosimilar >= Iqsimilar and sNaosimilar >= Iq3dsimilar:
        setattr(Sauce, 'title', sNao.title)
        setattr(Sauce, 'similiar', sNaosimilar)
        setattr(Sauce, 'thumbnail', sNao.thumbnail)
        setattr(Sauce, 'url', sNao.url)
        setattr(Sauce, 'frm', "SauceNao")
        setattr(Sauce, 'another', saucer_sauceNao(name).raw)
    elif Iqsimilar >= sNaosimilar and Iqsimilar >= Iq3dsimilar:
        setattr(Sauce, 'title', Iq.title[:240 - len(Iq.title)] + "...")
        setattr(Sauce, 'similiar', Iqsimilar)
        setattr(Sauce, 'thumbnail', Iq.thumbnail)
        setattr(Sauce, 'url', f"https:{Iq.url}")
        setattr(Sauce, 'frm', "Iqdb")
        setattr(Sauce, 'another', saucer_Iqdb(name).raw)
    elif Iq3dsimilar >= sNaosimilar and Iq3dsimilar >= Iqsimilar:
        setattr(Sauce, 'title', Iq3d.title[:240 - len(Iq3d.title)] + "...")
        setattr(Sauce, 'similiar', Iq3dsimilar)
        setattr(Sauce, 'thumbnail', Iq3d.thumbnail)
        setattr(Sauce, 'url', f"https:{Iq3d.url}")
        setattr(Sauce, 'frm', "Iqdb 3D")
        setattr(Sauce, 'another', saucer_Iqdb3d(name).raw)
    


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