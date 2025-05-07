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

slingl_x, slingl_y = 130, 370
slingr_x, slingr_y = 145, 380

score = 0

game_state = 6
levels_drawn = False
bird_path = []
counter = 0
restart_counter = False
bonus_score_once = True



wall = False



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

    global sound_on
    global count
    global mouse_pressed_to_shoot
    global tick_to_next_circle

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



    global wall



    
    pg.init()
    screen_width, screen_height = 1200, 650
    screen = pg.display.set_mode((1200, 650), pg.RESIZABLE)

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

    slingr_scaled_width = int(slingr.get_width() * 0.05)
    slingr_scaled_height = int(slingr.get_height() * 0.05)
    slingl_scaled_width = int(slingl.get_width() * 0.135)
    slingl_scaled_height = int(slingl.get_height() * 0.135)

    n11 = pg.transform.scale(n11, (n11_scaled_width, n11_scaled_height))
    sahur = pg.transform.scale(sahur, (sahur_scaled_width, sahur_scaled_height))
    slingr = pg.transform.scale(slingr, (slingr_scaled_width, slingr_scaled_height))
    slingl = pg.transform.scale(slingl, (slingl_scaled_width, slingl_scaled_height))

    bomb0 = pg.image.load(load_resource("./resources/images/bomb0.png")).convert_alpha()
    bomb1 = pg.image.load(load_resource("./resources/images/bomb1.png")).convert_alpha()
    bomb2 = pg.image.load(load_resource("./resources/images/bomb2.png")).convert_alpha()

    glorbo = pg.image.load(load_resource("./resources/images/glorbo.png")).convert_alpha()
    liri = pg.image.load(load_resource("./resources/images/liri.png")).convert_alpha()
    liri = pg.transform.scale(liri,(liri.get_width()*0.1,liri.get_height()*0.1))

    patapim_full = pg.image.load(load_resource("./resources/images/patapim_full.png")).convert_alpha()
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

    static_body = pm.Body(body_type=pm.Body.STATIC)
    static_lines = [pm.Segment(static_body, (0.0, 130.0), (1200.0, 130.0), 0.0)]
    static_lines1 = [pm.Segment(static_body, (1200.0, 200.0), (1200.0, 800.0), 0.0)]

    for line in static_lines:
        line.elasticity = 0.95
        line.collision_type = 3
        line.friction = 1
    for line in static_lines1:
        line.elasticity = 0.95
        line.collision_type = 3
        line.friction = 1

    space.add(static_body, *static_lines)

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
        return int(p.x), int(-p.y + 600)

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

        sx, sy = sling_anchor

        mx, my = x_mouse, y_mouse



        v = vector((sx, sy), (mx, my))

        uv = unit_vector(v)

        uv1 = uv[0]

        uv2 = uv[1]



        mouse_distance_raw = distance(sx, sy, mx, my)



        if mouse_distance_raw > rope_length:

            mouse_distance = rope_length

            pu = (uv1 * rope_length + sx, uv2 * rope_length + sy)

            x_sahur = pu[0] - sahur.get_width() // 2

            y_sahur = pu[1] - sahur.get_height() // 2

            if len(level.level_birds) >= 0:
                
                
                screen.blit(bird_img, (x_sahur, y_sahur))

                pg.draw.line(screen, (0, 0, 0), (slingr_x + 4, slingr_y + 3), pu, 5)

                pg.draw.line(screen, (0, 0, 0), (slingl_x + 2, slingl_y + 13), pu, 5)

        else:

            mouse_distance = mouse_distance_raw

            pu = (mx, my)

            x_sahur = mx - sahur.get_width() // 2 # Center bird on mouse

            y_sahur = my - sahur.get_height() // 2 # Center bird on mouse

            if len(level.level_birds) >= 0:

                screen.blit(bird_img, (x_sahur, y_sahur))

                pg.draw.line(screen, (0, 0, 0), (slingr_x + 4, slingr_y + 3), (mx, my), 5)

                pg.draw.line(screen, (0, 0, 0), (slingl_x + 2, slingl_y + 13), (mx, my), 5)



        dy = sy - pu[1] # Vector component from end of rope to anchor

        dx = sx - pu[0] # Vector component from end of rope to anchor

        if dx == 0:
            dx = 0.000000000000001

        angle = math.atan2(dy, dx)
        launch_angle = angle
        #print(f"launch_angle in sling_action: {math.degrees(launch_angle)}")
        
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
        momentum_damage_factor = 0.013
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

    def post_solve_bird_wood(arbiter, space, _):
        a, b = arbiter.shapes
        bird_body = a.body
        wood_body = b.body

        bird_momentum = bird_body.mass * bird_body.velocity.length
        base_damage = 0
        momentum_damage_factor = 0.013
        damage = base_damage + (bird_momentum * momentum_damage_factor)

        for wood in beams + columns + circles + triangles:
            if wood.body == wood_body:
                damage_threshold = 1000
                damage_factor = 0.03
                if arbiter.total_impulse.length > damage_threshold:
                    damage = (arbiter.total_impulse.length - damage_threshold) * damage_factor
                    wood.life -= damage
                    if wood.life <= 0:
                        space.remove(wood.shape, wood.body)
                        if wood in beams:
                            beams.remove(wood)
                        elif wood in columns:
                            columns.remove(wood)
                        elif wood in circles:
                            circles.remove(wood)
                        elif wood in triangles:
                            triangles.remove(wood)
                        global score
                        score += 5000
                impact_velocity_reduction_threshold = 3000
                velocity_reduction_factor = 0.3
                if arbiter.total_impulse.length > impact_velocity_reduction_threshold:
                    bird_body.velocity *= (1 - velocity_reduction_factor)

    space.add_collision_handler(0, 1).post_solve = post_solve_bird_pig
    space.add_collision_handler(1, 2).post_solve = post_solve_pig_wood
    space.add_collision_handler(0, 2).post_solve = post_solve_bird_wood

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
    level = Level(pigs, columns, beams, circles, triangles, space)
    level.load_level()

    def get_next_bird(mouse_distance, launch_angle, bird_x, bird_y, space):
        global bird
        bird = level.level_birds[-1]
        if bird == "sahur":
            bird = ch.Sahur(mouse_distance, launch_angle, bird_x, bird_y, space)
        elif bird == "liri":
            bird = ch.Liri(mouse_distance, launch_angle, bird_x, bird_y, space)
        elif bird == "palocleves":
            bird = ch.Palocleves(mouse_distance, launch_angle, bird_x, bird_y, space)
        return bird
    
    def get_next_bird_img():
        pass
   
    while running:
        
        stop_button_rect = stop_button.get_rect(topleft=(8, 8))
        mouse_button_down = False  # Flag to track if mouse button is pressed
        

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                running = False
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
                        pu = (140, 420)
                        mouse_pressed_to_shoot = False

                        if level.number_of_birds >= 0:
                            level.number_of_birds -= 1
                            t1 = time.time() * 1000
                            sx, sy = sling_anchor

                            impulse_factor = 10.0
                            #print(mouse_distance, impulse_factor, math.sin(launch_angle))
                            
                            
                            impulse_x = -mouse_distance * impulse_factor * math.cos(launch_angle)
                            impulse_y = mouse_distance * impulse_factor * math.sin(launch_angle)
                            #print(f"Impuls: {impulse_x}, {impulse_y}")
                            #print(f"Abschusswinkel: {math.degrees(launch_angle)}")
                            #print(f"Abschussdistanz: {mouse_distance}")

                            bird_x = sx
                            bird_y = sy - 150
                            print(level.level_birds)
                            bird = get_next_bird(mouse_distance, launch_angle, bird_x, bird_y, space)
                            
                            birds.append(bird)
                            bird_path = []
                            level.level_birds.pop()
                                

                            if level.number_of_birds == 0:
                                t2 = time.time()

            elif game_state == 5:
                if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                    x_mouse, y_mouse = event.pos

                    if (10 + stop_button.get_width() > x_mouse > 10 and
                            10 + stop_button.get_height() > y_mouse > 10):
                        game_state = 0

                    elif (80 + replay_button.get_width() > x_mouse > 80 and
                        170 + replay_button.get_height() > y_mouse > 190):
                        restart()
                        level.load_level()
                        game_state = 0
                        bird_path = []
                        score = 0

                    elif (105 + menu_button.get_width() > x_mouse > 105 and
                        307 + menu_button.get_height() > y_mouse > 307):
                        game_state = 6
                        levels_drawn = False

                    elif (60 + sound_button.get_width() > x_mouse > 55 and
                        565 + sound_button.get_height() > y_mouse > 565):
                        sound_on = not sound_on

            elif game_state == 4:
                if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                    x_mouse, y_mouse = event.pos

                    if (665 + next_button.get_width() > x_mouse > 665 and
                            480 + next_button.get_height() > y_mouse > 480):
                        restart()
                        level.number += 1
                        game_state = 0
                        level.load_level()
                        score = 0
                        bird_path = []
                        bonus_score_once = True

                    elif (559 + replay_button.get_width() > x_mouse > 559 and
                        486 + replay_button.get_height() > y_mouse > 486):
                        restart()
                        level.load_level()
                        game_state = 0
                        bird_path = []
                        score = 0

                    elif (452 + menu_button.get_width() > x_mouse > 452 and
                        490 + menu_button.get_height() > y_mouse > 490):
                        game_state = 6
                        levels_drawn = False

            elif game_state == 3:
                if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                    x_mouse, y_mouse = event.pos

                    if (559 + replay_button.get_width() > x_mouse > 559 and
                            486 + replay_button.get_height() > y_mouse > 486):
                        restart()
                        level.load_level()
                        game_state = 0
                        bird_path = []
                        score = 0

                    elif (452 + menu_button.get_width() > x_mouse > 452 and
                        490 + menu_button.get_height() > y_mouse > 490):
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
                        if (101 + menu_button.get_width() > x_mouse > 101 and
                                51 + menu_button.get_height() > y_mouse > 51):
                            game_state = 0
                            levels_drawn = False

        if game_state == 0:
            try:
                bird_img = pg.transform.scale(pg.image.load(load_resource(f"./resources/images/{level.level_birds[-1]}.png")).convert_alpha(),(30,30))
            except IndexError as e:
                pass
                
            menu_open = False
            screen.fill((130, 200, 100))
            bg_scaled = pg.transform.scale(bg, (screen_width, screen_height))
            screen.blit(bg_scaled, (0, 0))

            x_mouse, y_mouse = pg.mouse.get_pos()
            if pg.mouse.get_pressed()[0] and (110 < x_mouse < 170 and 250 < y_mouse < 400):
                mouse_pressed_to_shoot = True

            screen.blit(slingr, (120, 370))
            if game_state == 0:
                menu_open = False
                screen.fill((130, 200, 100))
                bg_scaled = pg.transform.scale(bg, (screen_width, screen_height))
                screen.blit(bg_scaled, (0, 0))

                x_mouse, y_mouse = pg.mouse.get_pos()
                if pg.mouse.get_pressed()[0] and (110 < x_mouse < 170 and 250 < y_mouse < 400):
                    mouse_pressed_to_shoot = True

                screen.blit(slingr, (120, 370))
                
                # birds behind sling
            if level.number_of_birds > 0:
                for i in range(level.number_of_birds):
                    
                    bird_type = level.level_birds[i]
                    try:
                        bird_behind_img = pg.transform.scale(pg.image.load(load_resource(f"./resources/images/{bird_type}.png")).convert_alpha(),(30,30))
                        x_position = 100 - i * 35
                        screen.blit(bird_behind_img, (x_position, 435))
                    except FileNotFoundError:
                        print(f"Error: Bird image not found for {bird_type}")
            if mouse_pressed_to_shoot and level.number_of_birds >= 0:
                sling_action()
            elif level.number_of_birds >= 0:
                screen.blit(pg.transform.scale(bird_img, (30,30)), (130, 370))
            else:
                pg.draw.line(screen, (0, 0, 0), (slingr_x + 4, slingr_y + 3), pu, 5)
                pg.draw.line(screen, (0, 0, 0), (slingl_x + 2, slingl_y + 13), pu, 5)

            bird_to_remove = []
            pig_to_remove = []

            for bird in birds:
                p = to_pygame(bird.shape.body.position)
                x, y = p
                blit_x = x - sahur.get_width() // 2
                blit_y = y - sahur.get_height() // 2
                screen.blit(pg.transform.scale(pg.image.load(load_resource(bird.img)).convert_alpha(),(30,30)), (blit_x, blit_y))
                pg.draw.circle(screen, BLUE, p, int(bird.shape.radius), 2)
                bird_path.append(p)
                if (bird.shape.body.position.y < 0 or bird.shape.body.position.x < -50 or
                        bird.shape.body.position.x > screen_width + 50 or
                        time.time() - bird.launch_time > bird.lifespan):
                    bird_to_remove.append(bird)

            for point in bird_path:
                if bird_path.index(point) % 5 == 0:
                    pg.draw.circle(screen, WHITE, point, 3)

            for bird in bird_to_remove:
                space.remove(bird.shape, bird.shape.body)
                birds.remove(bird)
                bird_path = []

            for pig in pigs:
                if pig.shape.body.position.y < 0:
                    pig_to_remove.append(pig)
                    print(pigs)
            
            for pig in pig_to_remove:
                space.remove(pig.body)
                pigs.remove(pig)

            for line in static_lines:
                body = static_body
                pv1 = body.position + line.a.rotated(body.angle)
                pv2 = body.position + line.b.rotated(body.angle)
                p1 = to_pygame(pv1)
                p2 = to_pygame(pv2)
                pg.draw.lines(screen, TRANSP, False, [p1, p2])

            for pig in pigs:
                #print(pig,type)
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

                # Calculate the bounding box of the *original* image, not the rotated one
                width, height = pig_img.get_size() # Use the size of the *original* image

                rotated_image = pg.transform.rotate(pig_img, angle_degree)
                
                offset = Vec2d(*rotated_image.get_size()) / 2
                #print("offset: ",offset)
                x -= offset[0]
                y -= offset[1]
                screen.blit(rotated_image, (x, y))
                pg.draw.circle(screen, BLUE, p, int(pig.radius), 2)
                if (pig.body.position.y < 0 or pig.body.position.x < -50 or
                        pig.body.position.x > screen_width + 50):
                    pig_to_remove.append(pig)
                
                    
            for column in columns:
                column.draw_poly(screen,column.shape)

            for beam in beams:
                beam.draw_poly(screen,beam.shape)
                
            for circle in circles:
                circle.draw_poly(screen,circle.shape)
                
            for triangle in triangles:
                triangle.draw_poly(screen,triangle.shape)

            dt = 1.0 / 50.0 / 2.0
            for x in range(2):
                space.step(dt)
            screen.blit(slingl, (120, 370))

            score_font = bold_font.render("SCORE", 1, WHITE)
            number_font = bold_font.render(str(score), 1, WHITE)

            screen.blit(score_font, (1060, 90))
            if score == 0:
                screen.blit(number_font, (1150, 130))
            else:
                screen.blit(number_font, (1060, 130))

            screen.blit(stop_button, (8, 8))

            if not pigs and not mouse_pressed_to_shoot and not restart_counter and not birds:
                print("Level cleared! Setting game_state to 4")
                game_state = 4
                restart_counter = True

            if level.number_of_birds < 0 and pigs and not birds:
                game_state = 3

        elif game_state == 5:
            menu_open = True
            if sound_on:
                screen.blit(menu_son, (0, 0))
            else:
                screen.blit(menu_sof, (0, 0))

        elif game_state == 4:
            print(level.number)
            with open("cleared_levels.txt","r+") as f:
                if str(level.number+1) not in [line.rstrip("\n") for line in f.readlines()]:
                    f.write(f"{str(level.number+1)}\n")
                    print(f"written {level.number+1}")
                    
                
            level_cleared = bold_font3.render("Level cleared!", 1, WHITE)
            score_level_cleared = bold_font2.render(str(score), 1, WHITE)
            if level.number_of_birds >= 0 and not pigs and bonus_score_once:
                score += (level.number_of_birds) * 10000
                bonus_score_once = False

            rect = pg.Rect(300, 0, 600, 650)
            pg.draw.rect(screen, (PURPLE), rect)
            screen.blit(level_cleared, (450, 90))

            if score >= level.one_star:
                screen.blit(star1, (370, 190))
            if score >= level.two_star:
                screen.blit(star2, (440, 140))
            if score >= level.three_star:
                screen.blit(star3, (660, 190))

            screen.blit(score_level_cleared, (555, 400))
            screen.blit(replay_button, (555, 480))
            screen.blit(next_button, (665, 480))
            screen.blit(menu_button, (445, 480))

        elif game_state == 3:
            level_failed = bold_font3.render("Level failed!", 1, WHITE)
            score_level_failed = bold_font2.render(str(score), 1, WHITE)

            rect = pg.Rect(300, 0, 600, 650)
            pg.draw.rect(screen, (PURPLE), rect)
            screen.blit(level_failed, (450, 90))

            if score >= level.one_star:
                screen.blit(star1, (370, 190))
            if score >= level.two_star:
                screen.blit(star2, (440, 140))
            if score >= level.three_star:
                screen.blit(star3, (660, 190))

            screen.blit(score_level_failed, (555, 400))
            screen.blit(replay_button, (555, 480))
            screen.blit(menu_button, (445, 480))

        elif game_state == 6:
            if not levels_drawn:
                num_levels = 21
                screen.blit(pg.transform.scale(bg, (screen_width, screen_height)), (0, 0))
                x, y = 100, 50
                level_icon_rect = level_icon.get_rect()

                for i in range(num_levels):
                    level_number = i + 1
                    level_method_name = f"build_{level_number}"
                    
                    icon_x = x
                    icon_y = y

                    if getattr(level, level_method_name, None):
                        with open("cleared_levels.txt","r+") as f:
                            if str(level_number) in [line.rstrip("\n") for line in f.readlines()]:
                                icon = level_icon
                            else:
                                icon = locked_level_icon
                    else:
                        icon = locked_level_icon

                    level_text = str(level_number)
                    level_font = bold_font3.render(level_text, 1, WHITE)
                    text_rect = level_font.get_rect(center=level_icon_rect.center)
                    screen.blit(icon, (icon_x, icon_y))
                    if getattr(level, level_method_name, None):
                        with open("cleared_levels.txt","r+") as f:
                            if str(level_number) in [line.rstrip("\n") for line in f.readlines()]:
                                screen.blit(level_font, (icon_x + text_rect.x, icon_y + text_rect.y))

                    x += 151
                    if level_number % 7 == 0:
                        y += 160
                        x = 100

            levels_drawn = True

            
        pg.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main_loop()

    pg.quit()
    sys.exit()

