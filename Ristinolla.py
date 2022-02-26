"""
TIE-02100 Johdatus ohjelmointiin, kevät 2018
TIE-02106 Introduction to Programming, Spring 2018
tekijän nimi: Tomi Lotila
opnro: 274802
ohjelma: Ristinolla - Tic tac toe
pelissä on kaksi pelityyliä moninpeli - multiplayer ja yksinpeli singleplayer.
Moninpeli vaatii kaksi pelaaja, ensimmäinen pelaaja joka saa kolme merkkiä (X tai 0)
voittaa pelin. Yksinpelissä pelaaja pelaa tietokenetta vastaa, muuten sama.

käynnistyksen jälkeen pitää valita pelityyli ennen kuin pääsee pelaan.

pelin ohjemointi on tehty skaalautuvaksi, pelikentän napit on tallennettu listaan
ja niihin tehdään muutoksia for-lausekkeen avulla.
"""

from tkinter import *
import random

ROWS = 3
COLUMNS = 3
SPOTS = 9
victory_lines = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7],
                 [2, 5, 8], [0, 4, 8], [2, 4, 6]]


class Tic_tac_toe:

    def __init__(self):
        self.__window = Tk()
        self.__window.title("Tic tac toe")
        self.__board_buttons = []
        self.__turn = None
        self.__player_points = None
        self.__bot = None
        self.__empty_spot_list = None

        # luo tekstin Tic Tac toe ikkunaan
        self.__start_menu = Label(self.__window, text="Tic tac toe", font="Verdana 12"
                                  , padx=30, pady=35)
        self.__start_menu.grid(row=0, column=0)

        # luo Multipalyer napin, nappi kutsuu self.start_game
        self.__start_game_button = Button(self.__window, text="Multiplayer"
                                          , command=self.start_game, padx=30, pady=10)
        self.__start_game_button.grid(row=1, column=0)

        # luo Singlepalyer napin, nappi kutsuu self.active_bot
        self.__start_game_button = Button(self.__window, text="Singleplayer"
                                          , command=self.active_bot, padx=30, pady=10)
        self.__start_game_button.grid(row=2, column=0)

        # luo self.__info labelin tuleevaa tekstiä varten
        self.__info = Label(self.__window, font="Verdana 12", padx=30, pady=5)
        self.__info.grid(row=3, column=1, columnspan=3)

        # luo Exit napin poistumista varten
        Button(self.__window, text="Exit", command=self.__window.destroy, padx=30, pady=3) \
            .grid(row=3, column=0)

        # luo kentän napit ja lisää ne listaan self.__button_boards
        for row in range(0, ROWS):
            for column in range(0, COLUMNS):
                if row == 0:
                    lock = self.lock(column)
                elif row == 1:
                    lock = self.lock(3 + column)
                else:
                    lock = self.lock(6 + column)

                new_button = Button(self.__window, padx=10, pady=5, borderwidth=5
                                    , command=lock, background="light grey", state=DISABLED
                                    , text="  ", font="Verdana 35")
                new_button.grid(row=row, column=1 + column)
                self.__board_buttons.append(new_button)

    def change_turn(self):
        # vaihtaa pelaajan vuoroa, ja päivittää info-tekstin
        if self.__turn == ["0", 1]:
            self.__turn = ["X", 0]
        else:
            self.__turn = ["0", 1]
        self.__info.configure(text="Player {} turn".format(self.__turn[0]))

    def lock(self, number):
        """
        sulkeumafunkio
        :param number: lista, joka siältää painonapin rivin ja sarakkeen
        :return: sulkeumafunktio
        """
        def function():
            self.lock_button(number)
        return function

    def random_mark(self):
        # luo satunnaisen vuoron
        random1 = random.randint(0, 1)
        if random1 == 0:
            self.__turn = ["X", 0]
        else:
            self.__turn = ["0", 1]

    def start_game(self):
        # luo alkuasetukset uuden pelin alkamiselle
        self.random_mark()
        self.__player_points = [[], []]
        self.__bot = None
        self.__start_game_button.configure(text="Singleplayer")
        self.__empty_spot_list = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.__info.configure(text="Player {} turn".format(self.__turn[0]))
        self.reset_board()

    def lock_button(self, button):
        """
        1. sulkee kutsutun napin
        2. kutsuu etsi_voittaja funktion
        3. käynnistää tietokonevastuksen jos on päällä ja sen vuoro
        :param button: suljettavan napin numero
        """
        self.__empty_spot_list.remove(button)
        self.__board_buttons[button].configure(text=self.__turn[0], state=DISABLED)
        self.__player_points[self.__turn[1]].append(button)
        if self.find_winner() is True:
            self.disable_board()
        else:
            self.change_turn()
            if self.__bot == "active" and self.__turn[0] == "X":
                self.bot_script()

    def find_winner(self):
        # etsii voittaja tai pätee tasapelin ja tulostaa tiedon
        for line in victory_lines:
            # jos pelaajalla on sama kolmen merkin linjassa
            # kuin victory_lines-listassa pelaaja voittaa
            if line[0] in self.__player_points[self.__turn[1]] and line[1] \
                    in self.__player_points[self.__turn[1]] and line[2] \
                    in self.__player_points[self.__turn[1]]:
                self.__info.configure(text="Player {} wins!".format(self.__turn[0]))
                # vaihtaa voitto linjass olevien nappien värit vihreäksi
                for button_number in line:
                    self.__board_buttons[button_number].configure(background="green")
                return True

        # jos tasapeli
        if len(self.__player_points[0]) + len(self.__player_points[1]) == SPOTS:
            self.__info.configure(text="The game ends in a Tie!".format(self.__turn[0]))
            return True

    def reset_board(self):
        # asettaa kaikki peliketän napit alkuarvoiksi
        for button in self.__board_buttons:
            button.configure(state=NORMAL, text="  ", font="Verdana 35",
                             background="light grey")

    def disable_board(self):
        # estää kentän nappejen painamisen
        for button in self.__board_buttons:
            button.configure(state=DISABLED)

    def active_bot(self):
        # valmistaa tietokone vastuksen ja käynnistää pelin
        self.start_game()
        self.__start_game_button.configure(text="Singleplayer\nbot = X")
        self.__bot = "active"
        if self.__turn[0] == "X":
            self.bot_script()

    def bot_script(self):
        """
        bot funktio käy läpi järjestyksessä kolme vaihetta ja
        suorittaa niistä ensimmäisen sopivan (valitsee ruudukosta kohdan)
        1. jos itsellä on kaksi merkkiä linjassa ja kolmas paikka on tyhjä lisää sen ja voittaa
        2. jos vastustajalla on kaksi merkkiä linjassa,
            lisää kolmannen paikan tilalle oman merkin, estää voiton
        3. lisää merkin satunnaiseen tyhjään paikkaan
        """
        # 1.
        for line in victory_lines:
            times = 0
            for button_number in line:  # käy läpi voitto linjan
                if button_number in self.__player_points[0]:
                    times += 1
            if times == 2:  # jos kaksi
                for button_number in line:
                    # lisää merkin komanteen paikkaan, jos tyhjä
                    if button_number in self.__empty_spot_list:
                        self.lock_button(button_number)
                        return
        # 2. (kohtia 1 ja 2 ei voida laittaa samaan for lauseeseen, koska
                # victory_lines-lista käy läpi voittolinjat tietyssä järjestyksessä
        for line in victory_lines:
            times = 0
            for button_number in line:  # käy läpi voitto linjan
                if button_number in self.__player_points[1]:
                    times += 1
            if times == 2:  # jos kaksi
                for button_number in line:
                    # lisää merkin komanteen paikkaan, jos tyhjä
                    if button_number in self.__empty_spot_list:
                        self.lock_button(button_number)
                        return
        # 3.
        random2 = random.randint(0, len(self.__empty_spot_list)-1)
        button = self.__empty_spot_list[random2]
        self.lock_button(button)

    def start(self):
        # aukaisee ikkunan
        self.__window.mainloop()


def main():
    ui = Tic_tac_toe()
    ui.start()


main()