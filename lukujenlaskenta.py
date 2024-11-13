from tkinter import *
from tkinter import constants

class UI():
    def __init__(self, root):
        self._root = root
        self._eka_nro = DoubleVar()
        self._toka_nro = DoubleVar()

    def start(self):
        self._root.geometry("600x500")
        self._root.columnconfigure(1, weight=1, minsize=300)

        Label(self._root, text="Annatko ensimmäisen numeron:").grid(row=0, column=0)
        Label(self._root, text="Annatko toisen numeron:").grid(row=1, column=0)

        self._vastaus = Label(self._root)
        self._vastaus.grid(row=3, column=1)
        self._entry1 = Entry(self._root, textvariable=self._eka_nro).grid(row=0, column=1, sticky=(constants.E, constants.W), padx=5, pady=5)
        self._entry2 = Entry(self._root, textvariable=self._toka_nro).grid(row=1, column=1, sticky=(constants.E, constants.W), padx=5, pady=5)
        self._laskenappi = Button(self._root, text="Laske yhteen!", command=self._laske_yhteen).grid(row=2, column=1)

    def _laske_yhteen(self):
        try:
            yhteensa = self._eka_nro.get() + self._toka_nro.get()
            self._vastaus.config(text=f"Yhteensä: {round(yhteensa, 2)}")
        except TclError as virhe:
            print(virhe.args)
            self._vastaus.config(text=f"Virheellinen syöte!\nVain numeroita kiitos!")

if __name__ == "__main__":
    ikkuna = Tk()
    ui = UI(ikkuna)
    ui.start()

    ikkuna.mainloop()
