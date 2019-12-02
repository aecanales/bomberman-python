from game.engine import GameObject, PoolEvent, euclidean_distance
from game.game_logic.animations import EMPTY_SPRITE
from game.game_logic.parameters import ENEMY_CONSTANTS
from random import choice, uniform, expovariate


class EnemySpawner(GameObject):

    def __init__(self, front_end, back_end, map, player):
        super().__init__(name='EnemySpawner', x=0, y=0, front_end=front_end, back_end=back_end, image=EMPTY_SPRITE, solid=False)

        self.box_collider = None

        self.empty_tiles = map.empty_tiles
        self.player_position = player.transform.position

        self.spawn('non_hostile_enemy')
        self.spawn('non_hostile_enemy')
        self.spawn('hostile_enemy')

        self.non_hostile_timer = uniform(ENEMY_CONSTANTS['A_NON_HOSTILE'], ENEMY_CONSTANTS['B_NON_HOSTILE'])
        self.hostile_timer = expovariate(ENEMY_CONSTANTS['HOSTILE_LAMDA'])
        print(f'EnemySpawner: Spawning a non-hostile in {self.non_hostile_timer}')
        print(f'EnemySpawner: Spawning a hostile in... {self.hostile_timer}')

    def update(self, dt: float, input_handler):
        self.non_hostile_timer -= dt
        self.hostile_timer -= dt

        if self.non_hostile_timer <= 0:
            self.spawn('non_hostile_enemy')
            self.non_hostile_timer = uniform(ENEMY_CONSTANTS['A_NON_HOSTILE'], ENEMY_CONSTANTS['B_NON_HOSTILE'])
            print(f'EnemySpawner: Spawning a non-hostile in {self.non_hostile_timer}')

        if self.hostile_timer <= 0:
            self.spawn('hostile_enemy')
            self.hostile_timer = expovariate(ENEMY_CONSTANTS['HOSTILE_LAMDA'])
            print(f'EnemySpawner: Spawning a hostile in... {self.hostile_timer}')

    def get_empty_tile_at_distance(self):
        tiles_at_distance = [tile for tile in self.empty_tiles
                             if euclidean_distance(tile.transform.position, self.player_position) > ENEMY_CONSTANTS['MIN_SPAWN_DISTANCE']]
        return choice(tiles_at_distance)

    def spawn(self, enemy_type: str):
        x, y = self.get_empty_tile_at_distance().center
        self.add_pool_object.emit(PoolEvent(type=enemy_type, x=x, y=y))
