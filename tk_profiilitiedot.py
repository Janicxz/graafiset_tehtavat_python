

from tkinter import *

root = Tk()
root.title("Rekisteröinti-ikkuna Gridillä")
root.geometry("500x300")   # asetetaan aloitusikkunan koko
root.maxsize(500, 300)     # leveys x korkeus
root.config(bg="lightgrey")

# Profiilin kuva
image = PhotoImage(file="profiiliKuva.gif")
small_img = image.subsample(4,4)

img = Label(root, image=small_img)
img.grid(row=0, column=0, rowspan=6, padx=5, pady=5)

# Seuraavissa widgeteissä syötetään profiilin tiedot
enter_info = Label(root, text="Syötä tietosi: ", bg="lightgrey")
enter_info.grid(row=0, column=1, columnspan=4, padx=5, pady=5)

# Nimi label ja syöttökentän (entry) widgets
Label(root, text="Nimi", bg="lightgrey").grid(row=1, column=1, padx=5, pady=5, sticky=E)

nimi = Entry(root, bd=3)
nimi.grid(row=1, column=2, padx=5, pady=5)

# Sukupuoli label ja alasveto widgets
sukupuoli = Menubutton(root, text="Sukupuoli")
sukupuoli.grid(row=2, column=2, padx=5, pady=5, sticky=W)
sukupuoli.menu = Menu(sukupuoli, tearoff=0)
sukupuoli["menu"] = sukupuoli.menu

# Valitaan sukupuoli alasvetovalikosta
sukupuoli.menu.add_cascade(label="Mies")
sukupuoli.menu.add_cascade(label="Nainen")
sukupuoli.menu.add_cascade(label="Muu")
sukupuoli.grid()

# Silmien väri label jä syöttökentän (entry) widgets
Label(root, text="Silmien väri", bg="lightgrey").grid(row=3, column=1, padx=5, pady=5, sticky=E)
silmat = Entry(root, bd=3)
silmat.grid(row=3, column=2, padx=5, pady=5)

# Paino ja pituus labelit ja syöttökenttien (entry) widgets
Label(root, text="Paino", bg="lightgrey").grid(row=4, column=1, padx=5, pady=5, sticky=E)
Label(root, text="kiloa", bg="lightgrey").grid(row=4, column=3, sticky=W)

paino = Entry(root, bd=3)
paino.grid(row=4, column=2, padx=5, pady=5)

Label(root, text="Pituus", bg="lightgrey").grid(row=5, column=1, padx=5, pady=5, sticky=E)
Label(root, text="senttiä", bg="lightgrey").grid(row=5, column=3, sticky=W)

pituus = Entry(root, bd=3)
pituus.grid(row=5, column=2, padx=5, pady=5)

root.mainloop()