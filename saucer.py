from saucenao_api import SauceNao

b = open("API_sauceNao")
saucer = SauceNao(b.readline())

def saucer_sauceNao(name):
    sauce = saucer.from_url(name)
    return sauce
