import pymunk as pm
import pygame as pg
from pymunk import Vec2d
import math
import sys
import os

def load_resource(path):
    """Gets the absolute path to a resource, handling both bundled and unbundled."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, path)
    else:
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), path)

class Polygon():

    def __init__(self, pos, length, height, space, life, element_type, mass=5.0):
        moment = 1000
        body = pm.Body(mass, moment)
        body.position = Vec2d(*pos)
        shape = pm.Poly.create_box(body, (length, height))

        shape.friction = 1
        shape.collision_type = 2
        space.add(body, shape)

        self.body = body
        self.shape = shape
        self.length = length  # Store the physical dimensions
        self.height = height
        self.life = life
        self.element_type = element_type
        self.original_image = None
        self.load_image()

    def load_image(self):
        wood1 = pg.image.load(load_resource("./resources/images/wood.png")).convert_alpha()
        wod1 = pg.Rect(22, 378, 30, 120)
        wod2 = pg.Rect(24, 502, 30, 120)

        if self.element_type == "beams":
            self.original_image = wood1.subsurface(wod1).copy()
        elif self.element_type == "columns":
            self.original_image = wood1.subsurface(wod2).copy()

    def to_pygame(self, p):
        return (int(p.x), int(-p.y + 600))

    def draw_poly(self, screen):
        poly = self.shape
        ps = poly.get_vertices()
        ps.append(ps[0])
        ps = map(self.to_pygame, ps)
        ps = list(ps)
        pg.draw.lines(screen, (255, 0, 0), True, ps)

        if self.original_image:
            p = poly.body.position
            p = Vec2d(*self.to_pygame(p))

            scaled_image = pg.transform.scale(self.original_image, (int(self.length), int(self.height)))
            angle_degrees = math.degrees(poly.body.angle) + 180
            rotated_image = pg.transform.rotate(scaled_image, angle_degrees)
            offset = Vec2d(*rotated_image.get_size()) / 2
            p = p - offset
            screen.blit(rotated_image, (p.x, p.y))