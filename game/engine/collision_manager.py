class CollisionManager:

    def __init__(self):
        self.colliding = []  # Tuples in the form (BoxCollider, BoxCollider).

    def run_collision_test(self, game_objects: list):
        # Game objects with box colliders set to None have collisions 'disabled'.
        colliders = [g_o.box_collider for g_o in game_objects if g_o.box_collider is not None]
        for pair in self.create_pairs(colliders):
            this, other = pair
            are_colliding = this.is_colliding_with(other)
            if are_colliding and pair not in self.colliding:
                self.colliding.append(pair)
                this.collision_enter.emit(other.collision_event(this))
                other.collision_enter.emit(this.collision_event(other))
            elif are_colliding and pair in self.colliding:
                this.collision_stay.emit(other.collision_event(this))
                other.collision_stay.emit(this.collision_event(other))
            elif not are_colliding and pair in self.colliding:
                self.colliding.remove(pair)
                this.collision_exit.emit(other.collision_event(this))
                other.collision_exit.emit(this.collision_event(other))

    def bump_solid_object(self):
        solid_pairs = [pair for pair in self.colliding if pair[0].solid and pair[1].solid]
        for pair in solid_pairs:
            if pair[1].unmovable:
                pair[0].bump_into(pair[1])
            elif pair[0].unmovable:
                pair[1].bump_into(pair[0])
            elif pair[1].has_moved:
                pair[1].bump_into(pair[0])
            elif pair[0].has_moved:
                pair[0].bump_into(pair[1])
            else:
                pair[0].bump_into(pair[1])

    @staticmethod
    def create_pairs(items: list):
        """
        Returns a list of tuples of all the possible pairs with the objects in items.
        As seen at http://www.wellho.net/resources/ex.php4?item=y104/tessapy
        """
        result = []
        for i1 in range(len(items)):
            for i2 in range(i1 + 1, len(items)):
                # Optimization: I don't check for collision between objects that can't move.
                if not(items[i1].unmovable and items[i2].unmovable):
                    result.append((items[i1], items[i2]))
        return result



