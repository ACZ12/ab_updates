import pymunk as pm
import pygame as pg
from pymunk import Vec2d
import math


class Polygon():

    def __init__(self, pos, length, height, space, life, mass=5.0):
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

        wood1 = pg.image.load("./resources/images/wood.png").convert_alpha()
        wood2 = pg.image.load("./resources/images/wood1.png").convert_alpha()

        wod1 = pg.Rect(22, 378, 30, 120)
        wod2 = pg.Rect(24, 502, 30, 120)

        self.original_beam_image = wood1.subsurface(wod1).copy()
        self.original_column_image = wood1.subsurface(wod2).copy()

    def to_pygame(self, p):
        return (int(p.x), int(-p.y + 600))

    def draw_poly(self, element, screen):
        poly = self.shape
        ps = poly.get_vertices()
        ps.append(ps[0])
        ps = map(self.to_pygame, ps)
        ps = list(ps)
        pg.draw.lines(screen, (255, 0, 0), True, ps)

        if element == "beams":
            p = poly.body.position
            p = Vec2d(*self.to_pygame(p))

            # Resize the beam image to match the physical dimensions
            scaled_beam_image = pg.transform.scale(self.original_beam_image, (int(self.length), int(self.height)))

            angle_degrees = math.degrees(poly.body.angle) + 180
            rotated_logo_image = pg.transform.rotate(scaled_beam_image, angle_degrees)
            offset = Vec2d(*rotated_logo_image.get_size()) / 2
            p = p - offset
            screen.blit(rotated_logo_image, (p.x, p.y))

        if element == "columns":
            p = poly.body.position
            p = Vec2d(*self.to_pygame(p))

            # Resize the column image to match the physical dimensions
            scaled_column_image = pg.transform.scale(self.original_column_image, (int(self.length), int(self.height)))

            angle_degrees = math.degrees(poly.body.angle) + 180
            rotated_logo_image = pg.transform.rotate(scaled_column_image, angle_degrees)
            offset = Vec2d(*rotated_logo_image.get_size()) / 2
            p = p - offset
            screen.blit(rotated_logo_image, (p.x, p.y))