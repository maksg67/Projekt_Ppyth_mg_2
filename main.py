from tkinter import *
import tkintermapview
import controller

root = Tk()
root.title("Projekt_MG")
root.geometry("1700x900")

domy, pracownicy, pensjonariusze = controller.load_data()

ramka_gora = Frame(root)
ramka_gora.pack(side=TOP, fill=X, pady=10)

ramka_listy = Frame(ramka_gora)
ramka_listy.pack(side=LEFT, padx=10)

ramka_form = Frame(ramka_gora)
ramka_form.pack(side=RIGHT, padx=10, fill=Y)

ramka_mapa = Frame(root)
ramka_mapa.pack(side=BOTTOM, fill=BOTH, expand=True)

map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1700, height=400, corner_radius=4)
map_widget.set_zoom(6)
map_widget.set_position(52.2, 21.0)
map_widget.pack(fill=BOTH, expand=True)

active_marker = None
all_markers = []
active_list = "domy"
filter_text = ""


def clear_markers():
    global all_markers, active_marker
    for m in all_markers:
        m.delete()
    all_markers = []
    if active_marker:
        active_marker.delete()
        active_marker = None


def rysuj_markery_klasy():
    clear_markers()
    ft = filter_text.lower()

    if active_list == "domy":
        for d in domy:
            if ft in d.nazwa.lower():
                all_markers.append(
                    map_widget.set_marker(d.coordinates[0], d.coordinates[1], text=d.nazwa)
                )

    elif active_list == "pracownicy":
        for p in pracownicy:
            if ft in p.imie.lower():
                all_markers.append(
                    map_widget.set_marker(p.coordinates[0], p.coordinates[1], text=p.imie)
                )

    elif active_list == "pensjonariusze":
        for p in pensjonariusze:
            if ft in p.imie.lower():
                all_markers.append(
                    map_widget.set_marker(p.coordinates[0], p.coordinates[1], text=p.imie)
                )



def pokaz_marker(obj):
    global active_marker
    if active_marker:
        active_marker.delete()
    text = getattr(obj, "nazwa", getattr(obj, "imie", ""))
    active_marker = map_widget.set_marker(obj.coordinates[0], obj.coordinates[1], text=text)
    map_widget.set_position(obj.coordinates[0], obj.coordinates[1])
    map_widget.set_zoom(12)


def odswiez_listy():
    lista_domow.delete(0, END)
    for d in domy:
        if filter_text.lower() in d.nazwa.lower():
            lista_domow.insert(END, d.nazwa)

    lista_pracownikow.delete(0, END)
    for p in pracownicy:
        if filter_text.lower() in p.imie.lower():
            lista_pracownikow.insert(END, p.imie)

    lista_pensjonariuszy.delete(0, END)
    for p in pensjonariusze:
        if filter_text.lower() in p.imie.lower():
            lista_pensjonariuszy.insert(END, p.imie)


def szczegoly_dom(event):
    global active_list
    active_list = "domy"
    i = lista_domow.curselection()
    if not i:
        return
    nazwa = lista_domow.get(i[0])
    d = next(x for x in domy if x.nazwa == nazwa)
    label_dom_nazwa.config(text=f"Nazwa: {d.nazwa}")
    label_dom_lokalizacja.config(text=f"Lokalizacja: {d.lokalizacja}")
    lista_prac_dom.delete(0, END)
    for p in d.pracownicy:
        lista_prac_dom.insert(END, f"{p.imie} {p.nazwisko}")
    lista_pens_dom.delete(0, END)
    for p in d.pensjonariusze:
        lista_pens_dom.insert(END, f"{p.imie} {p.nazwisko}")
    ustaw_formularz_domy(d)
    rysuj_markery_klasy()
    pokaz_marker(d)


def szczegoly_prac(event):
    global active_list
    active_list = "pracownicy"
    i = lista_pracownikow.curselection()
    if not i:
        return
    imie = lista_pracownikow.get(i[0])
    p = next(x for x in pracownicy if x.imie == imie)
    label_prac_imie.config(text=f"Imię: {p.imie}")
    label_prac_nazwisko.config(text=f"Nazwisko: {p.nazwisko}")
    label_prac_wiek.config(text=f"Wiek: {p.wiek}")
    label_prac_rola.config(text=f"Rola: {p.rola}")
    label_prac_dom.config(text=f"Dom: {p.dom.nazwa}")
    ustaw_formularz_pracownik(p)
    rysuj_markery_klasy()
    pokaz_marker(p)


def szczegoly_pens(event):
    global active_list
    active_list = "pensjonariusze"
    i = lista_pensjonariuszy.curselection()
    if not i:
        return
    imie = lista_pensjonariuszy.get(i[0])
    p = next(x for x in pensjonariusze if x.imie == imie)
    label_pens_imie.config(text=f"Imię: {p.imie}")
    label_pens_nazwisko.config(text=f"Nazwisko: {p.nazwisko}")
    label_pens_wiek.config(text=f"Wiek: {p.wiek}")
    label_pens_choroby.config(text=f"Choroby: {p.choroby}")
    label_pens_dom.config(text=f"Dom: {p.dom.nazwa}")
    ustaw_formularz_pensjonariusz(p)
    rysuj_markery_klasy()
    pokaz_marker(p)


def ustaw_formularz_domy(dom=None):
    for w in form_widgets:
        w.pack_forget()
    label_form_typ.config(text="Formularz: Dom")
    label_f1.config(text="Nazwa")
    label_f2.config(text="Lokalizacja")
    label_f3.config(text="")
    label_f4.config(text="")
    entry_f1.delete(0, END)
    entry_f2.delete(0, END)
    entry_f3.delete(0, END)
    entry_f4.delete(0, END)
    if dom:
        entry_f1.insert(0, dom.nazwa)
        entry_f2.insert(0, dom.lokalizacja)
    label_f1.pack(anchor="w")
    entry_f1.pack(fill=X)
    label_f2.pack(anchor="w")
    entry_f2.pack(fill=X)
    btn_dodaj.pack(fill=X, pady=2)
    btn_edytuj.pack(fill=X, pady=2)
    btn_usun.pack(fill=X, pady=2)


def ustaw_formularz_pracownik(prac=None):
    for w in form_widgets:
        w.pack_forget()
    label_form_typ.config(text="Formularz: Pracownik")
    label_f1.config(text="Imię")
    label_f2.config(text="Nazwisko")
    label_f3.config(text="Wiek")
    label_f4.config(text="Rola")
    entry_f1.delete(0, END)
    entry_f2.delete(0, END)
    entry_f3.delete(0, END)
    entry_f4.delete(0, END)
    dom_var.set(domy[0].nazwa if domy else "")
    if prac:
        entry_f1.insert(0, prac.imie)
        entry_f2.insert(0, prac.nazwisko)
        entry_f3.insert(0, str(prac.wiek))
        entry_f4.insert(0, prac.rola)
        dom_var.set(prac.dom.nazwa)
    label_f1.pack(anchor="w")
    entry_f1.pack(fill=X)
    label_f2.pack(anchor="w")
    entry_f2.pack(fill=X)
    label_f3.pack(anchor="w")
    entry_f3.pack(fill=X)
    label_f4.pack(anchor="w")
    entry_f4.pack(fill=X)
    label_dom_select.pack(anchor="w")
    dom_menu.pack(fill=X)
    btn_dodaj.pack(fill=X, pady=2)
    btn_edytuj.pack(fill=X, pady=2)
    btn_usun.pack(fill=X, pady=2)


def ustaw_formularz_pensjonariusz(pens=None):
    for w in form_widgets:
        w.pack_forget()
    label_form_typ.config(text="Formularz: Pensjonariusz")
    label_f1.config(text="Imię")
    label_f2.config(text="Nazwisko")
    label_f3.config(text="Wiek")
    label_f4.config(text="Choroby")
    entry_f1.delete(0, END)
    entry_f2.delete(0, END)
    entry_f3.delete(0, END)
    entry_f4.delete(0, END)
    dom_var.set(domy[0].nazwa if domy else "")
    if pens:
        entry_f1.insert(0, pens.imie)
        entry_f2.insert(0, pens.nazwisko)
        entry_f3.insert(0, str(pens.wiek))
        entry_f4.insert(0, pens.choroby)
        dom_var.set(pens.dom.nazwa)
    label_f1.pack(anchor="w")
    entry_f1.pack(fill=X)
    label_f2.pack(anchor="w")
    entry_f2.pack(fill=X)
    label_f3.pack(anchor="w")
    entry_f3.pack(fill=X)
    label_f4.pack(anchor="w")
    entry_f4.pack(fill=X)
    label_dom_select.pack(anchor="w")
    dom_menu.pack(fill=X)
    btn_dodaj.pack(fill=X, pady=2)
    btn_edytuj.pack(fill=X, pady=2)
    btn_usun.pack(fill=X, pady=2)


def znajdz_dom_po_nazwie(nazwa):
    return next((d for d in domy if d.nazwa == nazwa), None)


def dodaj_obiekt():
    if active_list == "domy":
        nazwa = entry_f1.get().strip()
        lok = entry_f2.get().strip()
        if not nazwa or not lok:
            return
        if any(d.nazwa == nazwa for d in domy):
            return
        nowy = controller.DomOpieki(nazwa, lok)
        domy.append(nowy)
    elif active_list == "pracownicy":
        imie = entry_f1.get().strip()
        nazw = entry_f2.get().strip()
        try:
            wiek = int(entry_f3.get().strip())
        except ValueError:
            return
        rola = entry_f4.get().strip()
        dom_nazwa = dom_var.get()
        dom = znajdz_dom_po_nazwie(dom_nazwa)
        if not dom:
            return
        nowy = controller.Pracownik(imie, nazw, wiek, rola, dom)
        pracownicy.append(nowy)
        dom.pracownicy.append(nowy)
    elif active_list == "pensjonariusze":
        imie = entry_f1.get().strip()
        nazw = entry_f2.get().strip()
        try:
            wiek = int(entry_f3.get().strip())
        except ValueError:
            return
        chor = entry_f4.get().strip()
        dom_nazwa = dom_var.get()
        dom = znajdz_dom_po_nazwie(dom_nazwa)
        if not dom:
            return
        nowy = controller.Pensjonariusz(imie, nazw, wiek, chor, dom)
        pensjonariusze.append(nowy)
        dom.pensjonariusze.append(nowy)
    odswiez_listy()
    rysuj_markery_klasy()
    controller.save_model(domy, pracownicy, pensjonariusze)


def edytuj_obiekt():
    if active_list == "domy":
        i = lista_domow.curselection()
        if not i:
            return
        stara_nazwa = lista_domow.get(i[0])
        d = next(x for x in domy if x.nazwa == stara_nazwa)
        nowa_nazwa = entry_f1.get().strip()
        lok = entry_f2.get().strip()
        if not nowa_nazwa or not lok:
            return
        d.nazwa = nowa_nazwa
        d.lokalizacja = lok
        d.coordinates = controller.get_coordinates(lok)
    elif active_list == "pracownicy":
        i = lista_pracownikow.curselection()
        if not i:
            return
        imie_sel = lista_pracownikow.get(i[0])
        p = next(x for x in pracownicy if x.imie == imie_sel)
        p.imie = entry_f1.get().strip()
        p.nazwisko = entry_f2.get().strip()
        try:
            p.wiek = int(entry_f3.get().strip())
        except ValueError:
            return
        p.rola = entry_f4.get().strip()
        dom_nazwa = dom_var.get()
        dom = znajdz_dom_po_nazwie(dom_nazwa)
        if dom and dom is not p.dom:
            if p in p.dom.pracownicy:
                p.dom.pracownicy.remove(p)
            p.dom = dom
            dom.pracownicy.append(p)
        p.coordinates = p.dom.coordinates
    elif active_list == "pensjonariusze":
        i = lista_pensjonariuszy.curselection()
        if not i:
            return
        imie_sel = lista_pensjonariuszy.get(i[0])
        p = next(x for x in pensjonariusze if x.imie == imie_sel)
        p.imie = entry_f1.get().strip()
        p.nazwisko = entry_f2.get().strip()
        try:
            p.wiek = int(entry_f3.get().strip())
        except ValueError:
            return
        p.choroby = entry_f4.get().strip()
        dom_nazwa = dom_var.get()
        dom = znajdz_dom_po_nazwie(dom_nazwa)
        if dom and dom is not p.dom:
            if p in p.dom.pensjonariusze:
                p.dom.pensjonariusze.remove(p)
            p.dom = dom
            dom.pensjonariusze.append(p)
        p.coordinates = p.dom.coordinates
    odswiez_listy()
    rysuj_markery_klasy()
    controller.save_model(domy, pracownicy, pensjonariusze)


def usun_obiekt():
    if active_list == "domy":
        i = lista_domow.curselection()
        if not i:
            return
        nazwa = lista_domow.get(i[0])
        d = next(x for x in domy if x.nazwa == nazwa)
        for p in list(d.pracownicy):
            pracownicy.remove(p)
        for p in list(d.pensjonariusze):
            pensjonariusze.remove(p)
        domy.remove(d)
    elif active_list == "pracownicy":
        i = lista_pracownikow.curselection()
        if not i:
            return
        imie_sel = lista_pracownikow.get(i[0])
        p = next(x for x in pracownicy if x.imie == imie_sel)
        if p in p.dom.pracownicy:
            p.dom.pracownicy.remove(p)
        pracownicy.remove(p)
    elif active_list == "pensjonariusze":
        i = lista_pensjonariuszy.curselection()
        if not i:
            return
        imie_sel = lista_pensjonariuszy.get(i[0])
        p = next(x for x in pensjonariusze if x.imie == imie_sel)
        if p in p.dom.pensjonariusze:
            p.dom.pensjonariusze.remove(p)
        pensjonariusze.remove(p)
    odswiez_listy()
    rysuj_markery_klasy()
    controller.save_model(domy, pracownicy, pensjonariusze)


def ustaw_filter(*args):
    global filter_text
    filter_text = entry_filter.get().strip()
    odswiez_listy()
    rysuj_markery_klasy()


kol1 = Frame(ramka_listy)
kol1.pack(side=LEFT, padx=20)

kol2 = Frame(ramka_listy)
kol2.pack(side=LEFT, padx=20)

kol3 = Frame(ramka_listy)
kol3.pack(side=LEFT, padx=20)

Label(kol1, text="Domy").pack()
lista_domow = Listbox(kol1, width=30, height=15)
lista_domow.pack()
lista_domow.bind("<<ListboxSelect>>", szczegoly_dom)

Label(kol2, text="Pracownicy").pack()
lista_pracownikow = Listbox(kol2, width=30, height=15)
lista_pracownikow.pack()
lista_pracownikow.bind("<<ListboxSelect>>", szczegoly_prac)

Label(kol3, text="Pensjonariusze").pack()
lista_pensjonariuszy = Listbox(kol3, width=30, height=15)
lista_pensjonariuszy.pack()
lista_pensjonariuszy.bind("<<ListboxSelect>>", szczegoly_pens)

Label(kol1, text="Szczegóły domu").pack(pady=5)
label_dom_nazwa = Label(kol1, text="---")
label_dom_nazwa.pack()
label_dom_lokalizacja = Label(kol1, text="---")
label_dom_lokalizacja.pack()
Label(kol1, text="Pracownicy domu").pack(pady=5)
lista_prac_dom = Listbox(kol1, width=30, height=6)
lista_prac_dom.pack()
Label(kol1, text="Pensjonariusze domu").pack(pady=5)
lista_pens_dom = Listbox(kol1, width=30, height=6)
lista_pens_dom.pack()

Label(kol2, text="Szczegóły pracownika").pack(pady=5)
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

Label(kol3, text="Szczegóły pensjonariusza").pack(pady=5)
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

Label(ramka_form, text="Filtr").pack(anchor="w")
entry_filter = Entry(ramka_form)
entry_filter.pack(fill=X)
entry_filter.bind("<KeyRelease>", ustaw_filter)

Label(ramka_form, text="").pack(pady=5)

label_form_typ = Label(ramka_form, text="Formularz")
label_form_typ.pack(anchor="w")

label_f1 = Label(ramka_form, text="")
entry_f1 = Entry(ramka_form)
label_f2 = Label(ramka_form, text="")
entry_f2 = Entry(ramka_form)
label_f3 = Label(ramka_form, text="")
entry_f3 = Entry(ramka_form)
label_f4 = Label(ramka_form, text="")
entry_f4 = Entry(ramka_form)

dom_var = StringVar()
label_dom_select = Label(ramka_form, text="Dom")
dom_menu = OptionMenu(ramka_form, dom_var, *[d.nazwa for d in domy])

btn_dodaj = Button(ramka_form, text="Dodaj", command=dodaj_obiekt)
btn_edytuj = Button(ramka_form, text="Edytuj", command=edytuj_obiekt)
btn_usun = Button(ramka_form, text="Usuń", command=usun_obiekt)

form_widgets = [
    label_f1, entry_f1,
    label_f2, entry_f2,
    label_f3, entry_f3,
    label_f4, entry_f4,
    label_dom_select, dom_menu,
    btn_dodaj, btn_edytuj, btn_usun
]

ustaw_formularz_domy()
odswiez_listy()
rysuj_markery_klasy()

root.mainloop()
