# main.py
import os
import sys
import math
import pygame as pg
import time
import pymunk as pm
from level import Level
import character as ch
from pygame.locals import *
import msal
import requests
import zipfile
import shutil
import json
from pymunk import Vec2d
import random
from Polygon import Static_line, Polygon # Assuming Polygon.py is in the same directory

# GLOBALS
bird = None
bird_img = None
sling_anchor = (130, 380)
x_mouse,y_mouse = 0,0
pigs = []
birds = []
balls = []
polys = []
beams = []
columns = []
circles = []
triangles = []
poly_points = []
ball_num = 0
polys_dict = {}
mouse_distance = 0
rope_length = 90
angle = 90
launch_angle = 0
pu = 0
levels_drawn = False
ssahur = None


sound_on = True
count = 0
mouse_pressed_to_shoot = False
tick_to_next_circle = 10

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TRANSP = (0, 0, 0, 0)



score = 0

game_state = 7
levels_drawn = False
bird_path = []
counter = 0
restart_counter = False
bonus_score_once = True

loaded = False

wall = False

# Add at the top with other globals
slingl = None
slingr = None
slingl_scaled_width = None
slingl_scaled_height = None
slingr_scaled_width = None
slingr_scaled_height = None

POLY_POLY_COLLISION_IMPULSE_THRESHOLD = 1500.0 
POLY_POLY_DAMAGE_VALUE = 15  
POLY_DESTROY_SCORE = 500     
ABILITY_COLLISION_IMPULSE_THRESHOLD = 2000.0 



def main_loop():
    
    # GLOBALS
    global POLY_DESTROY_SCORE
    global POLY_POLY_COLLISION_IMPULSE_THRESHOLD
    global POLY_POLY_DAMAGE_VALUE
    global ABILITY_COLLISION_IMPULSE_THRESHOLD

    global bird_img
    global bird
    global sling_anchor
    global x_mouse
    global y_mouse
    global pigs
    global birds
    global balls
    global polys
    global beams
    global columns
    global circles
    global triangles
    global poly_points
    global ball_num
    global polys_dict
    global mouse_distance
    global rope_length
    global angle
    global launch_angle
    global pu
    global slingl, slingr, slingl_scaled_width, slingl_scaled_height, slingr_scaled_width, slingr_scaled_height
    global ssahur

    global sound_on
    global count
    global mouse_pressed_to_shoot
    global tick_to_next_circle
    global loaded

    global RED
    global BLUE
    global YELLOW
    global ORANGE
    global PURPLE
    global PINK
    global BLACK
    global WHITE
    global TRANSP

    global slingl_x
    global slingl_y
    global slingr_x
    global slingr_y

    global score

    global game_state
    global levels_drawn
    global bird_path
    global counter
    global restart_counter
    global bonus_score_once
    global levels_drawn



    global wall



    
    pg.init()
    screen_width, screen_height = 1200, 650
    screen = pg.display.set_mode((1200, 650), pg.RESIZABLE)
    
    screen_width, screen_height = pg.display.get_surface().get_size()
    base_width, base_height = 1200, 650
    scale_x = screen_width / base_width
    scale_y = screen_height / base_height
    
    

    def scale_pos(x, y):
        return x * scale_x, y * scale_y

    def scale_size(width, height):
        return width * scale_x, height * scale_y
    
    sling_anchor = scale_pos(130, 380)
    
    # Base positions for sling
    base_slingl_x, base_slingl_y = 120, 370
    base_slingr_x, base_slingr_y = 120, 370
    
    
    def get_sling_positions():
        # Base positions for sling
        base_slingl_x, base_slingl_y = 120, 370
        base_slingr_x, base_slingr_y = 120, 370
        return scale_pos(base_slingl_x, base_slingl_y)

    bold_font = pg.font.SysFont("arial", 20, bold=True)
    bold_font2 = pg.font.SysFont("arial", 30, bold=True)
    bold_font3 = pg.font.SysFont("arial", 50, bold=True)
    
    bird_scale_factor = 0.3
    pig_scale_factor = 1
    star13_scale_factor = 0.5
    star2_scale_factor = 1


    def load_resource(path):
        """Helper to get resource paths, works for normal run & PyInstaller bundle."""
        if hasattr(sys, '_MEIPASS'):
            # PyInstaller bundles stuff here
            return os.path.join(sys._MEIPASS, path)
        else:
            # Normal execution path
            return os.path.join(os.path.dirname(os.path.abspath(__file__)), path)

    bg = pg.image.load(load_resource("./resources/images/bg.png")).convert_alpha()
    buttons = pg.image.load(load_resource("./resources/images/buttons.png")).convert_alpha()
    buttons2 = pg.image.load(load_resource("./resources/images/buttons2.png")).convert_alpha()
    menu_son = pg.image.load(load_resource("./resources/images/menu_son.png")).convert_alpha()
    menu_sof = pg.image.load(load_resource("./resources/images/menu_sof.png")).convert_alpha()
    menu_son = pg.transform.scale(menu_son, (250, screen_height))
    menu_sof = pg.transform.scale(menu_sof, (250, screen_height))

    rect = pg.Rect(32, 19, 122 - 32, 116 - 19)
    replay_button = buttons.subsurface(rect).copy()

    rect = pg.Rect(25, 142, 122 - 25, 243 - 142)
    stop_button = pg.transform.scale(buttons.subsurface(rect).copy(), (65, 65))

    rect = pg.Rect(173, 444, 274 - 173, 552 - 444)
    next_button = buttons.subsurface(rect).copy()

    rect = pg.Rect(165, 132, 277 - 165, 259 - 132)
    exit_button = buttons.subsurface(rect).copy()

    rect = pg.Rect(18, 264, 114 - 18, 365 - 264)
    go_button = buttons.subsurface(rect).copy()

    rect = pg.Rect(167, 288, 284 - 167, 409 - 288)
    sound_button = buttons.subsurface(rect).copy()

    sound_button_scaled_width = int(sound_button.get_width() * 0.5)
    sound_button_scaled_height = int(sound_button.get_height() * 0.5)

    sound_button = pg.transform.scale(sound_button, (sound_button_scaled_width, sound_button_scaled_height))

    rect = pg.Rect(73, 192, 92 - 73, 212 - 192)
    muted_sound_button = buttons2.subsurface(rect).copy()
    muted_sound_button = pg.transform.scale(muted_sound_button, (sound_button.get_width(), sound_button.get_height()))

    rect = pg.Rect(26, 385, 117 - 26, 478 - 385)
    menu_button = buttons.subsurface(rect).copy()

    rect = pg.Rect(291, 11, 547 - 291, 181 - 11)
    play_button = buttons.subsurface(rect).copy()

    wood1 = pg.image.load(load_resource("./resources/images/wood.png")).convert_alpha()
    star1 = pg.image.load(load_resource("./resources/images/stars/gold_star.png")).convert_alpha()
    star2 = pg.image.load(load_resource("./resources/images/stars/jew_star.png")).convert_alpha()
    star3 = pg.image.load(load_resource("./resources/images/stars/soviet_star.png")).convert_alpha()

    sling = pg.image.load(load_resource("./resources/images/sling.png")).convert_alpha()
    slingl = pg.image.load(load_resource("./resources/images/slingl.png")).convert_alpha()
    slingr = pg.image.load(load_resource("./resources/images/slingr.png")).convert_alpha()

    n11 = pg.image.load(load_resource("./resources/images/n1.1.png")).convert_alpha()
    n12 = pg.image.load(load_resource("./resources/images/n1.2.png")).convert_alpha()
    n21 = pg.image.load(load_resource("./resources/images/n2.1.png")).convert_alpha()
    n22 = pg.image.load(load_resource("./resources/images/n2.2.png")).convert_alpha()
    n31 = pg.image.load(load_resource("./resources/images/n3.1.png")).convert_alpha()
    n32 = pg.image.load(load_resource("./resources/images/n3.2.png")).convert_alpha()
    n41 = pg.image.load(load_resource("./resources/images/n4.1.png")).convert_alpha()
    n42 = pg.image.load(load_resource("./resources/images/n4.2.png")).convert_alpha()
    n51 = pg.image.load(load_resource("./resources/images/n5.1.png")).convert_alpha()
    n52 = pg.image.load(load_resource("./resources/images/n5.2.png")).convert_alpha()

    trala = pg.image.load(load_resource("./resources/images/trala.png")).convert_alpha()
    sahur = pg.image.load(load_resource("./resources/images/sahur.png")).convert_alpha()

    n11_scaled_width = int(n11.get_width() * pig_scale_factor)
    n11_scaled_height = int(n11.get_height() * pig_scale_factor)

    sahur_scaled_width = int(sahur.get_width() * bird_scale_factor)
    sahur_scaled_height = int(sahur.get_height() * bird_scale_factor)

    star13_scaled_width = int(star1.get_width() * star13_scale_factor)
    star13_scaled_height = int(star1.get_height() * star13_scale_factor)
    star2_scaled_width = int(star2.get_width() * star2_scale_factor)
    star2_scaled_height = int(star2.get_height() * star2_scale_factor)

    star1 = pg.transform.scale(star1, (star13_scaled_width, star13_scaled_height))
    star3 = pg.transform.scale(star3, (star13_scaled_width, star13_scaled_height))
    star2 = pg.transform.scale(star2, (star2_scaled_width, star2_scaled_height))

    # Calculate initial scaled dimensions
    slingl_scaled_width = int(slingl.get_width() * 0.135)  # design const
    slingl_scaled_height = int(slingl.get_height() * 0.135) # design const
    slingr_scaled_width = int(slingr.get_width() * 0.05) # design const
    slingr_scaled_height = int(slingr.get_height() * 0.05) # design const
    
    # Initial scaling of sling images
    slingl = pg.transform.scale(slingl, scale_size(slingl_scaled_width, slingl_scaled_height))
    slingr = pg.transform.scale(slingr, scale_size(slingr_scaled_width, slingr_scaled_height))

    n11 = pg.transform.scale(n11, (n11_scaled_width, n11_scaled_height))
    sahur = pg.transform.scale(sahur, (sahur_scaled_width, sahur_scaled_height))
    #print(slingr.get_width(), slingr.get_height())
    #print(slingl.get_width(), slingl.get_height())
    

    bomb0 = pg.image.load(load_resource("./resources/images/bomb0.png")).convert_alpha()
    bomb1 = pg.image.load(load_resource("./resources/images/bomb.png")).convert_alpha()
    bomb2 = pg.image.load(load_resource("./resources/images/bomb2.png")).convert_alpha()

    glorbo = pg.image.load(load_resource("./resources/images/glorbo.png")).convert_alpha()
    liri = pg.image.load(load_resource("./resources/images/liri.png")).convert_alpha()
    liri = pg.transform.scale(liri,(liri.get_width()*0.1,liri.get_height()*0.1))

    patapim_full = pg.image.load(load_resource("./resources/images/patapim.png")).convert_alpha()
    patapim_leg1 = pg.image.load(load_resource("./resources/images/patapim_leg1.png")).convert_alpha()
    patapim_leg2 = pg.image.load(load_resource("./resources/images/patapim_leg2.png")).convert_alpha()

    levels_menu = pg.image.load(load_resource("./resources/images/levels_menu.png")).convert_alpha()
    rect = pg.Rect(220, 79, 359 - 220, 218 - 79)
    level_icon = pg.transform.scale(levels_menu.subsurface(rect).copy(), (100, 100))
    rect = pg.Rect(1563, 600, 1700 - 1563, 740 - 600)
    locked_level_icon = pg.transform.scale(levels_menu.subsurface(rect).copy(), (100, 100))

    clock = pg.time.Clock()

    running = True

    # base physics

    space = pm.Space()
    space.gravity = (0.0, -700.0)

    
    # STATIC FLOOR

    floor = Static_line(screen_height,screen_width,space)

    def get_all_files_listdir(directory):
        all_files = []
        try:
            for entry in os.listdir(load_resource(directory)):
                path = os.path.join(load_resource(directory), entry)
                if os.path.isfile(path):
                    all_files.append(entry)
        except FileNotFoundError:
            print(f"Error: Directory not found: {directory}")
        return all_files

    win_imgs = get_all_files_listdir("./resources/images/win_imgs")
    lose_imgs = get_all_files_listdir("./resources/images/lose_imgs")

    buttons = pg.image.load(load_resource("./resources/images/buttons.png")).convert_alpha()

    def to_pygame(p):
        x, y = p.x, -p.y + 600
        return scale_pos(x, y)

    def vector(p0, p1):  # return vector of p1 and p2
        a = p1[0] - p0[0] # x component
        b = p1[1] - p0[1] # y component
        return a, b

    def unit_vector(v): # get unit vector
        h = ((v[0] ** 2 + (v[1] ** 2)) ** 0.5)
        if h == 0:
            h = 0.000000000000001
        ua = v[0] / h
        ub = v[1] / h
        return ua, ub

    def distance(x0, y0, x, y): # calculate distance between two points
        dx = x - x0
        dy = y - y0
        d = ((dx ** 2) + (dy ** 2)) ** 0.5
        return d

    def sling_action(): # change pos of sling
        global launch_angle
        global x_mouse # mouse coords are global
        global y_mouse
        global impulse_x
        global impulse_y
        global sling_anchor
        global mouse_distance
        global pu

        sx, sy = scale_pos(*sling_anchor)
        mx, my = x_mouse, y_mouse

        v = vector((sx, sy), (mx, my))
        uv = unit_vector(v) # unit vector for direction
        uv1 = uv[0]
        uv2 = uv[1]
        # distance from sling anchor to mouse
        mouse_distance_raw = distance(sx, sy, mx, my)

        if mouse_distance_raw > rope_length:
            mouse_distance = rope_length
            pu = uv1 * rope_length + sx, uv2 * rope_length + sy
            x_sahur = pu[0] - sahur.get_width() // 2
            y_sahur = pu[1] - sahur.get_height() // 2
            # Draw bird and sling lines if bird is available
            if len(level.level_birds) >= 0:

                screen.blit(bird_img, (x_sahur, y_sahur))
                slingl_x, slingl_y = get_sling_positions()
                slingr_x, slingr_y = get_sling_positions()
                pg.draw.line(screen, (0, 0, 0), (slingr_x + 4 * scale_x, slingr_y + 3 * scale_y), pu, 5)
                pg.draw.line(screen, (0, 0, 0), (slingl_x + 2 * scale_x, slingl_y + 13 * scale_y), pu, 5)
        else:
            mouse_distance = mouse_distance_raw
            pu = mx, my
            x_sahur = mx - sahur.get_width() // 2
            y_sahur = my - sahur.get_height() // 2
            # Draw bird and sling lines if bird is available
            if len(level.level_birds) >= 0:

                screen.blit(bird_img, (x_sahur, y_sahur))
                slingl_x, slingl_y = get_sling_positions()
                slingr_x, slingr_y = get_sling_positions()
                pg.draw.line(screen, (0, 0, 0), (slingr_x + 4 * scale_x, slingr_y + 3 * scale_y), (mx, my), 5)
                pg.draw.line(screen, (0, 0, 0), (slingl_x + 2 * scale_x, slingl_y + 13 * scale_y), (mx, my), 5)
        # calculate angle for launch
        dy = sy - pu[1]
        dx = sx - pu[0]
        if dx == 0:
            dx = 0.000000000000001

        angle = math.atan2(dy, dx)
        launch_angle = angle

    def restart():
        global mouse_pressed_to_shoot, restart_counter
        mouse_pressed_to_shoot = False
        restart_counter = False

        # First, clean up any ability polygons (like Sahur's bat)
        # These are often tracked in the 'columns' list.
        for bird_instance in list(birds): # Iterate a copy
            if hasattr(bird_instance, 'ability_polygon') and bird_instance.ability_polygon:
                poly = bird_instance.ability_polygon
                if poly.shape and poly.body and poly.shape in space.shapes:
                    space.remove(poly.shape, poly.body)
                poly.in_space = False # Mark the Polygon object
                if poly in columns: # Remove from the 'columns' list
                    columns.remove(poly)
                bird_instance.ability_polygon = None # Nullify bird's reference

        # Next, remove all active birds from the game and space
        for bird_instance in list(birds): # Iterate a copy
            if bird_instance.shape and bird_instance.body and bird_instance.shape in space.shapes:
                space.remove(bird_instance.shape, bird_instance.body)
        birds.clear()

        # Then, remove all pigs
        for pig_instance in list(pigs): # Iterate a copy
            if pig_instance.shape and pig_instance.body and pig_instance.shape in space.shapes:
                space.remove(pig_instance.shape, pig_instance.body)
        pigs.clear()

        # Finally, clear out all other game elements (blocks, etc.)
        # Note: some 'columns' might be ability polygons already removed.
        # The Polygon class's 'in_space' helps track this.
        
        # Columns
        for column_item in list(columns):
            if column_item.shape and column_item.body and column_item.shape in space.shapes:
                space.remove(column_item.shape, column_item.body)
            column_item.in_space = False
        columns.clear()

        # Beams
        for beam_item in list(beams):
            if beam_item.shape and beam_item.body and beam_item.shape in space.shapes:
                space.remove(beam_item.shape, beam_item.body)
            beam_item.in_space = False
        beams.clear()
            
        # Circles
        for circle_item in list(circles):
            if circle_item.shape and circle_item.body and circle_item.shape in space.shapes:
                space.remove(circle_item.shape, circle_item.body)
            circle_item.in_space = False
        circles.clear()

        # Triangles
        for triangle_item in list(triangles):
            if triangle_item.shape and triangle_item.body and triangle_item.shape in space.shapes:
                space.remove(triangle_item.shape, triangle_item.body)
            triangle_item.in_space = False
        triangles.clear()

    def post_solve_bird_pig(arbiter, space, _):
        a, b = arbiter.shapes
        bird_body = a.body
        pig_body = b.body
        bird_momentum = bird_body.mass * bird_body.velocity.length # for damage calc
        base_damage = 0
        momentum_damage_factor = 0.99 # Further increased from 0.66
        damage = base_damage + (bird_momentum * momentum_damage_factor)

        pig_to_remove = []
        for pig in pigs:
            if pig.body == pig_body and bird_momentum > 25:
                pig.life -= damage # deal damage
                if pig.life <= 0:
                    pig_to_remove.append(pig)
                    global score
                    score += 10000

        for pig in pig_to_remove:
            space.remove(pig.shape, pig.body)
            pigs.remove(pig)
            
    def post_solve_bird_wood(arbiter, space, _):
        global beams
        global columns
        global triangles
        global circles
        element_to_remove = []
        a, b = arbiter.shapes
        bird_body = a.body
        wood_body = b.body  # Get the wood's body.  Need this.
        bird_momentum = bird_body.mass * bird_body.velocity.length # Bird's momentum

        base_damage = 0
        momentum_damage_factor = 0.13
        damage = base_damage + (bird_momentum * momentum_damage_factor)

        if arbiter.total_impulse.length > 2000:
            for element in columns + circles + beams + triangles:
                if element.shape.body == wood_body:  # Change to check the body
                    element.life -= damage
                    if element.life <= 0:
                        element_to_remove.append(element)
                        global score
                        score += 1000
        for element in element_to_remove:
            space.remove(element.shape, element.body)
            if element.element_type == "columns":
                columns.remove(element)
            elif element.element_type == "beams":
                beams.remove(element)
            elif element.element_type == "circles":
                circles.remove(element)
            elif element.element_type == "triangles":
                triangles.remove(element)

    def post_solve_pig_wood(arbiter, space, _):
        pig_to_remove = []
        pig_shape, wood_poly_shape = arbiter.shapes # wood_poly_shape is the type 2 object (polygon/bat)

        is_sahurs_bat_collision = False
        # Check if the wood_poly_shape is Sahur's active bat
        if birds: # Ensure there's at least one bird (the active one)
            active_bird = birds[-1] # The bird currently in play
            if isinstance(active_bird, ch.Sahur) and \
               active_bird.fahigkeit_verwendet and \
               hasattr(active_bird, 'ability_polygon') and \
               active_bird.ability_polygon is not None and \
               active_bird.ability_polygon.shape == wood_poly_shape:
                is_sahurs_bat_collision = True
        
        damage_amount = 0
        should_damage_pig = False

        if is_sahurs_bat_collision: # Sahur's bat is special
            # Sahur's bat hitting a pig: use a very low impulse threshold
            if arbiter.total_impulse.length > 10.0: # Minimal impulse to confirm "real" collision
                damage_amount = 1000 # Further increased from 750 for Sahur's bat
                should_damage_pig = True
        else: # Regular wood/poly collision
            # Regular wood/poly hitting a pig: use the standard higher impulse threshold
            if arbiter.total_impulse.length > ABILITY_COLLISION_IMPULSE_THRESHOLD: # e.g., 2000.0
                damage_amount = 60 # Further increased from 40 for regular polygon damage
                should_damage_pig = True
        
        if should_damage_pig and damage_amount > 0:
            for pig in pigs:
                if pig.shape == pig_shape:
                    pig.life -= damage_amount # Deal damage to pig
                    if pig.life <= 0:
                        pig_to_remove.append(pig)
                        global score
                        score += 10000
        for pig in pig_to_remove:
            space.remove(pig.shape, pig.body)
            pigs.remove(pig)

    def post_solve_bird_ground(arbiter, space, _):
        global birds # Access the list of active bird instances
        
        # Determine which shape is the bird (type 0) and which is the ground (type 3)
        bird_shape, ground_shape = arbiter.shapes
        if bird_shape.collision_type != 0: # Ensure shape_a is the bird
            bird_shape, ground_shape = ground_shape, bird_shape # Swap them
        
        if bird_shape.collision_type == 0 and ground_shape.collision_type == 3:
            colliding_bird_instance = None
            for b_instance in birds:
                if b_instance.shape == bird_shape:
                    colliding_bird_instance = b_instance
                    break
            
            if colliding_bird_instance:
                # Check if the ground shape's body is part of the static floor lines
                for ground_line in floor.static_lines:
                    if ground_line.body == ground_shape.body:
                        impact_velocity_reduction_threshold = 3000 # Threshold for hard hit
                        velocity_reduction_factor = 0.3 # How much to slow down
                        if arbiter.total_impulse.length > impact_velocity_reduction_threshold:
                            colliding_bird_instance.body.velocity *= (1 - velocity_reduction_factor*2)
                        colliding_bird_instance.bird_hit_ground = True
                        break # Found the ground, stop checking
                
    def post_solve_poly_vs_poly(arbiter, space, data):
        global columns, beams, circles, triangles, score, birds # Ensure all necessary globals are accessible

        shape_a, shape_b = arbiter.shapes
        
        poly_a_obj = None
        poly_b_obj = None
        
        # Ability polygons (bats/projectiles) are often stored in 'columns' list by character.py
        all_polys = columns + beams + circles + triangles
        for poly in all_polys:
            if poly.shape == shape_a:
                poly_a_obj = poly
            if poly.shape == shape_b:
                poly_b_obj = poly
            if poly_a_obj and poly_b_obj: # Found both
                break

        if not poly_a_obj or not poly_b_obj:
            # One or both shapes aren't our Polygon objects, bail.
            return

        # --- Part 1: Handle Active Special Ability Polygons (e.g., Sahur's Bat, Glorbo's Projectile) ---
        active_ability_item = None
        source_bird_for_ability = None

        if birds: # Check if there are active birds
            last_bird_launched = birds[-1] # The bird currently in play or last launched
            if last_bird_launched.fahigkeit_verwendet and \
            hasattr(last_bird_launched, 'ability_polygon') and \
            last_bird_launched.ability_polygon is not None:
                
                if poly_a_obj == last_bird_launched.ability_polygon:
                    active_ability_item = poly_a_obj
                    source_bird_for_ability = last_bird_launched
                elif poly_b_obj == last_bird_launched.ability_polygon:
                    active_ability_item = poly_b_obj
                    source_bird_for_ability = last_bird_launched
        
        elements_to_remove_from_ability_collision = []

        if active_ability_item:
            attacker_poly = active_ability_item # This is the ability item (e.g., bat, projectile)
            victim_poly = poly_b_obj if attacker_poly == poly_a_obj else poly_a_obj

            # Ability items (bats/projectiles) are typically STATIC. They damage DYNAMIC, non-"bats" polygons.
            # Also ensure victim_poly is not None (it should be caught by the initial check, but good practice)
            if victim_poly.body.body_type == pm.Body.DYNAMIC and victim_poly.element_type != "bats":
                damage_from_ability = 0
                apply_ability_damage = False
                score_for_ability_destroy = 1000

                if isinstance(source_bird_for_ability, ch.Sahur):
                    # Sahur's bat: very low impulse threshold for damage
                    if arbiter.total_impulse.length > 10.0:
                        damage_from_ability = 500 # Increased damage for Sahur's bat on polygons
                        apply_ability_damage = True
                elif isinstance(source_bird_for_ability, ch.Glorbo): # Glorbo's projectile (if any)
                    pass # Glorbo no longer has a damaging projectile, this path can be removed or left empty.
                
                if apply_ability_damage and damage_from_ability > 0:
                    victim_poly.life -= damage_from_ability
                    if victim_poly.life <= 0:
                        if victim_poly.in_space and victim_poly not in elements_to_remove_from_ability_collision:
                            elements_to_remove_from_ability_collision.append(victim_poly)
                            score += score_for_ability_destroy
                            
            for element in elements_to_remove_from_ability_collision:
                if element.in_space:
                    space.remove(element.shape, element.body)
                    element.in_space = False
                    if element in columns: columns.remove(element)
                    elif element in beams: beams.remove(element)
                    elif element in circles: circles.remove(element)
                    elif element in triangles: triangles.remove(element)
            return # Active ability collision handled, skip general poly-poly.

        # --- Part 2: Handle General Polygon-on-Polygon Collisions ---
        # This part executes if NEITHER poly_a_obj nor poly_b_obj is an ACTIVE ability item of the LATEST bird.
        elements_to_remove_from_general_collision = []
        impulse_strength = arbiter.total_impulse.length

        # Damage poly_a_obj if it's dynamic, not "bats", and impulse is high enough
        if poly_a_obj.body.body_type == pm.Body.DYNAMIC and poly_a_obj.element_type != "bats" and impulse_strength > POLY_POLY_COLLISION_IMPULSE_THRESHOLD:
            poly_a_obj.life -= POLY_POLY_DAMAGE_VALUE
            if poly_a_obj.life <= 0 and poly_a_obj.in_space and poly_a_obj not in elements_to_remove_from_general_collision:
                elements_to_remove_from_general_collision.append(poly_a_obj)
                score += POLY_DESTROY_SCORE
                
        # Damage poly_b_obj if it's dynamic, not "bats", and impulse is high enough
        if poly_b_obj.body.body_type == pm.Body.DYNAMIC and poly_b_obj.element_type != "bats" and impulse_strength > POLY_POLY_COLLISION_IMPULSE_THRESHOLD:
            poly_b_obj.life -= POLY_POLY_DAMAGE_VALUE
            if poly_b_obj.life <= 0 and poly_b_obj.in_space and poly_b_obj not in elements_to_remove_from_general_collision:
                elements_to_remove_from_general_collision.append(poly_b_obj)
                score += POLY_DESTROY_SCORE

        for element in elements_to_remove_from_general_collision:
            if element.in_space: # Check again before removal
                space.remove(element.shape, element.body)
                element.in_space = False
                if element in columns: columns.remove(element)
                elif element in beams: beams.remove(element)
                elif element in circles: circles.remove(element)
                elif element in triangles: triangles.remove(element)

    space.add_collision_handler(0, 1).post_solve = post_solve_bird_pig
    space.add_collision_handler(0, 2).post_solve = post_solve_bird_wood 
    space.add_collision_handler(1, 2).post_solve = post_solve_pig_wood
    space.add_collision_handler(0, 3).post_solve = post_solve_bird_ground 
    space.add_collision_handler(2, 2).post_solve = post_solve_poly_vs_poly # Polygon vs Polygon
    

    t1 = 0
    c = 0
    menu_open = False
    menu_open_time = 0
    menu_click_delay = 0.2  # seconds

    # game states:
    # 0:running
    # 5:paused
    # 3:lose
    # 4:win
    # 6:levels menu
    # Create and load the first level with the correct arguments
    level = Level(pigs, columns, beams, circles, triangles, space, screen_height, screen_width)
    level.load_level()

    def get_next_bird(mouse_distance, launch_angle, bird_x, bird_y, space, level):
        global bird
        if len(level.level_birds) > 0 :
            bird = level.level_birds[-1]
            if bird == "sahur":
                bird = ch.Sahur(mouse_distance, launch_angle, bird_x, bird_y, space, screen_height, screen_width, level)
            elif bird == "liri":
                bird = ch.Liri(mouse_distance, launch_angle, bird_x, bird_y, space, screen_height, screen_width, level)
            elif bird == "palocleves":
                bird = ch.Palocleves(mouse_distance, launch_angle, bird_x, bird_y, space, screen_height, screen_width, level)
            elif bird == "trala":
                bird = ch.Trala(mouse_distance, launch_angle, bird_x, bird_y, space, screen_height, screen_width, level)
            elif bird == "glorbo":
                bird = ch.Glorbo(mouse_distance, launch_angle, bird_x, bird_y, space, screen_height, screen_width, level)
            elif bird == "patapim":
                bird = ch.Patapim(mouse_distance, launch_angle, bird_x, bird_y, space, screen_height, screen_width, level)
            elif bird == "bomb":
                bird = ch.Bomb(mouse_distance, launch_angle, bird_x, bird_y, space, screen_height, screen_width, level)
            return bird
    
    def get_next_bird_img():
        pass
   
    def handle_resize(event):
        global slingl_scaled_width
        global slingl
        global slingr
        global slingl
        global slingl_scaled_height
        global slingr_scaled_width
        global slingr_scaled_height
        global levels_drawn
        nonlocal screen, screen_width, screen_height, scale_x, scale_y # bg is global, not nonlocal here
        # slingl, slingr are global, will be modified

        # Re-initialize in resizable mode with event dimensions
        screen = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
        
        # Update global screen dimensions and scaling factors
        screen_width, screen_height = event.w, event.h
        
        scale_x = screen_width / base_width
        scale_y = screen_height / base_height

        # Redraw the screen immediately after resize
        screen.fill((130, 200, 100)) # Or your bg color
        bg_scaled = pg.transform.scale(bg, (screen_width, screen_height))
        screen.blit(bg_scaled, (0, 0))

        # Rescale sling images using their current scaled design dimensions
        # These are the *design* dimensions, scale_size will apply current screen scaling
        slingl=pg.transform.scale(slingl, scale_size(slingl_scaled_width, slingl_scaled_height))
        slingr=pg.transform.scale(slingr, scale_size(slingr_scaled_width, slingr_scaled_height))
        # If in levels menu, need to redraw it
        if game_state == 6:
            levels_drawn = False
            draw_levels()
        pg.display.flip()

    while running:
        
        stop_button_rect = stop_button.get_rect(topleft=(8, 8))
        mouse_button_down = False  # Track if mouse button is pressed this frame
        

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                running = False
            elif event.type == pg.VIDEORESIZE:
                handle_resize(event)
            elif game_state == 0:
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_button_down = True # Flag it for this frame
                    print("mouse down")
                    

                elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                    mouse_button_down = False
                    x_mouse, y_mouse = event.pos # Capture mouse up position
                    if stop_button_rect.collidepoint(event.pos):
                        game_state = 5
                        menu_open = True
                        menu_open_time = time.time()
                    if mouse_pressed_to_shoot:
                        pu = scale_pos(140, 420)
                        mouse_pressed_to_shoot = False
                        # Launch a bird
                        if level.number_of_birds > 0:
                            level.number_of_birds -= 1
                            t1 = time.time() * 1000
                            sx, sy = sling_anchor

                            impulse_factor = 10.0
                            
                            
                            impulse_x = -mouse_distance * impulse_factor * math.cos(launch_angle)
                            impulse_y = mouse_distance * impulse_factor * math.sin(launch_angle)
                            
                            # Update bird starting position to align with sling
                            bird_x = sx
                            bird_y = sy - 180 # Adjust vertical offset (might need scaling)
                            bird_x, bird_y = bird_x, bird_y
                            #print(f"levlebirds: {level.level_birds}")
                            bird = get_next_bird(mouse_distance, launch_angle, bird_x, bird_y, space, level)
                            
                            birds.append(bird)
                            bird_path = []
                            level.level_birds.pop()
                                

                            if level.number_of_birds == 0:
                                t2 = time.time() # For timing or other logic if needed
                    else:
                        if birds: # Check if there's an active bird
                            active_bird = birds[-1]
                            
                            # Base condition: ability not yet used
                            can_use_ability = not active_bird.fahigkeit_verwendet
                            
                            # For non-Glorbo birds, they also must not have hit the ground
                            if not isinstance(active_bird, ch.Glorbo):
                                can_use_ability = can_use_ability and not active_bird.bird_hit_ground
                            
                            if can_use_ability:
                                active_bird.fahigkeit()
                                # Bird's fahigkeit() method handles setting its own 'fahigkeit_verwendet'
            elif game_state == 5:
                if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                    x_mouse, y_mouse = event.pos

                    if (10 + stop_button.get_width() > scale_x * x_mouse > 10 and
                            10 + stop_button.get_height() > scale_y * y_mouse > 10):
                        game_state = 0

                    elif (80 + replay_button.get_width() > scale_x * x_mouse > 80 and
                        170 + replay_button.get_height() > scale_y * y_mouse > 190):
                        restart()
                        level.load_level()
                        game_state = 0
                        bird_path = []
                        score = 0

                    elif (105 + menu_button.get_width() > scale_x * x_mouse > 105 and
                        307 + menu_button.get_height() > scale_y * y_mouse > 307):
                        game_state = 6
                        levels_drawn = False

                    elif (60 + sound_button.get_width() > scale_x * x_mouse > 55 and
                        565 + sound_button.get_height() > scale_y * y_mouse > 565):
                        sound_on = not sound_on

            elif game_state == 4:
                if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                    x_mouse, y_mouse = event.pos

                    if (665 + next_button.get_width() > scale_x * x_mouse > 665 and
                            480 + next_button.get_height() > scale_y * y_mouse > 480):
                        restart()
                        level.number += 1
                        game_state = 0
                        level.load_level()
                        score = 0
                        bird_path = []
                        bonus_score_once = True

                    elif (559 + replay_button.get_width() > scale_x * x_mouse > 559 and
                        486 + replay_button.get_height() > scale_y * y_mouse > 486):
                        restart()
                        level.load_level()
                        game_state = 0
                        bird_path = []
                        score = 0

                    elif (452 + menu_button.get_width() > scale_x * x_mouse > 452 and
                        490 + menu_button.get_height() > scale_y * y_mouse > 490):
                        game_state = 6
                        levels_drawn = False

            elif game_state == 3:
                if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                    x_mouse, y_mouse = event.pos

                    if (559 + replay_button.get_width() > scale_x * x_mouse > 559 and
                            486 + replay_button.get_height() > scale_y * y_mouse > 486):
                        restart()
                        level.load_level()
                        game_state = 0
                        bird_path = []
                        score = 0

                    elif (452 + menu_button.get_width() > scale_x * x_mouse > 452 and
                        490 + menu_button.get_height() > scale_y * y_mouse > 490):
                        game_state = 6
                        levels_drawn = False

            elif game_state == 6:
                
                
                    if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                        x_mouse, y_mouse = event.pos
                        level_icon_rect = level_icon.get_rect()
                        x_offset, y_offset = 100, 50
                        for i in range(21):
                            icon_x = x_offset + (i % 7) * 151
                            icon_y = y_offset + (i // 7) * 160
                            icon_x,icon_y = scale_pos(icon_x,icon_y)
                            current_icon_rect = level_icon_rect.move(icon_x, icon_y)
                            level_number = i + 1
                            level_method_name = f"build_{level_number}" # Korrigierter Methodenname
                            if current_icon_rect.collidepoint(x_mouse, y_mouse):
                                
                                with open("cleared_levels.txt","r+") as f:
                                    if str(level_number) in [line.rstrip("\n") for line in f.readlines()]:
                                        restart()
                                        level_loader = getattr(level, level_method_name, None)
                                        if level_loader:
                                            level_loader()
                                            game_state = 0
                                            levels_drawn = False
                                            bird_path = []
                                            score = 0
                                            bonus_score_once = True
                                            break
                        b_size_scaled = scale_size(menu_button.get_width(),menu_button.get_height()) # Scaled menu button
                        if (101 + b_size_scaled[0] > x_mouse > 101 and
                                51 + b_size_scaled[1] > y_mouse > 51):
                            game_state = 0
                            levels_drawn = False

        if game_state == 0:
            #print(level.level_birds)
            #print(birds)
            try:
                bird_img = pg.transform.scale(pg.transform.scale(pg.image.load(load_resource(f"./resources/images/{level.level_birds[-1]}.png")).convert_alpha(),(30,30)),scale_size(30,30))
            except IndexError as e:
                pass
                
            menu_open = False
            screen.fill((130, 200, 100))
            bg_scaled = pg.transform.scale(bg, (screen_width, screen_height))
            screen.blit(bg_scaled, (0, 0))

            x_mouse, y_mouse = pg.mouse.get_pos()
            if pg.mouse.get_pressed()[0] and (110 * scale_x < x_mouse < 170 * scale_x and 250 * scale_y < y_mouse < 400 * scale_y):
                mouse_pressed_to_shoot = True

            # screen.blit(slingr, scale_pos(130, 400)) # Example of old/debug code?
            
            # Draw birds waiting behind the sling
            if level.number_of_birds > 0: # If there are birds left to shoot
                #print(level.number_of_birds,level.level_birds)
                for i in range(level.number_of_birds-1):
                    print(i)
                    
                    bird_type = level.level_birds[-i-2]
                    try:
                        bird_behind_img = pg.transform.scale(pg.transform.scale(pg.image.load(load_resource(f"./resources/images/{bird_type}.png")).convert_alpha(),(30,30)),scale_size(30,30))
                        
                        x_position = 100 - i * 35
                        screen.blit(bird_behind_img, scale_pos(x_position, 445))
                        #print(scale_pos(0,435))
                    except FileNotFoundError:
                        print(f"Error: Bird image not found for {bird_type}")
            if mouse_pressed_to_shoot and level.number_of_birds > 0:
                sling_action() # Handles drawing bird in stretched sling
                
            # Draw bird in the sling if ready (not being dragged)
            elif level.number_of_birds > 0: # Bird is waiting in sling
                slingl_x, slingl_y = get_sling_positions()
                slingr_x, slingr_y = get_sling_positions()
                screen.blit(bird_img, scale_pos(130, 370))
                
                
                
                screen.blit(slingl, (slingl_x, slingl_y))
                screen.blit(slingr, (slingr_x, slingr_y))
            else: # No birds left, draw empty sling
                default_x = 140 * scale_x
                default_y = 420 * scale_y
                slingl_x, slingl_y = get_sling_positions()
                slingr_x, slingr_y = get_sling_positions()
                pg.draw.line(screen, (0, 0, 0), (slingr_x + 4 * scale_x, slingr_y + 3 * scale_y), (default_x, default_y), 5)
                pg.draw.line(screen, (0, 0, 0), (slingl_x + 2 * scale_x, slingl_y + 13 * scale_y), (default_x, default_y), 5)

            bird_to_remove = []
            pig_to_remove = []


            # Track bird path
            for bird in birds:                
                p = to_pygame(bird.shape.body.position)
                x, y = p
                angle_degree = math.degrees(bird.shape.body.angle)
                
                # Get bird's base design size (e.g., 30x30, 50x50)
                base_design_width = bird.scale[0]
                base_design_height = bird.scale[1]

                # --- Glorbo's visual growth effect ---
                current_bird_visual_scale_multiplier = 1.0 # Default for other birds or inactive Glorbo
                if isinstance(bird, ch.Glorbo) and bird.is_ability_visually_active:
                    if bird.is_growing: # Visual grows with physical
                        time_since_activation = time.time() - bird.ability_activation_time
                        growth_progress = min(time_since_activation / bird.growth_duration, 1.0)
                        
                        bird.current_visual_scale_multiplier = bird.initial_visual_scale + \
                            (bird.ability_visual_scale_multiplier - bird.initial_visual_scale) * growth_progress
                        current_bird_visual_scale_multiplier = bird.current_visual_scale_multiplier
                    elif bird.fahigkeit_verwendet: # If grown and ability used, keep large size
                        current_bird_visual_scale_multiplier = bird.ability_visual_scale_multiplier
                    # else: if ability not active, it remains 1.0 (default)
                                
                # Final pixel size for the bird, including screen scaling
                # Formula: (DesignSize * VisualMultiplier) * ScreenScale
                final_pixel_width = int(base_design_width * current_bird_visual_scale_multiplier * scale_x)
                final_pixel_height = int(base_design_height * current_bird_visual_scale_multiplier * scale_y)

                # Load fresh image for best scaling quality
                original_bird_surface = pg.image.load(load_resource(bird.img)).convert_alpha()
                
                # Scale it
                scaled_bird_surface = pg.transform.scale(original_bird_surface, (final_pixel_width, final_pixel_height))
                
                # And rotate
                rotated_image = pg.transform.rotate(scaled_bird_surface, angle_degree)

                # --- Glorbo's physics growth (hitbox, mass) ---
                if isinstance(bird, ch.Glorbo) and bird.is_growing:
                    time_since_activation = time.time() - bird.ability_activation_time # Reuse time_since_activation
                    growth_progress = min(time_since_activation / bird.growth_duration, 1.0)

                    # Target physical radius based on visual scale
                    # Visual "radius" is half its design width
                    initial_visual_design_radius = bird.scale[0] / 2.0
                    desired_target_physical_radius = initial_visual_design_radius * bird.ability_visual_scale_multiplier
                    
                    # Lerp physical radius
                    # initial_physical_radius was Pymunk radius at activation
                    current_physical_radius = bird.initial_physical_radius + \
                                              (desired_target_physical_radius - bird.initial_physical_radius) * growth_progress
                    
                    # Mass scales with area (multiplier^2)
                    target_mass = bird.initial_mass * (bird.ability_visual_scale_multiplier ** 2)
                    current_mass = bird.initial_mass + (target_mass - bird.initial_mass) * growth_progress
                    bird.shape.unsafe_set_radius(current_physical_radius)
                    bird.body.mass = current_mass
                    bird.body.moment = pm.moment_for_circle(current_mass, 0, current_physical_radius, (0,0)) # Update moment of inertia
                    space.reindex_shape(bird.shape)

                    if growth_progress >= 1.0:
                        bird.is_growing = False
                        # Ensure final values are set precisely
                        bird.shape.unsafe_set_radius(desired_target_physical_radius)
                        bird.body.mass = target_mass # target_mass is already the final desired mass
                        bird.body.moment = pm.moment_for_circle(target_mass, 0, desired_target_physical_radius, (0,0)) # Final moment
                        space.reindex_shape(bird.shape) # Reindex shape one last time
                
                # Offset for blitting rotated image
                offset = Vec2d(*rotated_image.get_size()) / 2
                blit_x = p[0] - offset[0] # Blit using scaled center x
                blit_y = p[1] - offset[1] # Blit using scaled center y
                
                if not bird.bird_hit_ground: # Add to trail if bird hasn't hit ground
                    bird_path.append(p) # p is already scaled center
                
                screen.blit(rotated_image, (blit_x, blit_y))
                
                if (bird.body.position.y < 0 or bird.body.position.x < -50 or
                        bird.body.position.x > screen_width + 50):
                    #print(f"bird removed (out of bounds): {bird.body.position}")
                    bird_to_remove.append(bird)
                

                current_time = time.time() * 1000
                if current_time - bird.launch_time > 7000:  # Birds live for 7 secs
                    bird_to_remove.append(bird)
                    bird_path = []  # Clear trail if this bird is removed due to timeout

            #for bird_to_remove in bird_to_remove:
            #    if bird_to_remove in birds: # Check if the bird is still in the list
            #        space.remove(bird_to_remove.shape, bird_to_remove.body)
            #        birds.remove(bird_to_remove)

            # Draw bird path
            for i, point in enumerate(bird_path):
                if i % 5 == 0:  # Draw every 5th stored point
                    # 'point' is already a scaled tuple (x, y) from to_pygame
                    pg.draw.circle(screen, WHITE, point, 3) # Draw the trail dot

            # Clean up birds marked for removal
            # Iterate a copy if modifying the list, or clear original at end.
            processed_birds_this_frame = list(bird_to_remove) # Copy to iterate safely
            bird_to_remove.clear() # Clear original for next frame

            for bird_instance_to_remove in processed_birds_this_frame:
                # Sahur's bat cleanup
                if isinstance(bird_instance_to_remove, ch.Sahur) and \
                   hasattr(bird_instance_to_remove, 'ability_polygon') and bird_instance_to_remove.ability_polygon:
                    poly_to_remove = bird_instance_to_remove.ability_polygon
                    if poly_to_remove in columns:
                        # Only remove from Pymunk if it's there
                        if poly_to_remove.shape and poly_to_remove.shape in space.shapes:
                            space.remove(poly_to_remove.shape, poly_to_remove.body)
                            poly_to_remove.in_space = False # Keep our 'in_space' flag consistent
                        columns.remove(poly_to_remove)
                    bird_instance_to_remove.ability_polygon = None

                # Glorbo: no ability polygon to clean

                # Remove the bird object
                if bird_instance_to_remove in birds: # Double check it's still in birds list
                    if bird_instance_to_remove.body and bird_instance_to_remove.shape:
                        space.remove(bird_instance_to_remove.shape, bird_instance_to_remove.body)
                    birds.remove(bird_instance_to_remove)
            
            if processed_birds_this_frame: # If birds were removed, clear the trail
                bird_path = []

            for pig in pigs:
                if pig.shape.body.position.y < 0:
                    pig_to_remove.append(pig)
                    # print(pigs) # debug
            
            for pig in pig_to_remove:
                space.remove(pig.body)
                pigs.remove(pig) # also remove from our list

            for line in floor.static_lines:
                body = floor.static_body
                pv1 = body.position + line.a.rotated(body.angle)
                pv2 = body.position + line.b.rotated(body.angle)
                p1 = to_pygame(pv1)
                p2 = to_pygame(pv2)
                pg.draw.lines(screen, TRANSP, False, [p1, p2]) # Draw transparent floor line (for debug?)

            for pig in pigs:
                pig_to_remove = []
                pigg=pig
                pig = pig.shape
                p = to_pygame(pig.body.position)
                x, y = p
                angle_degree = math.degrees(pig.body.angle)
                
                if pigg.type == "n11":
                    if pigg.life == 50: # Full health image
                        pig_img = pg.transform.scale(n11,(pigg.radius*2,pigg.radius*2))
                    else: # Damaged image
                        pig_img = pg.transform.scale(n12,(pigg.radius*2,pigg.radius*2))
                
                elif pigg.type == "n21":
                    if pigg.life == 50:
                        pig_img = pg.transform.scale(n21,(pigg.radius*2,pigg.radius*2))
                    else:
                        pig_img = pg.transform.scale(n22,(pigg.radius*2,pigg.radius*2))
                        
                elif pigg.type == "n31":
                    if pigg.life == 50:
                        pig_img = pg.transform.scale(n31,(pigg.radius*2,pigg.radius*2))
                    else:
                        pig_img = pg.transform.scale(n32,(pigg.radius*2,pigg.radius*2))
                        
                elif pigg.type == "n41":
                    if pigg.life == 50:
                        pig_img = pg.transform.scale(n41,(pigg.radius*2,pigg.radius*2))
                    else:
                        pig_img = pg.transform.scale(n42,(pigg.radius*2,pigg.radius*2))
                        
                if pigg.type == "n51":
                    if pigg.life == 50:
                        pig_img = pg.transform.scale(n51,(pigg.radius*2,pigg.radius*2))
                    else:
                        pig_img = pg.transform.scale(n52,(pigg.radius*2,pigg.radius*2))
                
                pig_img = pg.transform.rotate(pig_img, angle_degree)
                width, height = pig_img.get_size()
                rotated_image = pg.transform.rotate(pig_img, angle_degree)
                offset = Vec2d(*rotated_image.get_size()) / 2
                x -= offset[0]
                y -= offset[1]
                img_x, img_y = p[0]-width/2, p[1]-height/2
                screen.blit(rotated_image, (x, y))
                #pg.draw.circle(screen, BLUE, p, int(pig.radius), 2)
                if (pig.body.position.y < 0 or pig.body.position.x < -50 or
                        pig.body.position.x > screen_width + 50):
                    #print(f"Pig removed: {pig.body.position}")
                    pig_to_remove.append(pig)
                
            # Update bat position before drawing if Sahur's ability is active
            active_special_bird_instance = None # Will hold Sahur/Glorbo if ability active
            current_sahur_ability_polygon = None

            if birds: # Any active birds?
                last_bird = birds[-1] # Current bird in flight
                if last_bird.fahigkeit_verwendet: # Is its ability active?
                    if isinstance(last_bird, ch.Sahur):
                        active_special_bird_instance = last_bird
                        # Sahur's bat is stored in ability_polygon
                        if hasattr(last_bird, 'ability_polygon') and last_bird.ability_polygon:
                            current_sahur_ability_polygon = last_bird.ability_polygon
                    elif isinstance(last_bird, ch.Glorbo):
                        # Glorbo's ability is growth/stop
                        active_special_bird_instance = last_bird

            for column in columns:
                # Sahur's bat logic
                if column.element_type == "bats" and \
                   active_special_bird_instance and \
                   isinstance(active_special_bird_instance, ch.Sahur):
                        # Animation duration for bat swing & lifetime
                        animation_duration = 0.25 # Swing/lifetime is 0.25s

                        # Bat lifetime check for Sahur
                        if hasattr(active_special_bird_instance, 'ability_polygon_creation_time') and \
                           active_special_bird_instance.ability_polygon == column: # Is this Sahur's current bat?
                            bat_age = time.time() - active_special_bird_instance.ability_polygon_creation_time
                            if bat_age > animation_duration: 
                                if column.body and column.shape: # Check body/shape exist before Pymunk removal
                                    if column.shape in space.shapes: # Is it still in Pymunk space?
                                        space.remove(column.shape, column.body)
                                column.in_space = False # Mark Polygon as removed for our game logic
                                if column in columns: # Still in 'columns' list?
                                    columns.remove(column)
                                active_special_bird_instance.ability_polygon = None
                                current_sahur_ability_polygon = None # Bat gone, nullify ref for this frame
                                continue # Bat expired, skip rest of its logic

                        # If bat still alive, update its position
                        if active_special_bird_instance.ability_polygon == column: # Double check it wasn't just timed out
                            new_x = active_special_bird_instance.body.position.x + 50
                            new_y = active_special_bird_instance.body.position.y
                            column.body.position = Vec2d(new_x, new_y)

                            # Sahur's bat swing animation
                            bat_creation_time = active_special_bird_instance.ability_polygon_creation_time
                            current_time_for_swing = time.time() # Consistent time for age calc
                            bat_age_for_swing = current_time_for_swing - bat_creation_time
                            
                            # animation_duration defined earlier
                            start_angle_deg = 160.0 # Bat starts at 160 deg
                            end_angle_deg = 20.0   # Swings to 20 deg

                            if bat_age_for_swing <= animation_duration:
                                progress = min(bat_age_for_swing / animation_duration, 1.0) # Ensure progress doesn't exceed 1.0
                                current_angle_deg = start_angle_deg + (end_angle_deg - start_angle_deg) * progress
                                column.body.angle = math.radians(current_angle_deg)
                            # else: The bat will be at end_angle_deg when it's about to be removed by the timer.

                            if column.shape: # Reindex if shape exists
                                space.reindex_shape(column.shape)

                if column.in_space: # Only draw if not removed by timer/collision
                    column.draw_poly(screen, column.shape)
            # Draw other polygons        
            for beam in beams:
                beam.draw_poly(screen,beam.shape)
            for circle in circles:
                circle.draw_poly(screen,circle.shape)
                
            for triangle in triangles:
                triangle.draw_poly(screen,triangle.shape)

            dt = 1.0 / 50.0 / 2.0 # physics simulation step
            for x in range(2):
                space.step(dt)
            slingl_x, slingl_y = get_sling_positions()
            slingr_x, slingr_y = get_sling_positions()
            screen.blit(slingl, (slingl_x, slingl_y))
            screen.blit(slingr, (slingr_x, slingr_y))

            score_font = bold_font.render("SCORE", 1, WHITE)
            number_font = bold_font.render(str(score), 1, WHITE)

            screen.blit(score_font, scale_pos(1060, 90))
            if score == 0:
                screen.blit(number_font, scale_pos(1150, 130))
            else:
                screen.blit(number_font, scale_pos(1060, 130))

            screen.blit(stop_button, scale_pos(8, 8))

            if not pigs and not mouse_pressed_to_shoot and not restart_counter and not birds:
                print("Level cleared! Setting game_state to 4")
                game_state = 4
                restart_counter = True

            if level.number_of_birds < 0 and pigs and not birds:
                game_state = 3

        elif game_state == 5:
            menu_open = True
            if sound_on:
                screen.blit(menu_son, scale_pos(0, 0))
            else:
                screen.blit(menu_sof, scale_pos(0, 0))

        elif game_state == 4:
            #print(level.number)
            with open("cleared_levels.txt","r+") as f:
                if str(level.number+1) not in [line.rstrip("\n") for line in f.readlines()]:
                    f.write(f"{str(level.number+1)}\n")
                    print(f"written {level.number+1}")
                    
            level_cleared = bold_font3.render("Level cleared!", 1, WHITE)
            score_level_cleared = bold_font2.render(str(score), 1, WHITE)
            if level.number_of_birds >= 0 and not pigs and bonus_score_once:
                score += (level.number_of_birds) * 10000
                bonus_score_once = False

            # Centered purple background rect
            center_x = screen_width // 2
            center_y = screen_height // 2
            rect_width = min(screen_width * 0.8, 600)  # Width: 80% screen or 600px max
            rect_height = screen_height  # Height: full screen or a fixed value like 650px
            
            rect = pg.Rect(
                center_x - rect_width // 2,  # Center X
                center_y - rect_height // 2,  # Center Y
                rect_width,
                rect_height
            )
            pg.draw.rect(screen, (BLACK), rect)
            screen.blit(level_cleared, scale_pos(450, 90)) # "Level Cleared!" text

            if score >= level.one_star:
                screen.blit(star1, scale_pos(370, 190))
            if score >= level.two_star:
                screen.blit(star1, scale_pos(440, 140)) # Changed star2 to star1
            if score >= level.three_star:
                screen.blit(star1, scale_pos(660, 190)) # Changed star3 to star1

            screen.blit(score_level_cleared, scale_pos(555, 400)) # Display score
            screen.blit(replay_button, scale_pos(555, 480))
            screen.blit(next_button, scale_pos(665, 480))
            screen.blit(menu_button, scale_pos(445, 480))

        elif game_state == 3:
            level_failed = bold_font3.render("Level failed!", 1, WHITE)
            score_level_failed = bold_font2.render(str(score), 1, WHITE)

            # Centered background for fail screen
            center_x = screen_width // 2
            center_y = screen_height // 2
            rect_width = min(screen_width * 0.8, 600)
            rect_height = screen_height
            
            rect = pg.Rect( # Define the rectangle
                center_x - rect_width // 2,  # Center horizontally
                center_y - rect_height // 2,  # Center vertically
                rect_width,
                rect_height
            )
            pg.draw.rect(screen, (BLACK), rect)
            screen.blit(level_failed, scale_pos(450, 90))
            # Display stars earned, even on fail
            if score >= level.one_star:
                screen.blit(star1, scale_pos(370, 190))
            if score >= level.two_star:
                screen.blit(star1, scale_pos(440, 140)) # Changed star2 to star1
            if score >= level.three_star:
                screen.blit(star1, scale_pos(660, 190)) # Changed star3 to star1

            screen.blit(score_level_failed, scale_pos(555, 400)) # Show score
            screen.blit(replay_button, scale_pos(555, 480))
            screen.blit(menu_button, scale_pos(445, 480))

        elif game_state == 6:
            def draw_levels():
                global levels_drawn
            
                print("Drawing levels")
                num_levels = 21
                screen.blit(pg.transform.scale(bg, (screen_width, screen_height)), scale_pos(0, 0))
                    
                # Base pos & spacing for level icons
                base_x = 100
                base_y = 50
                base_spacing_x = 151
                base_spacing_y = 160
                levels_per_row = 7
                
                # Scale icons to screen size
                icon_width = int(100 * scale_x)
                icon_height = int(100 * scale_y)
                level_icon_scaled = pg.transform.scale(level_icon, (icon_width, icon_height))
                locked_icon_scaled = pg.transform.scale(locked_level_icon, (icon_width, icon_height))
                level_icon_rect = level_icon_scaled.get_rect()

                for i in range(num_levels):
                    level_number = i + 1
                    level_method_name = f"build_{level_number}"
                    
                    # Scaled position for each icon
                    row = i // levels_per_row
                    col = i % levels_per_row
                    x = base_x + (col * base_spacing_x)
                    y = base_y + (row * base_spacing_y)
                    x, y = scale_pos(x, y)

                    # Locked or unlocked icon
                    if getattr(level, level_method_name, None):
                        with open("cleared_levels.txt","r+") as f:
                            if str(level_number) in [line.rstrip("\n") for line in f.readlines()]:
                                icon = level_icon_scaled # Unlocked
                            else:
                                icon = locked_icon_scaled # Locked
                    else:
                        icon = locked_icon_scaled

                    # Scale level number text
                    level_text = str(level_number)
                    level_font = bold_font3.render(level_text, 1, WHITE)
                    text_rect = level_font.get_rect(center=level_icon_rect.center)
                    
                    # Draw icon & its number
                    screen.blit(icon, (x, y))
                    if getattr(level, level_method_name, None):
                        with open("cleared_levels.txt","r+") as f:
                            if str(level_number) in [line.rstrip("\n") for line in f.readlines()]:
                                screen.blit(level_font, (x + text_rect.x, y + text_rect.y))

                # Menu button scaling/pos (currently commented out from blitting)
                menu_button_scaled = pg.transform.scale(menu_button, 
                    (int(menu_button.get_width() * scale_x), 
                    int(menu_button.get_height() * scale_y)))
                menu_x, menu_y = scale_pos(101, 51)
                #screen.blit(menu_button_scaled, (menu_x, menu_y))
                levels_drawn = True
                
            if not levels_drawn:
                draw_levels()
            #levels_drawn = True
            
            
        # start menu
        elif game_state == 7: # Main Menu
            #print(pigs)
            
            level_loader = getattr(level, "build_0", None)
            if level_loader and not loaded:
                level_loader()
                loaded=True
                
            try:
                # Random bird image for menu background?
                bird_img = pg.transform.scale(pg.transform.scale(pg.image.load(load_resource(f"./resources/images/{level.level_birds[random.randint(0,level.number_of_birds)]}.png")).convert_alpha(),(30,30)),scale_size(30,30))
            except IndexError as e:
                pass
            
            screen.blit(pg.transform.scale(bg, (screen_width, screen_height)), scale_pos(0, 0))
                
            
            # Click play button
            x_mouse, y_mouse = pg.mouse.get_pos()
            if pg.mouse.get_pressed()[0] and (478 * scale_x < x_mouse < 711 * scale_x and 247 * scale_y < y_mouse < 400 * scale_y):
                game_state = 6

            
            
            
                
            
            # Background birds animation for menu
            for bird in birds:
                bird_to_remove = []
                
                
                p = to_pygame(bird.shape.body.position)
                x, y = p
                angle_degree = math.degrees(bird.shape.body.angle)
                #print(angle_degree)
                
                
                bird_img = pg.transform.scale(pg.image.load(bird.img), (bird.scale[0]*scale_x, bird.scale[1]*scale_y))
                bird_img = pg.transform.rotate(bird_img, angle_degree)
                width, height = bird_img.get_size()
                rotated_image = pg.transform.rotate(bird_img, angle_degree)
                offset = Vec2d(*rotated_image.get_size()) / 2
                x -= offset[0]
                y -= offset[1]
                img_x, img_y = p[0]-width/2, p[1]-height/2
                screen.blit(rotated_image, (x, y))
                #pg.draw.circle(screen, BLUE, p, int(bird.radius), 2)
                if (bird.body.position.y < 0 or bird.body.position.x < -50 or
                        bird.body.position.x > screen_width + 50):
                    #print(f"bird removed: {bird.body.position}")
                    bird_to_remove.append(bird)
                    
                bird_path.append((img_x, img_y))  # Store original coordinates for trail
                
                

            

            
            
            pig_to_remove = []
            for pig in pig_to_remove:
                
                space.remove(pig.body)
                pigs.remove(pig)

            for line in floor.static_lines: # Draw floor (transparent, so for debug?)
                body = floor.static_body
                pv1 = body.position + line.a.rotated(body.angle)
                pv2 = body.position + line.b.rotated(body.angle)
                p1 = to_pygame(pv1)
                p2 = to_pygame(pv2)
                pg.draw.lines(screen, TRANSP, False, [p1, p2])

            for pig in pigs: # Draw pigs for menu background
                pig_to_remove = []
                pigg=pig
                pig = pig.shape
                p = to_pygame(pig.body.position)
                x, y = p
                angle_degree = math.degrees(pig.body.angle)
                
                if pigg.type == "n11":
                    if pigg.life == 30: # Using 30 as full health for menu?
                        pig_img = pg.transform.scale(n11,(pigg.radius*2,pigg.radius*2))
                    else:
                        pig_img = pg.transform.scale(n12,(pigg.radius*2,pigg.radius*2))
                
                elif pigg.type == "n21":
                    if pigg.life == 30: 
                        pig_img = pg.transform.scale(n21,(pigg.radius*2,pigg.radius*2))
                    else:
                        pig_img = pg.transform.scale(n22,(pigg.radius*2,pigg.radius*2))
                        
                elif pigg.type == "n31":
                    if pigg.life == 30: 
                        pig_img = pg.transform.scale(n31,(pigg.radius*2,pigg.radius*2))
                    else:
                        pig_img = pg.transform.scale(n32,(pigg.radius*2,pigg.radius*2))
                        
                elif pigg.type == "n41":
                    if pigg.life == 30: 
                        pig_img = pg.transform.scale(n41,(pigg.radius*2,pigg.radius*2))
                    else:
                        pig_img = pg.transform.scale(n42,(pigg.radius*2,pigg.radius*2))
                        
                if pigg.type == "n51":
                    if pigg.life == 30: 
                        pig_img = pg.transform.scale(n51,(pigg.radius*2,pigg.radius*2))
                    else:
                        pig_img = pg.transform.scale(n52,(pigg.radius*2,pigg.radius*2))
                
                pig_img = pg.transform.rotate(pig_img, angle_degree)
                width, height = pig_img.get_size()
                rotated_image = pg.transform.rotate(pig_img, angle_degree)
                offset = Vec2d(*rotated_image.get_size()) / 2
                x -= offset[0]
                y -= offset[1]
                img_x, img_y = p[0]-width/2, p[1]-height/2
                screen.blit(rotated_image, (x, y))
                #pg.draw.circle(screen, BLUE, p, int(pig.radius), 2)
                if (pig.body.position.y < 0 or pig.body.position.x < -50 or
                        pig.body.position.x > screen_width + 50):
                    #print(f"Pig removed: {pig.body.position}")
                    pig_to_remove.append(pig) # Remove if off-screen
                if len(pigs) > 50:
                    pigs.remove(pigs[0]) # Limit number of pigs in menu
                #print(len(pigs))
                
            dt = 1.0 / 50.0 / 2.0 # Physics step for menu animations
            for x in range(2):
                # print("space.step called for menu")
                space.step(dt)
    
            screen.blit(play_button,(screen_width/2-play_button.get_width()/2,screen_height/2-play_button.get_height()/2))

            
        pg.display.flip()
        clock.tick(60)

        

    pg.quit()
    sys.exit()

main_loop()