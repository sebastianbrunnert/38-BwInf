#!/usr/bin/env python3

# Libary zum Zeichnen der Karte
import matplotlib as mlp
import matplotlib.pyplot as plt
# Libary zum Ausrechnen von Verschiedenem
import math
import sys

# Setze des Rekursions-Limit auf eine extremst hohe Zahl.
sys.setrecursionlimit(10**6)

# Aus der Kartendatei geladenen Strassen:
#   - ["p1"]["x"]: Int - x-Koord des ersten Punktes
#   - ["p1"]["y"]: Int - y-Koord des ersten Punktes
#   - ["p2"]["x"]: Int - x-Koord des zweiten Punktes
#   - ["p2"]["y"]: Int - y-Koord des zweiten Punktes
strassen = []

# Öffnen die Kartendatei...
try:
    kartenDatei = open(input("Pfad zur Karte: ")).readlines()
except IOError as err:
    print("Die angegebene Datei existiert nicht")
    exit()

for i in range(3,len(kartenDatei)):
    zahlen = kartenDatei[i].replace("(","").replace(")","").replace(" ",",").replace("\n","").split(",")
    strassen.append({
        "p1": {
            "x": int(zahlen[0]),
            "y": int(zahlen[1])
        },
        "p2": {
            "x": int(zahlen[2]),
            "y": int(zahlen[3])
        }
    })

# Startpunkt
#   - ["x"]: Int - x-Koord des Startpunktes
#   - ["y"]: Int - x-Koord des Startpunktes
start = {
    "x": int(kartenDatei[1].split(",")[0].replace("(","")),
    "y": int(kartenDatei[1].split(",")[1].replace(")","")),
}

# Zielpunkt
#   - ["x"]: Int - x-Koord des Endpunkt
#   - ["y"]: Int - x-Koord des Endpunkt
ziel = {
    "x": int(kartenDatei[2].split(",")[0].replace("(","")),
    "y": int(kartenDatei[2].split(",")[1].replace(")","")),
}

# Hilfsfunktion, um zu ermitteln welche Abzweigungen genommen werden können
# @arg1 - Array:
#   - ["x"]: Int - aktuelle x-Koord
#   - ["y"]: Int - aktuelle y-Koord
# @retrun - Array:
#   - ["strecke"]: Int - Strecke, die zurückgelegt werden muss
#   - ["koords"]["x"]: Int - x-Koordinate, die nach diesem Zug angenommen werden
#   - ["koords"]["y"]: Int - y-Koordinate, die nach diesem Zug angenommen werden
#   - ["strasse"]: Int - Index der Straße
#   - ["abbiegen"]: Boolean - Muss für diese Straße abgebogen werden?
def moeglicheStrassen(aktuelleKoord):
    moeglicheStrassen = []
    # Gehe alle Straßen durch
    for i in range(0,len(strassen)):
        strasse = strassen[i]
        # Prüfen, ob der Start- oder Endpunkt die aktuelle Koordinate ist
        if(strasse["p1"] == aktuelleKoord):
            # Diese Straße kann genommen werden, soll also später ausgegeben werden
            moeglicheStrassen.append({
                # Ausrechnen der benötigten Strecke mithilfe des Satz des Pythagoras
                "strecke": math.sqrt((strasse["p2"]["x"] - aktuelleKoord["x"])**2 + (strasse["p2"]["y"] - aktuelleKoord["y"])**2),
                "koords": {
                    "x": strasse["p2"]["x"],
                    "y": strasse["p2"]["y"]
                },
                "index": i
            })
        if(strasse["p2"] == aktuelleKoord):
            # Diese Straße kann genommen werden, soll also später ausgegeben werden
            moeglicheStrassen.append({
                # Ausrechnen der benötigten Strecke mithilfe des Satz des Pythagoras
                "strecke": math.sqrt((strasse["p1"]["x"] - aktuelleKoord["x"])**2 + (strasse["p1"]["y"] - aktuelleKoord["y"])**2),
                "koords": {
                    "x": strasse["p1"]["x"],
                    "y": strasse["p1"]["y"]
                },
                "index": i
            })

    return moeglicheStrassen

# Hilfsfunktion, um zu ermitteln, ob abgebogen werden muss
# @arg1 - Int: Index der Straße, von der Bilal kommt
# @arg2 - Int: Index der Straße, in die Bilal fahren möchte
def mussAbgebogenWerden(von,zu):
    # Mathematisch bedeutet abbiegen, dass die Steigung der Graphen sich verändert.
    # Da senkrechte Geraden keine Steigung wird dort nur geprüft, ob die beiden x-Koordinaten einer der beiden Straßen gleich sind.
    if(strassen[von]["p1"]["x"] == strassen[von]["p2"]["x"] or strassen[zu]["p1"]["x"] == strassen[zu]["p2"]["x"]):
        if(strassen[von]["p1"]["x"] == strassen[von]["p2"]["x"] == strassen[zu]["p1"]["x"] == strassen[zu]["p2"]["x"]):
            return 0
        return 1
    # Es wird nun also von beiden Straßen die Steigung ausgerechnet und geprüft, ob diese gleich sind. 
    elif( ((strassen[von]["p2"]["y"] - strassen[von]["p1"]["y"]) / (strassen[von]["p2"]["x"] - strassen[von]["p1"]["x"])) == ((strassen[zu]["p2"]["y"] - strassen[zu]["p1"]["y"]) / (strassen[zu]["p2"]["x"] - strassen[zu]["p1"]["x"]))):
        # Trifft dies zu, muss nicht abgebogen werden.
        return 0

    return 1



# Array der alle Wege die mithilfe des Algorithmus berechnet werden in sich trägt
#   - ["koords"]["x"]: Int - aktuelle x-Koordinate
#   - ["koords"]["y"]: Int - aktuelle y-Koordinate
#   - ["strecke"]: Int - Zurückgelegte Strecke
#   - ["abbiegen"]: Int - Gibt an wie oft abgebogen werden musste
abzweigungen = []

# Dieser Array gibt an, welche Wege erfolgreich am Endpunkt angelangt sind
erfolgreicheWege = []

# Dieser Boolean gibt an, ob die Zahl der Wege, die in der Berechnung sind bereits einmal null war. Dies dient dazu, dass nicht alle Wege wieder berechnet werden und es zu einer Rekursion kommt.
ende = False

# Dieses Dictionary gibt dem Algorithmus an wie kurz die kürzeste Strecke war, um zu einen spezifischen Punkt zu gelangen (in Relation zum Abbiegezähler). Das ist insofern wichtig, dass somit die definitiv kürzeren Strecken von vornherein ausgeschlossen werden.
kuerzesteStreckeZuPunkt = {}

def naechsterSchritt():
    global abzweigungen, ende

    # Prüfe, ob noch kein Weg in der Berechnung war
    if(abzweigungen == []):
        # Wurde dieser Durchlauf bereits einmal getätigt?
        if(ende):
            # Beende die Funktion
            return
        # Gehe alle Straßen durch, die vom Startpunkt aus erreicht werden können.
        for moeglicheStrasse in moeglicheStrassen(start):
            # Prüfe, ob bereits jetzt das Ziel erreicht wurde
            if(moeglicheStrasse["koords"] == ziel):
                # Wenn ja, soll dies natürlich im nächsten Durchlauf nicht noch einmal wiederholt werden und dieser Pfad wird nicht mit in den Array für die Berechnungen des nächsten Durchlauf gegeben.
                erfolgreicheWege.append({
                    "strecke": moeglicheStrasse["strecke"],
                    "gefahrenerWeg": [moeglicheStrasse["index"]],
                    "abbiegen": 0
                })
            else:
                # Prüfe, ob ein Pfad bereits über diesen Punkt führte
                punktVereinfacht = str(moeglicheStrasse["koords"]["x"]) + "-" + str(moeglicheStrasse["koords"]["y"]) + "-0"
                if(not punktVereinfacht in kuerzesteStreckeZuPunkt):
                    # Wenn nicht, setze die nötige Strecke auf die gegebene Strecke
                    kuerzesteStreckeZuPunkt[punktVereinfacht] = moeglicheStrasse["strecke"]
                else:
                    # Wenn nicht, prüfe, ob die jetzig erreichte Strecke kürzer als die vorherige Strecke ist
                    if(kuerzesteStreckeZuPunkt[punktVereinfacht] > moeglicheStrasse["strecke"]):
                        # Wenn ja, wird die kürzest benötigte Strecke neu gesetzt
                        kuerzesteStreckeZuPunkt[punktVereinfacht] = moeglicheStrasse["strecke"]
                    else:
                        # Wenn nicht, wird dieser Pfad ignoriert
                        continue
                # Gebe diese Straßen in dein Array
                abzweigungen.append({
                    "strecke": moeglicheStrasse["strecke"],
                    "koords": moeglicheStrasse["koords"],
                    "gefahrenerWeg": [moeglicheStrasse["index"]],
                    "abbiegen": 0
                })
        # Setze ende auf wahr. Das bedeutet, dass dieser Durchlauf bereits einmal getätigt wurde,
        ende = True
        # Führe diese Funktion wieder aus (es wird die zweite Verzweigung ausgeführt)
        naechsterSchritt()
    else:
        # Kopiere den Array, damit die angefangenen Wege nicht mit in der Berechnung berücksichtigt werden und im nächsten Durchlauf wieder das selbe berechnet wird. Es wird also die Rekursion verhindert.
        abzweigungenDuplikat = abzweigungen.copy()
        # Leere den Array
        abzweigungen = []
        # Gehe alle nötigen Berechnungen durch
        for i in range(0,len(abzweigungenDuplikat)):
            # Gehe alle möglichen Abzweigungen durch
            abzweigung = abzweigungenDuplikat[i]
            for moeglicheStrasse in moeglicheStrassen(abzweigung["koords"]):
                # Prüfe, ob das Ziel erreicht wurde
                if(moeglicheStrasse["koords"] == ziel):
                    # Wenn ja, soll dies natürlich im nächsten Durchlauf nicht noch einmal wiederholt werden und dieser Pfad wird nicht mit in den Array für die Berechnungen des nächsten Durchlauf gegeben.
                    erfolgreicheWege.append({
                        "strecke": abzweigung["strecke"] + moeglicheStrasse["strecke"],
                        "gefahrenerWeg": abzweigung["gefahrenerWeg"] + [moeglicheStrasse["index"]],
                        "abbiegen": abzweigung["abbiegen"] + mussAbgebogenWerden(abzweigung["gefahrenerWeg"][-1],moeglicheStrasse["index"])
                    })
                # Prüfe, ob dieser Pfad diese Stelle schon durchlaufen ist. Wenn ja ist dieser Weg ganz sicher nicht der kürzeste mit der Anzahl an Abbiegen und der Weg wird vernachlässigt.
                elif(abzweigung["gefahrenerWeg"].count(moeglicheStrasse["index"]) < 1):
                    # Prüfe, ob ein Pfad bereits über diesen Punkt führte (in Relation zum Abbiegezähler)
                    punktVereinfacht = str(moeglicheStrasse["koords"]["x"]) + "-" + str(moeglicheStrasse["koords"]["y"]) + "-" + str(abzweigung["abbiegen"] + mussAbgebogenWerden(abzweigung["gefahrenerWeg"][-1],moeglicheStrasse["index"]))
                    if(not punktVereinfacht in kuerzesteStreckeZuPunkt):
                        # Wenn nicht, setze die nötige Strecke auf die gegebene Strecke
                        kuerzesteStreckeZuPunkt[punktVereinfacht] = moeglicheStrasse["strecke"]
                    else:
                        # Wenn nicht, prüfe, ob die jetzig erreichte Strecke kürzer als die vorherige Strecke ist
                        if(kuerzesteStreckeZuPunkt[punktVereinfacht] > moeglicheStrasse["strecke"]):
                            # Wenn ja, wird die kürzest benötigte Strecke neu gesetzt
                            kuerzesteStreckeZuPunkt[punktVereinfacht] = moeglicheStrasse["strecke"]
                        else:
                            # Wenn nicht, wird dieser Pfad ignoriert
                            continue
                    # Ansonsten wird der Pfad in den Array für den nächsten Berechnungsdurchlauf gegeben.
                    abzweigungen.append({
                        "strecke": abzweigung["strecke"] + moeglicheStrasse["strecke"],
                        "koords": moeglicheStrasse["koords"],
                        "gefahrenerWeg": abzweigung["gefahrenerWeg"] + [moeglicheStrasse["index"]],
                        "abbiegen": abzweigung["abbiegen"] + mussAbgebogenWerden(abzweigung["gefahrenerWeg"][-1],moeglicheStrasse["index"])
                    })

        naechsterSchritt()

# Führe den Algorithmus aus. Dieser wird sich selber so oft wie nötig ausführen (Rekursion)
naechsterSchritt()

# Dies wird der kürzester Weg sein, damit die Länge verglichen werden kann.
streckeKuerzesterWeg = None

# Suche kürzesten Weg herraus
for erfolgreicherWeg in erfolgreicheWege:
    if(streckeKuerzesterWeg == None):
        streckeKuerzesterWeg = erfolgreicherWeg["strecke"]
    elif(streckeKuerzesterWeg > erfolgreicherWeg["strecke"]):
        streckeKuerzesterWeg = erfolgreicherWeg["strecke"]

# Frage den Nutzer nach der maximalen Verlängerung
maximaleVerlaengerung = input("Um wieviel Prozent darf der Weg länger sein als der kürzeste Weg? ")
if(not maximaleVerlaengerung.isdigit()):
    # Und prüfe, ob eine Zahl angegeben wurde
    print("Du hast keine Zahl angegeben!")
    exit()

# Definiere die absolute maximale Länge
maximaleLaenge = (1+(int(maximaleVerlaengerung) / 100)) * streckeKuerzesterWeg

# Dies wird der gefundene optimale Weg sein
optimalerWeg = None

# Suche den optimalen Weg
for erfolgreicherWeg in erfolgreicheWege:
    if(optimalerWeg == None and erfolgreicherWeg["strecke"] <= maximaleLaenge):
        optimalerWeg = erfolgreicherWeg
    elif(erfolgreicherWeg["strecke"] <= maximaleLaenge and erfolgreicherWeg["abbiegen"] < optimalerWeg["abbiegen"]):
        optimalerWeg = erfolgreicherWeg


# Alle Linien einzeichnen
for i in optimalerWeg["gefahrenerWeg"]:
    strasse = strassen[i]
    plt.plot([strasse["p1"]["x"],strasse["p2"]["x"]],[strasse["p1"]["y"],strasse["p2"]["y"]])

# Zeichne das Koordinatensystem
plt.show()
