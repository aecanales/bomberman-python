from game.engine import GameObject, PoolEvent
from game.game_logic.animations import POWER_UP_ANIMATIONS
from random import choice


class PowerUp(GameObject):

    power_up_types = ['heart', 'bombs', 'speed', 'super speed', 'juggernaut']

    def __init__(self, name: str, x: int, y: int, front_end, back_end):
        super().__init__(name=name, x=x, y=y, front_end=front_end, back_end=back_end, image=POWER_UP_ANIMATIONS['heart'][0][0], solid=False)

        self.power_up_type = ''

        for power_up in self.power_up_types:
            self.animator.create_animation(power_up, *POWER_UP_ANIMATIONS[power_up], True)

    def activate(self):
        self.power_up_type = choice(self.power_up_types)
        self.animator.play_animation(self.power_up_type)
