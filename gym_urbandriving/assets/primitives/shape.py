import numpy as np
from copy import deepcopy
import shapely.geometry

SPRITE_DIR = "gym_urbandriving/visualizer/sprites/"


class Shape:
    SPRITE_DIR = "gym_urbandriving/visualizer/sprites/"
    def __init__(self, x, y, angle, mass, sprite="no_texture.png", static=False):
        self.x = x
        self.y = y
        self.angle = angle % 360
        self.mass = mass
        self.sprite = self.SPRITE_DIR + sprite
        self.static = static
        self.shapely_obj = None

    def get_pos(self):
        return np.array([self.x, self.y])

    def intersect(self, other):
        return self.get_shapely_obj().intersects(other.get_shapely_obj())

    def contains_point(self, point):
        return self.get_shapely_obj().contains(shapely.geomtry.Point(point))

    def dist_to(self, other):
        return self.get_shapely_obj().distance(other.get_shapely_obj())

    def get_sprite(self):
        return self.sprite

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            if k is "shapely_obj":
                setattr(result, k, None)
            else:
                setattr(result, k, deepcopy(v, memo))
        return result

    def collides(self, other):
        return self.can_collide(other) and self.intersect(other)
