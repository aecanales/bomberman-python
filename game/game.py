from game.game_logic import Bomb, Player, Map, Explosion, NonHostileEnemy, HostileEnemy, PowerUp, EnemySpawner
from game.game_logic.parameters import PLAYER_ONE_CONTROLS, PLAYER_TWO_CONTROLS


def start_one_player_game(menu, game_engine, game_screen, score_manager):
    game_map = Map(game_screen, game_engine)

    player = Player('player', 115, 55, game_screen, game_engine, game_map, score_manager, menu, PLAYER_ONE_CONTROLS, (10, 50, 10))

    bomb_pool = [Bomb(f'bomb_{i}', -100, -100, game_screen, game_engine, game_map, score_manager) for i in range(10)]
    explosion_pool = [Explosion(f'explosion_{i}', -100, -100, game_screen, game_engine) for i in range(60)]
    non_hostile_enemy_pool = [NonHostileEnemy(f'non_hostile_enemy_{i}', -100, -100, game_screen, game_engine, score_manager) for i in range(20)]
    hostile_enemy_pool = [HostileEnemy(f'hostile_enemy_{i}', -100, -100, game_screen, game_engine, player.transform.position, score_manager) for i in range(20)]
    power_up_pool = [PowerUp(f'power_up_{i}', -100, -100, game_screen, game_engine) for i in range(15)]

    game_engine.add_game_object(player)

    game_engine.add_object_pool('bomb', bomb_pool)
    game_engine.add_object_pool('explosion', explosion_pool)
    game_engine.add_object_pool('non_hostile_enemy', non_hostile_enemy_pool)
    game_engine.add_object_pool('hostile_enemy', hostile_enemy_pool)
    game_engine.add_object_pool('power_up', power_up_pool)

    game_engine.add_game_object(EnemySpawner(game_screen, game_engine, game_map, player))  # Needs to be added after enemy pools exist.


def start_two_player_game(menu, game_engine, game_screen, score_manager):
    game_map = Map(game_screen, game_engine)

    player_one = Player('player', 115, 55, game_screen, game_engine, game_map, score_manager, menu, PLAYER_ONE_CONTROLS, (10, 50, 10))
    player_two = Player('player', 500, 55, game_screen, game_engine, game_map, score_manager, menu, PLAYER_TWO_CONTROLS, (750, -50, 700))

    bomb_pool = [Bomb(f'bomb_{i}', -100, -100, game_screen, game_engine, game_map, score_manager) for i in range(10)]
    explosion_pool = [Explosion(f'explosion_{i}', -100, -100, game_screen, game_engine) for i in range(60)]
    non_hostile_enemy_pool = [NonHostileEnemy(f'non_hostile_enemy_{i}', -100, -100, game_screen, game_engine, score_manager) for i in range(20)]
    hostile_enemy_pool = [HostileEnemy(f'hostile_enemy_{i}', -100, -100, game_screen, game_engine, player_one.transform.position, score_manager) for i in range(20)]
    power_up_pool = [PowerUp(f'power_up_{i}', -100, -100, game_screen, game_engine) for i in range(15)]

    game_engine.add_game_object(player_one)
    game_engine.add_game_object(player_two)

    game_engine.add_object_pool('bomb', bomb_pool)
    game_engine.add_object_pool('explosion', explosion_pool)
    game_engine.add_object_pool('non_hostile_enemy', non_hostile_enemy_pool)
    game_engine.add_object_pool('hostile_enemy', hostile_enemy_pool)
    game_engine.add_object_pool('power_up', power_up_pool)

    game_engine.add_game_object(EnemySpawner(game_screen, game_engine, game_map, player_one))  # Needs to be added after enemy pools exist.