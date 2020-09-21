# Libary um Programm stoppen zu können und Übergabe von Kommandozeilenargumenten
import sys

# Prüfe ob eine Argument angegeben wurde
if len(sys.argv) != 2:
    print("Benutzung: python3 kacheln.py <Textdatei>")
else:
    try:
        file = open(sys.argv[1])
    except Exception:
        print("Benutzung: python3 kacheln.py <Textdatei>")
        sys.exit(0)

    # Deklariere Schema der Karte (siehe Dokumentation)
    lines = []

    # Gehe jede Zeile der Textdatei durch
    for line in file.readlines():
        # Überspring erst zwei Zeilen
        if(len(line) > 3):
            # Lösche Leerzeichen
            line = line.replace(" ", "")
            # Liste Ziffern auf
            fields = list(line)
            # Lösche \n an Zeilenende
            if(fields[-1] != "1" or fields[-1] != "0"):
                fields = fields[:-1]
            # Strings zu Zahlen
            for n, i in enumerate(fields):
                if i == "1":
                    fields[n] = 1
                elif i == "0":
                    fields[n] = 0
                else:
                    fields[n] = -1
            # Diese Zeile zu Resultat hinzufügen
            lines.append(fields)
    
    # Gehe alle Felder durch (sichere auch Index der Zeile (y) und des Feldes (x))
    for line_count in range(0,len(lines)):
        line = lines[line_count]
        for column_count in range(0,len(line)):
            column = line[column_count]
            
            # Feld ist nicht vorhanden
            if(column == -1):

                possible_solution = 1

                if(line_count % 2 == 0):
                    if(column_count  % 2 == 0):
                        # Feld ist oben links in Kachel
                        if(line_count-1 < 0 and column_count-1 < 0):
                            # Feld ist auf gesamten Feld oben links, aufgrunddessen ist es irrelevant welche Zahl zugewiesen wird
                            possible_solution = 1
                        elif(column_count-1 < 0):
                            # Feld hat auf x-Achse keinen linken Nachbarn, deswegen wird Wert des Feldes über diesem übernommen
                            possible_solution = lines[line_count-1][column_count]
                        elif(line_count-1 < 0):
                            # Feld hat auf y-Achse keinen oberen Nachbarn, deswegen wir Wert des Feldes links neben diesen übernommen
                            possible_solution = line[column_count-1]
                        else:
                            # Feld liegt nicht am Rand, deshalb muss Feld über und Feld links neben diesem, den selben Wert haben. Ist dies nicht
                            # der Fall, so ist diese Karte nicht lösbar
                            if(lines[line_count-1][column_count] == -1 and line[column_count-1] == -1):
                                # Beide benachbarten Felder sind noch nicht definiert
                                possible_solution = 1
                            elif(lines[line_count-1][column_count] == -1):
                                # Einer der beiden Werte ist noch nicht definiert
                                possible_solution = line[column_count-1]
                            elif(line[column_count-1] == -1):
                                possible_solution = lines[line_count-1][column_count]
                            elif(lines[line_count-1][column_count] == line[column_count-1]):
                                possible_solution = line[column_count-1]
                            else:
                                print("Diese Karte ist nicht lösbar")
                                sys.exit(0)
                    else:
                        # Feld ist oben rechts in Kachel
                        if(line_count-1 < 0 and column_count+1 == len(line)):
                            # Feld ist auf dem gesammten Feld oben rehts, aufgrunddessen ist es irrelevant welche Zahl zugewiesen wird
                            possible_solution = 1
                        elif(column_count+1 == len(line)):
                            # Feld hat auf x-Achse keinen rechten Nachbarn, deswegen wird Wert des Feldes über diesem übernommen
                            possible_solution = lines[line_count-1][column_count]
                        elif(line_count-1 < 0):
                            # Feld hat auf y-Achse keinen oberen Nachbarn, deswegen wir Wert des Feldes links neben diesen übernommen
                            possible_solution = line[column_count-1]
                        else:
                            # Feld liegt nicht am Rand, deshalb muss Feld über und Feld rechts neben diesen, den selben Wert haben. Ist dies nicht
                            # der Fall, so ist Karte nicht lösbar
                            if(lines[line_count-1][column_count] == -1 and line[column_count+1] == -1):
                                # Beide benachbarten Felder sind noch nicht definiert
                                possible_solution = 1
                            elif(lines[line_count-1][column_count] == -1):
                                # Einer der beiden Werte ist noch nicht definiert
                                possible_solution = line[column_count+1]
                            elif(line[column_count+1] == -1):
                                # Einer der beiden Werte ist noch nicht definiert
                                possible_solution = lines[line_count-1][column_count]                        
                            elif(lines[line_count-1][column_count] == line[column_count+1]):
                                possible_solution = line[column_count+1]
                            else:
                                print("Diese Karte ist nicht lösbar")
                                sys.exit(0)
                        
                else:
                    if(column_count  % 2 == 0):
                        # Feld ist unten links in Kachel
                        if(line_count+1 == len(lines) and column_count-1 < 0):
                            # Feld ist auf gesamten Feld unten links, aufgrunddessen ist es irrelevant welche Zahl zugewiesen wird
                            possible_solution = 1
                        elif(column_count-1 < 0):
                            # Feld hat auf x-Achse keinen linken Nachbarn, deswegen wird Wert des Feldes über diesem übernommen
                            possible_solution = lines[line_count+1][column_count]
                        elif(line_count+1 == len(lines)):
                            # Feld hat auf y-Achse keinen unteren Nachbarn, deswegen wir Wert des Feldes links neben diesen übernommen
                            possible_solution = line[column_count-1]
                        else:
                            # Feld liegt nicht am Rand, deshalb muss Feld unter und Feld links neben diesem, den selben Wert haben. Ist dies nicht
                            # der Fall, so ist diese Karte nicht lösbar
                            if(lines[line_count+1][column_count] == -1 and line[column_count-1] == -1):
                                # Beide benachbarten Felder sind noch nicht definiert
                                possible_solution = 1
                            elif(lines[line_count+1][column_count] == -1):
                                # Einer der beiden Werte ist noch nicht definiert
                                possible_solution = line[column_count-1]
                            elif(line[column_count-1] == -1):
                                # Einer der beiden Werte ist noch nicht definiert
                                possible_solution = lines[line_count+1][column_count]
                            elif(lines[line_count+1][column_count] == line[column_count-1]):
                                possible_solution = line[column_count-1]
                            else:
                                print("Diese Karte ist nicht lösbar")
                                sys.exit(0)
                    else:
                        # Feld ist oben rechts in Kachel
                        if(line_count+1 == len(lines) < 0 and column_count+1 == len(line)):
                            # Feld ist auf dem gesammten Feld unten rehts, aufgrunddessen ist es irrelevant welche Zahl zugewiesen wird
                            possible_solution = 1
                        elif(column_count+1 == len(line)):
                            # Feld hat auf x-Achse keinen rechten Nachbarn, deswegen wird Wert des Feldes über diesem übernommen
                            possible_solution = lines[line_count+1][column_count]
                        elif(line_count+1 == len(lines)):
                            # Feld hat auf y-Achse keinen unteren Nachbarn, deswegen wir Wert des Feldes links neben diesen übernommen
                            possible_solution = line[column_count-1]
                        else:
                            # Feld liegt nicht am Rand, deshalb muss Feld unter und Feld rechts neben diesen, den selben Wert haben. Ist dies nicht
                            # der Fall, so ist Karte nicht lösbar
                            if(lines[line_count+1][column_count] == -1 and line[column_count+1] == -1):
                                # Beide benachbarten Felder sind noch nicht definiert
                                possible_solution = 1
                            elif(lines[line_count+1][column_count] == -1):
                                # Einer der beiden Werte ist noch nicht definiert
                                possible_solution = line[column_count+1]
                            elif(line[column_count+1] == -1):
                                # Einer der beiden Werte ist noch nicht definiert
                                possible_solution = lines[line_count+1][column_count]
                            elif(lines[line_count+1][column_count] == line[column_count+1]):
                                # Einer der beiden Werte ist noch nicht definiert
                                possible_solution = line[column_count+1]
                            else:
                                print("Diese Karte ist nicht lösbar")
                                sys.exit(0)



                lines[line_count][column_count] = possible_solution

    print(lines)
