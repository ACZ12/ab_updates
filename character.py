import pymunk as pm
from pymunk import Vec2d
import math
import time
import pygame as pg
from Polygon import Polygon

class Bird():
    
    def __init__(self,distance,angle,x,y,space,screen_height, screen_width, level):
        # pg.display.init() # Pygame display should be initialized once in the main game file
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
        shape.elasticity = 0.2
        shape.friction = 5
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
        self.ability_polygon_creation_time = 0 # Time when the bat was created
        self.bird_hit_ground = False
    bat_img = "./resources/images/bat.png"
    img = "./resources/images/sahur.png"
    scale = (30,30)
    
    
    def fahigkeit(self):
        print("fahigkeit verwendet!")

        # If Sahur already has an ability polygon, remove it first
        if hasattr(self, 'ability_polygon') and self.ability_polygon and self.ability_polygon in self.level.columns:
            if self.ability_polygon.body and self.ability_polygon.shape: # Ensure they exist
                self.level.space.remove(self.ability_polygon.shape, self.ability_polygon.body) # Remove from Pymunk space
            self.level.columns.remove(self.ability_polygon)
        self.ability_polygon = None # Clear previous reference
        
        # Calculate initial position with +70 x offset for Sahur's bat
        initial_pos_x = self.body.position.x + 70
        initial_pos_y = self.body.position.y
        bat_initial_pos = Vec2d(initial_pos_x, initial_pos_y)
        
        new_bat_polygon = Polygon(
            pos=bat_initial_pos, # Use the offset position
            length=20, height=130, # Longer and skinnier bat dimensions
            space=self.level.space,
            life=1000, # Bat life
            element_type="bats", # Special type for Sahur's bat
            screen_height=self.screen_height, screen_width=self.screen_width,
            # bird_pos is not used by Polygon for "bats", so removed for clarity
            image_path=Sahur.bat_img)
        self.level.columns.append(new_bat_polygon)
        self.ability_polygon = new_bat_polygon # Store reference to the new bat
        self.ability_polygon.body.angle = math.radians(160) # Set initial angle of the bat
        self.fahigkeit_verwendet = True
        self.ability_polygon_creation_time = time.time() # Record creation time
        
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
        self.is_ability_visually_active = False # Flag for visual effect (ability has been triggered)

        # Attributes for gradual growth
        self.initial_mass = self.body.mass # Capture initial mass from Bird's constructor
        self.is_growing = False
        self.ability_activation_time = 0.0 # Timestamp of ability activation
        self.growth_duration = 0.1  # seconds for full growth (FASTER)

        self.initial_visual_scale = 1.0
        # target_visual_scale will use ability_visual_scale_multiplier
        self.current_visual_scale_multiplier = 1.0 # Current visual size multiplier

        self.initial_physical_radius = 0.0 # To be set from self.shape.radius on activation
        # Target physical radius is calculated dynamically during growth
    img = "./resources/images/glorbo.png"
    scale = (50,50)
    ability_visual_scale_multiplier = 5 # Target multiplier for visual and physical size change
    
    def fahigkeit(self):
        print("fahigkeit verwendet!")

        # --- Initiate Gradual Growth ---
        # This check ensures growth starts only once per ability use.
        # fahigkeit_verwendet will be set to True at the end of this method.
        if not self.is_growing and not self.fahigkeit_verwendet:
            self.is_growing = True
            self.is_ability_visually_active = True # Mark that the ability's visual aspect is now active
            self.ability_activation_time = time.time()
            
            self.initial_physical_radius = self.shape.radius # Capture current Pymunk shape radius at activation
            self.current_visual_scale_multiplier = self.initial_visual_scale # Reset visual scale at activation

        self.fahigkeit_verwendet = True
    
        # Stop Glorbo's horizontal movement
        self.body.velocity = (0, self.body.velocity.y)

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
        self.shape.collision_type = 1 # Collision type for pigs
        space.add(self.body, self.shape) # Add pig to the physics space
        
        