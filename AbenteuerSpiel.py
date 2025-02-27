from panda3d.core import LVecBase3f, TextNode
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectButton import DirectButton
from direct.gui.OnscreenText import OnscreenText
import random

class Game(ShowBase):
    def __init__(self):
        super().__init__()
        self.inventory = Inventory()  # Initialisiere das Inventar
        self.current_room = 'eingang'  # Füge die Zustandsvariable für den Raum hinzu
        self.set_background()
        self.bgm = self.loader.loadSfx("musik.mp3")  
        self.bgm.setLoop(True)
        self.bgm.play()

        self.intro_text = "Herzlich Willkommen zum Abenteuer deines Lebens!"
        self.eingang_text = "Du stehst vor der verschlossenen Eingangstür des Herrenhauses. Ein kleines Fenster auf der linken Seite ist offen."
        self.dusty_room_text = "Du kletterst durch das Fenster, und ein kalter Wind weht dir ins Gesicht."
        self.hallway_text = "Du bist jetzt im Flur und hörst ein seltsames Geräusch."

        self.current_text = self.intro_text
        self.previous_texts = []
        self.room_previous_texts = {'eingang': [], 'dusty_room': [], 'hallway': []}
        self.show_text(self.current_text)
        self.buttons = []
        self.create_button("Spiel starten", self.start_game, pos=(0, -0.3))

    def set_background(self):
        """Setze die Hintergrundfarbe des Fensters."""
        self.win.setClearColor((0.05, 0.05, 0.1, 1))  # Dunkelblau

    def show_text(self, text):
        """Zeige den gegebenen Text im Spiel an."""
        if hasattr(self, 'text_object'):
            self.text_object.destroy()  # Zerstöre vorherigen Text
        self.text_object = OnscreenText(text=text, pos=(-1.3, 0.5), scale=0.05,
                                          fg=(1, 0.8, 0.2, 1), align=TextNode.ALeft)

    def create_button(self, text, command, pos=(0, 0, 0)):
        """Erstelle eine Schaltfläche mit dem gegebenen Text und der zugehörigen Funktion."""
        pos_vec = LVecBase3f(pos[0], pos[1], 0)
        button = DirectButton(text=text, scale=0.05, pos=pos_vec, command=command,
                              text_fg=(1, 1, 1, 1), frameColor=(0.2, 0.6, 0.2, 1),
                              borderWidth=(0.1, 0.1))
        self.buttons.append(button)  # Füge die Schaltfläche zur Liste hinzu

    def update_buttons(self):
        """Aktualisiere die Schaltflächen basierend auf dem aktuellen Raum."""
        for button in self.buttons:
            button.destroy()  # Zerstöre vorherige Schaltflächen
        self.buttons.clear()  # Leere die Schaltflächenliste

        # Gemeinsamer Zurück-Button
        self.create_button("Zurück", self.back, pos=(1, -0.2, 0))  # Erstelle den Zurück-Button

        # Schaltflächen für verschiedene Szenen
        if self.current_room == 'eingang':
            self.create_button("An der Tür klopfen", self.knock_on_door, pos=(-1, 0.1, 0))
            self.create_button("Um das Gebäude herumgehen", self.walk_around_building, pos=(1, 0, 0))

        elif self.current_room == 'dusty_room':
            self.create_button("In den Flur gehen", self.back_to_hallway, pos=(1, 0.1, 0))
            self.create_button("Kisten durchsuchen", self.search_boxes, pos=(0, 0, 0))

        elif self.current_room == 'hallway':
            self.create_button("Durch den Flur gehen", self.walk_through_hallway, pos=(0, 0.1, 0))
            self.create_button("Tür untersuchen", self.inspect_door, pos=(-1, 0, 0))

    def knock_on_door(self):
        """Klopfe an die Tür und beschreibe die Reaktion."""
        self.previous_texts.append(self.current_text)  # Speichere den aktuellen Text
        self.current_text = "Die Tür blieb fest geschlossen, doch die Geräusche, die aus dem Inneren drangen, ließen dich wissen, dass du nicht allein warst."
        self.show_text(self.current_text)  # Zeige den neuen Text an
        self.update_buttons()  # Aktualisiere die Schaltflächen

    def walk_around_building(self):
        """Gehe um das Gebäude herum und zeige die Optionen für die Hintertür an."""
        self.room_previous_texts[self.current_room].append(self.current_text)  # Speichere den Text für den aktuellen Raum
        self.current_text = "Du gehst um das Gebäude herum und siehst viele Fenster und Türen."
        self.current_room = 'dusty_room'  # Aktualisiere den aktuellen Raum
        self.show_text(self.current_text)
        self.update_buttons()

    def back_to_hallway(self):
        """Gehe zurück in den Flur."""
        self.room_previous_texts[self.current_room].append(self.current_text)  # Speichere den Text für den aktuellen Raum
        self.current_text = self.hallway_text  # Setze den aktuellen Text auf den Flur
        self.current_room = 'hallway'  # Aktualisiere den aktuellen Raum
        self.show_text(self.current_text)  # Zeige den Flurtext an
        self.update_buttons()  # Aktualisiere die Schaltflächen

    def back(self):
        """Gehe zurück zum vorherigen Text im jeweiligen Raum."""
        if self.room_previous_texts[self.current_room]:
            self.current_text = self.room_previous_texts[self.current_room].pop()  # Hole den letzten gespeicherten Text
            self.show_text(self.current_text)  # Zeige den alten Text an
            self.update_buttons()  # Aktualisiere die Schaltflächen
        else:
            self.current_text = self.intro_text  # Gehe zurück zum Einführungstext
            self.current_room = 'eingang'  # Gehe zurück zum Eingang
            self.show_text(self.current_text)  # Zeige den Einführungstext an
            self.update_buttons()  # Aktualisiere die Schaltflächen

    def start_game(self):
        """Starte das Spiel und zeige den Eingangstext an."""
        self.previous_texts.append(self.current_text)  # Speichere den aktuellen Text
        self.current_text = self.eingang_text  # Setze den aktuellen Text auf den Eingangstext
        self.current_room = 'eingang'  # Setze den aktuellen Raum
        self.show_text(self.current_text)  # Zeige den Eingangstext an
        self.update_buttons()  # Aktualisiere die Schaltflächen

    def search_boxes(self):
        """Durchsuche Kisten nach Gegenständen."""
        found_items = ["ein altes Buch", "eine geheimnisvolle Notiz"]  # Liste möglicher Gegenstände
        found = random.choice(found_items)  # Wähle zufällig einen gefundenen Gegenstand aus
        self.inventory.add_item(found)  # Füge den Gegenstand zum Inventar hinzu
        self.show_text(f"Du durchsuchst die Kisten und findest {found}.")  # Zeige, was gefunden wurde
        self.update_buttons()  # Aktualisiere die Schaltflächen

    def walk_through_hallway(self):
        """Gehe durch den Flur und beschreibe die Umgebung."""
        self.room_previous_texts[self.current_room].append(self.current_text)  # Speichere den Text für den aktuellen Raum
        self.current_text = "Du gehst weiter durch den Flur. Die Wände sind kalt und das Licht flackert."
        self.current_room = 'hallway'  # Aktualisiere den aktuellen Raum
        self.show_text(self.current_text)
        self.update_buttons()

    def inspect_door(self):
        """Untersuche die Tür und beschreibe, was du siehst."""
        self.room_previous_texts[self.current_room].append(self.current_text)  # Speichere den Text für den aktuellen Raum
        self.current_text = "Du näherst dich einer der Türen und bemerkst, dass sie leicht geöffnet ist."
        self.show_text(self.current_text)
        self.update_buttons()

class Inventory:
    def __init__(self):
        self.items = []  # Initialisiere die Liste der Gegenstände

    def add_item(self, item):
        """Füge einen Gegenstand zum Inventar hinzu."""
        self.items.append(item)  # Füge den Gegenstand zur Liste hinzu

    def use_item(self, item):
        """Verwende einen Gegenstand aus dem Inventar."""
        if item in self.items:
            self.items.remove(item)  # Entferne den Gegenstand aus dem Inventar
            return f"Du verwendest {item}."  # Rückgabe einer Bestätigung
        else:
            return "Dieser Gegenstand ist nicht im Inventar."  # Rückgabe, wenn der Gegenstand nicht gefunden wurde

    def examine_item(self, item):
        """Untersuche einen Gegenstand im Inventar und gib eine Beschreibung zurück."""
        descriptions = {
            "ein altes Buch": "Es ist ein verstaubtes Buch mit geheimen Geschichten.",  # Beschreibung für ein altes Buch
            "eine geheimnisvolle Notiz": "Die Notiz enthält rätselhafte Hinweise."  # Beschreibung für eine geheimnisvolle Notiz
        }
        return descriptions.get(item, "Du kannst diesen Gegenstand nicht untersuchen.")  # Rückgabe der Beschreibung oder Fehlerhinweis

if __name__ == "__main__":
    game = Game()  # Erstelle ein neues Spiel
    game.run()  # Starte das Spiel