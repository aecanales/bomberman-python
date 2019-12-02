class Transform:
    """Contains the position and scale of its parent game object."""

    def __init__(self, x: int, y: int):
        self.position = Vector2(x, y)
        self.scale = Vector2(1, 1)

    @property
    def has_changed(self) -> bool:
        """Returns True if the position or scale have been changed."""
        has_changed = self.position.has_changed or self.scale.has_changed

        self.position.has_changed = False
        self.scale.has_changed = False

        return has_changed


class Vector2:
    """Represents an (x, y) vector. """

    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

        self.has_changed = False  # Set to true whenever x or y are changed.

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x
        self.has_changed = True

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y
        self.has_changed = True