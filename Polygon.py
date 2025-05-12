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
    def __init__(self, pos, length, height, space, life, element_type, screen_height, screen_width, mass=5.0, radius=15.0, triangle_points=None):
        self.life = life
        moment = 1000
        body = pm.Body(mass, moment)
        body.position = Vec2d(*pos)
        if element_type in ["columns", "beams"]:
            shape = pm.Poly.create_box(body, (length, height))
            self.length = length
            self.height = height
            self.original_image = self.load_image(element_type)
        elif element_type == "circles":
            shape = pm.Circle(body, radius, (0,0))
            self.length = None
            self.height = None
            self.original_image = self.load_image(element_type)
        elif element_type == "triangles":
            if triangle_points is None:
                # Default triangle points if none provided
                angle = math.radians(180)  # 180 degrees in radians
                cos_angle = math.cos(angle)
                sin_angle = math.sin(angle)
                
                # Original points
                points = [
                    (-length/2, height/2),   # Bottom left
                    (length/2, -height/2),   # Top right
                    (length/2, height/2)     # Bottom right
                ]
                
                # Rotate each point by 180 degrees
                triangle_points = []
                for x, y in points:
                    # Apply rotation matrix
                    new_x = x * cos_angle - y * sin_angle
                    new_y = x * sin_angle + y * cos_angle
                    triangle_points.append((new_x, new_y))
                    
            shape = pm.Poly(body, triangle_points)
            self.length = length
            self.height = height
            self.original_image = self.load_image(element_type)
        shape.friction = 1
        shape.collision_type = 2
        space.add(body, shape)
        self.body = body
        self.shape = shape
        self.element_type = element_type
        self.radius = radius
        
        # Set base dimensions
        self.base_width = 1200
        self.base_height = 650
        
        # Initialize scaling factors
        self.scale_x = screen_width / self.base_width
        self.scale_y = screen_height / self.base_height

    def update_scale_factors(self, screen_height, screen_width):
        """Update the scaling factors based on new screen dimensions."""
        self.scale_x = screen_width / self.base_width
        self.scale_y = screen_height / self.base_height

    def scale_pos(self, x, y):
        """Scale the given coordinates based on the current window size."""
        return x * self.scale_x, y * self.scale_y
    
    def scale_size(self, width, height):
        """Scale the given dimensions based on the current window size."""
        return int(width * self.scale_x), int(height * self.scale_y)

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
        return self.scale_pos(int(p.x), int(-p.y + 600))

    def draw_poly(self, screen, shape):
        if isinstance(shape, pm.Poly):
            ps = shape.get_vertices()
            body_pos = shape.body.position
            absolute_ps = [(p.x + body_pos.x, p.y + body_pos.y) for p in ps]
            absolute_ps.append(absolute_ps[0]) # Schließe das Polygon
            ps_pygame = [self.to_pygame(Vec2d(x, y)) for x, y in absolute_ps]
            pg.draw.lines(screen, (255, 0, 0), True, ps_pygame, width=3)
            if self.original_image and hasattr(shape, 'body'):
                p = shape.body.position
                p_pygame = Vec2d(*self.to_pygame(p))
                if hasattr(self, 'length') and hasattr(self, 'height'):
                    scaled_image = pg.transform.rotate(pg.transform.scale(self.original_image, self.scale_size(int(self.length), int(self.height))),90)
                else:
                    scaled_image = pg.transform.rotate(pg.transform.scale(self.original_image, (int(self.length), int(self.height))), 90)
                if self.element_type == "triangles":
                    angle_degrees = math.degrees(shape.body.angle)
                else:
                    angle_degrees = math.degrees(shape.body.angle) -90
                rotated_image = pg.transform.rotate(scaled_image, angle_degrees)
                offset = Vec2d(*rotated_image.get_size()) / 2
                p_pygame -= offset
                #screen.blit(rotated_image, (p_pygame[0]-rotated_image.get_width()/4,p_pygame[1]-rotated_image.get_height()/4))
                screen.blit(rotated_image, (p_pygame[0],p_pygame[1]))
        elif isinstance(shape, pm.Circle):
            p = self.to_pygame(shape.body.position)
            if self.original_image:
                scaled_image = pg.transform.scale(self.original_image, (int(self.radius * 2), int(self.radius * 2)))
                angle_degrees = math.degrees(shape.body.angle)
                rotated_image = pg.transform.rotate(scaled_image, angle_degrees)
                image_rect = rotated_image.get_rect(center=p)
                screen.blit(rotated_image, (p[0]-rotated_image.get_width()/2,p[1]-rotated_image.get_height()/2))
            else:
                pg.draw.circle(screen, (0, 0, 255), p, int(shape.radius))