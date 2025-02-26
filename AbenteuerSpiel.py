from panda3d.core import LVecBase3f, TextNode
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectButton import DirectButton
from direct.gui.OnscreenText import OnscreenText
import random

class Spiel(ShowBase):
    def __init__(self):
        super().__init__()

        # Setze die Hintergrundfarbe auf ein dunkles Blau
        self.set_background()

        # Lade die Hintergrundmusik und spiele sie in einer Schleife ab
        self.bgm = self.loader.loadSfx("horror.mp3")  # Ersetze durch den Namen deiner Musikdatei
        self.bgm.setLoop(True)
        self.bgm.play()

        # Text für verschiedene Spielabschnitte
        self.intro_text = "Herzlich Willkommen zum Abenteuer deines Lebens!"
        self.eingang_text = (
            "Du stehst vor der verschlossenen Eingangstür \n"
            "des Herrenhauses. Ein kleines Fenster auf der linken Seite \n"
            "ist offen."
        )
        self.staubiger_raum_text = (
                "Du kletterst durch das Fenster, und ein kalter Wind weht dir ins Gesicht. \n"
    "Du landest in einem düsteren, staubigen Raum, der von der Zeit vergessen scheint. \n"
    "Die Schatten der alten Möbel scheinen lebendig zu werden, während du dich vorsichtig \n"
    "umherschleichst. Überall sind verstaubte Bücher, deren Seiten vom Flüstern der Vergangenheit \n"
    "erzählen. In der Ecke, kaum sichtbar im schummrigen Licht, steht ein Tisch, \n"
    "auf dem ein altes Tagebuch liegt. Seine Seiten sind zerfetzt, als ob sie von einer \n"
    "unsichtbaren Hand berührt wurden, und ein unheimlicher Geruch von Moder und Geheimnissen \n"
    "umgibt es."
        )
        self.tagebuch_text = (
            "Das Tagebuch gehört dem Wissenschaftler. \n"
            "Es enthält Hinweise auf Rätsel, die im Haus versteckt sind."
        )
        self.abstellkammer_text = (
            "Du betrittst die Abstellkammer. \n"
            "Es riecht nach Staub und alten Erinnerungen. \n"
            "In der Ecke siehst du eine Schaufel, die halb im Schatten liegt. \n"
            "Regale sind voll mit alten Kisten und vergilbten Zeitungen."
        )
        self.flur_text = (
            "Du betrittst den Flur und hörst ein seltsames Geräusch. \n"
            "Es weht ein eiskalter Wind durch den Flur."
        )

        # Inhalte des Tagebuchs als Hinweise für den Spieler
        self.tagebuch_inhalte = {
            "geheime_tuer": (
                "Es gibt eine geheime Tür hinter dem Bücherregal im Wohnzimmer. \n"
                "Man muss das Buch mit dem blauen Einband ziehen, um sie zu öffnen."
            ),
            "experiment": (
                "Die letzte Entdeckung war ein Experiment mit einer alten Maschine. \n"
                "Die Notizen besagen, dass sie nur funktioniert, \n"
                "wenn die richtige Reihenfolge der Hebel betätigt wird."
            ),
            "zahlenraetsel": (
                "Das Schloss erfordert eine Kombination. \n"
                "Die Zahlen sind in einem Gedicht versteckt: \n"
                "'Drei Eichen stehen, der Wind weht, die Zeit vergeht, \n"
                "die Zahl ist Zwei.'"
            )
        }

        # Aktuellen und vorherigen Text initialisieren
        self.current_text = self.intro_text
        self.previous_texts = []  # Liste zur Speicherung der vorherigen Texte
        self.inventory = []  # Inventar initialisieren
        self.show_text(self.current_text)  # Zeige den Einführungstext an

        # Schaltfläche für den Spielstart erstellen
        self.buttons = []  # Liste zur Speicherung der Schaltflächen
        self.create_button("Spiel starten", self.start_game, pos=(0, -0.3))

    def set_background(self):
        # Setze die Hintergrundfarbe des Fensters
        self.win.setClearColor((0.05, 0.05, 0.1, 1))  # Dunkelblau

    def show_text(self, text):
        # Lösche alten Text, falls vorhanden
        if hasattr(self, 'text_object'):
            self.text_object.destroy()
        # Erstelle ein neues Textobjekt und zeige es auf dem Bildschirm an
        self.text_object = OnscreenText(text=text, pos=(-1.3, 0.5), scale=0.05,
                                          fg=(1, 0.8, 0.2, 1), align=TextNode.ALeft)

    def create_button(self, text, command, pos=(0, 0, 0)):
        # Erstelle eine Schaltfläche mit dem angegebenen Text und der Funktion
        pos_vec = LVecBase3f(pos[0], pos[1], 0)  # Z-Position auf 0 setzen
        button = DirectButton(text=text, scale=0.05, pos=pos_vec, command=command,
                              text_fg=(1, 1, 1, 1), frameColor=(0.2, 0.6, 0.2, 1),
                              borderWidth=(0.1, 0.1))
        self.buttons.append(button)  # Füge die Schaltfläche zur Liste hinzu

    def update_buttons(self):
        # Lösche alte Schaltflächen, um den Bildschirm neu zu gestalten
        for button in self.buttons:
            button.destroy()  # Zerstöre die Schaltfläche
        self.buttons.clear()  # Leere die Liste

        # Füge "Zurück"-Button hinzu, falls vorheriger Text vorhanden
        if self.previous_texts:
            self.create_button("Zurück", self.go_back, pos=(-1, 0, -0.15))

        # Neue Schaltflächen basierend auf dem aktuellen Text hinzufügen
        if self.current_text == self.eingang_text:
            self.create_button("Durch das Fenster klettern", self.durch_fenster, pos=(-1, 0, -0.1))
            self.create_button("An der Tür klopfen", self.door_klopfen, pos=(0, 0, -0.15))
            self.create_button("Um das Haus herumgehen", self.haus_rumgehen, pos=(1, 0, -0.2))
        elif self.current_text == self.flur_text:
            self.create_button("In das offene Fenster schauen", self.in_window, pos=(-1, 0, -0.1))

    def go_back(self):
        # Gehe zum letzten Text in der Liste zurück, falls vorhanden
        if self.previous_texts:
            self.current_text = self.previous_texts.pop()  # Entferne den letzten Eintrag
            self.show_text(self.current_text)  # Zeige den vorherigen Text an
            self.update_buttons()  # Aktualisiere die Schaltflächen

    def start_game(self):
        # Beginne das Spiel, indem du den aktuellen Text speicherst und den Eingangstext anzeigst
        self.previous_texts.append(self.current_text)  # Speichere aktuellen Text
        self.current_text = self.eingang_text
        self.show_text(self.current_text)  # Zeige den Eingangstext an
        self.update_buttons()  # Aktualisiere die Schaltflächen

    def durch_fenster(self):
        # Wechsel in den staubigen Raum, speichere den aktuellen Text
        self.previous_texts.append(self.current_text)  # Speichere aktuellen Text
        self.current_text = self.staubiger_raum_text
        self.show_text(self.current_text)  # Zeige den neuen Text an
        self.update_buttons()  # Aktualisiere die Schaltflächen
        self.create_room_selection_buttons()  # Füge Auswahlmöglichkeiten hinzu

    def create_room_selection_buttons(self):
        # Erstelle Schaltflächen für die Auswahl von Räumen
        self.create_button("In den Flur gehen", self.zurueck_zum_flur, pos=(-1, 0, -0.1))
        self.create_button("Zimmer durchsuchen", self.kisten_durchsuchen, pos=(1, 0, -0.1))

    def kisten_durchsuchen(self):
        # Durchsuche die Kisten im Raum und gib ein zufälliges gefundenes Objekt aus
        gefundene_dinge = ["ein altes Buch", "eine geheimnisvolle Notiz"]
        gefunden = random.choice(gefundene_dinge)  # Wähle zufällig ein gefundenes Objekt
        self.show_text(f"Du durchsuchst die Kisten und findest {gefunden}.")  # Zeige das Ergebnis an
        self.update_buttons()  # Aktualisiere die Schaltflächen
        self.create_room_selection_buttons()  # Bietet erneut die Auswahl zwischen Flur und Zimmer an

    def zurueck_zum_flur(self):
        # Gehe zurück zum Flur und speichere den aktuellen Text
        self.previous_texts.append(self.current_text)  # Speichere aktuellen Text
        self.current_text = self.flur_text  # Setze den aktuellen Text auf den Flur
        self.show_text(self.current_text)  # Zeige den Flurtext an
        self.update_buttons()  # Aktualisiere die Schaltflächen

    def update_inventory_display(self):
        # Aktualisiere die Anzeige des Inventars auf dem Bildschirm
        if hasattr(self, 'inventory_display'):
            self.inventory_display.destroy()  # Zerstöre die alte Anzeige
        # Erstelle den Text für das Inventar
        inventory_text = "Inventar:\n" + "\n".join(self.inventory) if self.inventory else "Inventar leer."
        self.inventory_display = OnscreenText(text=inventory_text, pos=(-1.1, 1), scale=0.05,
                                               fg=(1, 1, 1, 1), align=TextNode.ALeft)

    def in_window(self):
        # Interagiere mit dem offenen Fenster und zeige den entsprechenden Text an
        self.previous_texts.append(self.current_text)  # Speichere aktuellen Text
        self.current_text = (
            "Du beugst dich vor und blickst durch das offene Fenster. "
            "Im Inneren siehst du Schatten, die sich bewegen, und hörst leises Flüstern. "
            "Es scheint, als ob jemand im Raum ist, aber du kannst nicht genau erkennen, wer es ist."
        )
        self.show_text(self.current_text)  # Zeige den neuen Text an
        self.update_buttons()  # Aktualisiere die Schaltflächen

    def door_klopfen(self):
        # Interagiere mit der Tür und zeige den entsprechenden Text an
        self.previous_texts.append(self.current_text)  # Speichere aktuellen Text
        self.current_text = (
            "Die Tür blieb fest geschlossen, doch die Geräusche, die aus dem Inneren drangen,\n"
            "ließen dich wissen, dass du nicht allein warst. Etwas lauerte dort,\n"
            "verborgen hinter dem Holz, und es wartete nur auf den richtigen Moment, um hervor zu treten."
        )
        self.show_text(self.current_text)  # Zeige den neuen Text an
        self.update_buttons()  # Aktualisiere die Schaltflächen

    def haus_rumgehen(self):
        # Interagiere mit dem Haus und beschreibe die Umgebung
        self.previous_texts.append(self.current_text)  # Speichere aktuellen Text
        self.current_text = (
            "Während du um das Haus schlichst, fühltest du, wie der Wind durch die knorrigen Äste der Bäume strich, \n"
            "die wie gespenstische Finger in den Himmel ragten. Die Fenster des Hauses waren blind und leer, \n"
            "ihre zerbrochenen Scheiben schienen dich stumm zu beobachten. Ein kalter Schauer lief dir über den Rücken, \n"
            "als du die verwitterte Fassade mustertest, die von der Zeit gezeichnet war.\n\n"
            "Plötzlich bemerkst du ein schwaches Licht, das durch einen Spalt schimmerte. Neugierig näherst du dich \n"
            "und entdeckst ein offenes Fenster im Erdgeschoss. Der Vorhang, zerfetzt und schmutzig, wehte sanft im Wind,\n"
            "als ob er dich einladen wollte, einen Blick hineinzuwerfen. Ein kalter Hauch strömte aus dem Inneren und \n"
            "ließ dich frösteln."
        )
        self.show_text(self.current_text)  # Zeige den neuen Text an
        self.update_buttons()  # Aktualisiere die Schaltflächen

    def tagebuch_lesen(self):
        # Wähle einen zufälligen Inhalt aus dem Tagebuch und zeige ihn an
        self.previous_texts.append(self.current_text)  # Speichere aktuellen Text
        random_key = random.choice(list(self.tagebuch_inhalte.keys()))  # Wähle einen zufälligen Schlüssel
        self.current_text = self.tagebuch_inhalte[random_key]  # Setze den aktuellen Text auf den Tagebuchinhalt
        self.show_text(self.current_text)  # Zeige den neuen Text an
        self.update_buttons()  # Aktualisiere die Schaltflächen

    def schaufel_aufheben(self):
        # Füge die Schaufel zum Inventar hinzu und informiere den Spieler
        self.update_inventory("Schaufel")  # Aktualisiere das Inventar mit der Schaufel
        self.show_text("Du hast die Schaufel aufgehoben.")  # Informiere den Spieler über die Aktion
        self.update_buttons()  # Aktualisiere die Schaltflächen

    def update_inventory(self, item):
        # Füge ein Item zum Inventar hinzu, falls es noch nicht vorhanden ist
        if item not in self.inventory:
            self.inventory.append(item)  # Füge das Item zum Inventar hinzu
            self.show_text(f"Du hast {item} zum Inventar hinzugefügt.")  # Informiere den Spieler

if __name__ == "__main__":
    spiel = Spiel()  # Erstelle eine Instanz des Spiels
    spiel.run()  # Starte das Spiel