from panda3d.core import LVecBase3f, TextNode
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectButton import DirectButton
from direct.gui.OnscreenText import OnscreenText
import random
import os

class Game(ShowBase):
    def __init__(self):
        super().__init__()
        self.inventory = Inventory()  # Initialisiere das Inventar
        self.current_room = 'eingang'
        self.set_background()
        self.setup_music()  # Musik einrichten

        self.intro_text = "Herzlich Willkommen zum Abenteuer deines Lebens!"
        self.eingang_text = "Du stehst vor der verschlossenen Eingangstür des Herrenhauses. Ein kleines Fenster auf der linken Seite ist offen."
        self.dusty_room_text = "Du kletterst durch das Fenster, und ein kalter Wind weht dir ins Gesicht."
        self.hallway_text = "Du bist jetzt im Flur und hörst ein seltsames Geräusch."
        self.kitchen_text = "In der Küche riecht es nach alten Gewürzen. Ein Kühlschrank steht in der Ecke."
        self.library_text = "Die Bibliothek ist still und dunkel. Regale voller Bücher stehen an den Wänden."
        self.walk_around_story = "Während du um das Haus gehst, bemerkst du ein offenes Fenster.\n " \
                                 "Es sieht einladend aus, aber du bist dir nicht sicher,\n" \
                                 "ob du es untersuchen oder hinein klettern sollst."

        self.current_text = self.intro_text
        self.previous_texts = []
        self.room_previous_texts = {
            'eingang': [],
            'dusty_room': [],
            'hallway': [],
            'kitchen': [],
            'library': []
        }
        self.show_text(self.current_text)
        self.buttons = []
        self.create_button("Spiel starten", self.start_game)

    def set_background(self):
        self.win.setClearColor((0.05, 0.05, 0.1, 1))

    def setup_music(self):
        try:
            music_path = os.path.join("musik.mp3")
            self.bgm = self.loader.loadSfx(music_path)  # Lade die Musikdatei
            self.bgm.setLoop(True)  # Setze die Musik auf Schleifen
            self.bgm.play()  # Spiele die Musik ab
        except Exception as e:
            print(f"Fehler beim Laden der Musik: {e}")

    def show_text(self, text):
        if hasattr(self, 'text_object'):
            self.text_object.destroy()
        self.text_object = OnscreenText(text=text, pos=(-1.3, 0.5), scale=0.05,
                                          fg=(1, 0.8, 0.2, 1), align=TextNode.ALeft)

    def create_button(self, text, command, pos_x=0):
        pos_vec = LVecBase3f(pos_x, -0.2, 0)  # Setze die y-Position konstant
        button = DirectButton(text=text, scale=0.05, pos=pos_vec, command=command,
                              text_fg=(1, 1, 1, 1), frameColor=(0.2, 0.6, 0.2, 1),
                              borderWidth=(0.1, 0.1))
        self.buttons.append(button)

    def update_buttons(self):
        # Alte Buttons zerstören
        for button in self.buttons:
            button.destroy()
        self.buttons.clear()  # Leere die Liste der Buttons

        left_button_x = -0.5  # Position für den linken Button
        right_button_x = 0.5  # Position für den rechten Button

        self.create_button("Zurück", self.back, pos_x=0)  # "Zurück"-Button in der Mitte

        # Neue Buttons je nach aktuellem Raum erstellen
        if self.current_room == 'eingang':
            self.create_button("An der Tür klopfen", self.knock_on_door, pos_x=left_button_x)
            self.create_button("Um das Gebäude herumgehen", self.walk_around_building, pos_x=right_button_x)

        elif self.current_room == 'dusty_room':
            self.create_button("In den Flur gehen", self.back_to_hallway, pos_x=left_button_x)
            self.create_button("Kisten durchsuchen", self.search_boxes, pos_x=right_button_x)

        elif self.current_room == 'hallway':
            self.create_button("Zur Küche gehen", self.go_to_kitchen, pos_x=left_button_x)
            self.create_button("Zur Bibliothek gehen", self.go_to_library, pos_x=right_button_x)

        elif self.current_room == 'kitchen':
            self.create_button("Zurück in den Flur", self.back_to_hallway, pos_x=left_button_x)

        elif self.current_room == 'library':
            self.create_button("Zurück in den Flur", self.back_to_hallway, pos_x=left_button_x)

    def load_eingang(self):
        self.current_text = self.eingang_text
        self.show_text(self.current_text)
        self.update_buttons()

    def load_dusty_room(self):
        self.current_text = self.dusty_room_text
        self.show_text(self.current_text)
        self.update_buttons()

    def load_hallway(self):
        self.current_text = self.hallway_text
        self.show_text(self.current_text)
        self.update_buttons()

    def load_kitchen(self):
        self.current_text = self.kitchen_text
        self.show_text(self.current_text)
        self.update_buttons()

    def load_library(self):
        self.current_text = self.library_text
        self.show_text(self.current_text)
        self.update_buttons()

    def knock_on_door(self):
        self.previous_texts.append(self.current_text)
        self.current_text = "Die Tür blieb fest geschlossen, doch die Geräusche,\n" \
                            "die aus dem Inneren drangen, ließen dich wissen, dass du nicht allein warst."
        self.show_text(self.current_text)
        self.update_buttons()

    def walk_around_building(self):
        self.room_previous_texts[self.current_room].append(self.current_text)
        self.current_text = self.walk_around_story
        self.show_text(self.current_text)
        self.update_buttons()
        
        left_button_x = -0.5  # Position für den linken Button
        right_button_x = 0.5  # Position für den rechten Button

        self.create_button("Weiter untersuchen", self.continue_investigation, pos_x=left_button_x)
        self.create_button("Ins Fenster klettern", self.climb_through_window, pos_x=right_button_x)

    def continue_investigation(self):
        self.current_text = "Du entscheidest dich, das Fenster genauer zu untersuchen.\n " \
                            "Es sieht so aus, als ob es einen Weg ins Innere gibt."
        self.show_text(self.current_text)
        self.update_buttons()

    def climb_through_window(self):
        self.room_previous_texts[self.current_room].append(self.current_text)
        self.current_room = 'dusty_room'  # Gehe durch das Fenster in den staubigen Raum
        self.load_dusty_room()  # Lade den staubigen Raum

    def back_to_hallway(self):
        self.room_previous_texts[self.current_room].append(self.current_text)
        self.current_room = 'hallway'
        self.load_hallway()

    def go_to_kitchen(self):
        self.room_previous_texts[self.current_room].append(self.current_text)
        self.current_room = 'kitchen'
        self.load_kitchen()

    def go_to_library(self):
        self.room_previous_texts[self.current_room].append(self.current_text)
        self.current_room = 'library'
        self.load_library()

    def back(self):
        if self.room_previous_texts[self.current_room]:
            self.current_text = self.room_previous_texts[self.current_room].pop()
            self.show_text(self.current_text)
            self.update_buttons()
        else:
            if self.current_room == 'eingang':
                self.load_eingang()
            elif self.current_room == 'dusty_room':
                self.load_dusty_room()
            elif self.current_room == 'hallway':
                self.load_hallway()
            elif self.current_room == 'kitchen':
                self.load_kitchen()
            elif self.current_room == 'library':
                self.load_library()

    def start_game(self):
        self.previous_texts.append(self.current_text)
        self.load_eingang()

    def search_boxes(self):
        found_items = ["ein altes Buch", "eine geheimnisvolle Notiz", "ein Schlüssel"]
        found = random.choice(found_items)
        self.inventory.add_item(found)
        self.show_text(f"Du durchsuchst die Kisten und findest {found}.")
        self.update_buttons()

class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def use_item(self, item):
        if item in self.items:
            self.items.remove(item)
            return f"Du verwendest {item}."
        else:
            return "Dieser Gegenstand ist nicht im Inventar."

    def examine_item(self, item):
        descriptions = {
            "ein altes Buch": "Es ist ein verstaubtes Buch mit geheimen Geschichten.",
            "eine geheimnisvolle Notiz": "Die Notiz enthält rätselhafte Hinweise.",
            "ein Schlüssel": "Ein alter, rostiger Schlüssel."
        }
        return descriptions.get(item, "Du kannst diesen Gegenstand nicht untersuchen.")

if __name__ == "__main__":
    game = Game()
    game.run()