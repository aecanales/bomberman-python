class InputManager:
    """
    Receives key press/release events from the front end.
    Is used by game objects to check user input.
    """

    def __init__(self):
        # Keys are stored as key codes (ints).
        self._pressed_keys = []
        self._held_keys = []
        self._released_keys = []

    def receive_key_press(self, event):
        """Slot for a signal from 'keyPressEvent'."""
        self._pressed_keys.append(event.key())

    def receive_key_release(self, event):
        """Slot for a signal from 'keyReleaseEvent'."""
        self._held_keys.remove(event.key())
        self._released_keys.append(event.key())

    def update_keys(self):
        """Called at the end of every frame."""
        self._held_keys.extend(key for key in self._pressed_keys)
        self._pressed_keys = []
        self._released_keys = []

    def is_key_pressed(self, key: int) -> bool:
        """Returns true for the frame the key was pressed."""
        return key in self._pressed_keys

    def is_key_held(self, key: int) -> bool:
        """Returns true every frame the key is held down."""
        return key in self._held_keys

    def is_key_released(self, key:int) -> bool:
        """Returns true the frame the key is released."""
        return key in self._released_keys