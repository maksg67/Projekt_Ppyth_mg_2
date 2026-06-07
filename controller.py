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


def add_dom(nazwa, lokalizacja):
    d = DomOpieki(nazwa, lokalizacja)
    domy.append(d)
    return d


def remove_dom(index):
    d = domy[index]
    for p in d.pracownicy:
        pracownicy.remove(p)
    for p in d.pensjonariusze:
        pensjonariusze.remove(p)
    domy.pop(index)


def update_dom(index, nazwa, lokalizacja):
    d = domy[index]
    d.nazwa = nazwa
    d.lokalizacja = lokalizacja
    d.coordinates = get_coordinates(lokalizacja)


def add_pracownik(imie, nazwisko, wiek, rola, nazwa_domu):
    d = next((x for x in domy if x.nazwa == nazwa_domu), None)
    if d is None:
        return False
    p = Pracownik(imie, nazwisko, wiek, rola, d)
    pracownicy.append(p)
    d.pracownicy.append(p)
    return True


def remove_pracownik(index):
    p = pracownicy[index]
    p.dom.pracownicy.remove(p)
    pracownicy.pop(index)


def update_pracownik(index, imie, nazwisko, wiek, rola, nazwa_domu):
    p = pracownicy[index]
    p.imie = imie
    p.nazwisko = nazwisko
    p.wiek = wiek
    p.rola = rola
    if p.dom.nazwa != nazwa_domu:
        p.dom.pracownicy.remove(p)
        d = next((x for x in domy if x.nazwa == nazwa_domu), None)
        if d:
            p.dom = d
            d.pracownicy.append(p)
            p.coordinates = d.coordinates


def add_pensjonariusz(imie, nazwisko, wiek, choroby, nazwa_domu):
    d = next((x for x in domy if x.nazwa == nazwa_domu), None)
    if d is None:
        return False
    p = Pensjonariusz(imie, nazwisko, wiek, choroby, d)
    pensjonariusze.append(p)
    d.pensjonariusze.append(p)
    return True


def remove_pensjonariusz(index):
    p = pensjonariusze[index]
    p.dom.pensjonariusze.remove(p)
    pensjonariusze.pop(index)


def update_pensjonariusz(index, imie, nazwisko, wiek, choroby, nazwa_domu):
    p = pensjonariusze[index]
    p.imie = imie
    p.nazwisko = nazwisko
    p.wiek = wiek
    p.choroby = choroby
    if p.dom.nazwa != nazwa_domu:
        p.dom.pensjonariusze.remove(p)
        d = next((x for x in domy if x.nazwa == nazwa_domu), None)
        if d:
            p.dom = d
            d.pensjonariusze.append(p)
            p.coordinates = d.coordinates
