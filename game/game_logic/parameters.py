from PyQt5.QtCore import Qt

MAP_CONSTANTS = {
    'TILE_SIZE': 40,  # In pixels.
    'XY_ORIGIN': (90, 0),  # From where the map starts.
    'MAP_FILE_PATH': 'game/assets/mapa.txt'
}

MAP_ASSETS = {
    'INDESTRUCTIBLE_TILE': 'game/assets/sprites/map/indestructible_wall.png',
    'DESTRUCTIBLE_TILE': 'game/assets/sprites/map/destructible_wall.png',
    'EMPTY_TILE': 'game/assets/sprites/map/empty_tile.png'
}

PLAYER_ONE_CONTROLS = {
    'up': Qt.Key_Up,
    'left': Qt.Key_Left,
    'down': Qt.Key_Down,
    'right': Qt.Key_Right,
    'bomb': Qt.Key_Space
}

PLAYER_TWO_CONTROLS = {
    'up': Qt.Key_W,
    'left': Qt.Key_A,
    'down': Qt.Key_S,
    'right': Qt.Key_D,
    'bomb': Qt.Key_F
}

CHARACTER_CONSTANTS = {
    'MOVEMENT_VELOCITY': 150,  # In pixels per second.
    'INITIAL_HEALTH': 3,
    'INVULNERABILITY_TIME': 3,  # In seconds.
    'SUPER_SPEED_TIME': 10,  # In seconds.
    'JUGGERNAUT_TIME': 5  # In seconds.
}

ENEMY_CONSTANTS = {
    'CHANGE_DIRECTION_TIME': 2,  # In seconds.
    'MIN_SPAWN_DISTANCE': 200,  # In pixels.
    'A_NON_HOSTILE': 5,  # In seconds.
    'B_NON_HOSTILE': 10,  # In seconds.
    'MIN_DETECTION_DISTANCE': 150, # In pixels.
    'HOSTILE_SPEED_MODIFIER': 0.8,  # [0, 1]. Since having the same speed as the player makes it too fast...
    'HOSTILE_LAMDA': 1/20
}

BOMB_CONSTANTS = {
    'BOMB_TIMER': 2,  # In seconds.
    'KICK_SPEED': 200  # In pixels per second.
}

SCORE_CONSTANTS = {
    'ENEMY_SCORE': 5,
    'WALL_SCORE': 1,
    'TIME_SCORE': 10,
    'TIME_FOR_SCORE': 30,  # In seconds.
    'DIFFICULTY_INCREASE': 30
}
