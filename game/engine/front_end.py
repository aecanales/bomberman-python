from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget
from game.engine.back_end import Engine


class Screen(QWidget):

    key_press = pyqtSignal(QKeyEvent)
    key_release = pyqtSignal(QKeyEvent)

    def __init__(self, back_end: Engine, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Key signals are connected to the corresponding slots in the back end's input manager.
        self.key_press.connect(back_end.input_manager.receive_key_press)
        self.key_release.connect(back_end.input_manager.receive_key_release)

        self.initialize()

    def initialize(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Code with Fire')

    @staticmethod
    def render_sprite(render_event):
        """Updates the label not only considering its new position but also any modification to size."""
        label, pixmap = render_event.sprite.label, render_event.sprite.pixmap
        x, y = render_event.transform.position.x, render_event.transform.position.y
        scale_x, scale_y = render_event.transform.scale.x, render_event.transform.scale.y
        width, height = pixmap.width(), pixmap.height()

        label.setGeometry(x, y, width * scale_x, height * scale_y)
        label.setPixmap(pixmap.scaled(width * scale_x, height * scale_y))

    # isAutoRepeat() prevents these events being called every frame due to a held key.
    def keyPressEvent(self, event):
        if event.isAutoRepeat():
            return
        self.key_press.emit(event)

    def keyReleaseEvent(self, event):
        if event.isAutoRepeat():
            return
        self.key_release.emit(event)