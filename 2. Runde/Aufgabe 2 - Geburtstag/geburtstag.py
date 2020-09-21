import sys

sys.setrecursionlimit(10**6)

# Liste, in welcher aufgestellte Terme gespeichert werden
solvingSteps = []

# Funktion, welche rekursiv ausgeführt werden wir zum aufstellen des Termes
# @arg1 (String): Aktuell aufgestellter Term
# @arg2 (String): Teil des Terms, welcher noch nicht umgewandelt wurde (in String-Form)
# @arg3 (int): Teil des Terms, welcher noch nicht umgewandelt wurde (als Zahl)
# @arg3 (int): Zu verwendende Ziffer
def solve(fullTerm,toReplaceStr,toReplaceInt,digit):
    # Dieses Element wird aus Liste entfernt, damit spätere Elemente nachher ausgeführt werden könnten
    solvingSteps.pop(0)

    # Nun wird jede Grundrechenart ausgeführt und es wird mit dieser ein neuer Term aufgestellt
    # Bei jeder Grundrechenart wird geprüft, bis zu welcher "Zahl" (also z.B. 5; 55 oder 610) gerechnet werden könnte

    # Multiplikation
    # Anzahl der Ziffern werden immer erhöht
    for i in range(1,7):
        # Zahl wird aufgestellt anhand Anzahl i an Ziffern
        digitNew = int(i * str(digit))

        # Es wird geprüft, ob die aufgestellte Zahl sinnvoll ist:
        if(toReplaceInt / digitNew < 1):
            # Ist das Ergebnis kleiner als 1, kann auch nicht ohne Rest geteilt werden (bei ganzen Zahlen)
            break
        if(toReplaceInt / digitNew % 1 != 0):
            # Kann eine Zahl mit n-1 Ziffern nicht mehr durch eine Zahl ohne Rest geteilt werden, so kann auch eine Zahl mit n Ziffern nicht mehr ohne Rest durch diese Zahl geteilt werden
            break

        toReplaceIntNew = toReplaceInt / digitNew

        fullTermNew = fullTerm.replace(toReplaceStr,"(" + str(toReplaceIntNew).replace(".0","") + ")*" + str(digitNew))
        
        toReplaceStrNew = str(toReplaceIntNew).replace(".0","")

        solvingSteps.append({"fullTerm": fullTermNew, "toReplaceStr": toReplaceStrNew, "toReplaceInt": toReplaceIntNew})

        # Prüfe, ob alle Vorraussetzungen erfüllt sind
        if(fits(fullTermNew,digit)):
            print(fullTermNew)
            exit()

    # Division 
    for i in range(1,7):
        digitNew = int(i * str(digit))

        if(digitNew > toReplaceInt):
            break

        toReplaceIntNew = toReplaceInt * digitNew

        fullTermNew = fullTerm.replace(toReplaceStr,"(" + str(toReplaceIntNew).replace(".0","") + ")/" + str(digitNew))
        
        toReplaceStrNew = str(toReplaceIntNew).replace(".0","")

        solvingSteps.append({"fullTerm": fullTermNew, "toReplaceStr": toReplaceStrNew, "toReplaceInt": toReplaceIntNew})

        if(fits(fullTermNew,digit)):
            print(fullTermNew)
            exit()

    # Addition
    for i in range(1,7):
        digitNew = int(i * str(digit))

        if(digitNew > toReplaceInt):
            break

        toReplaceIntNew = toReplaceInt - digitNew

        fullTermNew = fullTerm.replace(toReplaceStr,"(" + str(toReplaceIntNew).replace(".0","") + ")+" + str(digitNew))

        toReplaceStrNew = str(toReplaceIntNew).replace(".0","")

        solvingSteps.append({"fullTerm": fullTermNew, "toReplaceStr": toReplaceStrNew, "toReplaceInt": toReplaceIntNew})

        if(fits(fullTermNew,digit)):
            print(fullTermNew)
            exit()

    # Subtraktion
    for i in range(1,7):
        digitNew = int(i * str(digit))

        if(digitNew > toReplaceInt):
            break
        
        toReplaceIntNew = toReplaceInt + digitNew

        fullTermNew = fullTerm.replace(toReplaceStr,"(" + str(toReplaceIntNew).replace(".0","") + ")-" + str(digitNew))

        toReplaceStrNew = str(toReplaceIntNew).replace(".0","")

        solvingSteps.append({"fullTerm": fullTermNew, "toReplaceStr": toReplaceStrNew, "toReplaceInt": toReplaceIntNew})

        if(fits(fullTermNew,digit)):
            print(fullTermNew)
            exit()

    # Potenz
    toReplaceIntNew = toReplaceInt**(1/digit)

    fullTermNew = fullTerm.replace(toReplaceStr,"(" + str(toReplaceIntNew).replace(".0","") + ")^" + str(digit))

    toReplaceStrNew = str(toReplaceIntNew).replace(".0","")

    solvingSteps.append({"fullTerm": fullTermNew, "toReplaceStr": toReplaceStrNew, "toReplaceInt": toReplaceIntNew})

    if(fits(fullTermNew,digit)):
        print(fullTermNew)
        exit()

    # Prüfung ob noch Element vorhanden
    if(len(solvingSteps) == 0):
        print("Nicht lösbar!")
        exit()


    # Funktion führt sich erneut rekursiv aus
    solve(solvingSteps[0]["fullTerm"],solvingSteps[0]["toReplaceStr"],solvingSteps[0]["toReplaceInt"],digit)



# Hilfsfunktion zur Überprüfung, ob aufgestellter Term erlaubt ist
def fits(term,digit):
    for i in range(0,10):
        if(i != digit):
            if(term.count(str(i)) != 0):
                return False

    return True 

input_number = input("Welche Zahl soll aufgelöst werden: ")
input_digit = int(input("Aus welcher Ziffer: "))

solvingSteps.append({"fullTerm": input_number, "toReplaceStr": input_number, "toReplaceInt": int(input_number)})
solve(input_number,input_number,int(input_number),input_digit)

