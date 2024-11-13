from tkinter import *

class Asiakasikkuna:

    def __init__(self):
        self.__ikkuna = Tk()
        self.__ikkuna.title("ASIAKASIKKUNA")
        self.__labelasnro=Label(self.__ikkuna, text = "Asiakas nro:")
        self.__tekstiasnro=Entry(self.__ikkuna, width = 25)
        self.__labelnimi=Label(self.__ikkuna, text = "Nimi:")
        self.__tekstinimi=Entry(self.__ikkuna, width = 25)
        self.__labelosoite=Label(self.__ikkuna, text = "Osoite:")
        self.__tekstiosoite=Entry(self.__ikkuna, width = 25)
        self.__labelpuhelin=Label(self.__ikkuna, text = "Puhelin:")
        self.__tekstipuhelin=Entry(self.__ikkuna, width = 25)
        self.__labelsposti=Label(self.__ikkuna, text = "Sähköposti:")
        self.__tekstisposti=Entry(self.__ikkuna, width = 25)
        self.__nappitallenna = Button(self.__ikkuna,
                                      text = "Tallenna",
                                      command = self.tallenna)

        self.__labelasnro.grid(row=0,column=0,sticky=W)
        self.__tekstiasnro.grid(row=0,column=1)
        self.__labelnimi.grid(row=1,column=0,sticky=W)
        self.__tekstinimi.grid(row=1,column=1)
        self.__labelosoite.grid(row=2,column=0,sticky=W)
        self.__tekstiosoite.grid(row=2,column=1)
        self.__labelpuhelin.grid(row=3,column=0,sticky=W)
        self.__tekstipuhelin.grid(row=3,column=1)
        self.__labelsposti.grid(row=4,column=0,sticky=W)
        self.__tekstisposti.grid(row=4,column=1)
        self.__nappitallenna.grid(row=5,column=1)

        mainloop()

    def tallenna(self):
        pass

oma_ikkuna = Asiakasikkuna()