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
            "Die Schatten der alten Möbel scheinen lebendig zu werden."
        )
        self.flur_text = (
            "Du bist jetzt im Flur und hörst ein seltsames Geräusch. \n"
            "Es weht ein eiskalter Wind durch den Flur."
        )

        # Aktuellen und vorherigen Text initialisieren
        self.current_text = self.intro_text
        self.previous_texts = []  # Liste zur Speicherung der vorherigen Texte
        self.inventory = []  # Inventar initialisieren
        self.show_text(self.current_text)  # Zeige den Einführungstext an

        # Schaltflächen initialisieren
        self.buttons = []  # Liste zur Speicherung der Schaltflächen
        self.create_button("Spiel starten", self.start_game, pos=(0, -0.3))

    def set_background(self):
        self.win.setClearColor((0.05, 0.05, 0.1, 1))  # Dunkelblau

    def show_text(self, text):
        if hasattr(self, 'text_object'):
            self.text_object.destroy()
        self.text_object = OnscreenText(text=text, pos=(-1.3, 0.5), scale=0.05,
                                          fg=(1, 0.8, 0.2, 1), align=TextNode.ALeft)

    def create_button(self, text, command, pos=(0, 0, 0)):
        pos_vec = LVecBase3f(pos[0], pos[1], 0)
        button = DirectButton(text=text, scale=0.05, pos=pos_vec, command=command,
                              text_fg=(1, 1, 1, 1), frameColor=(0.2, 0.6, 0.2, 1),
                              borderWidth=(0.1, 0.1))
        self.buttons.append(button)

    def update_buttons(self):
        for button in self.buttons:
            button.destroy()
        self.buttons.clear()

        # Gemeinsamer Zurück-Button
        self.create_button("Zurück", self.zurueck, pos=(0, -0.2, 0))

        if self.current_text == self.eingang_text:
            self.create_button("An der Tür klopfen", self.door_klopfen, pos=(-1, 0.1, 0))
            self.create_button("Um das Gebäude herumgehen", self.um_das_gebaeude, pos=(1, 0, 0))

        elif self.current_text == self.staubiger_raum_text:
            self.create_button("In den Flur gehen", self.zurueck_zum_flur, pos=(0, 0.1, 0))
            self.create_button("Kisten durchsuchen", self.kisten_durchsuchen, pos=(0, 0, 0))

        elif self.current_text == self.flur_text:
            self.create_button("Durch den Flur gehen", self.gehe_durch_den_flur, pos=(0, 0.1, 0))
            self.create_button("Tür untersuchen", self.untersuchen_tuer, pos=(0, 0, 0))

    def um_das_gebaeude(self):
        self.previous_texts.append(self.current_text)
        self.current_text = (
            "Du gehst um das Gebäude herum und siehst viele Fenster und Türen. \n"
            "Es gibt eine Hintertür, die leicht offen steht."
        )
        self.show_text(self.current_text)
        self.update_buttons()
        # Auswahl-Buttons für die Hintertür
        self.create_button("Hintertür untersuchen", self.untersuchen_hintertuer, pos=(1, 0.1, 0))
        self.create_button("Hintertür öffnen", self.oefnen_hintertuer, pos=(-1, 0, 0))

    def untersuchen_hintertuer(self):
        self.previous_texts.append(self.current_text)
        self.current_text = (
            "Du näherst dich der Hintertür und bemerkst, dass sie leicht knarrt.\n"
            "Ein unheimliches Gefühl überkommt dich."
        )
        self.show_text(self.current_text)
        self.update_buttons()

    def oefnen_hintertuer(self):
        self.previous_texts.append(self.current_text)
        self.current_text = (
            "Du öffnest die Hintertür und trittst vorsichtig ein. \n"
            "Ein kalter Wind weht dir entgegen und du hörst ein leises Flüstern."
        )
        self.show_text(self.current_text)
        self.update_buttons()

    def gehe_durch_den_flur(self):
        self.previous_texts.append(self.current_text)
        self.current_text = (
            "Du gehst weiter durch den Flur. Die Wände sind kalt und das Licht flackert.\n"
            "Du hörst ein leises Geräusch aus einem der Zimmer."
        )
        self.show_text(self.current_text)
        self.update_buttons()

    def untersuchen_tuer(self):
        self.previous_texts.append(self.current_text)
        self.current_text = (
            "Du näherst dich einer der Türen und bemerkst, dass sie leicht geöffnet ist.\n"
            "Ein seltsames Licht strahlt aus dem Raum."
        )
        self.show_text(self.current_text)
        self.update_buttons()

    def zurueck(self):
        if self.previous_texts:
            self.current_text = self.previous_texts.pop()
            self.show_text(self.current_text)
            self.update_buttons()
        else:
            self.current_text = self.intro_text
            self.show_text(self.current_text)
            self.update_buttons()

    def zurueck_zum_eingang(self):
        self.previous_texts.append(self.current_text)
        self.current_text = self.eingang_text
        self.show_text(self.current_text)
        self.update_buttons()

    def start_game(self):
        self.previous_texts.append(self.current_text)
        self.current_text = self.eingang_text
        self.show_text(self.current_text)
        self.update_buttons()

    def durch_fenster(self):
        self.previous_texts.append(self.current_text)
        self.current_text = self.staubiger_raum_text
        self.show_text(self.current_text)
        self.update_buttons()

    def kisten_durchsuchen(self):
        gefundene_dinge = ["ein altes Buch", "eine geheimnisvolle Notiz"]
        gefunden = random.choice(gefundene_dinge)
        self.show_text(f"Du durchsuchst die Kisten und findest {gefunden}.")
        self.update_buttons()

    def zurueck_zum_flur(self):
        self.previous_texts.append(self.current_text)
        self.current_text = self.flur_text
        self.show_text(self.current_text)
        self.update_buttons()

    def door_klopfen(self):
        self.previous_texts.append(self.current_text)
        self.current_text = (
            "Die Tür blieb fest geschlossen, doch die Geräusche, die aus dem Inneren drangen,\n"
            "ließen dich wissen, dass du nicht allein warst."
        )
        self.show_text(self.current_text)
        self.update_buttons()

    def zurueck_zum_staubigen_raum(self):
        self.previous_texts.append(self.current_text)
        self.current_text = self.staubiger_raum_text
        self.show_text(self.current_text)
        self.update_buttons()

if __name__ == "__main__":
    spiel = Spiel()
    spiel.run()