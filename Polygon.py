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
    def __init__(self, pos, length, height, space, life, element_type, mass=5.0, radius=15.0, triangle_points=None):
        self.life = life
        moment = 1000
        body = pm.Body(mass, moment)
        body.position = Vec2d(*pos)
        if element_type in ["columns", "beams", "triangles"]:
            #print("element_type in [columns, beams, triangles]")
            shape = pm.Poly.create_box(body, (length, height))
            self.length = length  # Store the physical dimensions for polygons
            self.height = height
            self.original_image = self.load_image(element_type) # Load image based on element_type
            #print(f"Erstelle {element_type} mit Länge: {length}, Höhe: {height}")
            #print(f"Bild geladen: {self.original_image is not None}")
            #print(f"Polygon __init__: {self.original_image is not None}, type: {element_type}")
        elif element_type == "circles":
            #print("element_type == circles")
            shape = pm.Circle(body,radius,(0,0))
            self.length = None # No length or height for circles
            self.height = None
            self.original_image = self.load_image(element_type)
            #print(f"Polygon __init__: {self.original_image is not None}, type: {element_type}")
        elif element_type == "triangles":
            #print("element_type == triangles")
            shape = pm.Poly(body, triangle_points)
            self.original_image = self.load_image(element_type)
        shape.friction = 1
        shape.collision_type = 2
        space.add(body, shape)
        self.body = body
        self.shape = shape
        self.element_type = element_type
        self.radius = radius

    def is_clockwise(self, points):
        """
        Check if the points are in clockwise order.
        https://stackoverflow.com/questions/1165647/how-to-determine-if-a-list-of-polygon-points-are-in-clockwise-order
        """
        n = len(points)
        if n < 3:
            return False
        sum = 0.0
        for i in range(n):
            p1 = points[i]
            p2 = points[(i + 1) % n]
            sum += (p2[0] - p1[0]) * (p2[1] + p1[1])
        return sum > 0

    def load_image(self, element_type):
        #print("load image called")
        texture = None
        if self.life == 20:
            texture = pg.image.load(load_resource("./resources/images/wood3.png")).convert_alpha()
        elif self.life == 30:
            texture = pg.image.load(load_resource("./resources/images/stone.png")).convert_alpha()
        elif self.life == 10:
            texture = pg.image.load(load_resource("./resources/images/ice.png")).convert_alpha()

        wod1 = pg.Rect(131, 301, 154-131, 548-301)
        wod2 = pg.Rect(45, 255, 90-45, 299-255)
        wod3 = pg.Rect(86,102,161-86,202-102)
        ston1 = pg.Rect(181, 285, 205-181, 501-285)
        ston2 = pg.Rect(44, 247, 82-44, 287-247)
        ston3 = pg.Rect(165,106,241-165,193-106)
        #print(f"element type: {element_type}")
        image = None
        
        if element_type == "beams":
            if self.life == 20:
                image = pg.transform.rotate(texture.subsurface(wod1).copy(), 90) # Rotated here
            elif self.life == 30:
                image = pg.transform.rotate(texture.subsurface(ston1).copy(), 90) # Rotated here
            elif self.life == 10:
                image = pg.transform.rotate(texture.subsurface(wod1).copy(), 90) # Rotated here
                
        elif element_type == "columns":
            if self.life == 20:
                image = texture.subsurface(wod1).copy()
            elif self.life == 30:
                image = texture.subsurface(ston1).copy()
            elif self.life == 10:
                image = texture.subsurface(wod1).copy()
                
        elif element_type == "circles":
            if self.life == 20:
                image = texture.subsurface(wod2).copy()
            elif self.life == 30:
                image = texture.subsurface(ston2).copy()
            elif self.life == 10:
                image = texture.subsurface(wod2).copy()
                
        elif element_type == "triangles":
            if self.life == 20:
                image = texture.subsurface(wod3).copy()
            elif self.life == 30:
                image = texture.subsurface(ston3).copy()
            elif self.life == 10:
                image = texture.subsurface(wod3).copy()
                
        print(image)
        return image # image zurückgeben

    def to_pygame(self, p):
        return (int(p.x), int(-p.y + 600))

    def draw_poly(self, screen, shape):
        if isinstance(shape, pm.Poly):
            #print("shape: poly")
            ps = shape.get_vertices()
            #print("ps: ",ps)
            body_pos = shape.body.position
            #print("body_pos=",body_pos) # HIER: Hole die Körperposition
            absolute_ps = [(p.x + body_pos.x, p.y + body_pos.y) for p in ps]
            #print("absolut pos", absolute_ps)
            absolute_ps.append(absolute_ps[0]) # Schließe das Polygon
            ps_pygame = [self.to_pygame(Vec2d(x, y)) for x, y in absolute_ps]
            #print("pspygame",ps_pygame)
            pg.draw.lines(screen, (255, 0, 0), True, ps_pygame, width=3)
            #print(self.original_image,hasattr(shape, 'body'))
            if self.original_image and hasattr(shape, 'body'):
                p = shape.body.position
                #print("p:",p)
                p_pygame = Vec2d(*self.to_pygame(p))
                #print("p_pygame",p_pygame)
                if hasattr(self, 'length') and hasattr(self, 'height'):
                    #print("has height, has lenght")
                    scaled_image = pg.transform.scale(self.original_image, (int(self.length), int(self.height)))
                else:
                    #print("has no height, has no lenght")
                    scaled_image = pg.transform.scale(self.original_image, (int(self.length), int(self.height)))
                angle_degrees = math.degrees(shape.body.angle) + 180
                rotated_image = pg.transform.rotate(scaled_image, angle_degrees)
                offset = Vec2d(*rotated_image.get_size()) / 2
                #print("offset: ",offset)
                p_pygame -= offset
                screen.blit(rotated_image, (p_pygame.x, p_pygame.y))
        elif isinstance(shape, pm.Circle):
            p = self.to_pygame(shape.body.position)
            if self.original_image:
                scaled_image = pg.transform.scale(self.original_image, (int(self.radius * 2), int(self.radius * 2)))
                angle_degrees = math.degrees(shape.body.angle)
                rotated_image = pg.transform.rotate(scaled_image, angle_degrees)
                image_rect = rotated_image.get_rect(center=p)
                screen.blit(rotated_image, image_rect)
            else:
                pg.draw.circle(screen, (0, 0, 255), p, int(shape.radius))