package de.sebastianbrunnert.parallelen;

import javax.swing.JOptionPane;

public class Main {

    public static void main(String[] args){
        
        // Eingabe des Textes
        String text = JOptionPane.showInputDialog(null,"Welcher Text soll nach Parallelität untersucht werden?", "Junioraufgabe 1 - Parallelen", JOptionPane.PLAIN_MESSAGE);
        // Eingabe der Nummer bis zum wievielten Wort der Text nach Parallelität überprüft werden soll (siehe Aufgabenstellung "in der ersten Hälfte des Gedichts"
        Integer range = 0;
        try {
            range = Integer.parseInt(JOptionPane.showInputDialog(null,"Bis zu welchem Wort soll der Text nach Parallelität untersucht werden?", "Junioraufgabe 1 - Parallelen", JOptionPane.PLAIN_MESSAGE));            
        } catch (Exception e) {
            JOptionPane.showMessageDialog(null, "Es muss eine Zahl angegeben werden! Bitte versuche es erneut.", "Junioraufgabe 1 - Parallelen", JOptionPane.ERROR_MESSAGE);
            System.exit(0);
        }
                        
        // Da Sonderzeichen keine Worte darstellen, werden diese aus dem Text genommen
        text = text.replaceAll("[^a-zA-Z0-9\\s]", "");        
        // Alle Worte heraussuchen
        String[] words = text.split("\\W+");

        // Prüfe, ob angegebene Nummer größer ist als Menge an Wörtern im von Nutzer angegebenen Text
        if(range > words.length){
            // Setze Nummer zur Textlänge
            range = words.length;
        }

        // Deklariere das Wort, welches das letzte Wort sein wird. Es wird nur eine Variable benötigt, da im Fall, dass es verschiedene Endwörter gibt, das Programm gestoppt wird, da Text nicht parallel ist
        String endingWord = null;

        // Gehe jedes Wort durch, welches in der angegebene Range liegt (für jedes muss das Endwort herausgesucht werden)
        for(int i = 0; i < range; i++){
            // Suche das Wort
            String word = words[i];

            // Kopiere i (aus Schleife), da diese Variable verändert werden wird
            // current steht für den Index des Wortes, welches gerade geprüft wird
            int current = i;

            // Eine normal unendliche Schleife muss genutzt werden, da Text unendlich viele Zeichen haben kann
            while(true) {
                // Prüfe, ob ein Vorgang noch möglich wäre (wenn nein, ist das Endwort erreicht)
                if(words.length <= current+words[current].length()) {
                    if(endingWord == null){
                        // Sollte dies das erste Endwort sein, wird es als solches gespeichert
                        endingWord = words[current];                        
                    } else if(words[current] != endingWord){
                        // Falls das erste Endwort nicht mit diesem überinstimmt, ist Parallelität nicht gewährleistet
                        JOptionPane.showMessageDialog(null, "Der angegebene Text ist bis zum " + range + "ten Wort *nicht* parallel.", "Junioraufgabe 1 - Parallelen", JOptionPane.WARNING_MESSAGE);
                        System.exit(0);
                    }
                    // Stoppe unendliche Schleife
                    break;
                }
                // Setze den Index für das aktuelle Wort zu dem bereits vorhandenen Wort + der Länge des aktuellen Wort, wie in Aufgabenstellung beschrieben
                current += words[current].length();
            }
        }

        // Sollte nach diesem Algorithmus das Programm nicht gestoppt worden sein, ist der Text parallel
        JOptionPane.showMessageDialog(null, "Der angegebene Text *ist* bis zum " + range + "ten Wort parallel.", "Junioraufgabe 1 - Parallelen", JOptionPane.PLAIN_MESSAGE);
    }
}
