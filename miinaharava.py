#Ohjelman käyttämät moduulit.

import datetime
import time
import random
import functions


#Vino pino listoja joiden avulla ohjelma pyörii.

pelaaja_tila = {
    "kentta": None
    }

tila = {
    "kentta": None
    }
    
alku = {
    "leveys": None,
    "korkeus": None,
    "miinoja": None
    }
    
tilastot = {
    "vuorojenmaara": 0,
    "lopputulos": None,
    }
    
kesto = {
    "alku": None,
    "loppu": None,
    "kokonais": None,
    "minuutit": None
    }
    
def tallenna_tilastot():
    """
    Tallentaa pelatun pelin tiedot tiedostoon.
    """
    try:
        with open("tilastot.txt", "a") as kohde:
            kohde.write("pvm: {aika}, kesto: {sek} s , vuorot: {vuorot}, lopputulos: {lopputulos}, kenttä: {leveys} x {korkeus}, miinat: {miinat} \n".format(
                aika=datetime.datetime.now().strftime("%d.%m.%y. %H:%M"),
                sek="%05.2F" % kesto["kokonais"],
                vuorot=tilastot["vuorojenmaara"],
                lopputulos=tilastot["lopputulos"],
                leveys=alku["leveys"],
                korkeus=alku["korkeus"],
                miinat=alku["miinoja"]                
            ))
    except IOError:
        print("Kohdetiedostoa ei voitu avata.")
                               
def laske_kesto():
    """
    Laskee, kuinka kauan peli kestää. Pelin kesto näkyy tässä vaiheessa
    pelkkinä sekunteina.
    """     
    aika = kesto["loppu"] - kesto["alku"]
    kesto["kokonais"] = aika 

def aika_minuuteiksi():
    """
    Muuttaa laske_kesto():sta saadun sekunti määrän minuuteiksi ja sekunneiksi.
    """    
    kesto["minuutit"] = 0
    if kesto["kokonais"] >= 60:
        kesto["minuutit"] = kesto["minuutit"] + 1
        kesto["kokonais"] - 60
 
def voitit_pelin():
    """
    Kun kaikki miinat on liputettu, funktio printtaa voittoilmoituksen
    ja antaa tallenna_tilastot() funktiolle olennaisia tietoja.
    Funktio myöskin sulkee peli ikkunan.
    """
    print("*************************")
    print("*****ONNEKSI OLKOON!*****")
    print("******VOITIT PELIN!******")
    print("*************************")
    laske_kesto()
    aika_minuuteiksi()
    tilastot["lopputulos"] = "Voitto"
    tallenna_tilastot()
    functions.lopeta()
    jatko = input("Paina mitä tahansa jatkaaksesi.")

def astuit_miinaan():
    """
    Kun pelaaja klikkaa miinaa, funktio printtaa häviöilmoituksen ja antaa
    tallenna_tilastot() funktiolle olennaisia tietoja. Häviö tiedostoja ei
    kuitenkaan tällä hetkellä tallenneta, koska kuka nyt niitä haluaisi ihailla.
    Funktio myöskin sulkee peli ikkunan.
    """
    print("*************************")
    print("***********KOPS!*********")
    print("******OSUIT MIINAAN!*****")
    print("*************************")
    laske_kesto()
    aika_minuuteiksi()
    tilastot["lopputulos"] = "Häviö"
    #tallenna_tilastot()
    functions.lopeta()
    jatko = input("Paina mitä tahansa jatkaaksesi.")  
    
def tulvataytto(lista, x, y):
    """
    Tyhjää ruutua painettaessa, funktio näyttää painetun ruudun ympärillä olevat
    numeroruudut sekä tyhjätruudut.
    """
    newlist = [(x, y)]
    while newlist:
        x, y = newlist.pop()
        pelaaja_tila["kentta"][y][x] = lista[y][x]
        if lista[y][x] == "0":
            for rivi in range(y - 1, y + 2):
                for sarake in range(x - 1, x + 2):
                    if len(lista) - 1 >= rivi >= 0 and len(lista[0]) - 1 >= sarake >= 0 and pelaaja_tila["kentta"][rivi][sarake] == " ":
                        newlist.append((sarake, rivi))
  
def laske_miinat(lista):
    """
    Muokkaa listan sellaiseen muotoon, että käsittele_hiiri ymmärtää lopettavansa,
    kun voittoehto täyttyy. Tätä funktiota vertaillaan laske_liput() funktioon.
    """  
    newlist = []    
    for rivi in lista:
        for merkki in rivi:
            newlist.append(merkki)
    return newlist

def laske_liput(lista):
    """        
    Muokkaa listan sellaiseen muotoon, että käsittele hiiri ymmärtää lopettavansa,
    kun voittoehto täyttyy. Tätä funktiota vertaillaan laske_miinat() funktioon.    
    """
    newlist2 = []   
    for rivi in lista:
        for merkki in rivi:
            if merkki == "f":
                newlist2.append("x")
            else:
                newlist2.append(merkki)           
    return newlist2
    
 
def kasittele_hiiri(x, y, nappi, muokkausnäppäimet):
    """
    Käsittelee hiiren painalluksia pelikentällä ja johdattaa ohjelman klikkauksia
    vastaaviin jatkotoimenpiteisiin.
    """   
    y_index = int(y // 40)
    x_index = int(x // 40)
    if laske_miinat(tila["kentta"]) != laske_liput(pelaaja_tila["kentta"]):
        if nappi == functions.HIIRI_VASEN:
            try:
                if tila["kentta"][y_index][x_index] == "x":
                    tilastot["vuorojenmaara"] += 1
                    kesto["loppu"] = time.monotonic()
                    astuit_miinaan()                   
                elif pelaaja_tila["kentta"][y_index][x_index] == " ":
                    tulvataytto(tila["kentta"], x_index, y_index)
                    tilastot["vuorojenmaara"] += 1              
                else:
                    pelaaja_tila["kentta"][y_index][x_index] = tila["kentta"][y_index][x_index]
                    tilastot["vuorojenmaara"] += 1
                    
            except IndexError:
                print("Et osunut kenttään")
                           
        elif nappi == functions.HIIRI_OIKEA:     
            if pelaaja_tila["kentta"][y_index][x_index] == " ":
                pelaaja_tila["kentta"][y_index][x_index] = "f"
                tilastot["vuorojenmaara"] += 1
            elif pelaaja_tila["kentta"][y_index][x_index] == "f":
                pelaaja_tila["kentta"][y_index][x_index] = " "
                tilastot["vuorojenmaara"] += 1
    
    else:
        kesto["loppu"] = time.monotonic()      
        voitit_pelin()
     
def piirra_kentta():
    """
    Kertoo functions.aseta_piirto_kasittelija:lle, millainen kenttä tulee piirtää.
    """   
    functions.tyhjaa_ikkuna()
    functions.piirra_tausta()
    functions.aloita_ruutujen_piirto()
    for riviN, rivi in enumerate(pelaaja_tila["kentta"]):
        for sarakeN, ruutu in enumerate(rivi):
            functions.lisaa_piirrettava_ruutu(ruutu, 40 * sarakeN, 40 * riviN)
    functions.piirra_ruudut()
  
def laske_ymparilla(x, y, lista):    
    """
    Laskee kuinka monta miinaa tietyn koordinaatin ympärillä on.
    """  
    miinoja = 0
    for rivi in range(y - 1, y + 2):
        for sarake in range(x - 1, x + 2):
            if len(lista) -1 >= rivi >= 0 and len(lista[0]) - 1 >= sarake >= 0 and lista[rivi][sarake] == "x":
                miinoja += 1
    return miinoja   
            
      
def lisaa_numerot(kentta):
    """
    Lisää kenttään ympäröivien miinojen määrää kuvaavat luvut. Funktio käyttäää apuna
    laske_ymparilla() funktiota.
    """  
    for riviN, rivi in enumerate(kentta):
        for sarakeN, ruutu in enumerate(rivi):
            luku = laske_ymparilla(sarakeN, riviN, kentta)
            if kentta[riviN][sarakeN] != "x":
                kentta[riviN][sarakeN] = str(luku)

             
def miinoita(lista, vapaat_ruudut, miina_n):
    """
    Sijoittaa kentälle sovitun määrän miinoja täysin satunnaisiin paikkoihin.
    """   
    for lkm in range(miina_n):  #lkm = 0,1,2,3...
        miina_x, miina_y = random.choice(vapaat_ruudut)
        lista[miina_y][miina_x] = "x"
        vapaat_ruudut.remove((miina_x, miina_y))

    
def nayta_tilastot():
    """
    Näyttää tietoja aiemmin pelatuista peleistä. Tilastoja näytetään tällähetkellä
    niin paljon kuin niitä on.
    """   
    with open("tilastot.txt", "r") as luku:
        print(luku.read())
                

def luo_peli():
    """
    Luo useiden funktioiden avulla peli kentän ja grafiikat. Apuna käytetty functions-
    kirjastoa.
    """
    try:
        alku["leveys"] = abs(int(input("Anna kentän leveys (suositeltu max 50): ")))
        alku["korkeus"] = abs(int(input("Anna kentän korkeus (suositeltu max 25): ")))
        alku["miinoja"] = abs(int(input("Anna miinojen lkm: ")))
    except ValueError:
        print("")
        print("Vain numerot kelpaavat!")
        print("")
    else:   
        kentta = []
        for rivi in range(alku["korkeus"]):
            kentta.append([])
            for sarake in range(alku["leveys"]):
                kentta[-1].append(" ")       
        tila["kentta"] = kentta
        
        p_kentta = []
        for rivi in range(alku["korkeus"]):
            p_kentta.append([])
            for sarake in range(alku["leveys"]):
                p_kentta[-1].append(" ")
        pelaaja_tila["kentta"] = p_kentta 
        
        jaljella = []
        for x in range(alku["leveys"]):
            for y in range(alku["korkeus"]):
                jaljella.append((x, y))
    
        miinoita(tila["kentta"], jaljella, alku["miinoja"])
        lisaa_numerot(tila["kentta"])
        functions.lataa_kuvat("spritet")
        functions.luo_ikkuna(leveys=alku["leveys"] * 40, korkeus=alku["korkeus"] * 40)
        functions.aseta_piirto_kasittelija(piirra_kentta)
        kesto["alku"] = time.monotonic()
        functions.aseta_hiiri_kasittelija(kasittele_hiiri)
        functions.aloita()
        

def main():
    """
    Päävalikko, josta kaikki lähtee liikkeelle.
    """
    print("")
    print("*************************")
    print("*************************")
    print("Tervetuloa miinaharavaan!")
    print("*************************")    
    print("*************************")
    print("")
    while True:
        valinta = input("Valitse: (1) pelaa / (2) Tilastot / (3) Lopeta: ")
        if valinta == "1":
            luo_peli()
        elif valinta == "2":
            nayta_tilastot()
        elif valinta == "3":
            break
        else:
            print("")
            print("Valinta ei kelpaa.")
            print("")
            
"""
Käynnistää ohjelman.
"""            
main()
            
    