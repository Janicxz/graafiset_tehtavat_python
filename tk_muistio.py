from tkinter import *
from tkinter.ttk import *
from datetime import datetime
from tkinter import messagebox, filedialog, simpledialog, font
from tkinter.scrolledtext import ScrolledText
from tkinter.colorchooser import askcolor

from PIL import Image,ImageTk, ImageColor
from fpdf import *
import pypdf

#Vaatii PIL, FPDF, pypdf
# pip install pillow
# pip install FPDF
# pip install pypdf

# Omat ominaisuudet:
#-Kysy haluatko lopettaa vain jos tekstiä syötetty
#-Pimeä tila
#-Undo
#-Hotkeyt

#pääikkuna
ikkuna = Tk()
ikkuna.title("Muistio Pythonilla toteutettuna")
#ikkuna.resizable(0,0)
ikkuna.geometry("850x650")

notepad = ScrolledText(ikkuna, width = 100, height = 35, undo = True)
notepad.pack(fill="both", expand=True)
tiedostonimi = ""

def cmdUusiBind(event):
    cmdUusi()

def cmdUusi():
    global tiedostonimi
    if len(notepad.get("1.0", END+"-1c")) > 0:
        if messagebox.askyesno("Muistio", "Haluatko tallentaa muutokset?"):
            cmdTallenna()
        else:
            notepad.delete(0.0, END)
def cmdAvaaBind(event):
    cmdAvaa()

def cmdAvaa():
    try:
        fd = filedialog.askopenfile(parent=ikkuna, mode='r')
        if fd.name.endswith(".pdf"):
            tiedosto = _avaaPDF(fd.name)
        else:
            tiedosto = fd.read()
        notepad.delete(0.0, END)
        notepad.insert(0.0, tiedosto)
    except:
        pass

def _avaaPDF(tiedosto_nimi: str):
    global lisatyt_kuvat
    pdf = pypdf.PdfReader(tiedosto_nimi)
    teksti = ""
    for page in pdf.pages:
        teksti += page.extract_text()
        #TODO
#        for kuva in page.images:
#            lisattavaKuva = ImageTk.PhotoImage(kuva.image)
#            # Estä GC tuhoamasta lisätyt kuvat
#            lisatyt_kuvat.append((lisattavaKuva, ""))
#            notepad.image_create("current", image=lisattavaKuva)
    return teksti

def cmdTallennaBind(event):
    cmdTallenna()

def cmdTallenna():
    fd = filedialog.asksaveasfile(mode='w', defaultextension='.txt', filetypes=[("Text file", ".txt"), ("PDF file", ".pdf")])
    if fd != None:
        data = notepad.get("1.0", END)
    try:
        if fd.name.endswith(".pdf"):
            _tallennaPDF(data, fd.name)
        else:
            fd.write(data)
    except Exception as ex:
        print(ex)
        if fd:
            messagebox.showerror(title="Virhe", message="Tallentaminen ei onnistunut!")
def cmdTallennaNimellaBind(event):
    cmdTallennanimella()

def cmdTallennanimella():
    fd = filedialog.asksaveasfile(mode='w', defaultextension='.txt', filetypes=[("Text file", ".txt"), ("PDF file", ".pdf")])

    if fd != None:
        teksti = notepad.get(0.0, END)
    try:
        if fd.name.endswith(".pdf"):
            _tallennaPDF(teksti, fd.name)
        else:
            fd.write(teksti.rstrip())
    except Exception as ex:
        print(ex)
        if fd:
            messagebox.showerror(title="Virhe", message="Tallentaminen ei onnistunut!")

def _tallennaPDF(teksti: str, tiedosto_nimi: str):
    global fonttiAsetukset, lisatyt_kuvat
    fonttiNimi = fonttiAsetukset["fontti"]
    fonttiKoko = fonttiAsetukset["koko"].get()
    fonttiTyyli = ""
    fonttiVari = ImageColor.getrgb(fonttiAsetukset["vari"])
    # Fonttia ei ole valittu erikseen, default asetukset.
    if fonttiKoko == 0:
        fonttiKoko = 10
    if fonttiAsetukset["kursivoi"].get():
        fonttiNimi = fonttiNimi.replace(" italic", "")
        fonttiTyyli += "I"
    if fonttiAsetukset["lihavoi"].get():
        fonttiNimi = fonttiNimi.replace(" bold", "")
        fonttiTyyli += "B"
    if fonttiNimi == "system":
        fonttiNimi = "Arial"

    pdf = FPDF()
    pdf.add_page()
    #pdf.add_font(family=fonttiNimi, style=fonttiTyyli)
    pdf.set_font(family=fonttiNimi, style=fonttiTyyli, size=fonttiKoko)
    # Ei tulosteta valkoista tekstiä valkoiselle taustalle jos yötila on käytössä.
    if fonttiAsetukset["vari"] != "white" and fonttiAsetukset["vari"] != "systemwindowtext":
        pdf.set_text_color(fonttiVari[0], fonttiVari[1], fonttiVari[2])
    pdf.multi_cell(40, 10, teksti)
    #TODO
    for kuva in lisatyt_kuvat:
        pdf.image(name=kuva[1], w=100, h=100)
        #pdf.cell(link=pdf.image(name=kuva[1]))
    pdf.output(tiedosto_nimi)

def cmdLopeta(*args):
    if len(notepad.get("1.0", END+"-1c")) == 0 or messagebox.askyesno("Muistio", "Haluatko lopettaa?"):
        ikkuna.destroy()

def cmdLeikkaa(*args):
    notepad.event_generate("<<Cut>>")

def cmdKopioi(*args):
    notepad.event_generate("<<Copy>>")

def cmdLiita(*args):
    notepad.event_generate("<<Paste>>")

def cmdTyhjenna(*args):
    notepad.event_generate("<<Clear>>")

def cmdEtsiBind(event):
    cmdEtsi()

def cmdEtsi():
    notepad.tag_remove("Found", "1.0", END)
    find = simpledialog.askstring("Etsi", "Mitä haluat etsiä:")

    if find:
        index = '1.0'
        while 1:
            index = notepad.search(find, index, nocase = 1, stopindex = END)
            if not index:
                break
            lastindex = "%s+%dc" %(index, len(find))
            notepad.tag_add("Löytyi:", index, lastindex)
            index = lastindex
        notepad.tag_config("Löytyi:", foreground = "white", background = "blue")
        notepad.bind("<1>", notepad_etsi_m1_click)

def notepad_etsi_m1_click(e: Event):
    notepad.tag_config("Löytyi:", background= "white", foreground= "black")
    notepad.tag_remove("Löytyi:", "1.0", END)

def cmdValitsekaikki():
    notepad.event_generate("<<SelectAll>>")

def cmdTimeDateBind(event):
    cmdTimeDate()

def cmdTimeDate():
    now = datetime.now()

    dtString = now.strftime("%d/%m/%Y %H:%M:%S")
    label = messagebox.showinfo("Aika/Päiväys", dtString)

def cmdOhje():
    label = messagebox.showinfo("Yleistä", "Muistio")
def cmdTulostaBind(e: Event):
    cmdTulosta()

def cmdTulosta():
    pass

def cmdYoTila():
    _bg = notepad.cget("bg")
    _fg = notepad.cget("fg")
    print(_bg)
    if _bg == "SystemWindow":
        _bg = "black"
        if _fg == "SystemWindowText" or _fg == "black" or _fg == "#000000":
            _fg = "white"
    else:
        _bg = "SystemWindow"
        if _fg == "white":
            _fg = "SystemWindowText"
    print(f"notepad bg {_bg} fg {_fg}")
    fonttiAsetukset["vari"] = _fg
    notepad.config(bg=_bg, fg=_fg)

def cmdHiiriOikea(e: Event):
    valikko = Menu(None, tearoff=0, takefocus=0)
    valikko.add_command(label="Peruuta", command=cmdPeruuta)
    valikko.add_command(label="Tee uudelleen", command=cmdTeeUudelleen)
    valikko.add_separator()
    valikko.add_command(label="Leikkaa", command=cmdLeikkaa)
    valikko.add_command(label="Kopioi", command=cmdKopioi)
    valikko.add_command(label="Liitä", command=cmdLiita)
    valikko.add_command(label="Poista", command=cmdTyhjenna)

    valikko.tk_popup(e.x_root, e.y_root, entry="0")

def cmdTeeUudelleen(*args):
    try:
        notepad.edit_redo()
    except:
        pass

def cmdPeruuta(*args):
    try:
        notepad.edit_undo()
    except:
        pass

def cmdLisaaKuvaBind(e: Event):
    cmdLisaaKuva()

lisatyt_kuvat = []
def cmdLisaaKuva():
    global lisatyt_kuvat
    kuvaTiedosto = filedialog.askopenfilename(title = "Valitse lisättävä kuva", filetypes=[("Kuva", "*.gif"), ("Kuva", "*.jpg"), ("Kuva", "*.png")])
    pienempikuva = Image.open(kuvaTiedosto)
    pienempikuva = pienempikuva.resize((350,350))
    lisattavaKuva = ImageTk.PhotoImage(pienempikuva)
    # Estä GC tuhoamasta lisätyt kuvat
    lisatyt_kuvat.append((lisattavaKuva, kuvaTiedosto))
    notepad.image_create("current", image=lisattavaKuva)
    # TODO?
    #notepad.tag_add(kuvaTiedosto)

###
# Fontti ikkuna
###
def _fonttiOk():
    global fonttiIkkuna, fonttiAsetukset
    fontti = font.Font(family=fonttiAsetukset["fontti"], size=fonttiAsetukset["koko"].get())
    notepad.config(font=fontti, fg=fonttiAsetukset["vari"])

    if fonttiIkkuna:
        fonttiIkkuna.destroy()

def _fonttiPeruuta():
    global fonttiIkkuna
    if fonttiIkkuna:
        fonttiIkkuna.destroy()
def _fonttiVariValinta():
    vari = askcolor(title="Fontin värivalinta")
    fonttiAsetukset["vari"] = vari[1]
    fonttiEsimerkkiTeksti.config(fg=vari[1])
    fonttiIkkuna.focus()

def _fonttiEsikatsele(event: Event):
    global fonttiValintaGrid, fonttiEsimerkkiFont, fonttiAsetukset
    fonttiNimi = fonttiValintaGrid.get(fonttiValintaGrid.curselection())
    fonttiAsetukset["fontti"] = fonttiNimi

    if fonttiNimi:
        _fonttiKursivoi()
        _fonttiLihavoi()

        koko = fonttiAsetukset["koko"].get()
        fonttiEsimerkkiFont.config(family=fonttiNimi, size=koko)

def _fonttiKursivoi():
    fonttiNimi = fonttiAsetukset["fontti"]
    if fonttiAsetukset["kursivoi"].get():
        fonttiNimi += " italic"
    else:
        fonttiNimi = fonttiNimi.replace("italic", "")
    fonttiEsimerkkiFont.config(family=fonttiNimi)
    fonttiAsetukset["fontti"] = fonttiNimi
    #print(fonttiNimi)

def _fonttiLihavoi():
    fonttiNimi = fonttiAsetukset["fontti"]
    if fonttiAsetukset["lihavoi"].get():
        fonttiNimi += " bold"
    else:
        fonttiNimi = fonttiNimi.replace("bold", "")
    fonttiEsimerkkiFont.config(family=fonttiNimi)
    fonttiAsetukset["fontti"] = fonttiNimi
    #print(fonttiNimi)

fonttiIkkuna = None
fonttiEsimerkkiTeksti = None
fonttiEsimerkkiFont = None
fonttiValintaGrid = None
fonttiAsetukset = {"koko": IntVar(),
                    "fontti": "system",
                    "lihavoi": BooleanVar(),
                    "kursivoi": BooleanVar(),
                    "vari": "black"}

def cmdFontti():
    global fonttiIkkuna, fonttiEsimerkkiTeksti, fonttiValintaGrid, fonttiEsimerkkiFont

    #Alusta
    fonttiAsetukset["koko"].set(10)
    fonttiAsetukset["lihavoi"].set(False)
    fonttiAsetukset["kursivoi"].set(False)

    print(fonttiAsetukset["koko"].get())

    #Fonttivalikon ikkuna
    fonttiIkkuna = Toplevel(ikkuna)
    fonttiIkkuna.title("Valitse fontti")
    fonttiIkkuna.geometry("500x500")
    fonttiIkkuna.pack_propagate(0)

    #Fontti-listan scrollbar
    fonttiVieritys = Scrollbar(fonttiIkkuna)
    fonttiVieritys.grid(row=0,column=1, sticky="nsw")

    #Fontti-lista
    fonttiValintaGrid = Listbox(fonttiIkkuna, height=10)
    fonttiValintaGrid.grid(row=0, sticky="nswe")

    #FonttiListan scrollbar asetukset
    fonttiValintaGrid.config(yscrollcommand=fonttiVieritys.set)
    fonttiVieritys.config(command = fonttiValintaGrid.yview)

    fonttiEsimerkkiFont = font.Font(family='arial')

    for fontti in font.families():
        fonttiValintaGrid.insert('end', fontti)

    fonttiValintaGrid.bind("<ButtonRelease-1>", _fonttiEsikatsele)

    #Preview textbox
    fonttiEsimerkkiFrame = Frame(fonttiIkkuna, width=200, height=200)
    fonttiEsimerkkiFrame.grid(row=0, column=2, sticky="w")
    fonttiEsimerkkiFrame.grid_propagate(False)
    fonttiEsimerkkiTeksti = Text(fonttiEsimerkkiFrame, font=fonttiEsimerkkiFont, width=40, height=10)
    fonttiEsimerkkiTeksti.insert('end', "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum")
    fonttiEsimerkkiTeksti.grid(row=0, column=2)

    #Koko entry
    Label(fonttiIkkuna, text="Koko").grid(row=1, column=0)
    fonttiKokoEntry = Entry(fonttiIkkuna, textvariable=fonttiAsetukset["koko"]).grid(row=1, column=1)
    #fonttiAsetukset["koko"].trace_add('write', fonttiKokoCallback)
    Label(fonttiIkkuna, text="Lihavoi").grid(row=2,column=0)
    Checkbutton(fonttiIkkuna, variable=fonttiAsetukset["lihavoi"], onvalue=True, offvalue=False, command=_fonttiLihavoi).grid(row=2, column=1, sticky="w")

    Label(fonttiIkkuna, text="Kursivoi").grid(row=3,column=0)
    Checkbutton(fonttiIkkuna, variable=fonttiAsetukset["kursivoi"], onvalue=True, offvalue=False, command=_fonttiKursivoi).grid(row=3, column=1, sticky="w")
    #Napit
    Button(fonttiIkkuna, command=_fonttiOk, text="Ok").grid(row=4, column=0)
    Button(fonttiIkkuna, command=_fonttiPeruuta, text="Peruuta").grid(row=4, column=1, sticky="W")
    Button(fonttiIkkuna, command=_fonttiVariValinta, text="Valitse väri").grid(row=4, column=2, sticky="W")
###
# Fontti ikkuna loppu
###

#Muistion valikot
muistioValikko = Menu(ikkuna)
ikkuna.configure(menu=muistioValikko)

#Tiedosto-valikko
tiedostoValikko = Menu(muistioValikko, tearoff= False)
muistioValikko.add_cascade(label="Tiedosto", menu=tiedostoValikko)

#Alavalikot
tiedostoValikko.add_command(label="Uusi   Ctrl-N", command=cmdUusi)
tiedostoValikko.add_command(label="Avaa...   Ctrl-O", command=cmdAvaa)
tiedostoValikko.add_command(label="Tallenna   Ctrl-S", command=cmdTallenna)
tiedostoValikko.add_command(label="Tallenna nimellä...   Ctrl-Shift-S", command=cmdTallennanimella)
tiedostoValikko.add_separator()
#tiedostoValikko.add_command(label="Tulosta   Ctrl-P", command=cmdTulosta)
#tiedostoValikko.add_separator()
tiedostoValikko.add_command(label="Lopeta", command=cmdLopeta)

#Muokkaa valikko
muokkaaMenu = Menu(muistioValikko, tearoff= False)
muistioValikko.add_cascade(label="Muokkaa", menu=muokkaaMenu)

#Alavalikot
muokkaaMenu.add_command(label="Leikkaa   Ctrl-X", command=cmdLeikkaa)
muokkaaMenu.add_command(label="Kopioi   Ctrl-C", command=cmdKopioi)
muokkaaMenu.add_command(label="Liitä    Ctrl-V", command=cmdLiita)
muokkaaMenu.add_command(label="Poista   Del", command=cmdTyhjenna)
muokkaaMenu.add_separator()
muokkaaMenu.add_command(label="Etsi...   Ctrl-F", command=cmdEtsi)
muokkaaMenu.add_command(label="Lisää kuva   Ctrl-I", command=cmdLisaaKuva)
muokkaaMenu.add_separator()
muokkaaMenu.add_command(label="Valitse kaikki   Ctrl-A", command=cmdValitsekaikki)
muokkaaMenu.add_command(label="Time/Date    Ctrl-T", command=cmdTimeDate)

#Asetukset
asetuksetMenu = Menu(muistioValikko, tearoff= False)
muistioValikko.add_cascade(label="Asetukset", menu=asetuksetMenu)

#Alavalikot
asetuksetMenu.add_command(label="Fontti...", command=cmdFontti)
asetuksetMenu.add_command(label="Yötila/Tumma tila", command=cmdYoTila)

#Ohjevalikko
ohjeValikko = Menu(muistioValikko, tearoff= False)
muistioValikko.add_cascade(label="Ohje", menu=ohjeValikko)

#Yleistä-valikko
ohjeValikko.add_command(label="Yleistä", command=cmdOhje)

#Pikanäppäimet/Hotkeyt
notepad.bind("<Control-f>", cmdEtsiBind)
notepad.bind("<Control-s>", cmdTallennaBind)
# Ctrl-Shift-S
notepad.bind("<Control-S>", cmdTallennaNimellaBind)
notepad.bind("<Control-n>", cmdUusiBind)
notepad.bind("<Control-o>", cmdAvaaBind)
notepad.bind("<Control-p>", cmdTulostaBind)
notepad.bind("<Control-t>", cmdTimeDateBind)
notepad.bind("<Control-i>", cmdLisaaKuvaBind)
notepad.bind("<Button-3>", cmdHiiriOikea)

# Lopeta event
ikkuna.protocol("WM_DELETE_WINDOW", cmdLopeta)

ikkuna.mainloop()