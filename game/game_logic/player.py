from game.engine import GameObject, PoolEvent
from game.game_logic.animations import PLAYER_ANIMATIONS
from game.game_logic.parameters import CHARACTER_CONSTANTS, BOMB_CONSTANTS
from game.game_logic.heart import Heart
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal


class DeathEvent:

    def __init__(self, player, score):
        self.player = player
        self.score = score


class Player(GameObject):

    death_event = pyqtSignal(DeathEvent)

    def __init__(self, name: str, x: int, y: int, front_end, back_end, map, score_manager, window, keys, heart_pos):
        super().__init__(name=name, x=x, y=y, front_end=front_end, back_end=back_end, image=PLAYER_ANIMATIONS['initial_frame'], solid=True)

        self.animator.create_animation('walk_up', PLAYER_ANIMATIONS['walk_up'][0], PLAYER_ANIMATIONS['walk_up'][1], True)
        self.animator.create_animation('walk_left', PLAYER_ANIMATIONS['walk_left'][0], PLAYER_ANIMATIONS['walk_left'][1], True)
        self.animator.create_animation('walk_right', PLAYER_ANIMATIONS['walk_right'][0], PLAYER_ANIMATIONS['walk_right'][1], True)
        self.animator.create_animation('walk_down', PLAYER_ANIMATIONS['walk_down'][0], PLAYER_ANIMATIONS['walk_down'][1], True)

        self.keys = keys

        self.map = map

        self.speed = CHARACTER_CONSTANTS['MOVEMENT_VELOCITY']

        self.bombs = 1
        self.bomb_timers = []
        self.bomb_text = QLabel(f'Bombas: {self.bombs}', front_end)
        self.bomb_text.move(heart_pos[2], 150)

        self.power_ups = QLabel('', front_end)
        self.power_ups.move(heart_pos[2], 180)

        self.super_speed_timer = 0
        self.juggernaut_timer = 0

        self.invulnerability_timer = 0

        self.score_manager = score_manager
        self.death_event.connect(window.player_death)

        self.hearts = []
        for i in range(CHARACTER_CONSTANTS['INITIAL_HEALTH']):
            heart = Heart(f'heart_{i}', heart_pos[0] + heart_pos[1] * i, 10, front_end, back_end)
            back_end.add_game_object(heart)
            self.hearts.append(heart)

    def update(self, dt: float, input_handler):
        self.handle_movement(dt, input_handler)
        self.handle_bomb_creation(input_handler)
        self.handle_bomb_timer(dt)

        if self.invulnerability_timer > 0:
            self.invulnerability_timer -= dt
            self.sprite.label.setVisible(not self.sprite.label.isVisible())
        elif self.invulnerability_timer <= 0 and not self.sprite.label.isVisible():
            self.sprite.label.setVisible(True)

        if self.super_speed_timer > 0:
            self.super_speed_timer -= dt
        elif 'supervelocidad' in self.power_ups.text():
            self.remove_power_up_text('supervelocidad')

        if self.juggernaut_timer > 0:
            self.juggernaut_timer -= dt
        elif 'juggernaut' in self.power_ups.text():
            self.remove_power_up_text('juggernaut')

    def on_collision_enter(self, other):
        if ('explosion' in other.game_object.name or 'enemy' in other.game_object.name)\
                and self.invulnerability_timer <= 0 and self.juggernaut_timer <= 0:
            self.invulnerability_timer = CHARACTER_CONSTANTS['INVULNERABILITY_TIME']
            self.reduce_health()

        if 'bomb' in other.game_object.name and other.game_object.box_collider.solid and other.game_object.kick_direction == '':
            other.game_object.kick_direction = other.direction

        if 'power_up' in other.game_object.name:
            self.activate_power_up(other.game_object.power_up_type)
            self.return_pool_object.emit(PoolEvent(object=other.game_object, type='power_up'))

    def on_collision_exit(self, other):
        if 'bomb' in other.game_object.name:
            # When solid is set to True, the player will be able to kick it.
            other.game_object.box_collider.solid = True

    def handle_movement(self, dt: float, input_handler):
        speed = self.speed * dt

        if self.super_speed_timer > 0:
            speed *= 3

        if input_handler.is_key_held(self.keys['up']):
            self.animator.play_animation('walk_up')
            self.transform.position.y -= speed
        elif input_handler.is_key_held(self.keys['left']):
            self.animator.play_animation('walk_left')
            self.transform.position.x -= speed
        elif input_handler.is_key_held(self.keys['right']):
            self.animator.play_animation('walk_right')
            self.transform.position.x += speed
        elif input_handler.is_key_held(self.keys['down']):
            self.animator.play_animation('walk_down')
            self.transform.position.y += speed

        if input_handler.is_key_released(self.keys['up']) and self.animator.current_animation_name == 'walk_up' or \
           input_handler.is_key_released(self.keys['left']) and self.animator.current_animation_name == 'walk_left' or \
           input_handler.is_key_released(self.keys['right']) and self.animator.current_animation_name == 'walk_right' or \
           input_handler.is_key_released(self.keys['down']) and self.animator.current_animation_name == 'walk_down':
            self.animator.stop_animation()
            self.animator.set_frame(0)

    def handle_bomb_creation(self, input_handler):
        if input_handler.is_key_pressed(self.keys['bomb']) and self.bombs > 0:
            x, y = self.map.get_tile_center(*self.box_collider.center)
            self.add_pool_object.emit(PoolEvent(type='bomb', x=x, y=y))
            self.bombs -= 1
            self.bomb_text.setText(f'Bombas: {self.bombs}')
            self.bomb_timers.append(BOMB_CONSTANTS['BOMB_TIMER'])

    def handle_bomb_timer(self, dt):
        if len(self.bomb_timers) == 0: return

        for i in range(len(self.bomb_timers)):
            self.bomb_timers[i] -= dt

        for timer in list(self.bomb_timers):
            if timer <= 0:
                self.bomb_timers.remove(timer)
                self.bombs += 1
                self.bomb_text.setText(f'Bombas: {self.bombs}')

    def reduce_health(self):
        for heart in reversed(self.hearts):
            if heart.sprite.label.isVisible():
                heart.sprite.label.setVisible(False)
                if heart == self.hearts[0]:
                    self.death_event.emit(DeathEvent(0, self.score_manager.score))
                    self.remove_object.emit(PoolEvent(object=self))
                return

    def add_health(self):
        for heart in self.hearts:
            if not heart.sprite.label.isVisible():
                heart.sprite.label.setVisible(True)
                return

    def activate_power_up(self, type: str):
        if type == 'heart':
            self.add_health()
        elif type == 'bombs':
            self.bombs += 1
            self.bomb_text.setText(f'Bombas: {self.bombs}')
        elif type == 'speed':
            self.speed *= 1.25
            self.add_power_up_text('velocidad')
        elif type == 'super speed':
            self.super_speed_timer = CHARACTER_CONSTANTS['SUPER_SPEED_TIME']
            if 'supervelocidad' not in self.power_ups.text():
                self.add_power_up_text('supervelocidad')
        elif type == 'juggernaut':
            self.juggernaut_timer = CHARACTER_CONSTANTS['JUGGERNAUT_TIME']
            if 'juggernaut' not in self.power_ups.text():
                self.add_power_up_text('juggernaut')

    def add_power_up_text(self, text):
        self.power_ups.setText(self.power_ups.text() + f'\n{text}')
        self.power_ups.resize(self.power_ups.sizeHint())

    def remove_power_up_text(self, text):
        self.power_ups.setText(self.power_ups.text().replace(f'\n{text}', ''))
        self.power_ups.resize(self.power_ups.sizeHint())

