from game.engine import GameObject, PoolEvent
from game.game_logic.animations import BOMB_ANIMATIONS
from time import sleep


class Explosion(GameObject):

    def __init__(self, name: str, x: int, y: int, front_end, back_end):
        super().__init__(name=name, x=x, y=y, front_end=front_end, back_end=back_end,
                         image=BOMB_ANIMATIONS['explosion'][0][0], solid=False, unmovable=True)

        self.animator.create_animation('idle', BOMB_ANIMATIONS['explosion'][0], BOMB_ANIMATIONS['explosion'][1], False)

    def activate(self):
        self.animator.play_animation('idle')
        self.start()

    def deactivate(self):
        self.animator.stop_animation()

    def run(self):
        sleep(self.animator.get_animation_length('idle') * 3)
        self.return_pool_object.emit(PoolEvent(object=self, type='explosion'))

