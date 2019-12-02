from game.engine import GameObject, PoolEvent, euclidean_distance
from game.game_logic.animations import HOSTILE_ENEMY_ANIMATIONS
from game.game_logic.parameters import CHARACTER_CONSTANTS, ENEMY_CONSTANTS, SCORE_CONSTANTS
from PyQt5.QtCore import pyqtSignal
from random import choice


class HostileEnemy(GameObject):

    directions = ['up', 'left', 'right', 'down']
    score_adder = pyqtSignal(int)

    def __init__(self, name: str, x: int, y: int, front_end, back_end, player_position, score_manager):
        super().__init__(name=name, x=x, y=y, front_end=front_end, back_end=back_end,
                         image=HOSTILE_ENEMY_ANIMATIONS['idle'], solid=True)

        self.is_alive = True
        self.has_spotted_player = False
        self.player_position = player_position

        self.score_adder.connect(score_manager.add_score)

        self.direction = ''
        self.timer = 0
        self.set_direction()

    def activate(self):
        self.is_alive = True
        self.has_spotted_player = False

    def update(self, dt: float, input_handler):
        if not self.has_spotted_player:
            self.random_movement(dt)
            if self.distance_to_player() < ENEMY_CONSTANTS['MIN_DETECTION_DISTANCE']:
                self.has_spotted_player = True
        else:
            self.follow_player(dt)

    def distance_to_player(self):
        return euclidean_distance(self.transform.position, self.player_position)

    def random_movement(self, dt):
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

    def follow_player(self, dt):
        speed = ENEMY_CONSTANTS['HOSTILE_SPEED_MODIFIER'] * CHARACTER_CONSTANTS['MOVEMENT_VELOCITY'] * dt

        if self.transform.position.x < self.player_position.x - 10:
            self.transform.position.x += speed
        elif self.transform.position.x >= self.player_position.x + 10:
            self.transform.position.x -= speed

        if self.transform.position.y < self.player_position.y - 10:
            self.transform.position.y += speed
        elif self.transform.position.y >= self.player_position.y + 10:
            self.transform.position.y -= speed

    def on_collision_enter(self, other):
        if 'explosion' in other.game_object.name and self.is_alive:
            self.score_adder.emit(SCORE_CONSTANTS['ENEMY_SCORE'])
            self.return_pool_object.emit(PoolEvent(object=self, type='hostile_enemy'))
            self.is_alive = False
