from game.engine import GameObject, PoolEvent
from game.game_logic.animations import BOMB_ANIMATIONS
from game.game_logic.parameters import BOMB_CONSTANTS, SCORE_CONSTANTS
from PyQt5.QtCore import pyqtSignal
from time import sleep
from random import random


class Bomb(GameObject):

    score_adder = pyqtSignal(int)

    def __init__(self, name: str, x: int, y: int, front_end, back_end, map, score_manager):
        super().__init__(name=name, x=x, y=y, front_end=front_end, back_end=back_end, image=BOMB_ANIMATIONS['bomb_initial_frame'], solid=False)

        self.animator.create_animation('idle', BOMB_ANIMATIONS['bomb_animation'][0], BOMB_ANIMATIONS['bomb_animation'][1], True)

        self.map = map
        self.score_adder.connect(score_manager.add_score)

        self.explosion_timer = 0
        self.kick_direction = ''

    def activate(self):
        # When it isn't solid, the player can't kick it. It is set to solid when the player exits collision with it.
        self.box_collider.solid = False
        self.kick_direction = ''

        self.animator.play_animation('idle')
        self.explosion_timer = BOMB_CONSTANTS['BOMB_TIMER']

    def deactivate(self):
        self.animator.stop_animation()

    def update(self, dt: float, input_handler):
        self.explosion_timer -= dt

        if self.explosion_timer <= 0:
            self.explode()
            self.return_pool_object.emit(PoolEvent(object=self, type='bomb'))

        if self.kick_direction != '':  # AKA it's been kicked.
            speed = BOMB_CONSTANTS['KICK_SPEED'] * dt

            if self.kick_direction == 'above':
                self.transform.position.y -= speed
            elif self.kick_direction == 'below':
                self.transform.position.y += speed
            elif self.kick_direction == 'to left':
                self.transform.position.x -= speed
            elif self.kick_direction == 'to right':
                self.transform.position.x += speed

    def on_collision_enter(self, other):
        # First condition checks whether it collided in the direction in was moving.
        if self.kick_direction == other.direction and\
                ('tile' in other.game_object.name or 'enemy' in other.game_object.name or 'player' in other.game_object.name):
            self.kick_direction = ''

    def explode(self):
        for tile in self.map.get_explosion_tiles(self.transform.position.x, self.transform.position.y):
            x, y = tile.center
            self.add_pool_object.emit(PoolEvent(type='explosion', x=x, y=y))

            if tile.type == 'P':
                self.map.destroy_tile(tile)
                self.score_adder.emit(SCORE_CONSTANTS['WALL_SCORE'])
                if random() <= 0.3:
                    self.add_pool_object.emit(PoolEvent(type='power_up', x=x, y=y))

