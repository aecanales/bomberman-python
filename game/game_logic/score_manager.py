from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QLabel, QProgressBar
from game.game_logic.parameters import SCORE_CONSTANTS


class ScoreManager(QTimer):

    def __init__(self, front_end):
        super().__init__()

        self.text = QLabel('Puntaje: 0', front_end)
        self.text.move(10, 80)

        self.progress_bar = QProgressBar(front_end)
        self.progress_bar.setGeometry(10, 100, 80, 15)

        self.score = 0
        self.difficulty_increase = SCORE_CONSTANTS['DIFFICULTY_INCREASE']

        self.timeout.connect(self.add_timer_score)
        self.start(SCORE_CONSTANTS['TIME_FOR_SCORE'] * 1000)

    def add_score(self, value):
        self.score += value

        self.text.setText(f'Puntaje: {self.score}')
        self.text.resize(self.text.sizeHint())

        if self.score >= self.difficulty_increase:
            print("DIFFICULTY INCREASE")
            self.difficulty_increase += SCORE_CONSTANTS['DIFFICULTY_INCREASE']

        self.progress_bar.setValue(round(((self.score % SCORE_CONSTANTS['DIFFICULTY_INCREASE']) / SCORE_CONSTANTS['DIFFICULTY_INCREASE']) * 100))

    def add_timer_score(self):
        self.add_score(SCORE_CONSTANTS['TIME_SCORE'])