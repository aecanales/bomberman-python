from game.engine import GameObject
from game.game_logic.parameters import MAP_CONSTANTS, MAP_ASSETS


class Map:
    """Collection of tiles that represent the game map."""

    def __init__(self, front_end, back_end):
        self.tiles = []  # List of lists of Tiles. Each list represents a row.
        self.replacement_empty_tiles = []  # List of empty tiles to replace breakable tiles.

        self.initialize_map(front_end, back_end)

    def initialize_map(self, front_end, back_end):
        with open(MAP_CONSTANTS['MAP_FILE_PATH'], 'r') as file:
            x, y = MAP_CONSTANTS['XY_ORIGIN']
            i, j = 0, 0
            tile_size = MAP_CONSTANTS['TILE_SIZE']

            for row in file.readlines():
                tile_row = []

                for tile_type in row.replace(' ', '').rstrip('\n'):
                    tile = Tile(f'tile_({i},{j})', x, y, front_end, back_end, tile_type)
                    back_end.add_game_object(tile)
                    tile_row.append(tile)

                    if tile_type == '0':
                        replacement_tile = Tile(f'tile_({i},{j})', -100, -100, front_end, back_end, '0')
                        back_end.add_game_object(replacement_tile)
                        self.replacement_empty_tiles.append(replacement_tile)

                    x += tile_size
                    i += 1

                self.tiles.append(tile_row)

                y += tile_size
                j += 1

                x = MAP_CONSTANTS['XY_ORIGIN'][0]
                i = 0

    def get_tile(self, x, y):
        """Returns the Tile object at x, y."""
        x_origin, y_origin = MAP_CONSTANTS['XY_ORIGIN']

        column = int((x - x_origin) // MAP_CONSTANTS['TILE_SIZE'])
        row = int((y - y_origin) // MAP_CONSTANTS['TILE_SIZE'])

        return self.tiles[row][column]

    def get_tile_center(self, x, y):
        """Takes a position and returns the x, y center of the tile that position is on."""
        return self.get_tile(x, y).center

    def get_explosion_tiles(self, x, y):
        x, y = self.get_tile_center(x, y)

        tiles = list()
        tiles.append(self.get_tile(x, y))

        for direction in ('up', 'left', 'down', 'right'):
            tiles.extend(self.get_explosion_tiles_in_direction(x, y, direction))

        return tiles

    def get_explosion_tiles_in_direction(self, x, y, direction, tiles=None):
        if tiles is None:
            tiles = list()

        x, y = self.apply_direction(x, y, direction)
        tile = self.get_tile(x, y)

        if tile.type == 'X':
            return tiles
        elif tile.type == 'P':
            tiles.append(tile)
            return tiles
        elif tile.type == '0':
            tiles.append(tile)
            return self.get_explosion_tiles_in_direction(x, y, direction, tiles)

    @staticmethod
    def apply_direction(x, y, direction):
        if direction == 'up':
            return x, y - MAP_CONSTANTS['TILE_SIZE']
        elif direction == 'left':
            return x - MAP_CONSTANTS['TILE_SIZE'], y
        elif direction == 'down':
            return x, y + MAP_CONSTANTS['TILE_SIZE']
        elif direction == 'right':
            return x + MAP_CONSTANTS['TILE_SIZE'], y

    def destroy_tile(self, tile):
        for j in range(len(self.tiles)):
            for i in range(len(self.tiles[j])):
                if self.tiles[i][j] == tile:
                    replacement_tile = self.replacement_empty_tiles.pop()
                    replacement_tile.transform.position.x = tile.transform.position.x
                    replacement_tile.transform.position.y = tile.transform.position.y

                    tile.destroy()
                    self.tiles[i][j] = replacement_tile

    @property
    def empty_tiles(self):
        return [tile for row in self.tiles for tile in row if tile.type == '0']


class Tile(GameObject):

    @staticmethod
    def get_image(tile_type: str):
        if tile_type == 'X':
            return MAP_ASSETS['INDESTRUCTIBLE_TILE']
        elif tile_type == 'P':
            return MAP_ASSETS['DESTRUCTIBLE_TILE']
        elif tile_type == '0':
            return MAP_ASSETS['EMPTY_TILE']

    def __init__(self, name: str, x: int, y: int, front_end, back_end, tile_type: str):
        super().__init__(name=name, x=x, y=y, front_end=front_end, back_end=back_end,
                         image=self.get_image(tile_type), solid=True, unmovable=True)

        self.type = tile_type
        self.width = self.sprite.pixmap.width()
        self.height = self.sprite.pixmap.height()

        if self.type == '0':
            self.box_collider = None

    @property
    def center(self):
        return self.transform.position.x + self.width / 2, self.transform.position.y + self.height / 2

    def destroy(self):
        self.transform.position.x = -100
        self.transform.position.y = -100
        # I should properly destroy it... But I won't until it's actually a necessary optimization.

    def __repr__(self):
        return self.name