import pymunk as pm
import pygame as pg
from pymunk import Vec2d
import math
import sys
import os

def load_resource(path):
    """
    Helper to get resource paths, works for normal run & PyInstaller bundle.
    Also handles if the path is already absolute.
    """
    if os.path.isabs(path): # If path is already absolute, return it directly
        return path
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller bundles stuff here
        base_path = sys._MEIPASS
    else:
        # Normal execution path
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, path)

class Polygon():
    def __init__(self, pos, length, height, space, life, element_type, screen_height, screen_width, mass=5.0, radius=15.0, triangle_points=None, image_path=None, material_type=None):
        self.life = life
        self.original_life = life # Store the initial life for damage state comparison
        self.element_type = element_type
        self.length = length # Store for drawing, might be None for circles
        self.height = height # Store for drawing, might be None for circles
        self.radius = radius # Store for drawing, only for circles
        self.material_type = material_type

        # For material-based damage textures
        self.image_subsurface_normal = None
        self.image_subsurface_damaged = None
        # Calculate damage threshold based on original_life for this instance.
        # This makes it robust even if initial life values change for materials.
        self.damage_threshold_life = self.original_life // 2 # Integer division
        self.uses_material_damage_textures = False

        self.original_image = None

        # Define sub-rectangles for textures (used if uses_material_damage_textures)
        # USER ACTION: CRITICAL - Verify these rectangles match your spritesheet layouts!
        # Format: pg.Rect(left, top, width, height)
        rects_wood = {
            "beams": pg.Rect(131, 301, 23, 247),    # Original: 154-131, 548-301
            "columns": pg.Rect(131, 301, 23, 247),  # Original: 154-131, 548-301
            "circles": pg.Rect(45, 255, 45, 44),    # Original: 90-45, 299-255
            "triangles": pg.Rect(86, 102, 75, 100)  # Original: 161-86, 202-102
        }
        rects_stone = {
            "beams": pg.Rect(181, 285, 24, 216),   # Original: 205-181, 501-285
            "columns": pg.Rect(181, 285, 24, 216), # Original: 205-181, 501-285
            "circles": pg.Rect(44, 247, 38, 40),   # Original: 82-44, 287-247
            "triangles": pg.Rect(165, 106, 76, 87) # Original: 241-165, 193-106
        }
        # USER ACTION: Define specific rects for ice if ice.png/ice_dmg1.png
        # have a different layout than wood3.png.
        # These are placeholders assuming ice uses a similar layout to wood.
        # If your ice spritesheets are different, these MUST be changed.
        rects_ice = {
            "beams": pg.Rect(131, 301, 23, 247),    # Placeholder, verify!
            "columns": pg.Rect(131, 301, 23, 247),  # Placeholder, verify!
            "circles": pg.Rect(45, 255, 45, 44),    # Placeholder, verify!
            "triangles": pg.Rect(86, 102, 75, 100)  # Placeholder, verify!
        }

        if image_path: # Priority 1: If an explicit image_path is given, use it.
            self.original_image = pg.image.load(load_resource(image_path)).convert_alpha()
        elif element_type == "bats": # Bats *must* have an image_path.
            raise ValueError("image_path must be provided for 'bats' element_type")
        elif self.material_type and element_type in ["columns", "beams", "circles", "triangles"]:
            self.uses_material_damage_textures = True
            spritesheet_normal_full = None
            spritesheet_damaged_full = None
            mat_rects = None

            if self.material_type == "wood":
                spritesheet_normal_full = pg.image.load(load_resource("./resources/images/wood3.png")).convert_alpha()
                spritesheet_damaged_full = pg.image.load(load_resource("./resources/images/wood3_dmg1.png")).convert_alpha()
                mat_rects = rects_wood
            elif self.material_type == "stone":
                spritesheet_normal_full = pg.image.load(load_resource("./resources/images/stone.png")).convert_alpha()
                spritesheet_damaged_full = pg.image.load(load_resource("./resources/images/stone_dmg1.png")).convert_alpha()
                mat_rects = rects_stone
            elif self.material_type == "ice":
                spritesheet_normal_full = pg.image.load(load_resource("./resources/images/ice.png")).convert_alpha()
                spritesheet_damaged_full = pg.image.load(load_resource("./resources/images/ice_dmg1.png")).convert_alpha()
                mat_rects = rects_ice

            if spritesheet_normal_full and spritesheet_damaged_full and mat_rects and element_type in mat_rects:
                sub_rect = mat_rects[element_type]
                self.image_subsurface_normal = spritesheet_normal_full.subsurface(sub_rect).copy()
                self.image_subsurface_damaged = spritesheet_damaged_full.subsurface(sub_rect).copy()
                if element_type == "beams": # Beams are pre-rotated
                    self.image_subsurface_normal = pg.transform.rotate(self.image_subsurface_normal, 90)
                    self.image_subsurface_damaged = pg.transform.rotate(self.image_subsurface_damaged, 90)
            # self.original_image is not set here; draw_poly will use the subsurfaces.
        # else: self.original_image remains None if no explicit path and not a handled material type.

        current_body = None
        current_shape = None
        if element_type == "bats":
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
            # self.original_image is already handled by the unified logic above.

        elif element_type in ["columns", "beams"]: # Handles rectangular dynamic objects
            moment = pm.moment_for_box(mass, (length, height))
            current_body = pm.Body(mass, moment)
            current_body.position = Vec2d(*pos)
            current_shape = pm.Poly.create_box(current_body, (length, height))

        elif element_type in ["circles", "bombs"]:
            moment = pm.moment_for_circle(mass, 0, radius, (0,0))
            current_body = pm.Body(mass, moment)
            current_body.position = Vec2d(*pos)
            current_shape = pm.Circle(current_body, radius, (0,0))

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
        # Base dimensions for scaling calculations
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
        # Determines if a set of polygon vertices are in clockwise order
        n = len(points)
        if n < 3:
            return False
        sum = 0.0
        for i in range(n):
            p1 = points[i]
            p2 = points[(i + 1) % n]
            sum += (p2[0] - p1[0]) * (p2[1] + p1[1])
        return sum > 0

    def to_pygame(self, p):
        return self.scale_pos(int(p.x), int(-p.y + 600))

    def draw_poly(self, screen, shape): # Removed bird_pos parameter
        if isinstance(shape, pm.Poly):
            ps = shape.get_vertices()
            # Use the shape's actual body position for calculating vertices
            current_body_pos = shape.body.position
            absolute_ps = [(v.x + current_body_pos.x, v.y + current_body_pos.y) for v in ps] # Always use shape.body.position
            absolute_ps.append(absolute_ps[0]) # Close the polygon for drawing
            ps_pygame = [self.to_pygame(Vec2d(x, y)) for x, y in absolute_ps]
            # pg.draw.lines(screen, (255, 0, 0), True, ps_pygame, width=3) # Uncomment for debugging outline

            image_to_render = None
            if self.uses_material_damage_textures:
                # Original logic for selecting damaged or normal texture
                if self.life <= self.damage_threshold_life and self.life > 0 and self.life < self.original_life:
                    image_to_render = self.image_subsurface_damaged
                else:
                    image_to_render = self.image_subsurface_normal
            else: # Not using damage textures, use the original_image (e.g. for bats, bombs, or untextured polys)
                image_to_render = self.original_image

            if image_to_render and hasattr(shape, 'body'):
                # Use the shape's actual body position for blitting the image
                p_pygame = Vec2d(*self.to_pygame(shape.body.position))

                if self.length is not None and self.height is not None:
                    img_width, img_height = self.scale_size(int(self.length), int(self.height))
                    scaled_image = pg.transform.scale(image_to_render, (img_width, img_height))
                else:
                    # Fallback if length/height are not set (should not happen for standard polys)
                    scaled_image = image_to_render

                # Default rotation from physics body
                angle_degrees = math.degrees(shape.body.angle)

                if self.element_type == "triangles":
                    # Triangles have a specific asset orientation that needs an additional -90 deg adjustment
                    # relative to their physics body's angle.
                    angle_degrees -= 90
                # For beams, their texture was made horizontal in __init__.
                # So, applying shape.body.angle directly is correct for their final orientation.
                # For columns and other polygon types, applying shape.body.angle is also correct.
                rotated_image = pg.transform.rotate(scaled_image, angle_degrees)

                # Standard offset calculation to center the image on the body's position
                offset = Vec2d(*rotated_image.get_size()) / 2
                blit_pos = p_pygame - offset
                screen.blit(rotated_image, (blit_pos[0], blit_pos[1]))

        elif isinstance(shape, pm.Circle):
            p = self.to_pygame(shape.body.position)
            
            image_to_render_circle = None
            if self.uses_material_damage_textures: # For circles like ice/wood/stone
                # Original logic for selecting damaged or normal texture for circles
                if self.life <= self.damage_threshold_life and self.life > 0 and self.life < self.original_life:
                    image_to_render_circle = self.image_subsurface_damaged
                else:
                    image_to_render_circle = self.image_subsurface_normal
            else: # For circles with explicit image_path (like Bomb's projectile)
                image_to_render_circle = self.original_image

            if image_to_render_circle:
                img_w_px, img_h_px = 0, 0
                if self.length is not None and self.height is not None:
                    # If length and height are provided (e.g., for bomb projectile),
                    # use them as the base world dimensions for the image, then scale to pixels.
                    img_w_px, img_h_px = self.scale_size(int(self.length), int(self.height))
                else:
                    # Fallback for structural circles: use physics radius for image size.
                    diameter_world = self.radius * 2
                    img_w_px, img_h_px = self.scale_size(int(diameter_world), int(diameter_world))

                scaled_image = pg.transform.scale(image_to_render_circle, (img_w_px, img_h_px))
                angle_degrees = math.degrees(shape.body.angle)
                rotated_image = pg.transform.rotate(scaled_image, angle_degrees)
                image_rect = rotated_image.get_rect(center=p)
                screen.blit(rotated_image, image_rect.topleft)
            else: # No original_image, draw a primitive circle
                # shape.radius is in Pymunk world units.
                # Scale it to pixels for drawing. Use an average screen scale factor.
                avg_scale = (self.scale_x + self.scale_y) / 2.0
                pixel_radius = int(shape.radius * avg_scale)
                pg.draw.circle(screen, (0, 0, 255), p, pixel_radius)

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
            line.collision_type = 3 # Collision type for ground
            line.friction = 1
        self.space.add(self.static_body, *self.static_lines)
        
        
    
    def scale_pos(self, x, y):
        return x * self.scale_x, y * self.scale_y
