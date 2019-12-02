from functools import reduce
from time import sleep
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from typing import Callable, List


class AnimationEvent:

    def __init__(self, new_frame: QPixmap):
        self.new_frame = new_frame


class Animator:
    """Animates game objects."""

    def __init__(self, sprite):
        super().__init__()

        self.sprite = sprite

        self.animations = {}  # In the form 'animation_name': Animation.
        self.current_animation = None
        self.current_animation_name = ''

    def create_animation(self, animation_name: str, frame_paths: List[str], frame_length : List[float], loops: bool):
        self.animations[animation_name] = Animation(frame_paths, frame_length, loops, self.change_frame)

    def play_animation(self, animation_name: str):
        for animation in self.animations.keys():
            self.animations[animation].stop()

        self.current_animation_name = animation_name
        self.current_animation = self.animations[animation_name]
        self.current_animation.start()

    def stop_animation(self):
        self.current_animation.stop()

    def set_frame(self, frame_number: int):
        self.current_animation.set_frame(frame_number)

    def change_frame(self, event: AnimationEvent):
        self.sprite.pixmap = event.new_frame

    def get_animation_length(self, animation_name: str):
        return self.animations[animation_name].animation_length


class Animation(QThread):

    change_frame = pyqtSignal(AnimationEvent)

    def __init__(self, frame_paths: List[str], frame_length : List[float], loops: bool, frame_changer: Callable):
        super().__init__()

        self.current_frame = 0
        self.frames = [QPixmap(path) for path in frame_paths]
        self.frame_length = frame_length

        self.loops = loops
        self.is_playing = False
        self.timer = 0

        self.change_frame.connect(frame_changer)

    @property
    def frame_change_event(self):
        return AnimationEvent(self.frames[self.current_frame])

    @property
    def animation_length(self):
        return reduce(lambda x, y: x + y, self.frame_length)

    def run(self):
        self.is_playing = True
        self.timer = 0

        while self.is_playing and self.current_frame < len(self.frames):
            sleep(self.frame_length[self.current_frame])
            self.change_frame.emit(self.frame_change_event)
            self.current_frame += 1

        # If the animation actually completed...
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
            if self.loops and self.is_playing:
                self.run()

    def set_frame(self, frame_number: int):
        self.current_frame = frame_number
        self.change_frame.emit(self.frame_change_event)

    def stop(self):
        self.is_playing = False

