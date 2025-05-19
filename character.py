# character.py

import pymunk as pm
from pymunk import Vec2d
import time
import pygame as pg
from Polygon import Polygon

class Bird():
    
    def __init__(self,distance,angle,x,y,space,screen_height, screen_width, level):
        
        pg.display.init()
        self.life = 20
        mass = 5
        radius = 15
        inertia = pm.moment_for_circle(mass,0,radius,(0,0))
        body = pm.Body(mass,inertia)
        
        body.position = x,y
        power = distance*53
        impulse = power*Vec2d(1,0)
        angle = -angle
        body.apply_impulse_at_local_point(impulse.rotated(angle))
        shape = pm.Circle(body,radius ,(0,0))
        shape.elasticity = 0.6
        shape.friction = 1
        shape.collision_type = 0
        space.add(body,shape)
        self.body = body
        self.shape = shape
        self.launch_time = time.time() *1000
        self.lifespan = 7
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.level = level
        
        
        
class Sahur(Bird):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.radius = 15
        self.fahigkeit_verwendet = False
        self.bird_hit_ground = False
    bat_img = "./resources/images/bat.png"
    img = "./resources/images/sahur.png"
    scale = (30,30)
    
    
    def fahigkeit(self):
        print("fahigkeit verwendet!")
        
        self.level.columns.append(Polygon(self.body.position,20,85,self.level.space, 1000, "bats", self.screen_height, self.screen_width))
        self.fahigkeit_verwendet = True
        
class Liri(Bird):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.radius = 15
        self.fahigkeit_verwendet = False
        self.bird_hit_ground = False
    img = "./resources/images/liri.png"
    scale = (30,30)
    
    def fahigkeit(self):
        print("fahigkeit verwendet!")
        self.fahigkeit_verwendet = True
    
class Palocleves(Bird):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.radius = 15
        self.fahigkeit_verwendet = False
        self.bird_hit_ground = False
    img = "./resources/images/palocleves.png"
    scale = (50,50)
    
    def fahigkeit(self):
        print("fahigkeit verwendet!")
        self.fahigkeit_verwendet = True
    
class Trala(Bird):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.radius = 15
        self.fahigkeit_verwendet = False
        self.bird_hit_ground = False
    img = "./resources/images/trala.png"
    scale = (50,50)
    
    def fahigkeit(self):
        print("fahigkeit verwendet!")
        self.fahigkeit_verwendet = True
        
class Glorbo(Bird):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.radius = 15
        self.fahigkeit_verwendet = False
        self.bird_hit_ground = False
    img = "./resources/images/glorbo.png"
    scale = (50,50)
    
    def fahigkeit(self):
        print("fahigkeit verwendet!")
        self.fahigkeit_verwendet = True
    
class Patapim(Bird):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.radius = 15
        self.fahigkeit_verwendet = False
        self.bird_hit_ground = False
    img = "./resources/images/patapim.png"
    scale = (50,50)
    
    def fahigkeit(self):
        print("fahigkeit verwendet!")
        self.fahigkeit_verwendet = True
        
class Bomb(Bird):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.radius = 15
        self.fahigkeit_verwendet = False
        self.bird_hit_ground = False
    img = "./resources/images/bomb.png"
    scale = (50,50)
    
    def fahigkeit(self):
        print("fahigkeit verwendet!")
        self.fahigkeit_verwendet = True
        
        
        
class Pig():

    def __init__(self,x,y,space,radius,type):
        self.type = type
        self.life = 50
        self.mass = 5
        self.radius = radius
        inertia = pm.moment_for_circle(self.mass,0,self.radius,(0,0))
        self.body = pm.Body(self.mass,inertia)
        self.body.position = x, y
        self.shape = pm.Circle(self.body, self.radius)
        self.shape.elasticity = 0.6
        self.shape.friction = 1
        self.shape.collision_type = 1
        space.add(self.body, self.shape) # Korrigierte Zeile
        self.body = self.body
        self.shape = self.shape
        
        