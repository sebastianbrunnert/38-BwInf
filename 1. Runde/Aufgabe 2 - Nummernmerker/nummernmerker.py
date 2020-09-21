#!/usr/bin/env python3

# Libary für die Übergabe von Kommandozeilenargumenten
import sys

# Hilfs-Funktion, um mögliche Kombinationen zu finden die zusammen n ergeben
# @arg1 - Array der Zahlen die benutzt werden dürfen
# @arg2 - Nummer die schlussendlich in der Summe des Resultats herauskommen soll
# @arg3 - Generator Objekt; ist eine Liste dessen Inhalt Listen sind die in der Summen @arg2 ergeben
def possible_combinations(numbers, target, partial=[], partial_sum=0):
    if partial_sum == target:
        yield partial
    if partial_sum >= target:
        return
    for n in numbers:
        yield from possible_combinations(numbers, target, partial + [n], partial_sum + n)

# Prüfe ob eine Nummer angegeben wurde
if len(sys.argv) != 2:
    print("Benutzung: python nummernmerker.py <nummer>")
# Prüfe ob eine Zahl und keine Zeichenkette angegeben wurde
elif(not sys.argv[1].isdigit()):
    print("Bitte gebe eine Nummer an und keine Zeichenkette.")
elif(len(sys.argv[1])<2):
    print("Bitte gebe eine Nummer an, die mehrere Ziffern hat.")
else:
	# Rufe eingegebene Zeichenkette auf
    number = str(sys.argv[1])

	# Definiere mithilfe der Funktion possible_combinations eine Liste mit den erlaubten Blocklängen
    allowed_block_lengths = list(possible_combinations([2,3,4], len(number)))

	# Definiere ein Verzeichnis
	# @key - Liste mit den verschiedenen Blocklängen der Nummer
	# @value - Anzahl wieviele Blöcke mit 0 beginnen
    number_of_zeros = {}

    # Gehe in einer For-Schleife alle erlaubten Blocklängen durch und trage in number_of_zeros ein wieviele Bläcke mit 0 starten
    for block_lengths in allowed_block_lengths:
        zeros = 0
        # Kopiere den String, da dieser durch die Benutzung dieses Algorithmus verändert wird
        copy_number = number
        # Prüfe ob die erste Ziffer eine 0 ist
        if copy_number[0] == "0":
            zeros += 1
        for i in block_lengths:
            # Lösche die ersten n Ziffern
            copy_number = copy_number[i:]
            # Überprüfe ob nun die erste Ziffer existiert bzw. eine 0 ist (wenn er nicht existiert ist das Ende der Zahl erreicht)
            if len(copy_number) > 0 and copy_number[0] == "0":
                # Addiere einen zu der Anzahl der Nullen
                zeros += 1

        # Setze die Anzahl der Ziffern und die Blocklängen in das Verzeichnis number_of_zeros ein
        number_of_zeros[tuple(block_lengths)] = zeros

	# Suche nun die minimalste Anzahl an mit null beginnenden Blöcken hat
    solution = min(number_of_zeros.items(), key=lambda x: x[1])[0]

    # Suche nun die Varianten, die die minimalste Anzahl an mit null beginnenden Blöcken hat (und gleichzeitig die minimalste Anzahl an mit null beginnenden Blöcken)
    for possible_solution in number_of_zeros:
        if number_of_zeros[solution] == number_of_zeros[possible_solution]:
            if len(solution) > len(possible_solution):
                solution = possible_solution


    # Gehe jeden Block der Lösung durch, gebe den Block in der Konsole aus und lösche die Anzahl der Ziffern von der eingegebenen Zeichenkette
    for i in solution:
        print(number[:i] + " ", end='')
        number = number[i:]

    # Gebe eine neue Zeile in die Konsole aus
    print("")

    # Gebe in die Konsole aus, wieviele Blöcke mit null beginnen
    if(number_of_zeros[solution] == 0):
        print("Kein Block beginnt mit 0")
    elif(number_of_zeros[solution]  == 1):
        print("1 Block beginnt mit 0")
    else:
        print(str(number_of_zeros[solution]) + " Blöcke beginnen mit 0")
