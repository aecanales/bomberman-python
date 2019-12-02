from game.engine import GameObject, PoolEvent
from game.game_logic.animations import NON_HOSTILE_ENEMY_ANIMATIONS
from game.game_logic.parameters import CHARACTER_CONSTANTS, ENEMY_CONSTANTS, SCORE_CONSTANTS
from PyQt5.QtCore import pyqtSignal
from random import choice


class NonHostileEnemy(GameObject):

    directions = ['up', 'left', 'right', 'down']
    score_adder = pyqtSignal(int)

    def __init__(self, name: str, x: int, y: int, front_end, back_end, score_manager):
        super().__init__(name=name, x=x, y=y, front_end=front_end, back_end=back_end,
                         image=NON_HOSTILE_ENEMY_ANIMATIONS['idle'], solid=True)

        self.score_adder.connect(score_manager.add_score)

        self.direction = ''
        self.timer = 0
        self.set_direction()

        self.is_alive = True

    def activate(self):
        self.is_alive = True

    def update(self, dt: float, input_handler):
        speed = CHARACTER_CONSTANTS['MOVEMENT_VELOCITY'] * dt

        if self.direction == 'up':
            self.transform.position.y -= speed
        elif self.direction == 'left':
            self.transform.position.x -= speed
        elif self.direction == 'down':
            self.transform.position.y += speed
        elif self.direction == 'right':
            self.transform.position.x += speed

        self.timer -= dt
        if self.timer <= 0:
            self.set_direction()

    def set_direction(self):
        self.direction = choice(self.directions)
        self.timer = ENEMY_CONSTANTS['CHANGE_DIRECTION_TIME']

    def on_collision_enter(self, other):
        if 'explosion' in other.game_object.name and self.is_alive:
            self.score_adder.emit(SCORE_CONSTANTS['ENEMY_SCORE'])
            self.return_pool_object.emit(PoolEvent(object=self, type='non_hostile_enemy'))
            self.is_alive = False

