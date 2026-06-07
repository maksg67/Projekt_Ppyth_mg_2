from bs4 import BeautifulSoup
import requests
from model import domy, pracownicy, pensjonariusze


def get_coordinates(location):
    url = f"https://pl.wikipedia.org/wiki/{location}"
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = BeautifulSoup(response.text, 'html.parser')
    lat = float(html.select(".latitude")[1].text.replace(",", "."))
    lon = float(html.select(".longitude")[1].text.replace(",", "."))
    return [lat, lon]


class DomOpieki:
    def __init__(self, nazwa, lokalizacja):
        self.nazwa = nazwa
        self.lokalizacja = lokalizacja
        self.coordinates = get_coordinates(lokalizacja)
        self.pracownicy = []
        self.pensjonariusze = []


class Pracownik:
    def __init__(self, imie, nazwisko, wiek, rola, dom):
        self.imie = imie
        self.nazwisko = nazwisko
        self.wiek = wiek
        self.rola = rola
        self.dom = dom
        self.coordinates = dom.coordinates


class Pensjonariusz:
    def __init__(self, imie, nazwisko, wiek, choroby, dom):
        self.imie = imie
        self.nazwisko = nazwisko
        self.wiek = wiek
        self.choroby = choroby
        self.dom = dom
        self.coordinates = dom.coordinates


def load_data():
    obiekty_domy = []
    for d in domy:
        obiekty_domy.append(DomOpieki(d["nazwa"], d["lokalizacja"]))

    obiekty_prac = []
    for p in pracownicy:
        dom = next((x for x in obiekty_domy if x.nazwa == p["dom"]), None)
        if dom:
            obiekty_prac.append(Pracownik(p["imie"], p["nazwisko"], p["wiek"], p["rola"], dom))
            dom.pracownicy.append(obiekty_prac[-1])

    obiekty_pens = []
    for p in pensjonariusze:
        dom = next((x for x in obiekty_domy if x.nazwa == p["dom"]), None)
        if dom:
            obiekty_pens.append(Pensjonariusz(p["imie"], p["nazwisko"], p["wiek"], p["choroby"], dom))
            dom.pensjonariusze.append(obiekty_pens[-1])

    return obiekty_domy, obiekty_prac, obiekty_pens
