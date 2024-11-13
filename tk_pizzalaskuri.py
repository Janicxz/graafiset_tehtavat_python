from tkinter import *
from tkinter import constants, messagebox

from fpdf import FPDF

class UI():
    def __init__(self, root):
        self._root = root
        self._pizza_koko = IntVar()
        self._pizza_maara = IntVar()
        self._pizza_hinta = DoubleVar()
        self._tilaus_yhteensa = DoubleVar()
        self._maksutapa_etu = DoubleVar()
        self._hinnanmuokkaus_sallittu = BooleanVar()

        self._taytteet = [("Kinkku", 0.75), ("Ananas", 0.50), ("Meetwursti", 0.50), ("Kana", 0.50), ("Herkkusieni", 0.50), ("Aurajuusto", 0.50)]
        self._maksutavat = [("VISA (0%)", 0), ("Käteinen (-10%)", -10), ("Pankkikortti (+5%)", 5)]
        self._taytteet_var= []


    def start(self):
        self._root.geometry("900x650")
        #self._root.columnconfigure(1, weight=1, minsize=300)

        Label(self._root, text="Lasken pizzan hinnan ja tilauksen loppusumman huomioiden tilausmäärän ja a'-hinnan:").grid(row=0, column=0, sticky=constants.W)
        Label(self._root, text="Valitse pizzan koko:").grid(row=1, column=0, sticky=constants.W)

        self._pizza_r1 = Radiobutton(self._root, text="Normaali 5 €", variable=self._pizza_koko, value=5, command=self._muuta_hinta).grid(column=0, sticky=constants.W)
        self._pizza_r2 = Radiobutton(self._root, text="Perhe 9 €", variable=self._pizza_koko, value=9, command=self._muuta_hinta).grid(column=0, sticky=constants.W)

        Label(self._root, text="Valitse täytteet").grid(column=0, sticky=constants.W)

        for tayte in self._taytteet:
            tayte_var = DoubleVar()
            Checkbutton(self._root, text=f"{tayte[0]} + {tayte[1]} €", onvalue=tayte[1], offvalue=0, variable=tayte_var, command=self._muuta_hinta).grid(sticky=constants.W)
            self._taytteet_var.append(tayte_var)

        Label(self._root, text="Annatko pizzojen määrät:").grid(column=0, sticky=constants.W)
        self._pizza_maara_entry = Entry(self._root, textvariable=self._pizza_maara).grid(row=self._root.grid_size()[1]-1, column=1,sticky=constants.W)
        self._pizza_maara.set(1)

        Label(self._root, text="Pizzan hinta:").grid(column=0, sticky=constants.W)
        self._pizza_hinta_entry = Entry(self._root, textvariable=self._pizza_hinta, state="readonly")
        self._pizza_hinta_entry.grid(row=self._root.grid_size()[1]-1, column=1,sticky=constants.W)
        self_pizza_hinta_muokkaus = Checkbutton(self._root, variable=self._hinnanmuokkaus_sallittu, text="Pizzan hinnan muokkaus", onvalue=True, offvalue=False, command=self._tarkista_hinnan_muokkaus).grid(sticky=constants.W)

        Label(self._root, text="Maksutapa:").grid(sticky=constants.W)
        col = 1
        for maksutapa in self._maksutavat:
            Radiobutton(self._root, text=maksutapa[0], value=maksutapa[1], variable=self._maksutapa_etu, command=self._muuta_hinta).grid(row=self._root.grid_size()[1]-1, column=col, sticky=constants.W)
            col += 1

        self._tilaa_nappi = Button(self._root, text="Tilaa pizza", command=self._tilaa_pizza).grid(sticky=constants.W)

        Label(self._root, text="Kassakuitti").grid(sticky=constants.W)
        self._kuitti_text = Text(self._root, state=DISABLED, width=50, height=10)
        self._kuitti_text.grid(sticky=constants.W)

        Button(self._root, text="Tulosta kuitti", command=self._tulosta_kuitti).grid(sticky=constants.W, pady=5)
        Button(self._root, text="Poista tilaus", command=self._poista_tilaus).grid(row=self._root.grid_size()[1]-1, column=1, sticky=constants.W, pady=5)

        Label(self._root, text="Tilaus maksaa yhteensä:").grid(column=0, sticky=constants.W)
        self._tilaus_yhteensa_entry = Entry(self._root, textvariable=self._tilaus_yhteensa, state="readonly")
        self._tilaus_yhteensa_entry.grid(row=self._root.grid_size()[1]-1, column=1,sticky=constants.W)

    def _poista_tilaus(self):
        self._tilaus_yhteensa.set(0)
        self._kuitti_text.configure(state=NORMAL)
        self._kuitti_text.delete('1.0', END)
        self._kuitti_text.configure(state=DISABLED)

    def _tulosta_kuitti(self):
        kuitti_teksti = "Kuitti\n"
        kuitti_teksti += self._kuitti_text.get("1.0", END)
        kuitti_teksti += f"Tilaus yhteensä: {self._tilaus_yhteensa.get()}"

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', '', 7)
        pdf.multi_cell(0,7, kuitti_teksti)
        pdf.output('kuitti.pdf', 'F')

        messagebox.showinfo(message="Kuitti tulostettu tiedostoon kuitti.pdf")

    def _tarkista_hinnan_muokkaus(self):
        if self._hinnanmuokkaus_sallittu.get():
            self._pizza_hinta_entry.configure(state=NORMAL)
        else:
            self._pizza_hinta_entry.configure(state="readonly")

    def _muuta_hinta(self):
        self._pizza_hinta_entry.configure(state=NORMAL)
        self._pizza_hinta.set(self._laske_pizzan_hinta())
        self._tarkista_hinnan_muokkaus()

    def _laske_pizzan_hinta(self):
        hinta_yht = 0
        try:
            hinta_yht += self._pizza_koko.get()
            for tayte in self._taytteet_var:
                hinta_yht += tayte.get()

            maksutapa = self._maksutapa_etu.get()
            if maksutapa != 0:
                hinta_yht *= (1 + maksutapa / 100)
        except:
            messagebox.showinfo(message=f"Virheellinen määrä tai hinta!\nVain numeroita kiitos!")

        return round(hinta_yht, 2)

    def _lisaa_kuitti_teksti(self, teksti: str):
        self._kuitti_text.configure(state=NORMAL)
        self._kuitti_text.insert(END,teksti)
        self._kuitti_text.configure(state=DISABLED)

    def _tilaa_pizza(self):
        try:
            pizzan_hinta = float(self._pizza_hinta_entry.get())
            yhteensa = pizzan_hinta * self._pizza_maara.get()
            yhteensa = round(yhteensa, 2)

            koko_tilaus_yhteensa = round(self._tilaus_yhteensa.get() + yhteensa, 2)
            self._tilaus_yhteensa_entry.configure(state=NORMAL)
            self._tilaus_yhteensa.set(koko_tilaus_yhteensa)
            self._tilaus_yhteensa_entry.configure(state="readonly")

            kuitti_teksti = f"Määrä: {self._pizza_maara.get()} Hinta: {pizzan_hinta} Yhteensä: {yhteensa}\n"
            self._lisaa_kuitti_teksti(kuitti_teksti)

        except:
            messagebox.showinfo(message=f"Virheellinen määrä tai hinta!\nVain numeroita kiitos!")

if __name__ == "__main__":
    ikkuna = Tk()
    ui = UI(ikkuna)
    ui.start()

    ikkuna.mainloop()
