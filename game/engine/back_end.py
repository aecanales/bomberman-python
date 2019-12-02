from game.engine.collision_manager import CollisionManager
from game.engine.game_object import GameObject
from game.engine.input_manager import InputManager
from PyQt5.QtCore import QThread
from time import sleep

FRAMES_PER_SECOND = 30


class Engine(QThread):

    def __init__(self):
        super().__init__()

        self.paused = False
        self.stop = False

        self.game_objects = []
        self.object_pool = {}  # In form object_name: list of objects.

        self.input_manager = InputManager()
        self.collision_manager = CollisionManager()

    def add_game_object(self, game_object: GameObject):
        self.game_objects.append(game_object)

    def add_object_pool(self, object_name: str, game_objects: list):
        for game_object in game_objects:
            game_object._deactivate(True)

        self.object_pool[object_name] = game_objects

    def activate_object_from_pool(self, activate_event):
        for object in self.object_pool[activate_event.type]:
            if not object.active:
                self.game_objects.append(object)
                object._activate(activate_event.x, activate_event.y)
                return

    def deactivate_object_from_pool(self, deactivate_event):
        deactivate_event.object._deactivate()
        deactivate_event.object.render()  # Need to show it was moved off-screen!
        self.game_objects.remove(deactivate_event.object)
        self.object_pool[deactivate_event.type].append(deactivate_event.object)

    def remove_game_object(self, remove_event):
        remove_event.object._deactivate()
        remove_event.object.render()  # Need to show it was moved off-screen!
        self.game_objects.remove(remove_event.object)

    def toggle_pause(self):
        """If un-paused, pauses. If paused, un-pauses."""
        self.paused = not self.paused

    def run(self):
        """
        Runs the main game loop:
        1.- Waits a certain amount of milliseconds corresponding to the the frame rate.
        2.- Updates every game object.
        3.- Checks for collisions and re-positions solid objects.
        4.- Re-renders every game object whose state has changed (each game object internally checks if it has changed).
        5.- Updates input manager.
        """
        while True:
            #  Ignores pause because key events are still sent when it's paused.
            self.input_manager.update_keys()

            if self.paused: continue
            if self.stop: break

            wait = 1 / FRAMES_PER_SECOND
            sleep(wait)

            for game_object in list(self.game_objects):
                game_object.update(wait, self.input_manager)

            self.collision_manager.run_collision_test(self.game_objects)
            self.collision_manager.bump_solid_object()

            for game_object in self.game_objects:
                game_object.render()
