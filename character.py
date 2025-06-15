import pymunk as pm
from pymunk import Vec2d
import math
import time
import pygame as pg
import os # Import the os module
from Polygon import Polygon # Assuming Polygon.py is in the same directory
from utils import load_resource


class Bird():
    
    def __init__(self,distance,angle,x,y,space,screen_height, screen_width, level: 'Level', impulse_factor=45): # Added impulse_factor, type hint as string
        # pg.display.init() # Pygame display should be initialized once in the main game file
        # Access the 'scale' attribute from the specific bird subclass (e.g., Sahur.scale)
        # This 'scale' defines the bird's design dimensions in world units.
        design_width, design_height = self.__class__.scale
        # Use the smaller dimension to determine the radius for the circular physics body
        physics_radius = min(design_width, design_height) / 2.0

        self.life = 20
        mass = 10
        inertia = pm.moment_for_circle(mass, 0, physics_radius, (0,0))
        body = pm.Body(mass,inertia)

        body.position = x,y
        power = distance * impulse_factor # Use the passed impulse_factor
        impulse = power*Vec2d(1,0)
        angle = -angle
        body.apply_impulse_at_local_point(impulse.rotated(angle))
        shape = pm.Circle(body, physics_radius, (0,0))
        shape.elasticity = 0.2 # Slightly increased elasticity
        shape.friction = 0.5
        shape.collision_type = 0
        space.add(body,shape)
        self.body = body
        self.shape = shape
        self.launch_time = time.time() *1000
        self.lifespan = 7
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.level = level
        self.in_water_flag = False # For water physics interaction
        
class Sahur(Bird):
    def __init__(self, distance, angle, x, y, space, screen_height, screen_width, level: 'Level', impulse_factor): # Added impulse_factor, type hint as string
        super().__init__(distance, angle, x, y, space, screen_height, screen_width, level, impulse_factor) # Pass impulse_factor
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
        if hasattr(self, 'ability_polygon') and self.ability_polygon:
            # Remove from Pymunk space if it's there and has physics components
            if self.ability_polygon.body and self.ability_polygon.shape and \
               hasattr(self.level, 'space') and self.ability_polygon.shape in self.level.space.shapes:
                self.level.space.remove(self.ability_polygon.shape, self.ability_polygon.body)
            
            # Remove from game list if it's there
            if hasattr(self.level, 'columns') and self.ability_polygon in self.level.columns:
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
    def __init__(self, distance, angle, x, y, space, screen_height, screen_width, level: 'Level', impulse_factor): # Added impulse_factor, type hint as string
        super().__init__(distance, angle, x, y, space, screen_height, screen_width, level, impulse_factor) # Pass impulse_factor
        self.radius = 30
        self.fahigkeit_verwendet = False
        self.bird_hit_ground = False
        # The self.mass = 500 line was here, but it didn't affect the physics body's mass.
        # We will now correctly set the Pymunk body's mass.

        liri_mass = 30  # Liri's desired heavy mass
        self.body.mass = liri_mass
        # Recalculate moment of inertia for the new mass and existing radius
        self.body.moment = pm.moment_for_circle(liri_mass, 0, self.shape.radius, (0,0))

    img = "./resources/images/liri.png"
    scale = (30,30)

    def fahigkeit(self):
        print("fahigkeit verwendet!")

    
class Palocleves(Bird):
    def __init__(self, distance, angle, x, y, space, screen_height, screen_width, level: 'Level', impulse_factor): # Added impulse_factor, type hint as string
        super().__init__(distance, angle, x, y, space, screen_height, screen_width, level, impulse_factor) # Pass impulse_factor
        self.radius = 15
        self.fahigkeit_verwendet = False
        self.exploded = False # For self-destruction after ability
        self.bird_hit_ground = False

    img = "./resources/images/palocleves.png"
    scale = (50,50)

    # Explosion parameters for Palocleves
    EXPLOSION_RADIUS = 200 # Increased range further
    EXPLOSION_DAMAGE_PIGS = 125    # Decreased base damage to pigs
    EXPLOSION_DAMAGE_POLYS = 1000   # Decreased base damage to polygons
    EXPLOSION_KNOCKBACK_BASE = 7500 # Base knockback impulse
    
    def fahigkeit(self):
        if self.fahigkeit_verwendet:
            return None # Ability already used

        print("Palocleves fahigkeit verwendet! BOOM!")
        self.fahigkeit_verwendet = True
        self.exploded = True # Mark for removal by game loop in game.py

        destroyed_pigs_count = 0
        destroyed_polys_count = 0
        explosion_center = self.body.position

        # Access lists and space from self.level
        pigs_list = self.level.pigs
        columns_list = self.level.columns
        # Ensure beams, circles, and triangles are accessed from self.level if they exist
        # and provide empty lists as fallbacks if not.
        beams_list = self.level.beams
        circles_list = self.level.circles
        triangles_list = self.level.triangles
        space = self.level.space

        # --- Damage and Knockback PIGS ---
        pigs_to_remove_locally = []
        for pig_obj in list(pigs_list): # Iterate a copy for safe removal
            if not pig_obj.body: continue

            dist_vec = pig_obj.body.position - explosion_center
            distance = dist_vec.length

            if distance < self.EXPLOSION_RADIUS:
                damage_falloff = max(0, (self.EXPLOSION_RADIUS - distance) / self.EXPLOSION_RADIUS)
                actual_damage = self.EXPLOSION_DAMAGE_PIGS * damage_falloff
                pig_obj.life -= actual_damage

                if pig_obj.life <= 0 and pig_obj not in pigs_to_remove_locally:
                    pigs_to_remove_locally.append(pig_obj)
                    destroyed_pigs_count += 1

                if distance > 0: # Apply knockback
                    knockback_dir = dist_vec.normalized()
                    knockback_impulse_magnitude = self.EXPLOSION_KNOCKBACK_BASE * damage_falloff
                    pig_obj.body.apply_impulse_at_local_point(knockback_dir * knockback_impulse_magnitude, (0,0))

        for pig_to_remove in pigs_to_remove_locally:
            if pig_to_remove.body and pig_to_remove.shape and pig_to_remove.shape in space.shapes:
                space.remove(pig_to_remove.shape, pig_to_remove.body)
            if pig_to_remove in pigs_list:
                pigs_list.remove(pig_to_remove)

        # --- Damage and Knockback POLYGONS ---
        all_destructible_polys = list(columns_list) + list(beams_list) + list(circles_list) + list(triangles_list)
        polys_to_remove_locally = []

        for poly_obj in all_destructible_polys:
            if not poly_obj.body or poly_obj.body.body_type == pm.Body.STATIC:
                continue

            dist_vec = poly_obj.body.position - explosion_center
            distance = dist_vec.length

            if distance < self.EXPLOSION_RADIUS:
                damage_falloff = max(0, (self.EXPLOSION_RADIUS - distance) / self.EXPLOSION_RADIUS)
                actual_damage = self.EXPLOSION_DAMAGE_POLYS * damage_falloff
                poly_obj.life -= actual_damage

                if poly_obj.life <= 0 and poly_obj not in polys_to_remove_locally:
                    polys_to_remove_locally.append(poly_obj)
                    destroyed_polys_count += 1

                if distance > 0: # Apply knockback
                    knockback_dir = dist_vec.normalized()
                    knockback_impulse_magnitude = self.EXPLOSION_KNOCKBACK_BASE * damage_falloff
                    poly_obj.body.apply_impulse_at_local_point(knockback_dir * knockback_impulse_magnitude, (0,0))

        for poly_to_remove in polys_to_remove_locally:
            if poly_to_remove.body and poly_to_remove.shape and poly_to_remove.shape in space.shapes:
                space.remove(poly_to_remove.shape, poly_to_remove.body)
            poly_to_remove.in_space = False
            if poly_to_remove in columns_list: columns_list.remove(poly_to_remove)
            elif poly_to_remove in beams_list: beams_list.remove(poly_to_remove)
            elif poly_to_remove in circles_list: circles_list.remove(poly_to_remove)
            elif poly_to_remove in triangles_list: triangles_list.remove(poly_to_remove)

        # Play Palocleves' explosion sound after damage logic
        # Assuming sound_on and bird_ability_explosion_sounds_list are accessible
        # This part might be better handled in game.py where sounds are managed,
        # but if direct access is intended here:
        # if self.level.sound_on and self.level.bird_ability_explosion_sounds_list: # Example access
        #     random.choice(self.level.bird_ability_explosion_sounds_list).play()

        return {"pigs": destroyed_pigs_count, "polys": destroyed_polys_count}
    
class Trala(Bird):
    def __init__(self, distance, angle, x, y, space, screen_height, screen_width, level: 'Level', impulse_factor): # Added impulse_factor, type hint as string
        super().__init__(distance, angle, x, y, space, screen_height, screen_width, level, impulse_factor) # Pass impulse_factor
        self.radius = 15
        self.fahigkeit_verwendet = False
        self.bird_hit_ground = False
    img = "./resources/images/trala.png"
    scale = (50,50)
    
    def fahigkeit(self):
        print("fahigkeit verwendet!")
        if self.fahigkeit_verwendet:
            return None
        self.fahigkeit_verwendet = True
        self.body.velocity = (self.body.velocity.x*2, self.body.velocity.y*2)  # Stop horizontal movement
        
class Glorbo(Bird):
    def __init__(self, distance, angle, x, y, space, screen_height, screen_width, level: 'Level', impulse_factor): # Added impulse_factor, type hint as string
        super().__init__(distance, angle, x, y, space, screen_height, screen_width, level, impulse_factor) # Pass impulse_factor
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
        if self.fahigkeit_verwendet and self.is_growing: # Prevent re-triggering if already growing or fully used
            return None

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
    
        return None # Glorbo's ability doesn't directly score
        # Stop Glorbo's horizontal movement
        self.body.velocity = (0, self.body.velocity.y)

class Patapim(Bird):
    def __init__(self, distance, angle, x, y, space, screen_height, screen_width, level: 'Level', impulse_factor): # Added impulse_factor, type hint as string
        super().__init__(distance, angle, x, y, space, screen_height, screen_width, level, impulse_factor) # Pass impulse_factor
        self.radius = 15
        self.fahigkeit_verwendet = False
        self.bird_hit_ground = False
    img = "./resources/images/patapim.png"
    scale = (50,50)
    potion_img = "./resources/images/potion_projectile.png" # Path to the projectile's image
    
    def fahigkeit(self):
        # This method is now primarily a placeholder if called without parameters.
        # The actual potion launch with aiming is handled by fahigkeit_launch_potion.
        print("fahigkeit verwendet!")
        if self.fahigkeit_verwendet:
            return None
        self.fahigkeit_verwendet = True
        # The old logic for immediate downward throw is removed.
        # Potion creation and launch will be handled by a new method or by game.py directly
        # passing parameters to a launch-specific method.
        return None

    def launch_potion(self, launch_angle_rad):
        """
        Creates and launches the potion projectile based on a given angle and fixed power.
        This method is called from game.py when the player releases the mouse button after aiming.
        """
        # fahigkeit_verwendet should already be True, set when aiming started.

        projectile_radius = 10  # Radius for the bomb projectile
        projectile_visual_size = projectile_radius * 2 # Visual size for Polygon class
        projectile_mass = 2 # Mass for the projectile

        # Determine starting position for the projectile
        # Spawn slightly in front of Patapim based on its current orientation
        offset_distance = self.radius + projectile_radius + 2 # Small gap
        launch_offset_x = math.cos(self.body.angle) * offset_distance
        launch_offset_y = math.sin(self.body.angle) * offset_distance

        start_pos_x = self.body.position.x + launch_offset_x
        start_pos_y = self.body.position.y + launch_offset_y

        # Ensure projectile doesn't spawn below the ground (ground is at y=130)
        ground_y_level = 130 
        min_spawn_y_center = ground_y_level + projectile_radius
        final_start_pos_y = max(start_pos_y, min_spawn_y_center)
        projectile_start_pos = Vec2d(start_pos_x, final_start_pos_y)

        new_potion_polygon = Polygon(
            pos=projectile_start_pos,
            length=projectile_visual_size, 
            height=projectile_visual_size, 
            space=self.level.space,
            life=1000, # Projectile life (can be adjusted for balance)
            element_type="potions", 
            screen_height=self.screen_height, screen_width=self.screen_width,
            image_path=Patapim.potion_img, # Path to the projectile's image
            radius=projectile_radius, # Physics radius of the projectile
            mass=projectile_mass, # Mass of the projectile
            owner_bird=self # Pass self (Patapim instance) as the owner
        )
        
        POTION_THROW_IMPULSE_MAGNITUDE = 1000 # Reduced throwing strength
        impulse_vec_x = math.cos(launch_angle_rad) * POTION_THROW_IMPULSE_MAGNITUDE
        impulse_vec_y = math.sin(launch_angle_rad) * POTION_THROW_IMPULSE_MAGNITUDE
        new_potion_polygon.body.apply_impulse_at_local_point(Vec2d(impulse_vec_x, impulse_vec_y), (0,0))
        
        self.ability_polygon = new_potion_polygon # Store reference to the launched potion
        self.level.columns.append(new_potion_polygon) # Add to a list for management (e.g. 'columns' or a new 'projectiles' list)
        return None # Score is handled by projectile's collision
        
        
class Bomb(Bird):
    def __init__(self, distance, angle, x, y, space, screen_height, screen_width, level: 'Level', impulse_factor): # Added impulse_factor, type hint as string
        super().__init__(distance, angle, x, y, space, screen_height, screen_width, level, impulse_factor) # Pass impulse_factor
        self.radius = 15
        self.fahigkeit_verwendet = False
        self.bird_hit_ground = False
    img = "./resources/images/bomb.png"
    scale = (50,50)
    bomb_img = "./resources/images/bomb_projectile.png"
    
    def fahigkeit(self):
        print("fahigkeit verwendet!")
        if self.fahigkeit_verwendet: # Ability already used or projectile launched
            return None
        self.fahigkeit_verwendet = True
        # Bomb's ability creates a projectile; score comes from projectile's explosion

        # Define projectile properties
        projectile_radius = 10  # Radius for the bomb projectile
        projectile_visual_size = projectile_radius * 4 # Visual size for Polygon class
        projectile_mass = 2 # Mass for the projectile

        # Determine starting position for the projectile
        # Spawn slightly below the Bomb character to avoid immediate self-collision
        # and to make it look like it's being dropped.
        # self.radius is the Bomb bird's physics radius (15)
        vertical_offset_from_bird_center = self.radius + projectile_radius + 5 # e.g., 15 + 10 + 5 = 30
        
        start_pos_x = self.body.position.x
        calculated_start_pos_y = self.body.position.y - vertical_offset_from_bird_center
        
        # Ensure projectile doesn't spawn below the ground (ground is at y=130)
        ground_y_level = 130 
        min_spawn_y_center = ground_y_level + projectile_radius
        final_start_pos_y = max(calculated_start_pos_y, min_spawn_y_center)

        projectile_start_pos = Vec2d(start_pos_x, final_start_pos_y)

        new_bomb_polygon = Polygon(
            pos=projectile_start_pos,
            length=projectile_visual_size, 
            height=projectile_visual_size/2, 
            space=self.level.space,
            life=1000, # Projectile life (can be adjusted for balance)
            element_type="bombs", # The projectile is a circle
            screen_height=self.screen_height, screen_width=self.screen_width,
            image_path=Bomb.bomb_img, # Path to the projectile's image
            radius=projectile_radius, # Physics radius of the projectile
            mass=projectile_mass # Mass of the projectile
        )

        # Set projectile's initial velocity to match the Bomb character's velocity,
        # plus a small additional downward push to ensure separation.
        # Dampen the inherited velocity to make the projectile slower overall.
        velocity_inheritance_factor = 0.5
        character_velocity_x = self.body.velocity.x * velocity_inheritance_factor
        character_velocity_y = self.body.velocity.y * velocity_inheritance_factor
        additional_downward_velocity = -100 # Reduced from -500 for a gentler drop

        new_bomb_polygon.body.velocity = Vec2d(character_velocity_x, character_velocity_y + additional_downward_velocity)
        
        self.ability_polygon = new_bomb_polygon
        self.level.columns.append(new_bomb_polygon)
        return None # Score is handled by projectile's collision
        
        
        
        
class Pig():

    def __init__(self,x,y,space,radius,type):
        self.type = type
        # Initialize life to a default value first.
        # This ensures self.life always exists.
        self.life = 75  # Default life for "n" series pigs

        if self.type in ["n11","n21","n31","n41","n51", "n61"]: # Added "n61"
            self.life = 75 # Increased pig health
        elif self.type in ["m11","m21","m31","m41","m51"]:
            self.life = 150 # Increased pig health
        # Any other types not explicitly handled will keep the default self.life = 75
        self.mass = 5
        self.radius = radius
        inertia = pm.moment_for_circle(self.mass,0,self.radius,(0,0))
        self.body = pm.Body(self.mass,inertia)
        self.body.position = x, y
        self.shape = pm.Circle(self.body, self.radius)
        self.shape.elasticity = 0.2
        self.shape.friction = 4
        self.shape.collision_type = 1 # Collision type for pigs
        space.add(self.body, self.shape) # Add pig to the physics space
        self.in_water_flag = False # For water physics interaction


class Explosion(pg.sprite.Sprite):
    def __init__(self, center_pos_world, frame_folder_path, frame_duration_ms, scale_factor_tuple_px, to_pygame_func):
        super().__init__()
        self.frames = []
        self.load_frames(frame_folder_path)
        if not self.frames:
            print(f"Warning: No frames loaded for explosion from {frame_folder_path}")
            self.is_finished = True # Mark as finished if no frames
            self.image = pg.Surface((0,0)) # Dummy image
            self.rect = self.image.get_rect()
            return

        self.current_frame_index = 0
        self.image = self.frames[self.current_frame_index]
        
        self.center_pos_screen = to_pygame_func(center_pos_world)
        self.rect = self.image.get_rect(center=self.center_pos_screen)
        
        self.frame_duration = frame_duration_ms / 1000.0 # Convert ms to seconds
        self.last_frame_update_time = time.time()
        self.is_finished = False

        self.scale_frames(scale_factor_tuple_px)

    def load_frames(self, folder_path):
        try:
            resolved_folder_path = load_resource(folder_path)
            if os.path.isdir(resolved_folder_path):
                # Sorts frames based on the number at the end of the filename,
                # e.g., exp_0.png, exp_1.png, animation_frame_10.png.
                # The prefix before the underscore can vary.
                filenames = sorted(
                    [f for f in os.listdir(resolved_folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))],
                    key=lambda x: int(os.path.splitext(x)[0].split('_')[-1]) 
                )
                for filename in filenames:
                    full_path = os.path.join(resolved_folder_path, filename)
                    try:
                        frame = pg.image.load(full_path).convert_alpha()
                        self.frames.append(frame)
                    except pg.error as e:
                        print(f"Warning: Could not load explosion frame {filename}: {e}")
            else:
                print(f"Warning: Explosion frames folder not found: {resolved_folder_path}")
        except Exception as e:
            print(f"Error accessing explosion frames folder '{folder_path}': {e}")

    def scale_frames(self, scale_factor_tuple_px):
        scaled_frames_temp = [pg.transform.scale(frame, scale_factor_tuple_px) for frame in self.frames]
        self.frames = scaled_frames_temp
        if self.frames: # Ensure frames list is not empty after scaling
            self.image = self.frames[self.current_frame_index]
            self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        if self.is_finished or not self.frames:
            return

        current_time = time.time()
        if current_time - self.last_frame_update_time > self.frame_duration:
            self.current_frame_index += 1
            if self.current_frame_index >= len(self.frames):
                self.is_finished = True
                self.kill() # Remove from all sprite groups if finished
            else:
                self.image = self.frames[self.current_frame_index]
                self.rect = self.image.get_rect(center=self.rect.center) # Keep centered
                self.last_frame_update_time = current_time
        
        