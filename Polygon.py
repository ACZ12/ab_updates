import pymunk as pm
import pygame as pg
from pymunk import Vec2d
import math
import sys
import os

def load_resource(path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, path)
    else:
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), path)

class Polygon():
    def __init__(self, pos, length, height, space, life, element_type, screen_height, screen_width, bird_pos=None, mass=5.0, radius=15.0, triangle_points=None, image_path=None):
        self.life = life
        self.element_type = element_type
        self.length = length # Store for drawing, might be None for circles
        self.height = height # Store for drawing, might be None for circles
        self.radius = radius # Store for drawing, only for circles

        current_body = None
        current_shape = None

        if element_type == "bats":
            if image_path is None:
                raise ValueError("image_path must be provided for bats element_type")
            self.original_image = pg.image.load(image_path).convert_alpha()
            
            # Define vertices for the bat's physics body.
            # Existing cut for the left side
            cut_left_percentage = 0.5 
            new_left_x = (-length / 2) + (length * cut_left_percentage)
            right_x = length / 2

            # New cut for the top side
            cut_top_percentage = 0.25
            bottom_y = -height / 2
            new_top_y = (height / 2) - (height * cut_top_percentage)
            bat_box_points = [(new_left_x, bottom_y), (right_x, bottom_y),
                              (right_x, new_top_y), (new_left_x, new_top_y)]

            current_body = pm.Body(body_type=pm.Body.STATIC) # Bat is STATIC
            current_body.position = Vec2d(*pos)
            current_shape = pm.Poly(current_body, bat_box_points)
            current_shape.friction = 0.5 # Bat-specific friction
            # collision_type will be set commonly below

        elif element_type in ["columns", "beams"]:
            moment = pm.moment_for_box(mass, (length, height)) # Calculate moment
            current_body = pm.Body(mass, moment)
            current_body.position = Vec2d(*pos)
            current_shape = pm.Poly.create_box(current_body, (length, height))
            self.original_image = self.load_image(element_type)

        elif element_type == "circles":
            moment = pm.moment_for_circle(mass, 0, radius, (0,0)) # Calculate moment
            current_body = pm.Body(mass, moment)
            current_body.position = Vec2d(*pos)
            current_shape = pm.Circle(current_body, radius, (0,0))
            self.original_image = self.load_image(element_type)

        elif element_type == "triangles":
            # Using a box approximation for triangle's moment of inertia for simplicity
            moment = pm.moment_for_box(mass, (length, height))
            current_body = pm.Body(mass, moment)
            current_body.position = Vec2d(*pos)

            if triangle_points is None:
                # Default triangle points if none provided
                angle = math.radians(0)
                cos_angle = math.cos(angle)
                sin_angle = math.sin(angle)
                # Original points
                points = [
                    (-length/2, height/2),   # Bottom left
                    (length/2, -height/2),   # Top right
                    (length/2, height/2)     # Bottom right
                ]
                final_triangle_points = []
                for x, y in points:
                    new_x = x * cos_angle - y * sin_angle
                    new_y = x * sin_angle + y * cos_angle
                    final_triangle_points.append((new_x, new_y))
                current_shape = pm.Poly(current_body, final_triangle_points)
            else: # Provided triangle_points
                current_shape = pm.Poly(current_body, triangle_points)
            self.original_image = self.load_image(element_type)
        else:
            raise ValueError(f"Unsupported element_type: {element_type}")

        # Common properties for all shapes
        if element_type != "bats": # Bats have their specific friction set above
            current_shape.friction = 1
        current_shape.collision_type = 2 # All polygons (including bats) are type 2

        self.body = current_body
        self.shape = current_shape

        if self.body and self.shape:
            space.add(self.body, self.shape) # Add to space

        self.base_width = 1200
        self.base_height = 650
        
        self.scale_x = screen_width / self.base_width
        self.scale_y = screen_height / self.base_height
        self.in_space = True 

    def update_scale_factors(self, screen_height, screen_width):
        self.scale_x = screen_width / self.base_width
        self.scale_y = screen_height / self.base_height

    def scale_pos(self, x, y):
        return x * self.scale_x, y * self.scale_y
    
    def scale_size(self, width, height):
        return int(width * self.scale_x), int(height * self.scale_y)

    def is_clockwise(self, points):

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
        
        #print(image)
        return image # image zurückgeben

    def to_pygame(self, p):
        return self.scale_pos(int(p.x), int(-p.y + 600))

    def draw_poly(self, screen, shape): # Removed bird_pos parameter
        if isinstance(shape, pm.Poly):
            ps = shape.get_vertices()
            # Use the shape's actual body position for calculating vertices
            current_body_pos = shape.body.position
            absolute_ps = [(v.x + current_body_pos.x, v.y + current_body_pos.y) for v in ps] # Always use shape.body.position
            absolute_ps.append(absolute_ps[0]) # Schließe das Polygon
            ps_pygame = [self.to_pygame(Vec2d(x, y)) for x, y in absolute_ps]
            # pg.draw.lines(screen, (255, 0, 0), True, ps_pygame, width=3) # Uncomment for debugging outline

            if self.original_image and hasattr(shape, 'body'):
                # Use the shape's actual body position for blitting the image
                p_pygame = Vec2d(*self.to_pygame(shape.body.position))

                if self.length is not None and self.height is not None:
                    img_width, img_height = self.scale_size(int(self.length), int(self.height))
                    scaled_image = pg.transform.scale(self.original_image, (img_width, img_height))
                else:
                    # Fallback if length/height are not set (should not happen for standard polys)
                    scaled_image = self.original_image 

                angle_degrees = 0
                if self.element_type != "triangles": # Original logic for columns, beams, (and now bats)
                    angle_degrees = math.degrees(shape.body.angle)
                else: # Triangles
                    angle_degrees = math.degrees(shape.body.angle) -90

                rotated_image = pg.transform.rotate(scaled_image, angle_degrees)

                # Standard offset calculation to center the image on the body's position
                offset = Vec2d(*rotated_image.get_size()) / 2
                blit_pos = p_pygame - offset
                screen.blit(rotated_image, (blit_pos[0], blit_pos[1]))

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
            
    
class Static_line():
    def __init__(self,screen_width,screen_height,space):
        self.space = space
        self.base_width = 1200
        self.base_height = 650
        self.scale_x = screen_width / self.base_width
        self.scale_y = screen_height / self.base_height
        self.static_body = pm.Body(body_type=pm.Body.STATIC)
        self.static_lines = [pm.Segment(self.static_body, (0.0, 130.0), (1200.0, 130.0), 0.0)]
        for line in self.static_lines:
            line.elasticity = 0.95
            line.collision_type = 3
            line.friction = 1
        self.space.add(self.static_body, *self.static_lines)
        
        
    
    def scale_pos(self, x, y):
        """Scale the given coordinates based on the current window size."""
        return x * self.scale_x, y * self.scale_y
