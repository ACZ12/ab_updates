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
from Polygon import Static_line

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



def main_loop():
    
    # GLOBALS
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

    def handle_resize(event):
        global slingl, slingr, slingl_scaled_width, slingl_scaled_height, slingr_scaled_width, slingr_scaled_height
        global levels_drawn
        nonlocal screen, screen_width, screen_height, scale_x, scale_y
        
        # Update screen and scaling factors
        screen = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
        screen_width, screen_height = event.w, event.h
        scale_x = screen_width / base_width
        scale_y = screen_height / base_height

        # Redraw the screen immediately after resize
        screen.fill((130, 200, 100))
        bg_scaled = pg.transform.scale(bg, (screen_width, screen_height))
        screen.blit(bg_scaled, (0, 0))
        #print("Resizing bg")
        
        # Rescale sling images
        slingl = pg.transform.scale(slingl, scale_size(slingl_scaled_width, slingl_scaled_height))
        slingr = pg.transform.scale(slingr, scale_size(slingr_scaled_width, slingr_scaled_height))
        
        if game_state == 6:
            #print("Resizing levels")
            levels_drawn = False
            draw_levels()
        pg.display.flip()

    bold_font = pg.font.SysFont("arial", 20, bold=True)
    bold_font2 = pg.font.SysFont("arial", 30, bold=True)
    bold_font3 = pg.font.SysFont("arial", 50, bold=True)
    
    bird_scale_factor = 0.3
    pig_scale_factor = 1
    star13_scale_factor = 0.5
    star2_scale_factor = 1


    def load_resource(path):
        """Gets the absolute path to a resource, handling both bundled and unbundled."""
        if hasattr(sys, '_MEIPASS'):
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            return os.path.join(sys._MEIPASS, path)
        else:
            # We are running in a regular Python environment
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
    slingl_scaled_width = int(slingl.get_width() * 0.135)
    slingl_scaled_height = int(slingl.get_height() * 0.135)
    slingr_scaled_width = int(slingr.get_width() * 0.05)
    slingr_scaled_height = int(slingr.get_height() * 0.05)
    
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
        a = p1[0] - p0[0]
        b = p1[1] - p0[1]
        return a, b

    def unit_vector(v):
        h = ((v[0] ** 2 + (v[1] ** 2)) ** 0.5)
        if h == 0:
            h = 0.000000000000001
        ua = v[0] / h
        ub = v[1] / h
        return ua, ub

    def distance(x0, y0, x, y):
        dx = x - x0
        dy = y - y0
        d = ((dx ** 2) + (dy ** 2)) ** 0.5
        return d

    def sling_action(): # change pos of sling
        global launch_angle
        global x_mouse
        global y_mouse
        global impulse_x
        global impulse_y
        global sling_anchor
        global mouse_distance
        global pu

        sx, sy = scale_pos(*sling_anchor)
        mx, my = x_mouse, y_mouse

        v = vector((sx, sy), (mx, my))
        uv = unit_vector(v)
        uv1 = uv[0]
        uv2 = uv[1]

        mouse_distance_raw = distance(sx, sy, mx, my)

        if mouse_distance_raw > rope_length:
            mouse_distance = rope_length
            pu = uv1 * rope_length + sx, uv2 * rope_length + sy
            x_sahur = pu[0] - sahur.get_width() // 2
            y_sahur = pu[1] - sahur.get_height() // 2

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

            if len(level.level_birds) >= 0:

                screen.blit(bird_img, (x_sahur, y_sahur))
                slingl_x, slingl_y = get_sling_positions()
                slingr_x, slingr_y = get_sling_positions()
                pg.draw.line(screen, (0, 0, 0), (slingr_x + 4 * scale_x, slingr_y + 3 * scale_y), (mx, my), 5)
                pg.draw.line(screen, (0, 0, 0), (slingl_x + 2 * scale_x, slingl_y + 13 * scale_y), (mx, my), 5)

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
        pigs_to_remove = []
        birds_to_remove = []
        columns_to_remove = []
        beams_to_remove = []
        circles_to_remove = []
        triangles_to_remove = []

        for pig in pigs:
            pigs_to_remove.append(pig)
        for pig in pigs_to_remove:
            space.remove(pig.shape, pig.shape.body)
            pigs.remove(pig)

        for bird in birds:
            birds_to_remove.append(bird)

        for bird in birds_to_remove:
            space.remove(bird.shape, bird.shape.body)
            birds.remove(bird)

        for column in columns:
            columns_to_remove.append(column)
        for column in columns_to_remove:
            space.remove(column.shape, column.shape.body)
            columns.remove(column)

        for beam in beams:
            beams_to_remove.append(beam)
        for beam in beams_to_remove:
            space.remove(beam.shape, beam.shape.body)
            beams.remove(beam)
            
        for circle in circles:
            circles_to_remove.append(circle)
        for circle in circles_to_remove:
            space.remove(circle.shape, circle.shape.body)
            circles.remove(circle)

        for triangle in triangles:
            triangles_to_remove.append(triangle)
        for triangle in triangles_to_remove:
            space.remove(triangle.shape, triangle.shape.body)
            triangles.remove(triangle)

    def post_solve_bird_pig(arbiter, space, _):
        a, b = arbiter.shapes
        bird_body = a.body
        pig_body = b.body
        bird_momentum = bird_body.mass * bird_body.velocity.length
        base_damage = 0
        momentum_damage_factor = 0.33
        damage = base_damage + (bird_momentum * momentum_damage_factor)

        pig_to_remove = []
        for pig in pigs:
            if pig.body == pig_body and bird_momentum > 25:
                pig.life -= damage
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
        bird_momentum = bird_body.mass * bird_body.velocity.length # Calculate bird momentum

        base_damage = 0
        momentum_damage_factor = 0.13
        damage = base_damage + (bird_momentum * momentum_damage_factor)

        if arbiter.total_impulse.length > 2000:
            for element in columns + circles + beams + triangles:
                if element.shape.body == wood_body:  # Change to check the body
                    element.life -= damage  # Apply damage
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
        if arbiter.total_impulse.length > 2000:
            pig_shape, wood_shape = arbiter.shapes
            for pig in pigs:
                if pig.shape == pig_shape:
                    pig.life -= 20
                    if pig.life <= 0:
                        pig_to_remove.append(pig)
                        global score
                        score += 10000
        for pig in pig_to_remove:
            space.remove(pig.shape, pig.body)
            pigs.remove(pig)

    def post_solve_bird_ground(arbiter, space, _):
        a, b = arbiter.shapes
        bird_body = a.body
        ground_body = b.body  

        for ground in floor.static_lines:
            if ground.body == ground_body:
                impact_velocity_reduction_threshold = 3000
                velocity_reduction_factor = 0.3
                if arbiter.total_impulse.length > impact_velocity_reduction_threshold:
                    bird_body.velocity *= (1 - velocity_reduction_factor*2)
                bird.bird_hit_ground = True
                print("birdhitground")
                

    space.add_collision_handler(0, 1).post_solve = post_solve_bird_pig
    space.add_collision_handler(0, 2).post_solve = post_solve_bird_wood 
    space.add_collision_handler(1, 2).post_solve = post_solve_pig_wood
    space.add_collision_handler(0, 3).post_solve = post_solve_bird_ground 
    

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
        nonlocal screen, screen_width, screen_height, scale_x, scale_y
        screen = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
        screen_width, screen_height = event.w, event.h
        scale_x = screen_width / base_width
        scale_y = screen_height / base_height
        # Redraw the screen immediately after resize
        screen.fill((130, 200, 100))
        bg_scaled = pg.transform.scale(bg, (screen_width, screen_height))
        screen.blit(bg_scaled, (0, 0))
        #print("Resizing bg")
        slingl=pg.transform.scale(slingl, scale_size(slingl_scaled_width, slingl_scaled_height))
        slingr=pg.transform.scale(slingr, scale_size(slingr_scaled_width, slingr_scaled_height))
        if game_state == 6:
            #print("Resizing levels")
            levels_drawn = False
            draw_levels()
            #levels_drawn = True
        pg.display.flip()

    while running:
        
        stop_button_rect = stop_button.get_rect(topleft=(8, 8))
        mouse_button_down = False  # Flag to track if mouse button is pressed
        

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                running = False
            elif event.type == pg.VIDEORESIZE:
                handle_resize(event)
            elif game_state == 0:
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_button_down = True
                    print("mouse down")
                    

                elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                    mouse_button_down = False
                    x_mouse, y_mouse = event.pos
                    if stop_button_rect.collidepoint(event.pos):
                        game_state = 5
                        menu_open = True
                        menu_open_time = time.time()
                    if mouse_pressed_to_shoot:
                        pu = scale_pos(140, 420)
                        mouse_pressed_to_shoot = False

                        if level.number_of_birds >= 0:
                            level.number_of_birds -= 1
                            t1 = time.time() * 1000
                            sx, sy = sling_anchor

                            impulse_factor = 10.0
                            
                            
                            impulse_x = -mouse_distance * impulse_factor * math.cos(launch_angle)
                            impulse_y = mouse_distance * impulse_factor * math.sin(launch_angle)
                            
                            # Update bird starting position to align with sling
                            bird_x = sx
                            bird_y = sy - 180 # Adjust vertical offset based on scale
                            bird_x, bird_y = bird_x, bird_y
                            print(level.level_birds)
                            bird = get_next_bird(mouse_distance, launch_angle, bird_x, bird_y, space, level)
                            
                            birds.append(bird)
                            bird_path = []
                            level.level_birds.pop()
                                

                            if level.number_of_birds == 0:
                                t2 = time.time()
                    else:
                        if birds and not birds[-1].fahigkeit_verwendet:
                            birds[-1].fahigkeit()
                            birds[-1].fahigkeit_verwendet = True

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
                        b_size_scaled = scale_size(menu_button.get_width(),menu_button.get_height())
                        if (101 + b_size_scaled[0] > x_mouse > 101 and
                                51 + b_size_scaled[1] > y_mouse > 51):
                            game_state = 0
                            levels_drawn = False

        if game_state == 0:
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

            #screen.blit(slingr, scale_pos(130, 400))
            
            # birds behind sling
            if level.number_of_birds > 0:
                for i in range(level.number_of_birds):
                    bird_type = level.level_birds[i]
                    try:
                        bird_behind_img = pg.transform.scale(pg.transform.scale(pg.image.load(load_resource(f"./resources/images/{bird_type}.png")).convert_alpha(),(30,30)),scale_size(30,30))
                        
                        x_position = 100 - i * 35
                        screen.blit(bird_behind_img, scale_pos(x_position, 445))
                        #print(scale_pos(0,435))
                    except FileNotFoundError:
                        print(f"Error: Bird image not found for {bird_type}")
            if mouse_pressed_to_shoot and level.number_of_birds >= 0:
                sling_action()
                
            # bird sitting in sling
            elif level.number_of_birds >= 0:
                slingl_x, slingl_y = get_sling_positions()
                slingr_x, slingr_y = get_sling_positions()
                screen.blit(bird_img, scale_pos(130, 370))
                
                
                
                screen.blit(slingl, (slingl_x, slingl_y))
                screen.blit(slingr, (slingr_x, slingr_y))
            else:
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
                    print(f"bird removed: {bird.body.position}")
                    bird_to_remove.append(bird)
                bird_path.append((img_x, img_y))  # Store original coordinates

                

                current_time = time.time() * 1000
                if current_time - bird.launch_time > 7000:  # 7 seconds lifetime
                    bird_to_remove.append(bird)
                    bird_path = []  # Clear path when *this* bird is removed

            #for bird_to_remove in bird_to_remove:
            #    if bird_to_remove in birds: #check if the bird is still in the list
            #        space.remove(bird_to_remove.shape, bird_to_remove.body)
            #        birds.remove(bird_to_remove)

            # Draw bird path
            for i, point in enumerate(bird_path):
                if i % 5 == 0:  # Draw point every 5 positions
                    for bird in birds:
                        if not bird.bird_hit_ground:
                            scaled_point = scale_pos(point[0]+15, point[1]+15)
                            pg.draw.circle(screen, WHITE, scaled_point, 3)
                    else:
                        pass
                        

            for bird in bird_to_remove:
                space.remove(bird.shape, bird.shape.body)
                birds.remove(bird)
                bird_path = []  # Clear path when bird is removed

            for pig in pigs:
                if pig.shape.body.position.y < 0:
                    pig_to_remove.append(pig)
                    #print(pigs)
            
            for pig in pig_to_remove:
                space.remove(pig.body)
                pigs.remove(pig)

            for line in floor.static_lines:
                body = floor.static_body
                pv1 = body.position + line.a.rotated(body.angle)
                pv2 = body.position + line.b.rotated(body.angle)
                p1 = to_pygame(pv1)
                p2 = to_pygame(pv2)
                pg.draw.lines(screen, TRANSP, False, [p1, p2])

            for pig in pigs:
                pig_to_remove = []
                pigg=pig
                pig = pig.shape
                p = to_pygame(pig.body.position)
                x, y = p
                angle_degree = math.degrees(pig.body.angle)
                
                if pigg.type == "n11":
                    if pigg.life == 30:
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
                    pig_to_remove.append(pig)
                
                    
            for column in columns:
                if column.element_type != "bats":
                    column.draw_poly(screen,column.shape)
                else:
                    if birds:
                        print(birds[-1].body.position)

                        column.draw_poly(screen,column.shape,birds[-1].body.position)
                    
            for beam in beams:
                beam.draw_poly(screen,beam.shape)
                
            for circle in circles:
                circle.draw_poly(screen,circle.shape)
                
            for triangle in triangles:
                triangle.draw_poly(screen,triangle.shape)

            dt = 1.0 / 50.0 / 2.0
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

            # Calculate center position for the purple background
            center_x = screen_width // 2
            center_y = screen_height // 2
            rect_width = min(screen_width * 0.8, 600)  # 80% of screen width or 600px, whichever is smaller
            rect_height = screen_height  # 80% of screen height or 650px, whichever is smaller
            
            rect = pg.Rect(
                center_x - rect_width // 2,  # Center horizontally
                center_y - rect_height // 2,  # Center vertically
                rect_width,
                rect_height
            )
            pg.draw.rect(screen, (BLACK), rect)
            screen.blit(level_cleared, scale_pos(450, 90))

            if score >= level.one_star:
                screen.blit(star1, scale_pos(370, 190))
            if score >= level.two_star:
                screen.blit(star2, scale_pos(440, 140))
            if score >= level.three_star:
                screen.blit(star3, scale_pos(660, 190))

            screen.blit(score_level_cleared, scale_pos(555, 400))
            screen.blit(replay_button, scale_pos(555, 480))
            screen.blit(next_button, scale_pos(665, 480))
            screen.blit(menu_button, scale_pos(445, 480))

        elif game_state == 3:
            level_failed = bold_font3.render("Level failed!", 1, WHITE)
            score_level_failed = bold_font2.render(str(score), 1, WHITE)

            # Calculate center position for the purple background
            center_x = screen_width // 2
            center_y = screen_height // 2
            rect_width = min(screen_width * 0.8, 600)  # 80% of screen width or 600px, whichever is smaller
            rect_height = screen_height  # 80% of screen height or 650px, whichever is smaller
            
            rect = pg.Rect(
                center_x - rect_width // 2,  # Center horizontally
                center_y - rect_height // 2,  # Center vertically
                rect_width,
                rect_height
            )
            pg.draw.rect(screen, (BLACK), rect)
            screen.blit(level_failed, scale_pos(450, 90))

            if score >= level.one_star:
                screen.blit(star1, scale_pos(370, 190))
            if score >= level.two_star:
                screen.blit(star2, scale_pos(440, 140))
            if score >= level.three_star:
                screen.blit(star3, scale_pos(660, 190))

            screen.blit(score_level_failed, scale_pos(555, 400))
            screen.blit(replay_button, scale_pos(555, 480))
            screen.blit(menu_button, scale_pos(445, 480))

        elif game_state == 6:
            def draw_levels():
                global levels_drawn
            
                print("Drawing levels")
                num_levels = 21
                screen.blit(pg.transform.scale(bg, (screen_width, screen_height)), scale_pos(0, 0))
                    
                # Calculate base positions and spacing
                base_x = 100
                base_y = 50
                base_spacing_x = 151
                base_spacing_y = 160
                levels_per_row = 7
                
                # Scale the icon size
                icon_width = int(100 * scale_x)
                icon_height = int(100 * scale_y)
                level_icon_scaled = pg.transform.scale(level_icon, (icon_width, icon_height))
                locked_icon_scaled = pg.transform.scale(locked_level_icon, (icon_width, icon_height))
                level_icon_rect = level_icon_scaled.get_rect()

                for i in range(num_levels):
                    level_number = i + 1
                    level_method_name = f"build_{level_number}"
                    
                    # Calculate position with proper scaling
                    row = i // levels_per_row
                    col = i % levels_per_row
                    x = base_x + (col * base_spacing_x)
                    y = base_y + (row * base_spacing_y)
                    x, y = scale_pos(x, y)

                    # Choose appropriate icon
                    if getattr(level, level_method_name, None):
                        with open("cleared_levels.txt","r+") as f:
                            if str(level_number) in [line.rstrip("\n") for line in f.readlines()]:
                                icon = level_icon_scaled
                            else:
                                icon = locked_icon_scaled
                    else:
                        icon = locked_icon_scaled

                    # Scale the level number text
                    level_text = str(level_number)
                    level_font = bold_font3.render(level_text, 1, WHITE)
                    text_rect = level_font.get_rect(center=level_icon_rect.center)
                    
                    # Draw the icon and text
                    screen.blit(icon, (x, y))
                    if getattr(level, level_method_name, None):
                        with open("cleared_levels.txt","r+") as f:
                            if str(level_number) in [line.rstrip("\n") for line in f.readlines()]:
                                screen.blit(level_font, (x + text_rect.x, y + text_rect.y))

                # Scale and position the menu button
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
        elif game_state == 7:
            #print(pigs)
            
            level_loader = getattr(level, "build_0", None)
            if level_loader and not loaded:
                level_loader()
                loaded=True
                
            try:
                bird_img = pg.transform.scale(pg.transform.scale(pg.image.load(load_resource(f"./resources/images/{level.level_birds[random.randint(0,level.number_of_birds)]}.png")).convert_alpha(),(30,30)),scale_size(30,30))
            except IndexError as e:
                pass
            
            screen.blit(pg.transform.scale(bg, (screen_width, screen_height)), scale_pos(0, 0))
                
            

            x_mouse, y_mouse = pg.mouse.get_pos()
            if pg.mouse.get_pressed()[0] and (478 * scale_x < x_mouse < 711 * scale_x and 247 * scale_y < y_mouse < 400 * scale_y):
                game_state = 6

            
            
            
                
            
            # Track bird path
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
                    
                bird_path.append((img_x, img_y))  # Store original coordinates
                
                

            

            
            
            pig_to_remove = []
            for pig in pig_to_remove:
                
                space.remove(pig.body)
                pigs.remove(pig)

            for line in floor.static_lines:
                body = floor.static_body
                pv1 = body.position + line.a.rotated(body.angle)
                pv2 = body.position + line.b.rotated(body.angle)
                p1 = to_pygame(pv1)
                p2 = to_pygame(pv2)
                pg.draw.lines(screen, TRANSP, False, [p1, p2])

            for pig in pigs:
                pig_to_remove = []
                pigg=pig
                pig = pig.shape
                p = to_pygame(pig.body.position)
                x, y = p
                angle_degree = math.degrees(pig.body.angle)
                
                if pigg.type == "n11":
                    if pigg.life == 30:
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
                    pig_to_remove.append(pig)
                if len(pigs) > 50:
                    pigs.remove(pigs[0])
                #print(len(pigs))
                
            dt = 1.0 / 50.0 / 2.0
            for x in range(2):
                #print("space.step called")
                space.step(dt)
    
            screen.blit(play_button,(screen_width/2-play_button.get_width()/2,screen_height/2-play_button.get_height()/2))

            
        pg.display.flip()
        clock.tick(60)

        

    pg.quit()
    sys.exit()

main_loop()