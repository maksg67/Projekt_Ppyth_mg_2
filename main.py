from tkinter import *
import tkintermapview
import controller

root = Tk()
root.title("Mapbook_AB")
root.geometry("1500x900")

domy, pracownicy, pensjonariusze = controller.load_data()

ramka_listy = Frame(root)
ramka_listy.pack(side=TOP, fill=X, pady=10)

ramka_mapa = Frame(root)
ramka_mapa.pack(side=BOTTOM, fill=BOTH, expand=True)

map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1500, height=400, corner_radius=4)
map_widget.set_zoom(6)
map_widget.set_position(52.2, 21.0)
map_widget.pack(fill=BOTH, expand=True)

active_marker = None


def pokaz_marker(obj):
    global active_marker
    if active_marker:
        active_marker.delete()
    text = obj.__dict__.get("nazwa", obj.__dict__.get("imie", ""))
    active_marker = map_widget.set_marker(obj.coordinates[0], obj.coordinates[1], text=text)
    map_widget.set_position(obj.coordinates[0], obj.coordinates[1])
    map_widget.set_zoom(12)


def odswiez_listy():
    lista_domow.delete(0, END)
    for d in domy:
        lista_domow.insert(END, d.nazwa)

    lista_pracownikow.delete(0, END)
    for p in pracownicy:
        lista_pracownikow.insert(END, p.imie)

    lista_pensjonariuszy.delete(0, END)
    for p in pensjonariusze:
        lista_pensjonariuszy.insert(END, p.imie)


def szczegoly_dom(event):
    i = lista_domow.curselection()
    if not i:
        return
    d = domy[i[0]]
    label_dom_nazwa.config(text=f"Nazwa: {d.nazwa}")
    label_dom_lokalizacja.config(text=f"Lokalizacja: {d.lokalizacja}")
    pokaz_marker(d)


def szczegoly_prac(event):
    i = lista_pracownikow.curselection()
    if not i:
        return
    p = pracownicy[i[0]]
    label_prac_imie.config(text=f"Imię: {p.imie}")
    label_prac_nazwisko.config(text=f"Nazwisko: {p.nazwisko}")
    label_prac_wiek.config(text=f"Wiek: {p.wiek}")
    label_prac_rola.config(text=f"Rola: {p.rola}")
    label_prac_dom.config(text=f"Dom: {p.dom.nazwa}")
    pokaz_marker(p)


def szczegoly_pens(event):
    i = lista_pensjonariuszy.curselection()
    if not i:
        return
    p = pensjonariusze[i[0]]
    label_pens_imie.config(text=f"Imię: {p.imie}")
    label_pens_nazwisko.config(text=f"Nazwisko: {p.nazwisko}")
    label_pens_wiek.config(text=f"Wiek: {p.wiek}")
    label_pens_choroby.config(text=f"Choroby: {p.choroby}")
    label_pens_dom.config(text=f"Dom: {p.dom.nazwa}")
    pokaz_marker(p)


kol1 = Frame(ramka_listy)
kol1.pack(side=LEFT, padx=20)

kol2 = Frame(ramka_listy)
kol2.pack(side=LEFT, padx=20)

kol3 = Frame(ramka_listy)
kol3.pack(side=LEFT, padx=20)

Label(kol1, text="Domy").pack()
lista_domow = Listbox(kol1, width=30, height=20)
lista_domow.pack()
lista_domow.bind("<<ListboxSelect>>", szczegoly_dom)

Label(kol2, text="Pracownicy").pack()
lista_pracownikow = Listbox(kol2, width=30, height=20)
lista_pracownikow.pack()
lista_pracownikow.bind("<<ListboxSelect>>", szczegoly_prac)

Label(kol3, text="Pensjonariusze").pack()
lista_pensjonariuszy = Listbox(kol3, width=30, height=20)
lista_pensjonariuszy.pack()
lista_pensjonariuszy.bind("<<ListboxSelect>>", szczegoly_pens)

Label(kol1, text="Szczegóły").pack(pady=5)
label_dom_nazwa = Label(kol1, text="---")
label_dom_nazwa.pack()
label_dom_lokalizacja = Label(kol1, text="---")
label_dom_lokalizacja.pack()

Label(kol2, text="Szczegóły").pack(pady=5)
label_prac_imie = Label(kol2, text="---")
label_prac_imie.pack()
label_prac_nazwisko = Label(kol2, text="---")
label_prac_nazwisko.pack()
label_prac_wiek = Label(kol2, text="---")
label_prac_wiek.pack()
label_prac_rola = Label(kol2, text="---")
label_prac_rola.pack()
label_prac_dom = Label(kol2, text="---")
label_prac_dom.pack()

Label(kol3, text="Szczegóły").pack(pady=5)
label_pens_imie = Label(kol3, text="---")
label_pens_imie.pack()
label_pens_nazwisko = Label(kol3, text="---")
label_pens_nazwisko.pack()
label_pens_wiek = Label(kol3, text="---")
label_pens_wiek.pack()
label_pens_choroby = Label(kol3, text="---")
label_pens_choroby.pack()
label_pens_dom = Label(kol3, text="---")
label_pens_dom.pack()

odswiez_listy()
root.mainloop()
