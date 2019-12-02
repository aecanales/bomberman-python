from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QWidget


class Sprite:
    """Visual representation of a game object in the front end."""

    def __init__(self, front_end: QWidget, image_location: str):
        self.label = QLabel('', front_end)
        self._pixmap = QPixmap(image_location)

        self._has_changed = False

    @property
    def pixmap(self):
        return self._pixmap

    @pixmap.setter
    def pixmap(self, value):
        self._pixmap = value
        self._has_changed = True

    @property
    def has_changed(self):
        has_changed = self._has_changed
        self._has_changed = False

        return has_changed


class RenderEvent:
    """Event to be signaled to the front end whenever the Sprite's QLabel must be re-rendered."""

    def __init__(self, sprite: Sprite, transform):
        self.sprite = sprite
        self.transform = transform