# character.py

import pymunk as pm
from pymunk import Vec2d
import time
import pygame as pg


class Bird():
    
    def __init__(self,distance,angle,x,y,space):
        
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
        shape = pm.Circle(body,radius,(0,0))
        shape.elasticity = 0.5
        self.friction = 0.95
        shape.collision_type = 0
        space.add(body,shape)
        self.body = body
        self.shape = shape
        self.launch_time = time.time()
        self.lifespan = 7
        
class Sahur(Bird):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    img = "./resources/images/sahur.png"
    scale = (30,30)
        
class Liri(Bird):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    img = "./resources/images/liri.png"
    scale = (30,30)
    
class Palocleves(Bird):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    img = "./resources/images/palocleves.png"
    scale = (50,50)
        
        
        
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
        
        