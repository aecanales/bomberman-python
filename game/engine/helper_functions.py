from math import sqrt


def euclidean_distance(position1, position2):
    return sqrt( (position1.x - position2.x)**2 + (position1.y - position2.y)**2 )
