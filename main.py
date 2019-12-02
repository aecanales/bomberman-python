import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit
from game.game import start_one_player_game, start_two_player_game
from game.engine import Screen, Engine
from game.game_logic import ScoreManager
from operator import itemgetter


class Menu(QWidget):

    def __init__(self):
        super().__init__()
        self.initialize()

    def initialize(self):
        self.setWindowTitle('Menu de inicio')
        self.setGeometry(200, 200, 300, 300)

        self.start_button_1p = QPushButton('Start - 1 Jugador', self)
        self.start_button_2p = QPushButton('Start - 2 Jugadores', self)
        self.highscore_button = QPushButton('Highscores', self)

        self.start_button_1p.clicked.connect(self.ask_for_one_player_name)
        self.start_button_2p.clicked.connect(self.ask_for_two_player_name)
        self.highscore_button.clicked.connect(self.open_highscores)

        vbox = QVBoxLayout()

        vbox.addStretch(1)
        vbox.addWidget(self.start_button_1p)
        vbox.addStretch(1)
        vbox.addWidget(self.start_button_2p)
        vbox.addStretch(1)
        vbox.addWidget(self.highscore_button)
        vbox.addStretch(1)

        self.setLayout(vbox)

    def ask_for_one_player_name(self):
        QWidget().setLayout(self.layout())  # Simple hack to empty the current layout - https://stackoverflow.com/a/10439207

        self.player_one_name_label = QLabel('Nombre jugador 1:', self)
        self.player_one_name = QLineEdit('Jugador1', self)

        self.ready_button = QPushButton('Listo', self)
        self.ready_button.clicked.connect(self.start_one_player_game)

        hbox = QHBoxLayout()

        hbox.addStretch(1)
        hbox.addWidget(self.player_one_name_label)
        hbox.addStretch(1)
        hbox.addWidget(self.player_one_name)
        hbox.addStretch(1)
        hbox.addWidget(self.ready_button)

        self.setLayout(hbox)

    def ask_for_two_player_name(self):
        QWidget().setLayout(self.layout())  # Simple hack to empty the current layout - https://stackoverflow.com/a/10439207

        self.player_one_name_label = QLabel('Nombre jugador 1:', self)
        self.player_one_name = QLineEdit('Jugador1', self)

        self.player_two_name_label = QLabel('Nombre jugador 2:', self)
        self.player_two_name = QLineEdit('Jugador2', self)

        self.ready_button = QPushButton('Listo', self)
        self.ready_button.clicked.connect(self.start_two_player_game)

        player_one = QHBoxLayout()

        player_one.addStretch(1)
        player_one.addWidget(self.player_one_name_label)
        player_one.addStretch(1)
        player_one.addWidget(self.player_one_name)
        player_one.addStretch(1)

        player_two = QHBoxLayout()

        player_two.addStretch(1)
        player_two.addWidget(self.player_two_name_label)
        player_two.addStretch(1)
        player_two.addWidget(self.player_two_name)
        player_two.addStretch(1)

        players = QVBoxLayout()

        players.addStretch(1)
        players.addLayout(player_one)
        players.addStretch(1)
        players.addLayout(player_two)
        players.addStretch(1)
        players.addWidget(self.ready_button)
        players.addStretch(1)

        self.setLayout(players)

    def start_one_player_game(self):
        self.game_window = GameWindow(self, [self.player_one_name.text()])
        self.game_window.show()
        self.hide()

    def start_two_player_game(self):
        self.game_window = GameWindow(self, [self.player_one_name.text(), self.player_two_name.text()])
        self.game_window.show()
        self.hide()

    def open_highscores(self):
        self.highscores = HighScores()
        self.highscores.show()


class GameWindow(QMainWindow):

    def __init__(self, menu, players):
        super().__init__()

        self.menu = menu

        self.setWindowTitle('Code with Fire')
        self.setGeometry(200, 50, 800, 650)

        self.player_names = players
        self.alive_players = len(players)

        self.game_engine = Engine()
        self.game_screen = Screen(self.game_engine)
        self.score_manager = ScoreManager(self.game_screen)

        self.setCentralWidget(self.game_screen)
        self.create_menu_bar()

        self.start_game(players)

    def start_game(self, players):
        if len(players) == 1:
            start_one_player_game(self, self.game_engine, self.game_screen, self.score_manager)
        elif len(players) == 2:
            start_two_player_game(self, self.game_engine, self.game_screen, self.score_manager)

        self.game_engine.start()

    def create_menu_bar(self):
        pause_button = QAction(QIcon(None), '&Pausar Juego', self)
        pause_button.setShortcut('Ctrl+P')
        pause_button.triggered.connect(self.game_engine.toggle_pause)

        quit_button = QAction(QIcon(None), '&Cerrar Juego', self)
        quit_button.setShortcut('Ctrl+E')
        quit_button.triggered.connect(self.quit_game)

        actions = self.menuBar().addMenu('&Menú')
        actions.addAction(pause_button)
        actions.addAction(quit_button)

    # I pass the key events to the game screen widget.
    def keyPressEvent(self, event):
        self.game_screen.keyPressEvent(event)

    def keyReleaseEvent(self, event):
        self.game_screen.keyReleaseEvent(event)

    def player_death(self, player_death_event):
        player_score = (self.player_names[player_death_event.player], player_death_event.score)
        HighScores.add_and_save_highscore(list(HighScores.get_highscores()), player_score)

        self.alive_players -= 1

        if self.alive_players <= 0:
            self.end_game()

    def quit_game(self):
        player_score = (self.player_names[0], self.score_manager.score)
        HighScores.add_and_save_highscore(list(HighScores.get_highscores()), player_score)

        self.end_game()

    def end_game(self):
        self.game_engine.stop = True
        self.hide()

        QWidget().setLayout(self.menu.layout())  # Simple hack to empty the current layout - https://stackoverflow.com/a/10439207
        self.menu.initialize()
        self.menu.show()
        self.menu.open_highscores()


class HighScores(QWidget):

    def __init__(self):
        super().__init__()
        self.initialize()

    def initialize(self):
        self.setWindowTitle('High Scores')
        self.setGeometry(300, 300, 300, 300)

        vbox = QVBoxLayout()
        vbox.addWidget(QLabel('     Nombre     Puntaje', self))
        vbox.addStretch(1)

        with open('highscores.csv', 'r') as file:
            for position, line in enumerate(file.readlines()[1:], 1):
                name, score = line.rstrip('\n').split(',')

                vbox.addWidget(QLabel(f'{position: <2d}.- {name:^10s}  {score: ^9s}', self))
                vbox.addStretch(1)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(vbox)
        hbox.addStretch(1)

        self.setLayout(hbox)

    @staticmethod
    def get_highscores():
        with open('highscores.csv', 'r') as infile:
            for line in infile.readlines()[1: ]:
                name, score = line.rstrip('\n').split(',')
                yield (name, int(score))

    @staticmethod
    def add_and_save_highscore(scores, new_score):
        scores.append(new_score)
        scores.sort(key=itemgetter(1), reverse=True)

        with open('highscores.csv', 'w') as outfile:
            outfile.write('name,score')
            for i in range(10):
                outfile.write(f'\n{scores[i][0]},{scores[i][1]}')


if __name__ == '__main__':

    def hook(type, value, traceback):
        print(type)
        print(traceback)


    sys.__excepthook__ = hook
    app = QApplication([])

    menu = Menu()
    menu.show()

    app.exec_()

