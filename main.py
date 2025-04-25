# main.py

import os
import sys
import math
import pygame as pg
import time
import pymunk as pm
from level import Level
from character import Bird
from pygame.locals import *

pg.init()
screen_width,screen_height = 1200,650
screen = pg.display.set_mode((1200,650),pg.RESIZABLE)

bird_scale_factor = 0.3
pig_scale_factor = 0.2
star13_scale_factor= 0.5
star2_scale_factor = 1

bg = pg.image.load("./resources/images/bg.png").convert_alpha()
buttons = pg.image.load("./resources/images/buttons.png").convert_alpha()
buttons2 = pg.image.load("./resources/images/buttons2.png").convert_alpha()


menu_son = pg.image.load("./resources/images/menu_son.png").convert_alpha()
menu_sof = pg.image.load("./resources/images/menu_sof.png").convert_alpha()
menu_son = pg.transform.scale(menu_son,(250,screen_height))
menu_sof = pg.transform.scale(menu_sof,(250,screen_height))


rect=pg.Rect(32,19,122-32,116-19)
replay_button = buttons.subsurface(rect).copy()

rect=pg.Rect(25,142,122-25,243-142)
stop_button = pg.transform.scale(buttons.subsurface(rect).copy(),(65,65))


rect=pg.Rect(173,444,274-173,552-444)
next_button = buttons.subsurface(rect).copy()

rect=pg.Rect(165,132,277-165,259-132)
exit_button = buttons.subsurface(rect).copy()

rect=pg.Rect(18,264,114-18,365-264)
go_button = buttons.subsurface(rect).copy()

rect=pg.Rect(167,288,284-167,409-288)
sound_button = buttons.subsurface(rect).copy()

sound_button_scaled_width = int(sound_button.get_width() * 0.5)
sound_button_scaled_height = int(sound_button.get_height() * 0.5)

sound_button = pg.transform.scale(sound_button,(sound_button_scaled_width,sound_button_scaled_height))

rect=pg.Rect(73,192,92-73,212-192)
muted_sound_button = buttons2.subsurface(rect).copy()
muted_sound_button = pg.transform.scale(muted_sound_button,(sound_button.get_width(),sound_button.get_height()))

rect=pg.Rect(26,385,117-26,478-385)
menu_button = buttons.subsurface(rect).copy()

rect=pg.Rect(291,11,547-291,181-11)
play_button = buttons.subsurface(rect).copy()

wood1 = pg.image.load("./resources/images/wood.png").convert_alpha()
#wood2 = pg.image.load("./resources/images/wood1.png").convert_alpha()
star1 = pg.image.load("./resources/images/stars/gold_star.png").convert_alpha()
star2 = pg.image.load("./resources/images/stars/jew_star.png").convert_alpha()
star3 = pg.image.load("./resources/images/stars/soviet_star.png").convert_alpha()

sling = pg.image.load("./resources/images/sling.png").convert_alpha()
slingl = pg.image.load("./resources/images/slingl.png").convert_alpha()
slingr = pg.image.load("./resources/images/slingr.png").convert_alpha()

n11 = pg.image.load("./resources/images/n1.1.png").convert_alpha()
n12 = pg.image.load("./resources/images/n1.2.png").convert_alpha()
n21 = pg.image.load("./resources/images/n2.1.png").convert_alpha()
n22 = pg.image.load("./resources/images/n2.2.png").convert_alpha()
n31 = pg.image.load("./resources/images/n3.1.png").convert_alpha()
n32 = pg.image.load("./resources/images/n3.2.png").convert_alpha()
n41 = pg.image.load("./resources/images/n4.1.png").convert_alpha()
n42 = pg.image.load("./resources/images/n4.2.png").convert_alpha()
n51 = pg.image.load("./resources/images/n5.1.png").convert_alpha()
n52 = pg.image.load("./resources/images/n5.2.png").convert_alpha()

trala = pg.image.load("./resources/images/trala.png").convert_alpha()
sahur = pg.image.load("./resources/images/sahur.png").convert_alpha()



n11_scaled_width = int(n11.get_width() * pig_scale_factor)
n11_scaled_height = int(n11.get_height() * pig_scale_factor)

sahur_scaled_width = int(sahur.get_width() * bird_scale_factor)
sahur_scaled_height = int(sahur.get_height() * bird_scale_factor)

star13_scaled_width = int(star1.get_width() * star13_scale_factor)
star13_scaled_height = int(star1.get_height() * star13_scale_factor)
star2_scaled_width = int(star2.get_width() * star2_scale_factor)
star2_scaled_height = int(star2.get_height() * star2_scale_factor)

star1 = pg.transform.scale(star1,(star13_scaled_width,star13_scaled_height))
star3 = pg.transform.scale(star3,(star13_scaled_width,star13_scaled_height))
star2 = pg.transform.scale(star2,(star2_scaled_width,star2_scaled_height))

slingr_scaled_width = int(slingr.get_width() * 0.05)
slingr_scaled_height = int(slingr.get_height() * 0.05)
slingl_scaled_width = int(slingl.get_width() * 0.135)
slingl_scaled_height = int(slingl.get_height() * 0.135)

n11 = pg.transform.scale(n11,(n11_scaled_width,n11_scaled_height))
sahur = pg.transform.scale(sahur, (sahur_scaled_width, sahur_scaled_height))
slingr = pg.transform.scale(slingr,(slingr_scaled_width, slingr_scaled_height))
slingl = pg.transform.scale(slingl,(slingl_scaled_width, slingl_scaled_height))

bomb0 = pg.image.load("./resources/images/bomb0.png").convert_alpha()
bomb1 = pg.image.load("./resources/images/bomb1.png").convert_alpha()
bomb2 = pg.image.load("./resources/images/bomb2.png").convert_alpha()

glorbo = pg.image.load("./resources/images/glorbo.png").convert_alpha()
liri = pg.image.load("./resources/images/liri.png").convert_alpha()

patapim_full = pg.image.load("./resources/images/patapim_full.png").convert_alpha()
patapim_leg1 = pg.image.load("./resources/images/patapim_leg1.png").convert_alpha()
patapim_leg2 = pg.image.load("./resources/images/patapim_leg2.png").convert_alpha()


levels_menu = pg.image.load("./resources/images/levels_menu.png").convert_alpha()
rect = pg.Rect(220,79,359-220,218-79)
level_icon = pg.transform.scale(levels_menu.subsurface(rect).copy(),(100,100))
rect = pg.Rect(1563,600,1700-1563,740-600)
locked_level_icon = pg.transform.scale(levels_menu.subsurface(rect).copy(),(100,100))


#rect = pg.Rect(181,1050,50,50)

#cropped = sahur.subsurface(rect).copy()

#sahur_image = pg.transform.scale(cropped, 30,30)


clock = pg.time.Clock()

running = True

# base physics

space = pm.Space()
space.gravity=(0.0,-700.0)

pigs = []
birds = []
balls = []
polys = []
beams = []
columns = []
poly_points = []
ball_num = 0
polys_dict = {}
mouse_distance = 0
rope_length = 90
angle = 90
x_mouse = 0
y_mouse = 0
launch_angle = 0
sling_anchor = (130,380)  # Example: Adjust to your actual anchor point
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

bold_font = pg.font.SysFont("arial", 20, bold=True)
bold_font2 = pg.font.SysFont("arial",30,bold=True)
bold_font3 = pg.font.SysFont("arial",50,bold=True)

wall = False

# STATIC FLOOR

static_body = pm.Body(body_type=pm.Body.STATIC)
static_lines = [pm.Segment(static_body,(0.0,130.0),(1200.0,130.0),0.0)]
static_lines1 = [pm.Segment(static_body,(1200.0,200.0),(1200.0,800.0),0.0)]

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
  for entry in os.listdir(directory):
    path = os.path.join(directory, entry)
    if os.path.isfile(path):
      all_files.append(entry)
  return all_files

win_imgs = get_all_files_listdir("./resources/images/win_imgs")
lose_imgs = get_all_files_listdir("./resources/images/lose_imgs")

buttons = pg.image.load("./resources/images/buttons.png").convert_alpha()


def to_pygame(p):
    return int(p.x),int(-p.y+600)

def vector(p0,p1):  # return vector of p1 and p2
    a = p1[0] - p0[0]
    b = p1[1] - p0[1]
    return a,b

def unit_vector(v):
    h = ((v[0]**2 + (v[1]**2))**0.5)

    if h == 0:
        h = 0.000000000000001

    ua = v[0]/h
    ub = v[1]/h

    return ua,ub

def distance(x0,y0,x,y):
    dx = x - x0
    dy = y - y0

    d = ((dx**2)+(dy**2))**0.5
    return d

def sling_action():  # change pos of sling
    global mouse_distance
    global rope_length
    global angle
    global x_mouse
    global y_mouse
    global launch_angle
    global sling_anchor
    global pu
    global level  # Assuming 'level' is a global variable

    # fix birb to sling rope

    sx, sy = sling_anchor
    mx, my = x_mouse, y_mouse

    v = vector((sx, sy), (mx, my))
    uv = unit_vector(v)
    uv1 = uv[0]
    uv2 = uv[1]

    mouse_distance_raw = distance(sx, sy, mx, my)
    print(f"mouse distance (raw): {mouse_distance_raw}")

    if mouse_distance_raw > rope_length:
        mouse_distance = rope_length
        pu = (uv1 * rope_length + sx, uv2 * rope_length + sy)
        # Calculate the position of sahur at the end of the rope
        x_sahur = pu[0] - sahur.get_width() // 2
        y_sahur = pu[1] - sahur.get_height() // 2
        if level.number_of_birds > 0:
            screen.blit(sahur, (x_sahur, y_sahur))
        pg.draw.line(screen, (0, 0, 0), (slingr_x + 4, slingr_y + 3), pu, 5)
        pg.draw.line(screen, (0, 0, 0), (slingl_x + 2, slingl_y + 13), pu, 5)
    else:
        mouse_distance = mouse_distance_raw
        pu = (mx, my)
        x_sahur = mx - sahur.get_width() // 2  # Center bird on mouse
        y_sahur = my - sahur.get_height() // 2  # Center bird on mouse
        if level.number_of_birds > 0:
            screen.blit(sahur, (x_sahur, y_sahur))
        pg.draw.line(screen, (0, 0, 0), (slingr_x + 4, slingr_y + 3), (mx, my), 5)
        pg.draw.line(screen, (0, 0, 0), (slingl_x + 2, slingl_y + 13), (mx, my), 5)

    # angle of impulse (OPPOSITE DIRECTION)
    dy = sy - pu[1]  # Vector component from end of rope to anchor
    dx = sx - pu[0]  # Vector component from end of rope to anchor

    if dx == 0:
        dx = 0.000000000000001

    angle = math.atan2(dy, dx)
    launch_angle = angle


def restart():
    mouse_pressed_to_shoot = False
    print("restarted")
    pigs_to_remove = []
    birds_to_remove = []
    columns_to_remove = []
    beams_to_remove = []


    for pig in pigs:
        pigs_to_remove.append(pig)
    for pig in pigs_to_remove:
        space.remove(pig.shape,pig.shape.body)
        pigs.remove(pig)

    for bird in birds:
        birds_to_remove.append(bird)

    for bird in birds_to_remove:
        space.remove(bird.shape,bird.shape.body)
        birds.remove(bird)
        print(f"{len(birds)} birds left")

    for column in columns:
        columns_to_remove.append(column)
    for column in columns_to_remove:
        space.remove(column.shape,column.shape.body)
        columns.remove(column)

    for beam in beams:
        beams_to_remove.append(beam)
    for beam in beams_to_remove:
        space.remove(beam.shape,beam.shape.body)
        beams.remove(beam)


def post_solve_bird_pig(arbiter, space, _):
    """Handles collision between bird and pig, applying damage based on bird's momentum."""
    surface = screen
    a, b = arbiter.shapes
    bird_body = a.body
    pig_body = b.body
    p = to_pygame(bird_body.position)
    p2 = to_pygame(pig_body.position)

    r = 20

    pg.draw.circle(surface, BLACK, p,r, 4)
    pg.draw.circle(surface, RED, p2, r, 4)

    pig_to_remove = []

    # Calculate the momentum of the bird at the moment of impact
    bird_momentum = bird_body.mass * bird_body.velocity.length

    # Define a base damage factor and a momentum-based damage multiplier
    base_damage = 0
    momentum_damage_factor = 0.013  # Adjust this value to control how much momentum affects damage

    # Calculate the damage dealt to the pig
    damage = base_damage + (bird_momentum * momentum_damage_factor)

    for pig in pigs:
        if pig.body == pig_body and bird_momentum > 25:
            pig.life -= damage
            print(f"Pig hit with momentum: {bird_momentum:.2f}, taking damage: {damage:.2f}, current life: {pig.life:.2f}")

            if pig.life <= 0:
                pig_to_remove.append(pig)
                global score
                score += 10000

    for pig in pig_to_remove:
        space.remove(pig.shape, pig.body)
        pigs.remove(pig)

def post_solve_pig_wood(arbiter, space, _):
    """Handles collision between pig and wood."""
    pig_to_remove = []
    if arbiter.total_impulse.length > 4000:  # if pig hits wood with enough force
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



def post_solve_bird_wood(arbiter,space,_):
    # handle collision between bird and wood
    global score
    if arbiter.total_impulse.length > 4000: # if bird hits wood with enough force
        """Handles collision between bird and pig, applying damage based on bird's momentum."""
    surface = screen
    a, b = arbiter.shapes
    bird_body = a.body
    wood_shape = b
    wood_body = b.body
    p = to_pygame(bird_body.position)
    p2_pymunk =  wood_body.position
    p2_pygame = to_pygame(p2_pymunk)
    r = 20

    pg.draw.circle(surface, BLACK, p, r, 4)

    bb = wood_shape.bb
    width = bb.right - bb.left
    height = bb.top - bb.bottom


    # Calculate the momentum of the bird at the moment of impact
    bird_momentum = bird_body.mass * bird_body.velocity.length

    # Define a base damage factor and a momentum-based damage multiplier
    base_damage = 0
    momentum_damage_factor = 0.013  # Adjust this value to control how much momentum affects damage

    # Calculate the damage dealt to the pig
    damage = base_damage + (bird_momentum * momentum_damage_factor)

    for wood in beams + columns:
        if wood.body == wood_body:
            damage_threshold = 1000  # Adjust this value
            damage_factor = 0.03      # Adjust this value
            if arbiter.total_impulse.length > damage_threshold:
                    damage = (arbiter.total_impulse.length - damage_threshold) * damage_factor
                    wood.life -= damage  # Assuming a 'life' attribute for wood
                    print(f"Wood hit, taking damage: {damage:.2f}, current life: {wood.life:.2f}, bird velocity: {bird_body.velocity.length:.2f}")
                    if wood.life <= 0:
                        space.remove(wood.shape, wood.body)
                        if wood in beams:
                            beams.remove(wood)
                        elif wood in columns:
                            columns.remove(wood)
                        score += 5000  # Award points for breaking wood

        # 3. Bird Behavior (Example: slightly reduce bird's velocity on strong impact)
        impact_velocity_reduction_threshold = 3000
        velocity_reduction_factor = 0.1
        if arbiter.total_impulse.length > impact_velocity_reduction_threshold:
            bird_body.velocity *= (1 - velocity_reduction_factor)
            print(f"Bird velocity reduced after hitting wood. {bird_body.velocity.length}")

        # 4. Score/Points (Award points for hitting wood)

        #score += 100  # Award points for any significant hit on wood

        # 5. Sound Effects (Conceptual - requires Pygame mixer setup)
        # if sound_enabled:
        #     wood_impact_sound.play()

    # You might also want to handle cases of weaker impacts differently
    else:
        # Perhaps a different visual cue or a softer sound
        pass



space.add_collision_handler(0,1).post_solve=post_solve_bird_pig
space.add_collision_handler(1,2).post_solve=post_solve_pig_wood
space.add_collision_handler(0,2).post_solve=post_solve_bird_wood




t1 = 0
c=0
menu_open = False
menu_open_time = 0
menu_click_delay = 0.2 # seconds

# game states:
# 0:running
# 5:paused
# 3:lose
# 4:win

# Create and load the first level with the correct arguments
level = Level(pigs, columns, beams, space)
level.load_level()

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
                if stop_button_rect.collidepoint(event.pos):
                    print("Mouse down on stop button") # For debugging
                    # You could set a flag here to indicate the button was pressed down over it

            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                mouse_button_down = False
                x_mouse, y_mouse = event.pos  # Get mouse position of the click
                if stop_button_rect.collidepoint(event.pos):
                    print("Stop button clicked!")
                    game_state = 5
                    menu_open = True
                    menu_open_time = time.time()
                # release birb
                if mouse_pressed_to_shoot:
                    pu = (140,420)
                    mouse_pressed_to_shoot = False
                    print(f"{level.number_of_birds} bird left")

                    if level.number_of_birds > 0:
                            level.number_of_birds -= 1
                            t1 = time.time() * 1000
                            sx, sy = sling_anchor  # Get anchor coordinates

                            # Calculate impulse based on mouse distance and launch angle
                            impulse_factor = 10.0  # Adjust this to control launch power
                            impulse_x = -mouse_distance * impulse_factor * math.cos(launch_angle) # Negated
                            impulse_y = mouse_distance * impulse_factor * math.sin(launch_angle)  # Negated (and sign adjusted for Pygame)

                            # Calculate initial position (centered at anchor)
                            bird_x = sx #- sahur.get_width() // 2
                            bird_y = sy-150 #- sahur.get_height() // 2

                            # Create the Bird object with the correct arguments
                            bird = Bird(mouse_distance, launch_angle, bird_x, bird_y, space)
                            birds.append(bird)
                            # The impulse is already applied in the Bird's __init__ method
                            bird_path = [] # Reset path for the new bird

                            if level.number_of_birds == 0:
                                t2 = time.time()

                    click_x, click_y = event.pos
                    print(f"Clicked at: ({click_x}, {click_y})")

        elif game_state == 5:
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                x_mouse, y_mouse = event.pos

                if (10 + stop_button.get_width() > x_mouse > 10 and
                    10 + stop_button.get_height() > y_mouse > 10):
                    print(f"Go button clicked!")
                    game_state = 0

                elif (80 + replay_button.get_width() > x_mouse > 80 and
                    170 + replay_button.get_height() > y_mouse > 190):
                    print(f"replay button clicked!")
                    restart()
                    print(f"loading level: {level.number}")
                    level.load_level()
                    game_state = 0
                    bird_path = []
                    score = 0

                elif (105 + menu_button.get_width() > x_mouse > 105 and
                    307 + menu_button.get_height() > y_mouse > 307):
                    print(f"menu button clicked!")

                elif (60 + sound_button.get_width() > x_mouse > 55 and
                    565 + sound_button.get_height() > y_mouse > 565):
                    print(f"sound button clicked!")
                    sound_on = not sound_on

        elif game_state == 4:
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                x_mouse, y_mouse = event.pos

                if (665 + next_button.get_width() > x_mouse > 665 and
                    480 + next_button.get_height() > y_mouse > 480):
                    print("Next button clicked!")
                    restart()
                    level.number += 1
                    game_state = 0
                    level.load_level()
                    score = 0
                    bird_path = []
                    bonus_score_once = True

                # restart button
                elif (559 + replay_button.get_width() > x_mouse > 559 and
                    486 + replay_button.get_height() > y_mouse > 486):
                    restart()
                    print(f"loading level: {level.number}")
                    level.load_level()
                    game_state = 0
                    bird_path = []
                    score = 0

                # menu button
                elif (452 + menu_button.get_width() > x_mouse > 452 and
                    490 + menu_button.get_height() > y_mouse > 490):
                    print("Menu button clicked!")
                    pass

        elif game_state == 3:
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                x_mouse, y_mouse = event.pos

                # restart button
                if (559 + replay_button.get_width() > x_mouse > 559 and
                    486 + replay_button.get_height() > y_mouse > 486):
                    # restart the current level
                    restart()
                    print(f"loading level: {level.number}")
                    level.load_level()
                    game_state = 0
                    bird_path = []
                    score = 0

                # menu button
                elif (452 + menu_button.get_width() > x_mouse > 452 and
                    490 + menu_button.get_height() > y_mouse > 490):
                    print("Menu button clicked!")
                    pass

        elif game_state == 6:
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                x_mouse, y_mouse = event.pos
                # Add logic for clicking on level icons here if needed

    if game_state == 0:
        menu_open = False
        screen.fill((130,200,100))
        bg_scaled = pg.transform.scale(bg, (screen_width, screen_height))
        screen.blit(bg_scaled, (0, 0))

        # Input handling for shooting the bird (only when mouse is held down in the sling area)
        x_mouse, y_mouse = pg.mouse.get_pos()
        if pg.mouse.get_pressed()[0] and (110 < x_mouse < 170 and 250 < y_mouse < 400):
            mouse_pressed_to_shoot = True

        screen.blit(slingr,(120,370))
        # draw birds behind sling
        if level.number_of_birds > 0:
            for i in range(level.number_of_birds-1):
                x = 100-(i*35)
                screen.blit(sahur,(x,446))

        # draw sling behaviour
        if mouse_pressed_to_shoot and level.number_of_birds >= 0: # Allow drawing even if no birds left (for visual feedback)
            sling_action()

        else:
            if time.time()*1000-t1>300 and level.number_of_birds > 0: # Keep drawing if no birds left
                screen.blit(sahur,(130,370))

            else:
                pg.draw.line(screen, (0, 0, 0), (slingr_x+4, slingr_y+3), pu, 5)
                pg.draw.line(screen, (0, 0, 0), (slingl_x+2, slingl_y+13), pu, 5)

        bird_to_remove = []
        pig_to_remove = []

        # draw birds
        for bird in birds:
            if (bird.shape.body.position.y < 0 or bird.shape.body.position.x < -50 or
                bird.shape.body.position.x > screen_width + 50
                or time.time() - bird.launch_time > bird.lifespan):
                bird_to_remove.append(bird)

            else:
                p = to_pygame(bird.shape.body.position)
                x,y = p
                blit_x = x - sahur.get_width() // 2 # Center image on body
                blit_y = y - sahur.get_height() // 2
                screen.blit(sahur, (blit_x, blit_y))
                pg.draw.circle(screen, BLUE, p, int(bird.shape.radius), 2) # Draw the hitbox (for debugging)
                bird_path.append(p) # Add current position to path

        # Draw the bird's path
        for point in bird_path:
            if bird_path.index(point) % 5 == 0:
                pg.draw.circle(screen, WHITE, point, 3) # Adjust color and radius as needed

        # remove birds and pigs
        for bird in bird_to_remove:
            space.remove(bird.shape,bird.shape.body)
            birds.remove(bird)
            bird_path = [] # Clear the path when the bird is removed

        for pig in pig_to_remove:
            space.remove(pig.shape,pig.shape.body)
            pigs.remove(pig)

        # draw static line
        for line in static_lines:
            body = static_body
            pv1 = body.position+line.a.rotated(body.angle)
            pv2 = body.position+line.b.rotated(body.angle)

            p1 = to_pygame(pv1)
            p2 = to_pygame(pv2)

            pg.draw.lines(screen,TRANSP,False,[p1,p2])

        # draw pigs
        i = 0
        for pig in pigs:
            pig = pig.shape
            if pig.body.position.y < 0:
                pig_to_remove.append(pig)

            p = to_pygame(pig.body.position)
            x,y = p
            angle_degree = math.degrees(pig.body.angle)
            img = pg.transform.rotate(n11, angle_degree)
            w,h = img.get_size()
            x -= w*0.5
            y -= h*0.5
            screen.blit(img,(x,y))
            pg.draw.circle(screen,BLUE,p,int(pig.radius),2)

        # draw columns and beams
        for column in columns:
            column.draw_poly("columns",screen)

        for beam in beams:
            beam.draw_poly("beams",screen)

        # update physics 2 update / second
        dt = 1.0/50.0/2.0
        for x in range(2):
            space.step(dt)
        # draw secnd part of sling
        screen.blit(slingl,(120,370))

        # draw score
        score_font = bold_font.render("SCORE",1,WHITE)
        number_font = bold_font.render(str(score),1,WHITE)

        screen.blit(score_font,(1060,90))
        if score == 0:
            screen.blit(number_font,(1150,130))
        else:
            screen.blit(number_font,(1060,130))

        screen.blit(stop_button, (8,8))


    elif game_state == 5:
        # paused
        mouse_pressed_to_shoot = False
        menu_open = True
        if sound_on == True:
            screen.blit(menu_son,(0,0))
        else:
            screen.blit(menu_sof, (0, 0))

    elif game_state == 4:
        # level win
        mouse_pressed_to_shoot = False
        level_cleared = bold_font3.render("Level cleared!", 1, WHITE)
        score_level_cleared = bold_font2.render(str(score), 1, WHITE)
        if level.number_of_birds >= 0 and not pigs:  # Check if no pigs are left
            if bonus_score_once:
                score += (level.number_of_birds) * 10000
                bonus_score_once = False

        rect = pg.Rect(300, 0, 600, 650)  # Define the background rectangle for the cleared screen
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
        screen.blit(menu_button, (445,480))

    elif game_state == 3:
        # level lose
        mouse_pressed_to_shoot = False
        level_failed = bold_font3.render("Level failed!", 1, WHITE)
        score_level_failed = bold_font2.render(str(score), 1, WHITE)
        if level.number_of_birds >= 0 and not pigs:  # Check if no pigs are left
            if bonus_score_once:
                score += (level.number_of_birds) * 10000
                bonus_score_once = False

        rect = pg.Rect(300, 0, 600, 650)  # Define the background rectangle for the cleared screen
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
        screen.blit(menu_button, (445,480))

    elif game_state == 6:
        # levels menu
        if not levels_drawn:
            num_levels = 21  # Or however many levels you have
            screen.blit(pg.transform.scale(bg, (screen_width, screen_height)), (0, 0))
            x, y = 100, 50
            level_icon_rect = level_icon.get_rect() # Get the rect of the icon

            for i in range(num_levels):
                level_number = i + 1
                level_method_name = f"build_{level_number}"

                icon_x = x
                icon_y = y

                if level_method_name not in level.locked: # Assuming 'level.locked' contains method names to lock
                    icon = level_icon
                else:
                    icon = locked_level_icon

                


                level_text = str(level_number)
                level_font = bold_font3.render(level_text, 1, WHITE)
                text_rect = level_font.get_rect(center=level_icon_rect.center)
                screen.blit(icon, (icon_x, icon_y))
                screen.blit(level_font, (icon_x + text_rect.x, icon_y + text_rect.y))

                x += 151
                if level_number % 7 == 0:
                    y += 160
                    x = 100

        levels_drawn = True

        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                x_mouse, y_mouse = event.pos
                level_icon_rect = level_icon.get_rect() # Get icon rect for collision
                x_offset, y_offset = 100, 50
                for i in range(num_levels):
                    icon_x = x_offset + (i % 7) * 151
                    icon_y = y_offset + (i // 7) * 160
                    current_icon_rect = level_icon_rect.move(icon_x, icon_y)
                    level_number = i + 1
                    level_method_name = f"load_level_{level_number}"

                    if current_icon_rect.collidepoint(x_mouse, y_mouse) and level_method_name not in level.locked:
                        print(f"Clicked on level {level_number}")
                        restart() # Ensure previous level is cleared
                        level_loader = getattr(level, level_method_name, None)
                        if level_loader:
                            level_loader() # Call the specific load_level_X method
                            level.number = level_number -1 # Update level number if needed
                            game_state = 0
                            levels_drawn = False # Reset for next visit
                            bird_path = []
                            score = 0
                            bonus_score_once = True
                        break # Exit the loop after a click

                if (101 + menu_button.get_width() > x_mouse > 101 and
                    51 + menu_button.get_height() > y_mouse > 51):
                    game_state = 0
                    levels_drawn = False # Reset for next visit
                

    pg.display.flip()
    clock.tick(50)
    pg.display.set_caption("Angry Birds")

pg.quit()
sys.exit()