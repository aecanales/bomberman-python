from PyQt5.QtCore import QThread, pyqtSignal


class CollisionEvent:

    def __init__(self, game_object, direction):
        self.game_object = game_object
        self.direction = direction


class BoxCollider(QThread):
    """Detects collisions in a rectangular area."""

    collision_enter = pyqtSignal(CollisionEvent)
    collision_stay = pyqtSignal(CollisionEvent)
    collision_exit = pyqtSignal(CollisionEvent)

    def __init__(self, parent, width: int, height: int, solid: bool, unmovable: bool):
        super().__init__()

        self.parent = parent
        self.width = width
        self.height = height
        self.solid = solid
        self.unmovable = unmovable

        self.previous_x, self.previous_y = self.parent.transform.position.x, self.parent.transform.position.y

        self.collision_enter.connect(parent.on_collision_enter)
        self.collision_stay.connect(parent.on_collision_stay)
        self.collision_exit.connect(parent.on_collision_exit)

    @property
    def left(self):
        return self.parent.transform.position.x

    @property
    def right(self):
        return self.parent.transform.position.x + self.width * self.parent.transform.scale.x

    @property
    def top(self):
        return self.parent.transform.position.y

    @property
    def bottom(self):
        return self.parent.transform.position.y + self.height * self.parent.transform.scale.y

    @property
    def center(self):
        return self.parent.transform.position.x + (self.width * self.parent.transform.scale.x) / 2,\
               self.parent.transform.position.y + (self.height * self.parent.transform.scale.y) / 2

    def collision_event(self, other):
        return CollisionEvent(self.parent, other.collision_direction(self))

    @property
    def has_moved(self):
        """Returns True if the collider has moved since the last time has_moved was called."""
        has_moved = (self.parent.transform.position.x != self.previous_x or self.parent.transform.position.y != self.previous_y)
        self.previous_x, self.previous_y = self.parent.transform.position.x, self.parent.transform.position.y
        return has_moved

    def is_colliding_with(self, other) -> bool:
        """
        Returns True if this box collider is colliding with the box collider `other`.
        Thanks to Claudio de Sa for the nudge in the right direction:
        http://devmag.org.za/2009/04/13/basic-collision-detection-in-2d-part-1/
        """
        return not (
                (self.bottom < other.top) or
                (self.top > other.bottom) or
                (self.left > other.right) or
                (self.right < other.left)
        )

    def bump_into(self, other):
        """
        Handles interaction between solid box colliders. This box collider is the one that shall move.
        Thanks to Photonic: https://stackoverflow.com/a/13349505
        :param other: The solid box collider this box collider is colliding with.
        """
        direction = self.collision_direction(other)

        if direction == 'above':
            self.move_side_to('top', other.bottom)
        elif direction == 'below':
            self.move_side_to('bottom', other.top)
        elif direction == 'to right':
            self.move_side_to('right', other.left)
        elif direction == 'to left':
            self.move_side_to('left', other.right)

    def collision_direction(self, other):
        """
        Returns where the box collider 'other' is in regard to this box collider.
        For example, if this box collider top collided with 'other''s bottom, it returns 'above'.
        """
        # The smallest difference represents the actual collision.
        bottom_collision = other.bottom - self.top
        top_collision = self.bottom - other.top
        left_collision = self.right - other.left
        right_collision = other.right - self.left

        if bottom_collision < top_collision and bottom_collision < left_collision and bottom_collision < right_collision:
            return 'above' # Collided into `other`'s bottom.
        if top_collision < bottom_collision and top_collision < left_collision and top_collision < right_collision:
            return 'below' # Collided into `other`'s top.
        if left_collision < bottom_collision and left_collision < top_collision and left_collision < right_collision:
            return 'to right' # Collided into `other`'s left.
        if right_collision < bottom_collision and right_collision < top_collision and right_collision < left_collision:
            return 'to left' # Collided into `other`'s right.

    def move_side_to(self, side: str, position: float):
        """Moves this object's `side` to `position` (x or y depends on which side it is)."""
        if side == 'bottom':
            self.parent.transform.position.y -= self.bottom - position
        elif side == 'top':
            self.parent.transform.position.y += position - self.top
        elif side == 'left':
            self.parent.transform.position.x += position - self.left
        elif side == 'right':
            self.parent.transform.position.x -= self.right - position
