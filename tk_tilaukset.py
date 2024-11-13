from tkinter import *
from tkinter import constants, messagebox

class UI():
    def __init__(self, root):
        self._root = root
        self._tuote_maara = IntVar()
        self._tuote_hinta = DoubleVar()
        self._maksutapa = IntVar()

    def start(self):
        self._root.geometry("600x500")
        #self._root.columnconfigure(1, weight=1, minsize=300)

        Label(self._root, text="Lasken tilauksen loppusumman huomioiden tilausmäärän, a'-hinnan ja maksutavan:").grid(row=0, column=0)
        Label(self._root, text="Annatko ostettavan tuotteen määrät:").grid(row=1, column=0)
        Label(self._root, text="Annatko ostettavan tuotteen hinnan:").grid(row=2, column=0)

        self._vastaus = Label(self._root)
        self._vastaus.grid(row=7, column=1)
        self._entry1 = Entry(self._root, textvariable=self._tuote_maara).grid(row=1, column=1, sticky=(constants.E, constants.W), padx=5, pady=5)
        self._entry2 = Entry(self._root, textvariable=self._tuote_hinta).grid(row=2, column=1, sticky=(constants.E, constants.W), padx=5, pady=5)

        self._maksutapa_r1 = Radiobutton(self._root, text="Käteinen + 3 % lisää hintaa", variable=self._maksutapa, value=0).grid(row=3, column=0, sticky=constants.W)
        self.maksutapa_r2 = Radiobutton(self._root, text="VISA - 2 % alennus", variable=self._maksutapa, value=1).grid(row=4, sticky=constants.W)
        self.maksutapa_r3 = Radiobutton(self._root, text="OP tilisiirto - 4 % alennus", variable=self._maksutapa, value=2).grid(row=5, sticky=constants.W)

        self._laskenappi = Button(self._root, text="Laske yhteen!", command=self.Laskeyhteensa).grid(row=6, column=1)

    def Maksutavanvalinta(self):
        hinnan_muutos = 0
        try:
            valinta = self._maksutapa.get()
        except:
            self._vastaus.config(text=f"Virhe, maksutapaa ei ole valittu!")
            return

        #  Käteinen + 3 %
        if valinta == 0:
            hinnan_muutos = 3
        # VISA - 2 %
        elif valinta == 1:
            hinnan_muutos = -2
        # OP Tilinsiirto - 4 %
        elif valinta == 2:
            hinnan_muutos = -4
        return hinnan_muutos


    def Laskeyhteensa(self):
        _hinta_maksutapa = self.Maksutavanvalinta()
        if _hinta_maksutapa == 0:
            return

        try:
            yhteensa = self._tuote_hinta.get() * (1 + _hinta_maksutapa / 100) * self._tuote_maara.get()
            self._vastaus.config(text=f"Yhteensä: {round(yhteensa, 2)}")
            messagebox.showinfo(message=f"Yhteensä: {round(yhteensa, 2)}")
        except TclError as virhe:
            print(virhe.args)
            self._vastaus.config(text=f"Virheellinen syöte!\nVain numeroita kiitos!")

if __name__ == "__main__":
    ikkuna = Tk()
    ui = UI(ikkuna)
    ui.start()

    ikkuna.mainloop()
