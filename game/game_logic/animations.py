player_walk_animation_frame_length = [0, 0]
player_walk_animation_frame_length.extend(0.1 for i in range(6))

PLAYER_ANIMATIONS = {
    'initial_frame': 'game/assets/sprites/bomberman/walk_down_0',
    'walk_up': ([f'game/assets/sprites/bomberman/walk_up_{i}' for i in range(8)], player_walk_animation_frame_length),
    'walk_left': ([f'game/assets/sprites/bomberman/walk_left_{i}' for i in range(8)], player_walk_animation_frame_length),
    'walk_down': ([f'game/assets/sprites/bomberman/walk_down_{i}' for i in range(8)], player_walk_animation_frame_length),
    'walk_right': ([f'game/assets/sprites/bomberman/walk_right_{i}' for i in range(8)], player_walk_animation_frame_length)
}

BOMB_ANIMATIONS = {
    'bomb_initial_frame': 'game/assets/sprites/bomberman/bomb_0',
    'bomb_animation': ([f'game/assets/sprites/bomberman/bomb_{i}' for i in range(2)], [0.1, 0.1]),
    'explosion': ([f'game/assets/sprites/bomberman/explosion_{i}' for i in range(5)], [0.1 for i in range(5)])
}

HEALTH_ANIMATIONS = {
    'full_health': 'game/assets/sprites/bomberman/heart'
}

NON_HOSTILE_ENEMY_ANIMATIONS = {
    'idle': 'game/assets/sprites/enemies/non_hostile/idle'
}

HOSTILE_ENEMY_ANIMATIONS = {
    'idle': 'game/assets/sprites/enemies/hostile/idle'
}

power_up_types = ['heart', 'bomb', 'speed', 'super speed', 'juggernaut']

POWER_UP_ANIMATIONS = {
    'heart': (['game/assets/sprites/power_up/heart'], [0.1]),
    'bombs': (['game/assets/sprites/power_up/bombs'], [0.1]),
    'speed': (['game/assets/sprites/power_up/speed'], [0.1]),
    'super speed': (['game/assets/sprites/power_up/super_speed'], [0.1]),
    'juggernaut': (['game/assets/sprites/power_up/juggernaut'], [0.1]),
}

EMPTY_SPRITE = 'game/assets/sprites/empty'
