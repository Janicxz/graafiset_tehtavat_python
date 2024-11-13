import tkinter.simpledialog
import turtle
import time
import random
import csv
import tkinter.messagebox

# Uudet ominaisuudet:
# Esc lopettaa, X painaminen ei kaada peliä.
# Aika ja pisteet teksti
# Pisteiden tallennus

# asetukset
viive = 0.1
pisteet = 0
pistelista = [("Tyhjä", 0), ("Tyhjä", 0), ("Tyhjä", 0)]

# Ruudun asetukset
ikkuna = turtle.Screen()
ikkuna.title("Matopeli - F1) Pisteet P) Tauko")
ikkuna.bgcolor("black")
ikkuna.setup(width=600, height=600)
ikkuna.tracer(0)

# Mato
mato = turtle.Turtle()
mato.shape("square")
mato.color("green")
mato.penup()
mato.goto(0, 0)
mato.direction = "stop"

# Omena
omena = turtle.Turtle()
omena.speed(0)
omena.shape("circle")
omena.color("red")
omena.penup()
omena.goto(0, 100)

# Mato kehon osat
keho_osat = []

# Ohjauskomennot
def mene_ylos():
    if mato.direction != "down":
        mato.direction = "up"
def mene_alas():
    if mato.direction != "up":
        mato.direction = "down"
def mene_vasemmalle():
    if mato.direction != "right":
        mato.direction = "left"
def mene_oikealle():
    if mato.direction != "left":
        mato.direction = "right"
def liiku():
    if mato.direction == "up":
        y = mato.ycor()
        mato.sety(y + RUUTU_KOKO)
    if mato.direction == "down":
        y = mato.ycor()
        mato.sety(y - RUUTU_KOKO)
    if mato.direction == "left":
        x = mato.xcor()
        mato.setx(x - RUUTU_KOKO)
    if mato.direction == "right":
        x = mato.xcor()
        mato.setx(x + RUUTU_KOKO)

def lopeta():
    global kaynnissa
    kaynnissa = False


def nayta_pisteet():
    global pistelista
    tkinter.messagebox.showinfo("Parhaat pisteet", f"Top 3:\n1) {pistelista[0][0]} ({pistelista[0][1]})\n2) {pistelista[1][0]} ({pistelista[1][1]})\n3) {pistelista[2][0]} ({pistelista[2][1]})")

def tauko():
    global peli_tauko, teksti_tauko, edellinen_aika
    peli_tauko = not peli_tauko

    if peli_tauko:
        teksti_tauko.color("red")
        teksti_tauko.penup()
        teksti_tauko.setpos(TEKSTI_TAUKO_POS[0], TEKSTI_TAUKO_POS[1])
        teksti_tauko.write("TAUKO\n Paina P Jatkaaksesi", font=("Arial", 15, "bold"))
        teksti_tauko.hideturtle()
    else:
        teksti_tauko.setpos(1000, 1000)
        teksti_tauko.clear()
        # Älä laske tauolla kulunutta aikaa
        edellinen_aika = time.time()

# Näppäinohjaus
ikkuna.listen()
ikkuna.onkey(mene_ylos, "Up")
ikkuna.onkey(mene_alas, "Down")
ikkuna.onkey(mene_vasemmalle, "Left")
ikkuna.onkey(mene_oikealle, "Right")
ikkuna.onkey(lopeta, "Escape")
ikkuna.onkey(tauko, "p")
ikkuna.onkey(nayta_pisteet, "F1")
# Jos ikkuna suljetaan muualta, kutsu lopeta funktiota
ikkuna._root.protocol("WM_DELETE_WINDOW", lopeta)

# Teksti
aika = 0
teksti_pisteet = turtle.Turtle()
teksti_peli_loppu = turtle.Turtle()
teksti_tauko = turtle.Turtle()

RUUTU_KOKO = 20
RUUTU_LEVEYS = 30
RUUTU_PITUUS = 30

REUNAT_X = (-290, 290)
REUNAT_Y = (-290, 290)
TEKSTI_TAUKO_POS = (-80, 0)
TEKSTI_PELI_LOPPU_POS = (-80, 0)
TEKSTI_PISTEET_AIKA_POS = (-250, 250)

def paivita_teksti():
    global teksti_pisteet
    teksti_pisteet.clear()

    teksti_pisteet.color("red")
    teksti_pisteet.penup()
    teksti_pisteet.setpos(TEKSTI_PISTEET_AIKA_POS[0], TEKSTI_PISTEET_AIKA_POS[1])
    teksti_pisteet.write(f"Pisteet: {pisteet} \nAika {round(aika, 2)}", font=("Arial", 15, "normal"))
    teksti_pisteet.hideturtle()

def uusi_peli():
    global pisteet, viive, aika, mato, omena, teksti_peli_loppu

    # Näytä gameover teksti
    teksti_peli_loppu.color("red")
    teksti_peli_loppu.penup()
    teksti_peli_loppu.setpos(TEKSTI_PELI_LOPPU_POS[0], TEKSTI_PELI_LOPPU_POS[1])
    teksti_peli_loppu.write("Peli loppui. Game over!", font=("Arial", 15, "bold"))

    # Tarkista hiscore
    tallenna_pisteet()

    # Pysäytä mato
    time.sleep(1)
    mato.goto(0, 0)
    mato.direction = "stop"

    # Piilota kehon osat
    for osa in keho_osat:
        osa.goto(1000, 1000)
    keho_osat.clear()

    # Arvo uusi omenan paikka
    siirra_omena_uuteenpos()

    # Nollaa asetukset
    pisteet = 0
    viive = 0.1
    aika = 0
    teksti_peli_loppu.clear()
    teksti_peli_loppu.setpos(1000, 1000)

def tallenna_pisteet():
    global pisteet, pistelista

    if pisteet > pistelista[0][1]:
        pistelista[2] = pistelista[1]
        pistelista[1] = pistelista[0]
        nimi = tkinter.simpledialog.askstring("Uusi ennätys!", f"Uusi ennätys!\n Top 3:\n1) Sinä ({pisteet})\n2) {pistelista[1][0]} ({pistelista[1][1]})\n3) {pistelista[2][0]} ({pistelista[2][1]}) \nAnna nimesi:")
        if nimi == None or nimi == "":
            nimi = "nimetön matopelaaja"
        pistelista[0] = (nimi, pisteet)

    try:
        with open("pisteet.csv", 'w') as tiedosto:
            csv_w = csv.writer(tiedosto)
            csv_w.writerows(pistelista)
    except:
        tkinter.messagebox.showerror("Virhe", "Pisteiden tallennus epäonnistui!")

def lue_pisteet():
    try:
        with open("pisteet.csv", "r") as tiedosto:
            csv_r = csv.reader(tiedosto)
            i = 0
            for rivi in csv_r:
                if rivi != []:
                    pistelista[i] = (rivi[0], int(rivi[1]))
                    i += 1
    except:
        pass

def siirra_omena_uuteenpos():
    global omena
    y = random.randint(REUNAT_Y[0], REUNAT_Y[1])
    x = random.randint(REUNAT_X[0], REUNAT_X[1])
    omena.goto(x, y)

def tarkista_tormays_reunoihin():
    global mato
    if (mato.xcor() > REUNAT_X[1] or mato.xcor() < REUNAT_X[0] or
        mato.ycor() > REUNAT_Y[1] or mato.ycor() < REUNAT_Y[0]):
        uusi_peli()

def tarkista_tormays_omena():
    global viive, pisteet, omena, keho_osat, mato
    if mato.distance(omena) < RUUTU_KOKO:
        siirra_omena_uuteenpos()

        # Lisää kehon osa
        uusi_osa = turtle.Turtle()
        uusi_osa.shape("square")
        uusi_osa.color("dark green")
        uusi_osa.penup()
        keho_osat.append(uusi_osa)

        viive -= 0.001
        pisteet += 10

def tarkista_tormays_itseensa():
    global keho_osat, mato
    for osa in keho_osat:
        if osa.distance(mato) < RUUTU_KOKO:
            uusi_peli()
    paivita_teksti()

def siirra_mato():
    global keho_osat, mato
    for i in range(len(keho_osat)-1, 0, -1):
            x = keho_osat[i-1].xcor()
            y = keho_osat[i-1].ycor()
            keho_osat[i].goto(x, y)

    if len(keho_osat) > 0:
        x = mato.xcor()
        y = mato.ycor()
        keho_osat[0].goto(x, y)

# Pääsilmukka
kaynnissa = True
peli_tauko = False

edellinen_aika = time.time()
lue_pisteet()
while kaynnissa:
    ikkuna.update()

    if peli_tauko:
        time.sleep(viive)
        continue

    tarkista_tormays_reunoihin()
    tarkista_tormays_omena()

    # Siirrä kehon osat
    siirra_mato()

    liiku()

    # Tarkista törmäys kehon osiin
    tarkista_tormays_itseensa()
    # Päivitä ajastin
    aika_kulunut = time.time() - edellinen_aika
    edellinen_aika = time.time()
    aika += aika_kulunut

    time.sleep(viive)

ikkuna.bye()
#ikkuna.mainloop()