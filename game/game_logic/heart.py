from game.engine import GameObject
from game.game_logic.animations import HEALTH_ANIMATIONS


class Heart(GameObject):

    def __init__(self,  name: str, x: int, y: int, front_end, back_end):
        super().__init__(name=name, x=x, y=y, front_end=front_end, back_end=back_end,
                         image=HEALTH_ANIMATIONS['full_health'], solid=False)

        self.box_collider = None
