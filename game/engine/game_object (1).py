from game.engine.components import Animator, BoxCollider, Transform, RenderEvent, Sprite
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget


class PoolEvent:
    """Used when getting/returning a game object from the engine's pool."""

    def __init__(self, object=None, type='', x=0, y=0):
        self.object = object
        self.type = type
        self.x = x
        self.y = y


class GameObject(QThread):
    """Base class for any object in the game."""

    renderer = pyqtSignal(RenderEvent)  # Signal to front end to update this game object's QLabel.
    add_pool_object = pyqtSignal(PoolEvent)  # Signal to add an object from the pool to the game.
    return_pool_object = pyqtSignal(PoolEvent)  # Signal to return object from the game to the pool.
    remove_object = pyqtSignal(PoolEvent)  # Signal to remove an object from the game for good.

    def __init__(self, name: str, x: int, y: int, front_end: QWidget, back_end, image: str, solid: bool, unmovable=False):
        super().__init__()

        self.active = True

        self.name = name
        self.transform = Transform(x, y)
        self.sprite = Sprite(front_end, image)
        self.animator = Animator(self.sprite)
        self.box_collider = BoxCollider(self, self.sprite.pixmap.width(), self.sprite.pixmap.height(), solid, unmovable)
        self._inactive_box_collider = self.box_collider  # Used for saving the box collider while the object is deactived (in pool).

        self.renderer.connect(front_end.render_sprite)
        self.renderer.emit(self.render_event)  # Needs to be rendered once or else it'll be invisible.

        self.add_pool_object.connect(back_end.activate_object_from_pool)
        self.return_pool_object.connect(back_end.deactivate_object_from_pool)
        self.remove_object.connect(back_end.remove_game_object)

    @property
    def render_event(self):
        """Returns an event for the renderer signal."""
        return RenderEvent(self.sprite, self.transform)

    def render(self):
        """Emits signal to front end if the game object has changed its position or sprite."""
        if self.transform.has_changed or self.sprite.has_changed:
            self.renderer.emit(self.render_event)

    def _activate(self, x, y):
        """Called on adding an object from a pool to a game. Base activation for any game object."""
        self.active = True
        self.box_collider = self._inactive_box_collider

        self.transform.position.x = x - self.box_collider.width / 2
        self.transform.position.y = y - self.box_collider.height / 2

        self.activate()

    def activate(self):
        """Specific activation behavior for this game object. Must be overriden."""
        pass

    def _deactivate(self, initialize=False):
        """
        Called when returning object from game to pool. Base deactivation for any game object.
        Is called when game object is added to pool (initialize=True).
        """
        self.active = False
        self.box_collider = None

        self.transform.position.x = -100
        self.transform.position.y = -100

        if not initialize:
            self.deactivate()

    def deactivate(self):
        """Specific deactivation behaviour for this game object. Must be overridden."""
        pass

    def update(self, dt: float, input_handler):
        """Called each frame. Must be overridden in a child class to add behavior to the game object."""
        pass

    def on_collision_enter(self, other):
        """Called on the frame this game object collides with `other`."""
        pass

    def on_collision_stay(self, other):
        """Called every frame where this game object stays in collision with `other`."""
        pass

    def on_collision_exit(self, other):
        """Called on the frame where this game object leaves collision with `other`."""
        pass
