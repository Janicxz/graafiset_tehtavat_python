import tkinter.simpledialog
import turtle
import time
import random
import csv
import tkinter.messagebox

# Uudet ominaisuudet:
# Esc lopettaa, X painaminen ei kaada peliä
# Aika ja pisteet teksti
# Pisteiden tallennus ja luku csv tiedostosta
# Mahdollisuus poistaa seinät käytöstä
# Bonus omena
# Taukotila P-näppäimellä

# asetukset
SUURIN_SALLITTU_FPS = 60
RUUTU_KOKO = 20
RUUTU_LEVEYS = 30
RUUTU_PITUUS = 30
REUNAT_X = (-290, 290)
REUNAT_Y = (-290, 290)
TEKSTI_TAUKO_POS = (-80, 0)
TEKSTI_PELI_LOPPU_POS = (-80, 0)
TEKSTI_PISTEET_AIKA_POS = (-250, 250)
OMENA_PISTE = 10
VIIVE_VAHENNYS = 0.001
SEINAT_KAYTOSSA = True
VERSIO = 1.0
viive = 0.1
pisteet = 0
pistelista = [("Tyhjä", 0), ("Tyhjä", 0), ("Tyhjä", 0)]

# Ruudun asetukset
ikkuna = turtle.Screen()
ikkuna.title(f"Matopeli v{VERSIO} - F1) Pisteet F2) Asetukset P) Tauko")
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

# Punainen omena
omena = turtle.Turtle()
omena.speed(0)
omena.shape("circle")
omena.color("red")
omena.penup()
omena.goto(0, 100)

# Bonus omena
bonus_omena = turtle.Turtle()
bonus_omena.speed(0)
bonus_omena.shape("circle")
bonus_omena.color("yellow")
bonus_omena.penup()
bonus_omena.goto(1000, 1000)

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

def kysy_asetukset():
    global SEINAT_KAYTOSSA
    SEINAT_KAYTOSSA = tkinter.messagebox.askyesno("", "Otetaanko seinät käyttöön?")
    #if tkinter.messagebox.askyesno("", "Haluatko asettaa tietyn seed?"):
    #    seed = tkinter.simpledialog.askinteger("", "Syötä seed:")
    #try:
    #    random.seed(seed)
    #except:
    #    pass

# Näppäinohjaus
ikkuna.listen()
ikkuna.onkey(mene_ylos, "Up")
ikkuna.onkey(mene_ylos, "w")
ikkuna.onkey(mene_alas, "Down")
ikkuna.onkey(mene_alas, "s")
ikkuna.onkey(mene_vasemmalle, "Left")
ikkuna.onkey(mene_vasemmalle, "a")
ikkuna.onkey(mene_oikealle, "Right")
ikkuna.onkey(mene_oikealle, "d")
ikkuna.onkey(lopeta, "Escape")
ikkuna.onkey(tauko, "p")
ikkuna.onkey(nayta_pisteet, "F1")
ikkuna.onkey(kysy_asetukset, "F2")
# Jos ikkuna suljetaan muualta, kutsu lopeta funktiota
ikkuna._root.protocol("WM_DELETE_WINDOW", lopeta)

# Teksti
aika = 0
teksti_pisteet = turtle.Turtle()
teksti_peli_loppu = turtle.Turtle()
teksti_tauko = turtle.Turtle()

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

    # Tuhoa entinen bonus omena jos se jäi kentälle
    tuhoa_bonus_omena()

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
    if SEINAT_KAYTOSSA:
        if (mato.xcor() > REUNAT_X[1] or mato.xcor() < REUNAT_X[0] or
            mato.ycor() > REUNAT_Y[1] or mato.ycor() < REUNAT_Y[0]):
            uusi_peli()
    else:
        if (mato.xcor() > REUNAT_X[1]):
            mato.setx(REUNAT_X[0] - RUUTU_KOKO)
        elif mato.xcor() < REUNAT_X[0]:
            mato.setx(REUNAT_X[1] + RUUTU_KOKO)
        elif mato.ycor() > REUNAT_Y[1]:
            mato.sety(REUNAT_Y[0] - RUUTU_KOKO)
        elif mato.ycor() < REUNAT_Y[0]:
            mato.sety(REUNAT_Y[1] + RUUTU_KOKO)

def lisaa_mato_osa():
    global keho_osat, mato
    uusi_osa = turtle.Turtle()
    uusi_osa.shape("square")
    uusi_osa.color("dark green")
    uusi_osa.penup()
    if len(keho_osat) > 0:
        uusi_osa.setpos(keho_osat[-1].pos())
    else:
        uusi_osa.setpos(mato.pos())
    keho_osat.append(uusi_osa)

def satunnainen_paikka():
    y = random.randint(REUNAT_Y[0], REUNAT_Y[1])
    x = random.randint(REUNAT_X[0], REUNAT_X[1])
    return (x, y)

bonus_omena.nakyvissa = False
bonus_omena.aikaa_jaljella_haviamiseen = 8
bonus_omena.aikaa_jaljella_uusibonus = random.randint(3, 7) # Ensimmäinen bonus tulee aikaisemmin

def uusi_bonus_omena():
    global bonus_omena

    bonus_omena.nakyvissa = True
    paikka = satunnainen_paikka()
    bonus_omena.setpos(paikka[0], paikka[1])
    bonus_omena.aikaa_jaljella_uusibonus = 0
    bonus_omena.aikaa_jaljella_haviamiseen = 8
    bonus_omena.vari = 0

def tuhoa_bonus_omena():
    global bonus_omena

    bonus_omena.setpos(1000, 1000)
    bonus_omena.nakyvissa = False
    bonus_omena.aikaa_jaljella_uusibonus = random.randint(3, 15)

def tarkista_bonus_omena():
    global bonus_omena, viive, pisteet, mato
    #print(f"uusi {bonus_omena.aikaa_jaljella_uusibonus}, h {bonus_omena.aikaa_jaljella_haviamiseen}")
    if not bonus_omena.nakyvissa:
        if bonus_omena.aikaa_jaljella_uusibonus < 0:
            uusi_bonus_omena()
        else:
            bonus_omena.aikaa_jaljella_uusibonus -= viive
    else:
        if mato.distance(bonus_omena) < RUUTU_KOKO:
            # Lisää kehon osa
            lisaa_mato_osa()
            lisaa_mato_osa()

            viive -= VIIVE_VAHENNYS*2
            pisteet += OMENA_PISTE*2
            tuhoa_bonus_omena()

        if bonus_omena.aikaa_jaljella_haviamiseen < 0:
            tuhoa_bonus_omena()
        else:
            # Muuta bonuksen väriä jäljellä olevan ajan mukaan
            vari = max(min(1,bonus_omena.vari), 0)
            bonus_omena.color(1,1,0 + vari)
            bonus_omena.aikaa_jaljella_haviamiseen -= viive
            if bonus_omena.vari == None:
                bonus_omena.vari = 0
            else:
                bonus_omena.vari += viive/10


def tarkista_tormays_omena():
    global viive, pisteet, omena, mato
    if mato.distance(omena) < RUUTU_KOKO:
        siirra_omena_uuteenpos()

        lisaa_mato_osa()

        viive -= VIIVE_VAHENNYS
        pisteet += OMENA_PISTE

def tarkista_tormays_itseensa():
    global keho_osat, mato
    for osa in keho_osat:
        if osa.distance(mato) < RUUTU_KOKO:
            uusi_peli()

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

def odota_ruudunpaivitys():
    global edellinen_ruudunpaivitys, ruudunpaivitys_aikavali_ms
    aika_ruudunpaivitys = time.time() - edellinen_ruudunpaivitys
    aika_ruudunpaivitys *= 1000 #käännä ms
    odotettava_aika = ruudunpaivitys_aikavali_ms - aika_ruudunpaivitys
    #print(f"ruudunpäivitys: {aika_ruudunpaivitys}/{ruudunpaivitys_aikavali_ms}, odotetaan {odotus_aika}")
    if aika_ruudunpaivitys < ruudunpaivitys_aikavali_ms:
        time.sleep(max(0, odotettava_aika / 1000))
        return True
    else:
        edellinen_ruudunpaivitys = time.time()
        return False

# Pääsilmukka
kaynnissa = True
peli_tauko = False
edellinen_aika = time.time()
edellinen_tick = time.time()
ruudunpaivitys_aikavali_ms = (1.0 / SUURIN_SALLITTU_FPS) * 1000
edellinen_ruudunpaivitys = time.time()

lue_pisteet()
#kysy_asetukset()

while kaynnissa:
    ikkuna.update()

    if peli_tauko:
        time.sleep(viive)
        continue

    paivita_teksti()

    # Rajoita haluttuun ruudunpäivitys nopeuteen
    if odota_ruudunpaivitys():
        continue

    # Päivitä ajastin
    aika_kulunut = time.time() - edellinen_aika
    edellinen_aika = time.time()
    aika += aika_kulunut

    # Rajoita pelin nopeutta
    # TODO
    aika_kulunut_edellisesta_tick = time.time() - edellinen_tick
    if aika_kulunut_edellisesta_tick < viive:
        #time.sleep(0.016)
        #aika -= 0.016
        continue
    edellinen_tick = time.time()

    tarkista_tormays_reunoihin()
    tarkista_tormays_omena()
    tarkista_bonus_omena()
    siirra_mato()
    liiku()
    tarkista_tormays_itseensa()

    #time.sleep(viive)

ikkuna.bye()
#ikkuna.mainloop()