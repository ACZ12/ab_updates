from character import Pig
from Polygon import Polygon
import pymunk as pm # Import pymunk for creating static shapes
import random
from constants import EXPLODING_CRATE_HP, EXPLODING_CRATE_MASS, EXPLODING_CRATE_IMG_PATH # Import constants


wood_hp = 400  # Increased wood health
stone_hp = 1000 # Increased stone health
ice_hp = 150   # Increased ice health

# Default explosion parameters for new crates
exploding_crate_params_default = {
    "radius": 100, "damage_pigs": 150, "damage_polys": 1000, "knockback": 6000
}

class Level():
    
    def __init__(self, pigs, columns, beams, circles, triangles, space, screen_height, screen_width):
        self.pigs = pigs
        self.columns = columns
        self.beams = beams
        self.circles = circles
        self.triangles = triangles
        self.loch_extent_x = None # Will store (start_x, end_x) for a loch, or None
        self.static_terrain_shapes = [] # For custom static terrain like hills/lochs
        self.space = space
        self.number = 0
        self.number_of_birds = 4
        self.bool_space = False # For a space theme, currently unused.
        self.locked = [""] * 42 # Initialize all 42 levels as potentially locked (empty string means unlocked for level 1)
        
        # Star score thresholds.
        self.one_star = 20000
        self.two_star = 32500
        self.three_star = 45000
        
        self.loch_water_surface_y_override = None # For rectangular loch water rendering
        self.loch_rect_bottom_y_for_water_fill = None # For rectangular loch water rendering
        # self.bool_space = False # Unused space theme flag.
        
        self.screen_height = screen_height
        self.screen_width = screen_width
        
        self.base_width, self.base_height = 1200, 650
        self.scale_x = self.screen_width / self.base_width
        self.scale_y = self.screen_height / self.base_height

        # Set initial lock status (example: first few unlocked, rest need build_X methods)
        for i in range(2, 43): # Levels 2 to 42
            self.locked[i-1] = f"build_{i}" # Assumes build_1 is the first, so index is number-1

    def _add_static_terrain(self, shape_type, points_or_params, elasticity=0.6, friction=1.0, terrain_tag="unknown", radius=0.0):
        """Helper to create and add static terrain shapes."""
        static_shape = None
        if shape_type == "poly":
            # points_or_params is expected to be a list of vertices for Poly
            static_shape = pm.Poly(self.space.static_body, points_or_params, radius=radius)
        elif shape_type == "segment":
            # points_or_params is expected to be (p_start, p_end) for Segment
            p_start, p_end = points_or_params
            static_shape = pm.Segment(self.space.static_body, p_start, p_end, radius=radius)
        
        if static_shape:
            static_shape.elasticity = elasticity
            static_shape.friction = friction
            static_shape.collision_type = 3 # Ground collision type
            static_shape.terrain_type = terrain_tag 
            self.space.add(static_shape)
            self.static_terrain_shapes.append(static_shape)
    
    

    def scale_pos(self, x, y):
        return x * self.scale_x, y * self.scale_y


    def clear_level(self):
        self.pigs.clear()
        self.columns.clear()
        self.beams.clear()
        self.circles.clear()
        self.triangles.clear()
        # Clear custom static terrain shapes from the space and the list
        for shape_to_remove in self.static_terrain_shapes:
            if shape_to_remove in self.space.shapes: # Check if it's actually in the space
                self.space.remove(shape_to_remove)
        self.static_terrain_shapes.clear()
        self.loch_water_surface_y_override = None # Reset for next level
        self.loch_rect_bottom_y_for_water_fill = None # Reset for next level
        self.loch_extent_x = None # Reset loch extent when clearing level
        
    

    def build_0(self):
        self.number = 1
        self.level_birds = ["sahur","liri","trala","palocleves","bomb","patapim","glorbo"]
        self.number_of_birds = 7
        ground_y = 130.0 # Base ground level

        # --- Terrain for build_0 ---
        hill_vertices = [(300, ground_y), (400, 200), (500, ground_y)]
        self._add_static_terrain("poly", hill_vertices, terrain_tag="hill")

        loch_start_x, loch_end_x = 550, 750
        original_loch_dip_y = 70
        new_loch_dip_y = max(5, 2 * original_loch_dip_y - ground_y) # ground_y is 130
        loch_segments_points = [
            ((loch_start_x, ground_y), (loch_start_x + 50, new_loch_dip_y)),
            ((loch_start_x + 50, new_loch_dip_y), (loch_end_x - 50, new_loch_dip_y)),
            ((loch_end_x - 50, new_loch_dip_y), (loch_end_x, ground_y))
        ]
        for p_start, p_end in loch_segments_points:
            self._add_static_terrain("segment", (p_start, p_end), terrain_tag="loch", radius=1.0)
        self.loch_extent_x = (loch_start_x, loch_end_x)

        # Random pigs, placed away from the new terrain
        pig_radius_default = 10 # Assume a default pig radius for placement
        pig_ground_level_y = ground_y + pig_radius_default # Pigs sit on the ground
        pig_min_y = pig_ground_level_y # Pigs sit on the ground
        pig_max_y = 400 # Lowered max_y to keep them on screen (can be adjusted if pigs are on structures)
        pig_min_x = 800 # Place pigs after the loch
        pig_max_x = 1100
        num_pigs = 5  # Reduced number of pigs for test level
        for i in range(num_pigs): # These pigs are randomly placed, might overlap slightly
            ptype = random.choice(["n11","n21","n31","n41","n51","n61"]) # Added n61 to random choices
            pradius = random.choice([10,12,15])
            pig = Pig(random.randint(int(pig_min_x), int(pig_max_x)), random.randint(int(pig_min_y), int(pig_max_y)), self.space, pradius, ptype)
            pig.life = 200 # Standardized life for test pigs
            self.pigs.append(pig)

        # Example of a simple, larger structure for testing
        struct_base_x = 950
        struct_ground_y = ground_y # Structure sits on the main ground
        # Smaller elements, more complex structure
        col_h_s, col_w_s = 70, 25  # Column dimensions
        beam_h_s, beam_l_s = 15, 100  # Wider beam
        pig_r_s = 10

        # Layer 1
        y_col1 = ground_y + col_h_s/2
        self.columns.append(Polygon((struct_base_x - 60, y_col1), col_w_s, col_h_s, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood"))
        self.columns.append(Polygon((struct_base_x, y_col1), col_w_s, col_h_s, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood"))
        self.columns.append(Polygon((struct_base_x + 60, y_col1), col_w_s, col_h_s, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood"))
        
        y_beam1 = y_col1 + col_h_s/2 + beam_h_s/2
        # Replace the two beams with a single, wider beam
        # The original two beams (each 80 long, offset by 30) spanned from struct_base_x - 70 to struct_base_x + 70.
        single_roof_beam_length = 140 
        self.beams.append(Polygon((struct_base_x, y_beam1), single_roof_beam_length, beam_h_s, self.space, wood_hp, "beams", self.screen_height, self.screen_width, material_type="wood"))
        
        # Pig with small guards
        y_pig1 = y_beam1 + beam_h_s/2 + pig_r_s # Pig sits on the beam
        self.pigs.append(Pig(struct_base_x, y_pig1, self.space, pig_r_s, "n11")) # Pig remains
        # The two small guard columns that were here have been removed.
        # Add extra pig
        self.pigs.append(Pig(struct_base_x + 80, ground_y + pig_r_s, self.space, pig_r_s, "n61"))

        # Layer 2
        y_col2 = y_beam1 + beam_h_s/2 + col_h_s/2
        self.columns.append(Polygon((struct_base_x - 25, y_col2), col_w_s, col_h_s, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone")) # Columns are touching, which is fine
        self.columns.append(Polygon((struct_base_x + 25, y_col2), col_w_s, col_h_s, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone"))
        # Add a beam for the pig in Layer 2
        y_beam2_struct0 = y_col2 + col_h_s/2 + beam_h_s/2
        self.beams.append(Polygon((struct_base_x, y_beam2_struct0), beam_l_s, beam_h_s, self.space, stone_hp, "beams", self.screen_height, self.screen_width, material_type="stone"))
        self.pigs.append(Pig(struct_base_x, y_beam2_struct0 + beam_h_s/2 + pig_r_s, self.space, pig_r_s, "n21"))

        # Add an exploding crate to level 0
        exploding_crate_params = {
            "radius": 120, "damage_pigs": 180, "damage_polys": 1500, "knockback": 7000 # Explosion parameters
        }
        self.circles.append(Polygon( # Adding as a circle type for physics, but custom element_type
            pos=(struct_base_x + 100, ground_y + 12), # Position it somewhere, adjusted for new radius
            length=25, height=25, # Visual dimensions (smaller)
            space=self.space,
            life=EXPLODING_CRATE_HP,
            element_type="exploding_crate", # Custom type
            screen_height=self.screen_height, screen_width=self.screen_width,
            mass=EXPLODING_CRATE_MASS, radius=12, # Physics radius (smaller)
            image_path=EXPLODING_CRATE_IMG_PATH, # Use constant
            is_explosive_obj=True, explosion_params=exploding_crate_params
        ))
        # Add another exploding crate
        self.circles.append(Polygon(
            pos=(struct_base_x - 150, ground_y + 12), 
            length=25, height=25, space=self.space, life=EXPLODING_CRATE_HP,
            element_type="exploding_crate", screen_height=self.screen_height,
            screen_width=self.screen_width, mass=EXPLODING_CRATE_MASS, radius=12,
            image_path=EXPLODING_CRATE_IMG_PATH,
            is_explosive_obj=True, explosion_params=exploding_crate_params_default
        ))



        # New stable stone outpost for build_0
        outpost_x = 500 # Position before the loch
        outpost_ground_y = ground_y # Outpost sits on the main ground
        outpost_col_w, outpost_col_h = 30, 50
        outpost_beam_l, outpost_beam_h = 70, 20
        
        # Base columns
        y_outpost_col1 = outpost_ground_y + outpost_col_h/2
        self.columns.append(Polygon((outpost_x - 30, y_outpost_col1), outpost_col_w, outpost_col_h, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone")) # Increased gap slightly
        self.columns.append(Polygon((outpost_x + 30, y_outpost_col1), outpost_col_w, outpost_col_h, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone")) # Increased gap slightly
        
        # Roof beam
        y_outpost_beam1 = y_outpost_col1 + outpost_col_h/2 + outpost_beam_h/2
        self.beams.append(Polygon((outpost_x, y_outpost_beam1), outpost_beam_l, outpost_beam_h, self.space, stone_hp, "beams", self.screen_height, self.screen_width, material_type="stone")) # Beam sits on columns
        
        # Pig on top
        pig_r_outpost = 10
        self.pigs.append(Pig(outpost_x, y_outpost_beam1 + outpost_beam_h/2 + pig_r_outpost, self.space, pig_r_outpost, "n31"))
        # Extra pig near outpost
        self.pigs.append(Pig(outpost_x + 50, ground_y + pig_r_outpost, self.space, pig_r_outpost, "n41"))

    def build_1(self):
        self.number = 1
        self.level_birds = ["sahur","sahur","liri","trala","palocleves","bomb","patapim","glorbo"] # Level 1 (build_0) keeps its bird count
        self.number_of_birds = 8
        # locked = False # Unused.
        x_offset = 100 # Shift structures to the right

        ground_y = 130.0

        # Define positions and dimensions in BASE Pymunk world coordinates.
        # Scaling for display will be handled by the drawing functions.
        # --- Structure 1: Simple tower ---
        # Using smaller elements to build a larger, more complex tower
        base_x1 = 700 + x_offset
        col_h_s, col_w_s = 55, 12  # Even smaller columns for more complexity
        beam_h_s, beam_l_s = 12, 60 # Even smaller beams
        pig_r_sml, pig_r_med = 8, 10

        # Layer 1 (Wider base)
        y_col1 = ground_y + col_h_s/2 # Columns sit on the ground
        self.columns.append(Polygon((base_x1 - 50, y_col1), col_w_s, col_h_s, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood"))
        self.columns.append(Polygon((base_x1, y_col1), col_w_s, col_h_s, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood"))
        self.columns.append(Polygon((base_x1 + 50, y_col1), col_w_s, col_h_s, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood"))
        y_beam1 = y_col1 + col_h_s/2 + beam_h_s/2
        self.beams.append(Polygon((base_x1, y_beam1), beam_l_s + 40, beam_h_s, self.space, wood_hp, "beams", self.screen_height, self.screen_width, material_type="wood"))
        self.pigs.append(Pig(base_x1, y_beam1 + beam_h_s/2 + pig_r_med, self.space, pig_r_med, "n11")) # Pig sits on the beam
        # Extra pig
        self.pigs.append(Pig(base_x1 - 70, ground_y + pig_r_med, self.space, pig_r_med, "n61"))

        # Layer 2
        y_col2 = y_beam1 + beam_h_s/2 + col_h_s/2
        self.columns.append(Polygon((base_x1 - 35, y_col2), col_w_s, col_h_s, self.space, ice_hp, "columns", self.screen_height, self.screen_width, material_type="ice"))
        self.columns.append(Polygon((base_x1 + 35, y_col2), col_w_s, col_h_s, self.space, ice_hp, "columns", self.screen_height, self.screen_width, material_type="ice"))
        y_beam2 = y_col2 + col_h_s/2 + beam_h_s/2
        self.beams.append(Polygon((base_x1, y_beam2), beam_l_s + 20, beam_h_s, self.space, ice_hp, "beams", self.screen_height, self.screen_width, material_type="ice"))
        self.pigs.append(Pig(base_x1, y_beam2 + beam_h_s/2 + pig_r_sml, self.space, pig_r_sml, "n21")) # Pig sits on the beam
        
        # Layer 3
        y_col3 = y_beam2 + beam_h_s/2 + col_h_s/2
        self.columns.append(Polygon((base_x1 - 25, y_col3), col_w_s, col_h_s, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood"))
        self.columns.append(Polygon((base_x1 + 25, y_col3), col_w_s, col_h_s, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood"))
        y_beam3 = y_col3 + col_h_s/2 + beam_h_s/2
        self.beams.append(Polygon((base_x1, y_beam3), beam_l_s + 10, beam_h_s, self.space, wood_hp, "beams", self.screen_height, self.screen_width, material_type="wood"))
        self.pigs.append(Pig(base_x1, y_beam3 + beam_h_s/2 + pig_r_sml, self.space, pig_r_sml, "n51")) # Pig sits on the beam
        # Add guards for the top pig
        guard_h_top = 15; guard_w_top = 5
        self.columns.append(Polygon((base_x1 - (beam_l_s + 10)/2 + guard_w_top, y_beam3 + beam_h_s/2 + guard_h_top/2), guard_w_top, guard_h_top, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood")) # Guards sit on the beam
        self.columns.append(Polygon((base_x1 + (beam_l_s + 10)/2 - guard_w_top, y_beam3 + beam_h_s/2 + guard_h_top/2), guard_w_top, guard_h_top, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood"))

        # --- Structure 2: Wider platform ---
        base_x2 = 950 + x_offset
        col_h_s2, col_w_s2 = 70, 20 # Smaller columns
        beam_h_s2, beam_l_s2_short, beam_l_s2_long = 20, 60, 120 # Smaller beams
        pig_r_sml2, pig_r_med2, pig_r_lrg2 = 8, 10, 12

        # Layer 1 (Stone base)
        y_col1_s2 = ground_y + col_h_s2/2 # Columns sit on the ground
        self.columns.append(Polygon((base_x2 - 70, y_col1_s2), col_w_s2, col_h_s2, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone"))
        self.columns.append(Polygon((base_x2, y_col1_s2), col_w_s2, col_h_s2, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone"))
        self.columns.append(Polygon((base_x2 + 70, y_col1_s2), col_w_s2, col_h_s2, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone"))
        
        y_beam1_s2 = y_col1_s2 + col_h_s2/2 + beam_h_s2/2
        self.beams.append(Polygon((base_x2 - 35, y_beam1_s2), beam_l_s2_short + 10, beam_h_s2, self.space, stone_hp, "beams", self.screen_height, self.screen_width, material_type="stone")) # Beams sit on columns
        self.beams.append(Polygon((base_x2 + 35, y_beam1_s2), beam_l_s2_short + 10, beam_h_s2, self.space, stone_hp, "beams", self.screen_height, self.screen_width, material_type="stone")) # Beams sit on columns
        
        y_pig1_s2 = y_beam1_s2 + beam_h_s2/2 + pig_r_sml2
        self.pigs.append(Pig(base_x2 - 30+20, y_pig1_s2, self.space, pig_r_sml2, "n31"))
        self.pigs.append(Pig(base_x2 + 30+20, y_pig1_s2, self.space, pig_r_sml2, "n41"))

        # Topper
        col_h_top_s, col_w_top_s = 60, 15
        beam_h_top_s, beam_l_top_s = 15, 70

        y_col_top_s2 = y_beam1_s2 + beam_h_s2/2 + col_h_top_s/2
        self.columns.append(Polygon((base_x2 - 30, y_col_top_s2), col_w_top_s, col_h_top_s, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood")) # Columns sit on beams
        self.columns.append(Polygon((base_x2 + 30, y_col_top_s2), col_w_top_s, col_h_top_s, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood"))
        y_beam_top_s2 = y_col_top_s2 + col_h_top_s/2 + beam_h_top_s/2
        self.beams.append(Polygon((base_x2, y_beam_top_s2), beam_l_top_s + 10, beam_h_top_s, self.space, wood_hp, "beams", self.screen_height, self.screen_width, material_type="wood"))
        y_pig_top_s2 = y_beam_top_s2 + beam_h_top_s/2 + pig_r_lrg2 
        self.pigs.append(Pig(base_x2, y_pig_top_s2, self.space, pig_r_lrg2, "n51"))
        # Guards for this pig too
        self.columns.append(Polygon((base_x2 - (beam_l_top_s + 10)/2 + guard_w_top, y_beam_top_s2 + beam_h_top_s/2 + guard_h_top/2), guard_w_top, guard_h_top, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood")) # Guards sit on the beam
        self.columns.append(Polygon((base_x2 + (beam_l_top_s + 10)/2 - guard_w_top, y_beam_top_s2 + beam_h_top_s/2 + guard_h_top/2), guard_w_top, guard_h_top, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood"))
        # Extra pig for structure 2
        self.pigs.append(Pig(base_x2 + 100, ground_y + pig_r_med2, self.space, pig_r_med2, "n11"))


        # --- Floating elements ---
        # The floating circle and triangle have been removed as per request.

        # --- Static Terrain Example: A Hill ---
        # This level already has terrain defined, so we use it.
        hill_peak_y = 230
        hill_start_x = 350
        hill_peak_x = 450
        hill_end_x = 550

        hill_vertices = [
            (hill_start_x, ground_y),  # Bottom-left
            (hill_peak_x, hill_peak_y),    # Peak
            (hill_end_x, ground_y)     # Bottom-right
        ]
        self._add_static_terrain("poly", hill_vertices, terrain_tag="hill")

        # Loch moved to be between the hill and the first structure
        loch_start_x = 560
        loch_dip_x1 = 570
        loch_dip_x2 = 650
        loch_end_x = 660
        loch_dip_y = 50

        loch_segments_points = [
            ((loch_start_x, ground_y), (loch_dip_x1, loch_dip_y)),
            ((loch_dip_x1, loch_dip_y), (loch_dip_x2, loch_dip_y)), # Flat bottom segment
            ((loch_dip_x2, loch_dip_y), (loch_end_x, ground_y))
        ]
        for p_start, p_end in loch_segments_points:
            self._add_static_terrain("segment", (p_start, p_end), terrain_tag="loch", radius=1.0, elasticity=0.5, friction=0.8)
        self.loch_extent_x = (loch_start_x, loch_end_x) # Store loch x-boundaries

        # Add an exploding crate to level 1
        exploding_crate_params_lvl1 = {
            "radius": 150, "damage_pigs": 200, "damage_polys": 1800, "knockback": 7500
        }
        self.circles.append(Polygon(
            pos=(base_x2 + 50, ground_y + 15), # Position near the second structure, adjusted for radius (15)
            length=30, height=30, # Visual dimensions (smaller)
            space=self.space,
            life=EXPLODING_CRATE_HP, # Use constant
            element_type="exploding_crate",
            screen_height=self.screen_height, screen_width=self.screen_width,
            mass=EXPLODING_CRATE_MASS, radius=15, # Physics radius (smaller)
            image_path=EXPLODING_CRATE_IMG_PATH, # Use constant
            is_explosive_obj=True, explosion_params=exploding_crate_params_lvl1))
        
        # Add another exploding crate
        self.circles.append(Polygon(
            pos=(base_x1 - 100, ground_y + 15), 
            length=30, height=30, space=self.space, life=EXPLODING_CRATE_HP,
            element_type="exploding_crate", screen_height=self.screen_height,
            screen_width=self.screen_width, mass=EXPLODING_CRATE_MASS, radius=15,
            image_path=EXPLODING_CRATE_IMG_PATH,
            is_explosive_obj=True, explosion_params=exploding_crate_params_default
        ))
        # New stable guard post for build_1
        guard_post_x = hill_start_x + (hill_peak_x - hill_start_x) / 2 # On the slope of the first hill
        guard_post_y_base = ground_y + (hill_peak_y - ground_y) / 2 # Mid-slope

        g_col_w, g_col_h = 25, 40
        g_beam_l, g_beam_h = 60, 15
        
        y_g_col1 = guard_post_y_base + g_col_h/2
        self.columns.append(Polygon((guard_post_x - 20, y_g_col1), g_col_w, g_col_h, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone")) # Columns sit on the hill slope
        self.columns.append(Polygon((guard_post_x + 20, y_g_col1), g_col_w, g_col_h, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone"))
        
        y_g_beam1 = y_g_col1 + g_col_h/2 + g_beam_h/2
        self.beams.append(Polygon((guard_post_x, y_g_beam1), g_beam_l, g_beam_h, self.space, stone_hp, "beams", self.screen_height, self.screen_width, material_type="stone")) # Beam sits on columns
        
        pig_r_g = 10
        self.pigs.append(Pig(guard_post_x, y_g_beam1 + g_beam_h/2 + pig_r_g, self.space, pig_r_g, "m11")) # Strong pig

        if self.bool_space:
            self.number_of_birds = 8
            
        


    def build_2(self):
        self.number = 2
        self.level_birds = ["sahur","liri","trala"] # Reduced birds
        self.number_of_birds = 3
        # locked = True # Unused.
        ground_y = 130.0

        # --- Terrain for build_2 ---
        hill_vertices = [(350, ground_y), (450, 210), (550, ground_y)]
        self._add_static_terrain("poly", hill_vertices, terrain_tag="hill")

        loch_start_x, loch_end_x = 580, 720 # Adjusted to not overlap tower too much
        original_loch_dip_y = 60
        new_loch_dip_y = max(5, 2 * original_loch_dip_y - ground_y)
        loch_segments_points = [
            ((loch_start_x, ground_y), (loch_start_x + 40, new_loch_dip_y)),
            ((loch_start_x + 40, new_loch_dip_y), (loch_end_x - 40, new_loch_dip_y)),
            ((loch_end_x - 40, new_loch_dip_y), (loch_end_x, ground_y))
        ]
        for p_start, p_end in loch_segments_points:
            self._add_static_terrain("segment", (p_start, p_end), terrain_tag="loch", radius=1.0)
        self.loch_extent_x = (loch_start_x, loch_end_x)

        # --- Tall multi-material tower ---
        base_x = 880 # Shifted slightly right
        col_h_s, col_w_s = 60, 15 # Smaller elements
        beam_h_s, beam_l_s_base, beam_l_s_mid, beam_l_s_top = 15, 100, 80, 60 # Smaller beams, varying length
        pig_r_sml, pig_r_med, pig_r_lrg = 8, 10, 12

        current_y = ground_y + col_h_s/2

        # Layer 1 (Stone Base)
        self.columns.append(Polygon((base_x - 50, current_y), col_w_s, col_h_s, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone")) # Wider
        self.columns.append(Polygon((base_x, current_y), col_w_s, col_h_s, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone")) # Central support
        self.columns.append(Polygon((base_x + 50, current_y), col_w_s, col_h_s, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone")) # Wider
        current_y += col_h_s/2 + beam_h_s/2
        self.beams.append(Polygon((base_x, current_y), beam_l_s_base + 20, beam_h_s, self.space, stone_hp, "beams", self.screen_height, self.screen_width, material_type="stone")) # Wider
        self.pigs.append(Pig(base_x, current_y + beam_h_s/2 + pig_r_med, self.space, pig_r_med, "n11"))
        current_y += beam_h_s/2 + col_h_s/2 # Prepare for next layer of columns

        # Layer 2 (Ice Middle)
        self.columns.append(Polygon((base_x - 35, current_y), col_w_s, col_h_s, self.space, ice_hp, "columns", self.screen_height, self.screen_width, material_type="ice")) # Wider
        self.columns.append(Polygon((base_x + 35, current_y), col_w_s, col_h_s, self.space, ice_hp, "columns", self.screen_height, self.screen_width, material_type="ice")) # Wider
        current_y += col_h_s/2 + beam_h_s/2
        self.beams.append(Polygon((base_x, current_y), beam_l_s_mid + 10, beam_h_s, self.space, ice_hp, "beams", self.screen_height, self.screen_width, material_type="ice")) # Wider
        self.pigs.append(Pig(base_x, current_y + beam_h_s/2 + pig_r_sml, self.space, pig_r_sml, "n21"))
        current_y += beam_h_s/2 + col_h_s/2

        # Layer 3 (Wood Top)
        self.columns.append(Polygon((base_x - 25, current_y), col_w_s, col_h_s, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood")) # Wider
        self.columns.append(Polygon((base_x + 25, current_y), col_w_s, col_h_s, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood")) # Wider
        current_y += col_h_s/2 + beam_h_s/2
        self.beams.append(Polygon((base_x, current_y), beam_l_s_top, beam_h_s, self.space, wood_hp, "beams", self.screen_height, self.screen_width, material_type="wood"))
        self.pigs.append(Pig(base_x+20, current_y + beam_h_s/2 + pig_r_lrg, self.space, pig_r_lrg, "n31"))

        # Layer 4 (Small topper)
        current_y += beam_h_s/2 + col_h_s/2
        self.columns.append(Polygon((base_x, current_y), col_w_s, col_h_s, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone"))
        # Add a small beam for the top pig for stability
        topper_beam_h = 10
        topper_beam_l = 30 # Wider than column
        y_topper_beam = current_y + col_h_s/2 + topper_beam_h/2
        self.beams.append(Polygon((base_x, y_topper_beam), topper_beam_l, topper_beam_h, self.space, stone_hp, "beams", self.screen_height, self.screen_width, material_type="stone"))
        self.pigs.append(Pig(base_x, y_topper_beam + topper_beam_h/2 + pig_r_sml, self.space, pig_r_sml, "n51"))
        # Extra pig
        self.pigs.append(Pig(base_x + 100, ground_y + pig_r_lrg, self.space, pig_r_lrg, "n61"))
        
        # --- Enhanced Small side structure (Stone Bunker) ---
        side_x = 780 # Moved to avoid loch
        bunker_col_w, bunker_col_h = 30, 45 # Sturdier columns
        bunker_beam_l, bunker_beam_h = 70, 20 # Sturdy roof

        y_bunker_col = ground_y + bunker_col_h/2
        self.columns.append(Polygon((side_x - 25, y_bunker_col), bunker_col_w, bunker_col_h, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone"))
        self.columns.append(Polygon((side_x + 25, y_bunker_col), bunker_col_w, bunker_col_h, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone"))
        
        y_bunker_roof = y_bunker_col + bunker_col_h/2 + bunker_beam_h/2
        self.beams.append(Polygon((side_x, y_bunker_roof), bunker_beam_l, bunker_beam_h, self.space, stone_hp, "beams", self.screen_height, self.screen_width, material_type="stone"))
        
        # Pig inside the bunker (slightly lower)
        pig_bunker_r = 10
        self.pigs.append(Pig(side_x, y_bunker_col + pig_bunker_r - 5, self.space, pig_bunker_r, "n41"))

        # Small wood triangle on top of bunker for visual
        tri_bunker_base, tri_bunker_h = 40, 20
        tri_bunker_points = [(-tri_bunker_base/2, -tri_bunker_h/2), (tri_bunker_base/2, -tri_bunker_h/2), (0, tri_bunker_h/2)]
        self.triangles.append(Polygon((side_x, y_bunker_roof + bunker_beam_h/2 + tri_bunker_h/2), tri_bunker_base, tri_bunker_h, self.space, wood_hp, "triangles", self.screen_height, self.screen_width, triangle_points=tri_bunker_points, material_type="wood"))

        # Add an exploding crate
        self.circles.append(Polygon(
            pos=(base_x - 150, ground_y + 12),
            length=25, height=25, space=self.space, life=EXPLODING_CRATE_HP,
            element_type="exploding_crate", screen_height=self.screen_height,
            screen_width=self.screen_width, mass=EXPLODING_CRATE_MASS, radius=12,
            image_path=EXPLODING_CRATE_IMG_PATH,
            is_explosive_obj=True, explosion_params=exploding_crate_params_default
        ))

        if self.bool_space:
            self.number_of_birds = 8
    
    
    def build_3(self):
        self.number = 3
        self.level_birds = ["bomb","patapim"] # Reduced birds
        self.number_of_birds = 2
        ground_y = 130.0

        # --- Terrain for build_3: Island Level ---
        # Launch-side small hill
        launch_hill_verts = [(250, ground_y), (320, 170), (390, ground_y)]
        self._add_static_terrain("poly", launch_hill_verts, terrain_tag="hill")

        # Define launch_side_struct_x and y early as they are used by crate placement
        launch_side_struct_x = launch_hill_verts[1][0] # Peak of launch hill
        launch_side_struct_y = launch_hill_verts[1][1] # Peak Y
        self._add_static_terrain("poly", launch_hill_verts, terrain_tag="hill")

        # Island
        island_center_x = 750
        island_width = 250
        island_height_above_water = 20 # How much the flat top of island is above ground_y
        island_top_y = ground_y + island_height_above_water
        
        island_vertices = [
            (island_center_x - island_width/2, ground_y - 10), # Base slightly submerged
            (island_center_x + island_width/2, ground_y - 10),
            (island_center_x + island_width/2 - 20, island_top_y), # Sloped sides
            (island_center_x - island_width/2 + 20, island_top_y)
        ]
        self._add_static_terrain("poly", island_vertices, terrain_tag="island")
        loch_start_x, loch_end_x = 400, 1100 # Wide loch surrounding the island approach
        original_loch_dip_y = 70
        new_loch_dip_y = max(5, 2 * original_loch_dip_y - ground_y)
        loch_segments_points = [
            ((loch_start_x, ground_y), (loch_start_x + 50, new_loch_dip_y)),
            ((loch_start_x + 50, new_loch_dip_y), (loch_end_x - 50, new_loch_dip_y)),
            ((loch_end_x - 50, new_loch_dip_y), (loch_end_x, ground_y))
        ]
        for p_start, p_end in loch_segments_points:
            self._add_static_terrain("segment", (p_start, p_end), terrain_tag="loch", radius=1.0)
        self.loch_extent_x = (loch_start_x, loch_end_x)

        # Structure on the island
        base_x = island_center_x
        col_h_s, col_w_s = 65, 20 # Slightly wider columns for base
        beam_h_s, beam_l_s = 20, 100 # Slightly wider beams
        pig_r_sml, pig_r_med, pig_r_lrg = 10, 12, 14

        # Layer 1 (Wider Stone Base)
        y_col1 = island_top_y + col_h_s/2
        self.columns.append(Polygon((base_x - 50, y_col1), col_w_s, col_h_s, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone"))
        self.columns.append(Polygon((base_x + 50, y_col1), col_w_s, col_h_s, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone"))
        y_beam1 = y_col1 + col_h_s/2 + beam_h_s/2
        self.beams.append(Polygon((base_x, y_beam1), beam_l_s + 20, beam_h_s, self.space, stone_hp, "beams", self.screen_height, self.screen_width, material_type="stone"))
        self.pigs.append(Pig(base_x, y_beam1 + beam_h_s/2 + pig_r_sml, self.space, pig_r_sml, "n11"))
        
        # Layer 2 (Wood Middle)
        y_col2 = y_beam1 + beam_h_s/2 + col_h_s/2 
        self.columns.append(Polygon((base_x - 40, y_col2), col_w_s-2, col_h_s, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood"))
        self.columns.append(Polygon((base_x + 40, y_col2), col_w_s-2, col_h_s, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood"))
        y_beam2 = y_col2 + col_h_s/2 + beam_h_s/2
        self.beams.append(Polygon((base_x, y_beam2), beam_l_s, beam_h_s, self.space, wood_hp, "beams", self.screen_height, self.screen_width, material_type="wood"))
        self.pigs.append(Pig(base_x, y_beam2 + beam_h_s/2 + pig_r_med, self.space, pig_r_med, "n21"))

        # Layer 3 (Ice Top)
        y_col3 = y_beam2 + beam_h_s/2 + col_h_s/2
        self.columns.append(Polygon((base_x - 30, y_col3), col_w_s-4, col_h_s, self.space, ice_hp, "columns", self.screen_height, self.screen_width, material_type="ice"))
        self.columns.append(Polygon((base_x + 30, y_col3), col_w_s-4, col_h_s, self.space, ice_hp, "columns", self.screen_height, self.screen_width, material_type="ice"))
        y_beam3 = y_col3 + col_h_s/2 + beam_h_s/2
        self.beams.append(Polygon((base_x, y_beam3), beam_l_s - 20, beam_h_s, self.space, ice_hp, "beams", self.screen_height, self.screen_width, material_type="ice"))
        self.pigs.append(Pig(base_x, y_beam3 + beam_h_s/2 + pig_r_lrg, self.space, pig_r_lrg, "n41")) 
        # Extra pig
        self.pigs.append(Pig(base_x + 120, island_top_y + pig_r_med, self.space, pig_r_med, "n51"))
        
        # A pig on the ground near the structure
        # self.pigs.append(Pig(base_x + beam_l_s/2 + 30, ground_y + pig_r_sml, self.space, pig_r_sml, "n31")) # Removed for island theme

        # Add an exploding crate to level 3 on the island structure
        exploding_crate_params_lvl3 = {
            "radius": 130, "damage_pigs": 190, "damage_polys": 1600, "knockback": 7200
        }
        self.circles.append(Polygon(
            pos=(base_x - 20, island_top_y + 14), # Position it on the island, adjusted for new radius
            length=28, height=28, # Visual dimensions (smaller)
            space=self.space,
            life=EXPLODING_CRATE_HP,
            element_type="exploding_crate",
            screen_height=self.screen_height, screen_width=self.screen_width,
            mass=EXPLODING_CRATE_MASS, radius=14, # Physics radius (smaller)
            image_path=EXPLODING_CRATE_IMG_PATH,
            is_explosive_obj=True, explosion_params=exploding_crate_params_lvl3))
        
        # Add another exploding crate
        self.circles.append(Polygon(
            pos=(launch_side_struct_x + 80, launch_hill_verts[1][1] + 14), 
            length=28, height=28, space=self.space, life=EXPLODING_CRATE_HP,
            element_type="exploding_crate", screen_height=self.screen_height,
            screen_width=self.screen_width, mass=EXPLODING_CRATE_MASS, radius=14,
            image_path=EXPLODING_CRATE_IMG_PATH,
            is_explosive_obj=True, explosion_params=exploding_crate_params_default
        ))

        # Small stable structure on the launch side hill
        lss_col_w, lss_col_h = 20, 30
        lss_beam_l, lss_beam_h = 50, 15
        self.columns.append(Polygon((launch_side_struct_x, launch_side_struct_y + lss_col_h/2), lss_col_w, lss_col_h, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone"))
        self.beams.append(Polygon((launch_side_struct_x, launch_side_struct_y + lss_col_h + lss_beam_h/2), lss_beam_l, lss_beam_h, self.space, stone_hp, "beams", self.screen_height, self.screen_width, material_type="stone"))
        self.pigs.append(Pig(launch_side_struct_x, launch_side_struct_y + lss_col_h + lss_beam_h + 10, self.space, 10, "n51"))

        # self.number_of_birds = 4 # Original line, seems to be overridden by class default or previous lines.
        if self.bool_space:
            self.number_of_birds = 8
    
    
    
    def build_4(self):
        self.number = 4
        self.level_birds = ["glorbo","sahur","liri"] # Reduced birds
        self.number_of_birds = 3
        # locked = True # Unused.
        ground_y = 130.0

        # --- Terrain for build_4 ---
        hill_vertices = [(380, ground_y), (480, 190), (580, ground_y)]
        self._add_static_terrain("poly", hill_vertices, terrain_tag="hill")
        loch_start_x, loch_end_x = 620, 840 # Slightly wider loch
        original_loch_dip_y = 75
        new_loch_dip_y = max(5, 2 * original_loch_dip_y - ground_y)
        loch_segments_points = [
            ((loch_start_x, ground_y), (loch_start_x + 50, new_loch_dip_y)),
            ((loch_start_x + 50, new_loch_dip_y), (loch_end_x - 50, new_loch_dip_y)),
            ((loch_end_x - 50, new_loch_dip_y), (loch_end_x, ground_y))
        ]
        for p_start, p_end in loch_segments_points:
            self._add_static_terrain("segment", (p_start, p_end), terrain_tag="loch", radius=1.0)
        self.loch_extent_x = (loch_start_x, loch_end_x)

        base_x = 950 # Structure base X
        col_h_s, col_w_s = 75, 20 # Smaller elements
        beam_h_s, beam_l_s = 20, 100 # Smaller elements
        pig_r_sml, pig_r_med, pig_r_lrg = 12, 10, 10 # Adjusted pig sizes

        # Layer 1
        y_col1 = ground_y + col_h_s/2
        self.columns.append(Polygon((base_x - 55, y_col1), col_w_s, col_h_s, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood")) # Wider
        self.columns.append(Polygon((base_x, y_col1), col_w_s, col_h_s, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood")) 
        self.columns.append(Polygon((base_x + 55, y_col1), col_w_s, col_h_s, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood")) # Wider
        y_beam1 = y_col1 + col_h_s/2 + beam_h_s/2
        self.beams.append(Polygon((base_x, y_beam1), beam_l_s + 30, beam_h_s, self.space, wood_hp, "beams", self.screen_height, self.screen_width, material_type="wood")) # Wider beam
        self.pigs.append(Pig(base_x, y_beam1 + beam_h_s/2 + pig_r_sml, self.space, pig_r_sml, "n11")) # pig_r_sml = 12
        
        # Layer 2 (Offset beams for instability)
        y_col2 = y_beam1 + beam_h_s/2 + col_h_s/2 
        self.columns.append(Polygon((base_x - 40, y_col2), col_w_s, col_h_s, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone")) # Wider
        self.columns.append(Polygon((base_x + 40, y_col2), col_w_s, col_h_s, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood")) # Changed one column to wood
        y_beam2 = y_col2 + col_h_s/2 + beam_h_s/2
        # Offset beams
        # Make them slightly less offset for more stability if needed, or ensure they are well supported
        self.beams.append(Polygon((base_x - 25, y_beam2), (beam_l_s - 30)*2, beam_h_s, self.space, stone_hp, "beams", self.screen_height, self.screen_width, material_type="stone")) # Wider offset beams
        self.pigs.append(Pig(base_x - 20, y_beam2 + beam_h_s/2 + pig_r_med, self.space, pig_r_med, "n21"))
        self.pigs.append(Pig(base_x + 20, y_beam2 + beam_h_s/2 + pig_r_lrg, self.space, pig_r_lrg, "n31"))

        # Layer 3 (Small central tower)
        y_col3 = y_beam2 + beam_h_s/2 + col_h_s/2 # Assuming beams are stacked on top of each other
        self.columns.append(Polygon((base_x, y_col3), col_w_s, col_h_s, self.space, ice_hp, "columns", self.screen_height, self.screen_width, material_type="ice"))
        y_beam3 = y_col3 + col_h_s/2 + beam_h_s/2
        self.beams.append(Polygon((base_x, y_beam3), beam_l_s - 50, beam_h_s, self.space, ice_hp, "beams", self.screen_height, self.screen_width, material_type="ice")) # Wider small beam
        self.pigs.append(Pig(base_x, y_beam3 + beam_h_s/2 + pig_r_med, self.space, pig_r_med, "n41")) 
        # Extra pig
        self.pigs.append(Pig(base_x + 150, ground_y + pig_r_lrg, self.space, pig_r_lrg, "n51"))

        # self.number_of_birds = 4
        if self.bool_space:
            self.number_of_birds = 8
    
    
    
    def build_5(self):
        self.number = 5
        self.level_birds = ["trala","palocleves"] # Reduced birds
        self.number_of_birds = 2
        # locked = True # Unused.
        ground_y = 130.0

        # --- Terrain for build_5 ---
        hill_vertices = [(420, ground_y), (520, 210), (620, ground_y)]
        self._add_static_terrain("poly", hill_vertices, terrain_tag="hill")
        loch_start_x, loch_end_x = 670, 890 # Wider loch
        original_loch_dip_y = 65
        new_loch_dip_y = max(5, 2 * original_loch_dip_y - ground_y)
        loch_segments_points = [
            ((loch_start_x, ground_y), (loch_start_x + 50, new_loch_dip_y)),
            ((loch_start_x + 50, new_loch_dip_y), (loch_end_x - 50, new_loch_dip_y)),
            ((loch_end_x - 50, new_loch_dip_y), (loch_end_x, ground_y))
        ]
        for p_start, p_end in loch_segments_points:
            self._add_static_terrain("segment", (p_start, p_end), terrain_tag="loch", radius=1.0)
        self.loch_extent_x = (loch_start_x, loch_end_x)

        base_x = 1000 # Structure base X
        col_h_s, col_w_s = 65, 16 # Smaller elements
        beam_h_s, beam_l_s = 16, 95 # Smaller elements
        pig_r_sml, pig_r_med, pig_r_lrg = 10, 12, 14

        # Layer 1
        y_col1 = ground_y + col_h_s/2
        self.columns.append(Polygon((base_x - 40, y_col1), col_w_s, col_h_s, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood")) # Wider
        self.columns.append(Polygon((base_x + 40, y_col1), col_w_s, col_h_s, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood")) # Wider
        y_beam1 = y_col1 + col_h_s/2 + beam_h_s/2
        self.beams.append(Polygon((base_x, y_beam1), beam_l_s + 10, beam_h_s, self.space, wood_hp, "beams", self.screen_height, self.screen_width, material_type="wood")) # Wider
        self.pigs.append(Pig(base_x, y_beam1 + beam_h_s/2 + pig_r_sml, self.space, pig_r_sml, "n11"))
        
        # Layer 2
        y_col2 = y_beam1 + beam_h_s/2 + col_h_s/2
        self.columns.append(Polygon((base_x - 40, y_col2), col_w_s, col_h_s, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone")) # Wider
        self.columns.append(Polygon((base_x + 40, y_col2), col_w_s, col_h_s, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone")) # Wider
        y_beam2 = y_col2 + col_h_s/2 + beam_h_s/2
        # Slightly shorter beam on top
        self.beams.append(Polygon((base_x, y_beam2), beam_l_s - 10, beam_h_s, self.space, stone_hp, "beams", self.screen_height, self.screen_width, material_type="stone")) # Wider
        self.pigs.append(Pig(base_x, y_beam2 + beam_h_s/2 + pig_r_med, self.space, pig_r_med, "n21"))

        # Layer 3 - Cross beams for complexity
        y_col3 = y_beam2 + beam_h_s/2 + col_h_s/2
        self.columns.append(Polygon((base_x - 30, y_col3), col_w_s, col_h_s, self.space, ice_hp, "columns", self.screen_height, self.screen_width, material_type="ice")) # Wider
        self.columns.append(Polygon((base_x + 30, y_col3), col_w_s, col_h_s, self.space, ice_hp, "columns", self.screen_height, self.screen_width, material_type="ice")) # Wider
        y_beam3 = y_col3 + col_h_s/2 + beam_h_s/2
        self.beams.append(Polygon((base_x, y_beam3), beam_l_s - 40, beam_h_s, self.space, ice_hp, "beams", self.screen_height, self.screen_width, material_type="ice"))
        self.pigs.append(Pig(base_x, y_beam3 + beam_h_s/2 + pig_r_lrg, self.space, pig_r_lrg, "n41")) # New pig

        self.pigs.append(Pig(base_x + 100, ground_y + pig_r_med, self.space, pig_r_med, "n51")) # Added extra pig

        # Pig on the ground
        self.pigs.append(Pig(base_x - beam_l_s/2 - 30, ground_y + pig_r_lrg, self.space, pig_r_lrg, "n31"))
        # Additional pig for complexity
        # self.pigs.append(Pig(base_x + beam_l_s/2 + 30, ground_y + pig_r_sml, self.space, pig_r_sml, "n41")) # Removed one to simplify

        # Add an exploding crate to level 5 near the main structure
        exploding_crate_params_lvl5 = {
            "radius": 110, "damage_pigs": 170, "damage_polys": 1400, "knockback": 6800
        }
        self.circles.append(Polygon(
            pos=(base_x + beam_l_s + 20, ground_y + 12), # Position it to the side, adjusted for new radius
            length=25, height=25, # Visual dimensions (smaller)
            space=self.space,
            life=EXPLODING_CRATE_HP,
            element_type="exploding_crate",
            screen_height=self.screen_height, screen_width=self.screen_width,
            mass=EXPLODING_CRATE_MASS, radius=12, # Physics radius (smaller)
            image_path=EXPLODING_CRATE_IMG_PATH,
            is_explosive_obj=True, explosion_params=exploding_crate_params_lvl5))
        # self.number_of_birds = 4
        # Add another exploding crate
        self.circles.append(Polygon(
            pos=(base_x - beam_l_s - 20, ground_y + 12), 
            length=25, height=25, space=self.space, life=EXPLODING_CRATE_HP,
            element_type="exploding_crate", screen_height=self.screen_height,
            screen_width=self.screen_width, mass=EXPLODING_CRATE_MASS, radius=12,
            image_path=EXPLODING_CRATE_IMG_PATH,
            is_explosive_obj=True, explosion_params=exploding_crate_params_default
        ))

        if self.bool_space:
            self.number_of_birds = 8
    
    
    
    def build_6(self):
        self.number = 6
        self.level_birds = ["bomb","patapim","sahur"] # Reduced birds
        self.number_of_birds = 3
        ground_y = 130.0

        # --- Terrain for build_6: Island Level ---
        launch_hill_verts = [(300, ground_y), (380, 180), (460, ground_y)]
        self._add_static_terrain("poly", launch_hill_verts, terrain_tag="hill")

        island_center_x = 850
        island_width = 300 
        island_height_above_water = 25
        island_top_y = ground_y + island_height_above_water
        
        island_vertices = [
            (island_center_x - island_width/2, ground_y - 15), 
            (island_center_x + island_width/2, ground_y - 15),
            (island_center_x + island_width/2 - 30, island_top_y), 
            (island_center_x - island_width/2 + 30, island_top_y)
        ]
        self._add_static_terrain("poly", island_vertices, terrain_tag="island")

        loch_start_x, loch_end_x = 470, 1180 # Wider loch
        original_loch_dip_y = 80 # Deeper loch
        new_loch_dip_y = max(5, 2 * original_loch_dip_y - ground_y)
        loch_segments_points = [
            ((loch_start_x, ground_y), (loch_start_x + 50, new_loch_dip_y)),
            ((loch_start_x + 50, new_loch_dip_y), (loch_end_x - 50, new_loch_dip_y)),
            ((loch_end_x - 50, new_loch_dip_y), (loch_end_x, ground_y))
        ]
        for p_start, p_end in loch_segments_points:
            self._add_static_terrain("segment", (p_start, p_end), terrain_tag="loch", radius=1.0)
        self.loch_extent_x = (loch_start_x, loch_end_x)

        # Structure on the island
        base_x = island_center_x 
        col_h_s, col_w_s = 60, 15 # Smaller elements
        beam_h_s, beam_l_s = 15, 80 # Smaller elements
        pig_r_sml, pig_r_med, pig_r_lrg = 10, 12, 13 # Adjusted pig sizes

        # Layer 1
        y_col1 = island_top_y + col_h_s/2
        self.columns.append(Polygon((base_x - 60, y_col1), col_w_s, col_h_s, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood")) # Wider
        self.columns.append(Polygon((base_x, y_col1), col_w_s, col_h_s, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood")) 
        self.columns.append(Polygon((base_x + 60, y_col1), col_w_s, col_h_s, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood")) # Wider
        
        y_beam1 = y_col1 + col_h_s/2 + beam_h_s/2
        self.beams.append(Polygon((base_x, y_beam1), beam_l_s + 40, beam_h_s, self.space, wood_hp, "beams", self.screen_height, self.screen_width, material_type="wood")) # Wider beam
        
        pig1 = Pig(base_x, y_beam1 + beam_h_s/2 + pig_r_sml, self.space, pig_r_sml, "n11") 
        pig1.life = 40 # Pig with reduced health.
        self.pigs.append(pig1)

        
        # Layer 2 - Asymmetric but stable
        y_col_layer2 = y_beam1 + beam_h_s/2 + col_h_s/2
        self.columns.append(Polygon((base_x - 25, y_col_layer2), col_w_s, col_h_s, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone"))
        # Add a balancing column for stability
        self.columns.append(Polygon((base_x + 35, y_col_layer2), col_w_s, col_h_s, self.space, ice_hp, "columns", self.screen_height, self.screen_width, material_type="ice")) # Wider and taller ice column
        
        y_beam_layer2 = y_col_layer2 + col_h_s/2 + beam_h_s/2
        self.beams.append(Polygon((base_x + 5, y_beam_layer2), beam_l_s + 10, beam_h_s, self.space, stone_hp, "beams", self.screen_height, self.screen_width, material_type="stone")) # Wider and offset
        self.pigs.append(Pig(base_x+40, y_beam_layer2 + beam_h_s/2 + pig_r_med, self.space, pig_r_med, "n21"))

        # Layer 3 - Small topper
        y_col_layer3 = y_beam_layer2 + beam_h_s/2 + col_h_s/2
        # Pig on column (col_w_s = 15, pig_r_lrg = 13 -> diameter 26, too wide for column)
        # Add a small beam for this pig
        self.columns.append(Polygon((base_x, y_col_layer3), col_w_s, col_h_s, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood"))
        top_beam_h, top_beam_l = 10, 30 # Small beam for stability
        y_top_beam = y_col_layer3 + col_h_s/2 + top_beam_h/2
        self.beams.append(Polygon((base_x, y_top_beam), top_beam_l, top_beam_h, self.space, wood_hp, "beams", self.screen_height, self.screen_width, material_type="wood"))
        self.pigs.append(Pig(base_x, y_top_beam + top_beam_h/2 + pig_r_lrg, self.space, pig_r_lrg, "n31"))
        # Extra pig
        self.pigs.append(Pig(base_x + 150, island_top_y + pig_r_med, self.space, pig_r_med, "n41"))

        # Add a circle element for variety
        self.circles.append(Polygon((island_center_x + island_width/2 - 25, island_top_y + 15), 25, 25, self.space, ice_hp, "circles", self.screen_height, self.screen_width, radius=12, material_type="ice"))

        # self.number_of_birds = 4
        if self.bool_space:
            self.number_of_birds = 8
        # Add an exploding crate
        self.circles.append(Polygon(
            pos=(base_x + 100, island_top_y + 12),
            length=25, height=25, space=self.space, life=EXPLODING_CRATE_HP,
            element_type="exploding_crate", screen_height=self.screen_height,
            screen_width=self.screen_width, mass=EXPLODING_CRATE_MASS, radius=12,
            image_path=EXPLODING_CRATE_IMG_PATH,
            is_explosive_obj=True, explosion_params=exploding_crate_params_default
        ))

    def build_7(self):
        self.number = 7
        self.level_birds = ["liri","glorbo"] # Reduced birds
        self.number_of_birds = 2
        # locked = True # Unused.
        ground_y = 130.0

        # --- Terrain for build_7 ---
        hill_vertices = [(300, ground_y), (400, 220), (500, ground_y)] # Taller hill
        self._add_static_terrain("poly", hill_vertices, terrain_tag="hill")
        loch_start_x, loch_end_x = 550, 780 # Wider loch
        original_loch_dip_y = 50 
        new_loch_dip_y = max(5, 2 * original_loch_dip_y - ground_y)
        loch_segments_points = [
            ((loch_start_x, ground_y), (loch_start_x + 70, new_loch_dip_y)),
            ((loch_start_x + 70, new_loch_dip_y), (loch_end_x - 70, new_loch_dip_y)),
            ((loch_end_x - 70, new_loch_dip_y), (loch_end_x, ground_y))
        ]
        for p_start, p_end in loch_segments_points:
            self._add_static_terrain("segment", (p_start, p_end), terrain_tag="loch", radius=1.0)
        self.loch_extent_x = (loch_start_x, loch_end_x)

        base_x = 850 # Structure base X
        col_h_s, col_w_s = 80, 20 # Smaller elements
        beam_h_s, beam_l_s = 20, 150 # Smaller elements
        circle_r_s = 20 # Smaller circle
        pig_r_sml, pig_r_med, pig_r_lrg, pig_r_xlrg = 10, 12, 14, 16

        # Layer 1 (Wood)
        y_col1 = ground_y + col_h_s/2
        self.columns.append(Polygon((base_x - 80, y_col1), col_w_s, col_h_s, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood")) # Wider
        self.columns.append(Polygon((base_x, y_col1), col_w_s, col_h_s, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood")) 
        self.columns.append(Polygon((base_x + 80, y_col1), col_w_s, col_h_s, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood")) # Wider
        y_beam1 = y_col1 + col_h_s/2 + beam_h_s/2
        self.beams.append(Polygon((base_x, y_beam1), beam_l_s + 40, beam_h_s, self.space, wood_hp, "beams", self.screen_height, self.screen_width, material_type="wood")) # Wider beam
        self.pigs.append(Pig(base_x - 60, y_beam1 + beam_h_s/2 + pig_r_sml, self.space, pig_r_sml, "n11")) # Wider
        self.pigs.append(Pig(base_x + 60, y_beam1 + beam_h_s/2 + pig_r_sml, self.space, pig_r_sml, "n21")) # Wider

        # Layer 2 (Stone)
        y_col2 = y_beam1 + beam_h_s/2 + col_h_s/2
        self.columns.append(Polygon((base_x - 70, y_col2), col_w_s, col_h_s, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone")) # Wider
        self.columns.append(Polygon((base_x + 70, y_col2), col_w_s, col_h_s, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone")) # Wider
        y_beam2 = y_col2 + col_h_s/2 + beam_h_s/2
        self.beams.append(Polygon((base_x, y_beam2), beam_l_s + 20, beam_h_s, self.space, stone_hp, "beams", self.screen_height, self.screen_width, material_type="stone")) # Wider
        self.pigs.append(Pig(base_x, y_beam2 + beam_h_s/2 + pig_r_med, self.space, pig_r_med, "n31"))

        # Layer 3 (Wood topper)
        y_col3 = y_beam2 + beam_h_s/2 + col_h_s/2
        self.columns.append(Polygon((base_x - 50, y_col3), col_w_s, col_h_s, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood")) # Wider
        self.columns.append(Polygon((base_x + 50, y_col3), col_w_s, col_h_s, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood")) # Wider
        y_beam3 = y_col3 + col_h_s/2 + beam_h_s/2
        self.beams.append(Polygon((base_x, y_beam3), beam_l_s - 20, beam_h_s, self.space, wood_hp, "beams", self.screen_height, self.screen_width, material_type="wood")) # Wider
        # self.pigs.append(Pig(base_x, y_beam3 + beam_h_s/2 + pig_r_lrg, self.space, pig_r_lrg, "n51")) # Original pig on this beam

        # Topmost part: Single pig on a new small beam, replacing circles
        # Remove original circles and pig on circles:
        # self.circles.append(Polygon((base_x - 35, y_circle_base), circle_r_s*2, circle_r_s*2, self.space, ice_hp, "circles", self.screen_height, self.screen_width, radius=circle_r_s, material_type="ice"))
        # self.circles.append(Polygon((base_x + 35, y_circle_base), circle_r_s*2, circle_r_s*2, self.space, ice_hp, "circles", self.screen_height, self.screen_width, radius=circle_r_s, material_type="ice"))
        # self.pigs.append(Pig(base_x, y_circle_base + circle_r_s + pig_r_xlrg, self.space, pig_r_xlrg, "n41"))
        
        # Add a single small beam on top of y_beam3 for the single top pig
        top_final_beam_h, top_final_beam_l = 15, 40
        y_top_final_beam = y_beam3 + beam_h_s/2 + top_final_beam_h/2
        self.beams.append(Polygon((base_x, y_top_final_beam), top_final_beam_l, top_final_beam_h, self.space, ice_hp, "beams", self.screen_height, self.screen_width, material_type="ice"))
        self.pigs.append(Pig(base_x, y_top_final_beam + top_final_beam_h/2 + pig_r_lrg, self.space, pig_r_lrg, "n41")) # Single pig on top
        # Extra pig
        self.pigs.append(Pig(base_x + 180, ground_y + pig_r_xlrg, self.space, pig_r_xlrg, "n51"))

        # Add an exploding crate to level 7, perhaps on one of the lower, wider beams
        exploding_crate_params_lvl7 = {
            "radius": 140, "damage_pigs": 210, "damage_polys": 1700, "knockback": 7300
        }
        self.circles.append(Polygon(
            pos=(base_x -30, y_beam1-70), # On the first layer beam, adjusted for new radius
            length=28, height=28, # Visual dimensions (smaller)
            space=self.space,
            life=EXPLODING_CRATE_HP,
            element_type="exploding_crate",
            screen_height=self.screen_height, screen_width=self.screen_width,
            mass=EXPLODING_CRATE_MASS, radius=14, # Physics radius (smaller)
            image_path=EXPLODING_CRATE_IMG_PATH,
            is_explosive_obj=True, explosion_params=exploding_crate_params_lvl7))
        # self.number_of_birds = 4
        # Add another exploding crate
        self.circles.append(Polygon(
            pos=(base_x + 100, ground_y + 14), 
            length=28, height=28, space=self.space, life=EXPLODING_CRATE_HP,
            element_type="exploding_crate", screen_height=self.screen_height,
            screen_width=self.screen_width, mass=EXPLODING_CRATE_MASS, radius=14,
            image_path=EXPLODING_CRATE_IMG_PATH,
            is_explosive_obj=True, explosion_params=exploding_crate_params_default
        ))
        if self.bool_space:
            self.number_of_birds = 8

    def build_8(self):
        self.number = 8
        self.level_birds = ["trala", "palocleves", "bomb"] # Reduced birds
        self.number_of_birds = 3
        # locked = True # Unused.
        ground_y = 130.0

        # --- Terrain for build_8 ---
        hill_vertices = [(320, ground_y), (420, 190), (520, ground_y)]
        self._add_static_terrain("poly", hill_vertices, terrain_tag="hill")
        loch_start_x, loch_end_x = 560, 800 # Wider loch
        original_loch_dip_y = 60
        new_loch_dip_y = max(5, 2 * original_loch_dip_y - ground_y)
        loch_segments_points = [
            ((loch_start_x, ground_y), (loch_start_x + 60, new_loch_dip_y)),
            ((loch_start_x + 60, new_loch_dip_y), (loch_end_x - 60, new_loch_dip_y)),
            ((loch_end_x - 60, new_loch_dip_y), (loch_end_x, ground_y))
        ]
        for p_start, p_end in loch_segments_points:
            self._add_static_terrain("segment", (p_start, p_end), terrain_tag="loch", radius=1.0)
        self.loch_extent_x = (loch_start_x, loch_end_x)

        base_x = 880 # Structure base X
        col_h_s, col_w_s = 80, 18 # Smaller ice columns
        beam_h_s, beam_l_s = 18, 140 # Smaller wood beam
        stone_col_h_s, stone_col_w_s = 70, 25 # Smaller stone column
        stone_beam_h_s, stone_beam_l_s = 22, 160 # Smaller stone beam
        tri_base_s, tri_h_s = 35, 35 # Smaller wood triangles
        pig_r_sml, pig_r_med, pig_r_lrg = 8, 10, 12

        # Layer 1 (Ice columns, Wood beam)
        y_col1 = ground_y + col_h_s/2
        self.columns.append(Polygon((base_x - 70, y_col1), col_w_s, col_h_s, self.space, ice_hp, "columns", self.screen_height, self.screen_width, material_type="ice")) # Wider
        self.columns.append(Polygon((base_x, y_col1), col_w_s, col_h_s, self.space, ice_hp, "columns", self.screen_height, self.screen_width, material_type="ice")) 
        self.columns.append(Polygon((base_x + 70, y_col1), col_w_s, col_h_s, self.space, ice_hp, "columns", self.screen_height, self.screen_width, material_type="ice")) # Wider
        y_beam1 = y_col1 + col_h_s/2 + beam_h_s/2
        self.beams.append(Polygon((base_x, y_beam1), beam_l_s + 30, beam_h_s, self.space, wood_hp, "beams", self.screen_height, self.screen_width, material_type="wood")) # Wider beam
        
        # Pigs on first beam
        self.pigs.append(Pig(base_x - 50, y_beam1 + beam_h_s/2 + pig_r_sml, self.space, pig_r_sml, "n11"))
        self.pigs.append(Pig(base_x + 50, y_beam1 + beam_h_s/2 + pig_r_sml, self.space, pig_r_sml, "n31")) # Wider

        # Layer 2 (Central Stone Column, Stone Beam)
        y_col2 = y_beam1 + beam_h_s/2 + stone_col_h_s/2
        self.columns.append(Polygon((base_x - 30, y_col2), stone_col_w_s, stone_col_h_s, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone")) # Wider
        self.columns.append(Polygon((base_x + 30, y_col2), stone_col_w_s, stone_col_h_s, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone")) # Wider
        y_beam2 = y_col2 + stone_col_h_s/2 + stone_beam_h_s/2
        self.beams.append(Polygon((base_x, y_beam2), stone_beam_l_s + 20, stone_beam_h_s, self.space, stone_hp, "beams", self.screen_height, self.screen_width, material_type="stone")) # Wider

        # Pigs on second beam
        self.pigs.append(Pig(base_x - 60, y_beam2 + stone_beam_h_s/2 + pig_r_lrg, self.space, pig_r_lrg, "n41")) # Wider
        self.pigs.append(Pig(base_x + 60, y_beam2 + stone_beam_h_s/2 + pig_r_lrg, self.space, pig_r_lrg, "n51")) # Wider

        # Layer 3 (Small wood topper)
        y_col3 = y_beam2 + stone_beam_h_s/2 + col_h_s/2 
        self.columns.append(Polygon((base_x, y_col3), col_w_s, col_h_s, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood"))
        y_pig3 = y_col3 + col_h_s/2 + pig_r_med
        self.pigs.append(Pig(base_x, y_pig3, self.space, pig_r_med, "n61")) 
        # Guards for this pig, adjusted for wider beam below potentially
        guard_h_top = 15; guard_w_top = 5; beam_width_for_guards = 40 # Approx width of the small platform
        self.columns.append(Polygon((base_x - beam_width_for_guards/2 + guard_w_top, y_col3 + col_h_s/2 - guard_h_top/2), guard_w_top, guard_h_top, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood"))
        self.columns.append(Polygon((base_x + beam_width_for_guards/2 - guard_w_top, y_col3 + col_h_s/2 - guard_h_top/2), guard_w_top, guard_h_top, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood"))
        # Extra pig
        self.columns.append(Polygon((base_x + beam_width_for_guards/2 - guard_w_top, y_col3 + col_h_s/2 - guard_h_top/2), guard_w_top, guard_h_top, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood"))

        # Triangles as decorative elements or small supports on the sides of the first beam
        tri_y_level = ground_y + col_h_s + beam_h_s/2 + tri_h_s/2 # Top of first beam + half triangle height
        tri_points = [(-tri_base_s/2, -tri_h_s/2), (tri_base_s/2, -tri_h_s/2), (0, tri_h_s/2)]
        self.triangles.append(Polygon((base_x - (beam_l_s + 30)/2 - tri_base_s/2 + 5 , tri_y_level - beam_h_s/2), tri_base_s, tri_h_s, self.space, wood_hp, "triangles", self.screen_height, self.screen_width, triangle_points=tri_points, material_type="wood")) # Adjusted for wider beam
        self.triangles.append(Polygon((base_x + (beam_l_s + 30)/2 + tri_base_s/2 - 5, tri_y_level - beam_h_s/2), tri_base_s, tri_h_s, self.space, wood_hp, "triangles", self.screen_height, self.screen_width, triangle_points=tri_points, material_type="wood")) # Adjusted for wider beam

        # Add an exploding crate
        self.circles.append(Polygon(
            pos=(base_x + 200, ground_y + 12),
            length=25, height=25, space=self.space, life=EXPLODING_CRATE_HP,
            element_type="exploding_crate", screen_height=self.screen_height,
            screen_width=self.screen_width, mass=EXPLODING_CRATE_MASS, radius=12,
            image_path=EXPLODING_CRATE_IMG_PATH,
            is_explosive_obj=True, explosion_params=exploding_crate_params_default
        ))

        # self.number_of_birds = 4
        if self.bool_space:
            self.number_of_birds = 8
    
    def load_level(self):
        self.clear_level() # Reset loch_extent_x and static_terrain_shapes before building
        try:
            current_level_to_load = self.number # Store the intended level number
            build_name = "build_" + str(current_level_to_load)
            
            if hasattr(self, build_name):
                getattr(self, build_name)()
            else:
                # This case should ideally not be hit if placeholders are correctly generated
                # and self.number is a valid placeholder number.
                print(f"Level build method '{build_name}' not found. Defaulting to Level 1.")
                self.number = 1 
                self.build_1()
        except AttributeError as e:
            print(f"Error loading level {self.number}: {e}. Defaulting to Level 1.")
            # If an error occurs during the execution of a build method (even a placeholder),
            # default to level 1 to prevent a crash loop.
            # The self.number was already set before this method, so if build_X fails,
            # it will try to load level 1 next time if not handled by game state.
            self.number = 1 
            self.build_1()

    def build_9(self): # "Loch Leap"
        self.number = 9
        self.level_birds = ["patapim", "sahur"] # Reduced birds
        self.number_of_birds = 2
        self.one_star = 22000
        self.two_star = 35000
        self.three_star = 48000
        ground_y = 130.0

        # --- Terrain: Wide Loch with a small launch-side hill ---
        # Small Hill near launch
        hill1_start_x = 250
        hill1_peak_x = 320
        hill1_end_x = 380 # Slightly smaller hill
        hill1_peak_y = 170 # Slightly shorter hill
        hill1_vertices = [(hill1_start_x, ground_y), (hill1_peak_x, hill1_peak_y), (hill1_end_x, ground_y)]
        self._add_static_terrain("poly", hill1_vertices, terrain_tag="hill")


        # Wide Loch
        loch_start_x = 410 # Loch starts at x=400
        loch_dip_x1 = 450  # Loch bottom starts dipping
        loch_dip_x2 = 850  # Loch bottom starts rising (wider)
        loch_end_x = 900   # Loch ends (wider)
        original_loch_dip_y = 60 
        new_loch_dip_y = max(5, 2 * original_loch_dip_y - ground_y)

        loch_segments_points = [
            ((loch_start_x, ground_y), (loch_dip_x1, new_loch_dip_y)),
            ((loch_dip_x1, new_loch_dip_y), (loch_dip_x2, new_loch_dip_y)), # Flat bottom
            ((loch_dip_x2, new_loch_dip_y), (loch_end_x, ground_y))
        ]
        for p_start, p_end in loch_segments_points:
            self._add_static_terrain("segment", (p_start, p_end), terrain_tag="loch", radius=1.0, elasticity=0.5, friction=0.8)
        self.loch_extent_x = (loch_start_x, loch_end_x)

        # --- Structures and Pigs ---
        # Structure 1: Taller, more stable island tower in the loch
        island1_base_x = 600 # Shifted island slightly more
        island_top_y = ground_y + 25 # Make island taller (top at 155)
        
        # Create a small static "island" base for the structure
        island_poly_pts = [
            (island1_base_x - 50, ground_y -10), # Wider island base
            (island1_base_x + 50, ground_y -10),
            (island1_base_x + 40, island_top_y), 
            (island1_base_x - 40, island_top_y)
        ]
        self._add_static_terrain("poly", island_poly_pts, terrain_tag="hill") # Island is a type of hill

        col_h_isl_s, col_w_isl_s = 60, 15 # Smaller elements for island tower
        beam_h_isl_s, beam_l_isl_s = 15, 50
        pig_r_isl_s = 10

        # Layer 1 on island
        y_col1_isl = island_top_y + col_h_isl_s/2
        self.columns.append(Polygon((island1_base_x - 20, y_col1_isl), col_w_isl_s, col_h_isl_s, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood")) # Wider
        self.columns.append(Polygon((island1_base_x + 20, y_col1_isl), col_w_isl_s, col_h_isl_s, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood")) 
        y_beam1_isl = y_col1_isl + col_h_isl_s/2 + beam_h_isl_s/2
        self.beams.append(Polygon((island1_base_x, y_beam1_isl), beam_l_isl_s + 10, beam_h_isl_s, self.space, wood_hp, "beams", self.screen_height, self.screen_width, material_type="wood")) 
        self.pigs.append(Pig(island1_base_x + 20, y_beam1_isl + beam_h_isl_s/2 + pig_r_isl_s, self.space, pig_r_isl_s, "n11")) # Shifted right by 30
        # Pig on single column (col_w_isl_s = 15, pig_r_isl_s = 10 -> diameter 20, too wide)
        # Replace vertical guard with a small horizontal beam for this pig.
        # Original guard: self.beams.append(Polygon((island1_base_x + col_w_isl_s/2 + 5, y_pig2_isl - pig_r_isl_s/2), 5, 15, self.space, ice_hp, "beams", self.screen_height, self.screen_width, material_type="ice"))

        # Layer 2 on island
        y_col2_isl = y_beam1_isl + beam_h_isl_s/2 + col_h_isl_s/2
        self.columns.append(Polygon((island1_base_x, y_col2_isl), col_w_isl_s, col_h_isl_s, self.space, ice_hp, "columns", self.screen_height, self.screen_width, material_type="ice"))
        y_pig2_isl = y_col2_isl + col_h_isl_s/2 + pig_r_isl_s
        # Guard for pig on single column
        # Replace vertical guard with a small horizontal beam
        pig_support_beam_h = 10
        pig_support_beam_l = 25 # Wider than column
        y_pig_support_beam = y_col2_isl + col_h_isl_s/2 + pig_support_beam_h/2
        self.beams.append(Polygon((island1_base_x, y_pig_support_beam), pig_support_beam_l, pig_support_beam_h, self.space, ice_hp, "beams", self.screen_height, self.screen_width, material_type="ice"))
        self.pigs.append(Pig(island1_base_x, y_pig_support_beam + pig_support_beam_h/2 + pig_r_isl_s, self.space, pig_r_isl_s, "n41"))
        # Extra pig on island
        self.pigs.append(Pig(island1_base_x - 60, island_top_y + pig_r_isl_s, self.space, pig_r_isl_s, "n31"))
        # Structure 2: Platform on solid ground AFTER the loch
        base_x2_after_loch = 1000 # Shifted further right for more landing space
        col_h_main_s, col_w_main_s = 70, 18 # Smaller elements
        beam_h_main_s, beam_l_main_s = 18, 60
        pig_r_main_s = 10

        # Layer 1 (mainland)
        y_col1_main = ground_y + col_h_main_s/2
        self.columns.append(Polygon((base_x2_after_loch - 35, y_col1_main), col_w_main_s, col_h_main_s, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone")) # Wider
        self.columns.append(Polygon((base_x2_after_loch + 35, y_col1_main), col_w_main_s, col_h_main_s, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone")) # Wider
        y_beam1_main = y_col1_main + col_h_main_s/2 + beam_h_main_s/2
        self.beams.append(Polygon((base_x2_after_loch, y_beam1_main), beam_l_main_s + 20, beam_h_main_s, self.space, stone_hp, "beams", self.screen_height, self.screen_width, material_type="stone")) # Wider beam
        self.pigs.append(Pig(base_x2_after_loch - 15, y_beam1_main + beam_h_main_s/2 + pig_r_main_s, self.space, pig_r_main_s, "n21")) # Wider

        # Layer 2 (mainland)
        y_col2_main = y_beam1_main + beam_h_main_s/2 + col_h_main_s/2
        self.columns.append(Polygon((base_x2_after_loch - 25, y_col2_main), col_w_main_s, col_h_main_s, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood")) # Wider
        self.columns.append(Polygon((base_x2_after_loch + 25, y_col2_main), col_w_main_s, col_h_main_s, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood")) # Wider
        y_beam2_main = y_col2_main + col_h_main_s/2 + beam_h_main_s/2
        self.beams.append(Polygon((base_x2_after_loch, y_beam2_main), beam_l_main_s - 10, beam_h_main_s, self.space, wood_hp, "beams", self.screen_height, self.screen_width, material_type="wood"))
        self.pigs.append(Pig(base_x2_after_loch, y_beam2_main + beam_h_main_s/2 + pig_r_main_s, self.space, pig_r_main_s, "n51")) 
        # Extra pig on mainland structure
        self.pigs.append(Pig(base_x2_after_loch + 80, ground_y + pig_r_main_s, self.space, pig_r_main_s, "n61"))

        # A floating ice block
        # Add an exploding crate
        self.circles.append(Polygon(
            pos=(base_x2_after_loch + 150, ground_y + 10),
            length=30, height=30, space=self.space, life=EXPLODING_CRATE_HP,
            element_type="exploding_crate", screen_height=self.screen_height,
            screen_width=self.screen_width, mass=EXPLODING_CRATE_MASS, radius=15,
            image_path=EXPLODING_CRATE_IMG_PATH,
            is_explosive_obj=True, explosion_params=exploding_crate_params_default
        ))


    def build_10(self): # "Rolling Hills & Hidden Pigs"
        self.number = 10
        self.level_birds = ["liri", "bomb", "trala"] # Reduced birds
        self.number_of_birds = 3
        self.one_star = 23000
        self.two_star = 36000
        self.three_star = 50000
        ground_y = 130.0

        # --- Terrain: Rolling Hills and a narrow loch ---
        # Hill 1
        h1_start_x, h1_peak_x, h1_end_x = 300, 400, 500
        h1_peak_y = 190 # Shorter hill
        h1_verts = [(h1_start_x, ground_y), (h1_peak_x, h1_peak_y), (h1_end_x, ground_y)]
        self._add_static_terrain("poly", h1_verts, terrain_tag="hill")

        # Valley 1 & Structure
        valley1_pig_x = (h1_end_x + 60) # Wider
        col_h_val_s, col_w_val_s = 45, 12 # Smaller column
        beam_h_val_s, beam_l_val_s = 12, 40
        pig_r_val_s = 8
        y_col_val1 = ground_y + col_h_val_s/2
        self.columns.append(Polygon((valley1_pig_x, y_col_val1), col_w_val_s + 5, col_h_val_s, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood")) # Slightly wider column
        y_beam_val1 = y_col_val1 + col_h_val_s/2 + beam_h_val_s/2
        self.beams.append(Polygon((valley1_pig_x, y_beam_val1), beam_l_val_s, beam_h_val_s, self.space, wood_hp, "beams", self.screen_height, self.screen_width, material_type="wood"))
        self.pigs.append(Pig(valley1_pig_x, y_beam_val1 + beam_h_val_s/2 + pig_r_val_s, self.space, pig_r_val_s, "n11"))

        # Hill 2 (Wider Plateau)
        h2_start_x, h2_plat_start_x, h2_plat_end_x, h2_end_x = 600, 670, 770, 840
        h2_peak_y = 200 # Lower plateau
        h2_verts = [
            (h2_start_x, ground_y), (h2_plat_start_x, h2_peak_y),
            (h2_plat_end_x, h2_peak_y), (h2_end_x, ground_y)
        ]
        self._add_static_terrain("poly", h2_verts, terrain_tag="hill")

        # Structure on Hill 2 (more complex)
        h2_struct_x = (h2_plat_start_x + h2_plat_end_x) / 2 
        col_h_h2_s, col_w_h2_s = 55, 14
        beam_h_h2_s, beam_l_h2_s = 14, 60
        pig_r_h2_s = 10

        # Layer 1 on hill 2
        y_col1_h2 = h2_peak_y + col_h_h2_s/2
        self.columns.append(Polygon((h2_struct_x - 30, y_col1_h2), col_w_h2_s, col_h_h2_s, self.space, ice_hp, "columns", self.screen_height, self.screen_width, material_type="ice")) # Wider
        self.columns.append(Polygon((h2_struct_x + 30, y_col1_h2), col_w_h2_s, col_h_h2_s, self.space, ice_hp, "columns", self.screen_height, self.screen_width, material_type="ice")) # Wider
        y_beam1_h2 = y_col1_h2 + col_h_h2_s/2 + beam_h_h2_s/2
        self.beams.append(Polygon((h2_struct_x, y_beam1_h2), beam_l_h2_s + 10, beam_h_h2_s, self.space, ice_hp, "beams", self.screen_height, self.screen_width, material_type="ice")) # Wider
        self.pigs.append(Pig(h2_struct_x, y_beam1_h2 + beam_h_h2_s/2 + pig_r_h2_s, self.space, pig_r_h2_s, "n31"))

        # Layer 2 on hill 2
        y_col2_h2 = y_beam1_h2 + beam_h_h2_s/2 + col_h_h2_s/2
        self.columns.append(Polygon((h2_struct_x - 20, y_col2_h2), col_w_h2_s, col_h_h2_s, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood")) # Wider
        self.columns.append(Polygon((h2_struct_x + 20, y_col2_h2), col_w_h2_s, col_h_h2_s, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood")) # Wider
        y_beam2_h2 = y_col2_h2 + col_h_h2_s/2 + beam_h_h2_s/2
        self.beams.append(Polygon((h2_struct_x, y_beam2_h2), beam_l_h2_s - 10, beam_h_h2_s, self.space, wood_hp, "beams", self.screen_height, self.screen_width, material_type="wood")) # Wider
        self.pigs.append(Pig(h2_struct_x, y_beam2_h2 + beam_h_h2_s/2 + pig_r_h2_s, self.space, pig_r_h2_s, "n51")) 
        # Extra pig on hill 2
        self.pigs.append(Pig(h2_struct_x + 80, h2_peak_y + pig_r_h2_s, self.space, pig_r_h2_s, "n61"))

        # Narrow, Deeper Loch
        loch_start_x = 900
        loch_dip_x1 = 920
        loch_bottom_mid_x = 950
        loch_dip_x2 = 980 
        loch_end_x = 1000 
        original_loch_dip_y = 35 
        new_loch_dip_y = max(5, 2 * original_loch_dip_y - ground_y) # Deeper
        new_loch_bottom_mid_y = max(0, 2 * (original_loch_dip_y - 10) - ground_y) # Deeper V point

        loch_segments_points = [
            ((loch_start_x, ground_y), (loch_dip_x1, new_loch_dip_y)),
            ((loch_dip_x1, new_loch_dip_y), (loch_bottom_mid_x, new_loch_bottom_mid_y)), 
            ((loch_bottom_mid_x, new_loch_bottom_mid_y), (loch_dip_x2, new_loch_dip_y)),
            ((loch_dip_x2, new_loch_dip_y), (loch_end_x, ground_y))
        ]
        for p_start, p_end in loch_segments_points:
            self._add_static_terrain("segment", (p_start, p_end), terrain_tag="loch", radius=1.0, elasticity=0.5, friction=0.8)
        self.loch_extent_x = (loch_start_x, loch_end_x)

        # Pig on a precarious perch over the loch (smaller perch)
        perch_x = (loch_start_x + loch_end_x) / 2
        beam_h_perch_s, beam_l_perch_s = 10, 40 # Slightly wider perch
        pig_r_perch_s = 8
        self.beams.append(Polygon((perch_x, ground_y + 30), beam_l_perch_s, beam_h_perch_s, self.space, wood_hp, "beams", self.screen_height, self.screen_width, material_type="wood"))
        self.pigs.append(Pig(perch_x, ground_y + 30 + beam_h_perch_s/2 + pig_r_perch_s, self.space, pig_r_perch_s, "n21"))
        # Add small side guards for the perch pig
        self.columns.append(Polygon((perch_x - beam_l_perch_s/2 + 3, ground_y + 30 + beam_h_perch_s/2 + 5), 5, 10, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood")) # Wider guards
        self.columns.append(Polygon((perch_x + beam_l_perch_s/2 - 3, ground_y + 30 + beam_h_perch_s/2 + 5), 5, 10, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood")) # Wider guards

        # Final small structure
        final_struct_x = 1130 # Shifted right more
        col_h_fin_s, col_w_fin_s = 50, 13
        # circle_r_fin_s = 12 # Smaller circle - will be removed
        pig_r_fin_s = 10
        y_col_fin = ground_y + col_h_fin_s/2
        self.columns.append(Polygon((final_struct_x - 10, y_col_fin), col_w_fin_s, col_h_fin_s, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone")) # Wider base
        self.columns.append(Polygon((final_struct_x + 10, y_col_fin), col_w_fin_s, col_h_fin_s, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone")) # Wider base
        # Remove circle: self.circles.append(Polygon((final_struct_x, y_circle_fin), circle_r_fin_s*2, circle_r_fin_s*2, self.space, stone_hp, "circles", self.screen_height, self.screen_width, radius=circle_r_fin_s, material_type="stone"))
        # Add a beam on top of the columns instead of the circle
        final_beam_h, final_beam_l = 10, 30
        y_final_beam = y_col_fin + col_h_fin_s/2 + final_beam_h/2
        self.beams.append(Polygon((final_struct_x, y_final_beam), final_beam_l, final_beam_h, self.space, stone_hp, "beams", self.screen_height, self.screen_width, material_type="stone"))
        self.pigs.append(Pig(final_struct_x, y_final_beam + final_beam_h/2 + pig_r_fin_s, self.space, pig_r_fin_s, "n41"))
        # Add an exploding crate
        self.circles.append(Polygon(
            pos=(final_struct_x - 80, ground_y + 12),
            length=25, height=25, space=self.space, life=EXPLODING_CRATE_HP,
            element_type="exploding_crate", screen_height=self.screen_height,
            screen_width=self.screen_width, mass=EXPLODING_CRATE_MASS, radius=12,
            image_path=EXPLODING_CRATE_IMG_PATH,
            is_explosive_obj=True, explosion_params=exploding_crate_params_default
        ))

    def build_11(self): # "Canyon Crossing" - Redesigned
        self.number = 11
        self.level_birds = ["glorbo", "patapim"] # Reduced birds
        self.number_of_birds = 2
        self.one_star = 24000
        self.two_star = 38000
        self.three_star = 52000
        ground_y = 130.0

        # --- Terrain: Launch Platform, Wide Canyon (Loch), Landing Plateau ---

        # Launch Platform (larger than a small hill)
        launch_plat_start_x = 200
        launch_plat_peak_start_x = 250
        launch_plat_peak_end_x = 350 # Wider flat top
        launch_plat_end_x = 400
        launch_plat_peak_y = 180 # Decent height
        launch_plat_verts = [
            (launch_plat_start_x, ground_y),
            (launch_plat_peak_start_x, launch_plat_peak_y),
            (launch_plat_peak_end_x, launch_plat_peak_y),
            (launch_plat_end_x, ground_y)
        ]
        self._add_static_terrain("poly", launch_plat_verts, terrain_tag="hill")

        # Wide and Deep Canyon (Loch)
        loch_start_x = launch_plat_end_x + 20 # Gap after launch platform
        loch_dip_x1 = loch_start_x + 80
        loch_dip_x2 = loch_start_x + 280 # Wider bottom
        loch_end_x = loch_start_x + 380 # Overall wider loch
        original_loch_dip_y = 20 # Very deep
        new_loch_dip_y = max(5, 2 * original_loch_dip_y - ground_y) # Ensure it's deep

        loch_segments_points = [
            ((loch_start_x, ground_y), (loch_dip_x1, new_loch_dip_y)),
            ((loch_dip_x1, new_loch_dip_y), (loch_dip_x2, new_loch_dip_y)), # Flat bottom
            ((loch_dip_x2, new_loch_dip_y), (loch_end_x, ground_y))
        ]
        for p_start, p_end in loch_segments_points:
            self._add_static_terrain("segment", (p_start, p_end), terrain_tag="loch", radius=2.0, elasticity=0.4, friction=0.9)
        self.loch_extent_x = (loch_start_x, loch_end_x)

        # Landing Plateau (Far side)
        landing_plat_start_x = loch_end_x + 20 # Gap after loch
        landing_plat_peak_start_x = landing_plat_start_x + 50
        landing_plat_peak_end_x = landing_plat_start_x + 200 # Wide landing area
        landing_plat_end_x = landing_plat_start_x + 250
        landing_plat_peak_y = 170 # Slightly lower than launch
        landing_plat_verts = [
            (landing_plat_start_x, ground_y),
            (landing_plat_peak_start_x, landing_plat_peak_y),
            (landing_plat_peak_end_x, landing_plat_peak_y),
            (landing_plat_end_x, ground_y)
        ]
        self._add_static_terrain("poly", landing_plat_verts, terrain_tag="hill")

        # --- Structures and Pigs ---
        col_h_s, col_w_s = 60, 18
        beam_h_s, beam_l_s = 18, 70
        pig_r_sml, pig_r_med = 10, 12

        # Structure 1 (Perch in the middle of the loch) has been removed.
        # The pig that was on it (n11) is also removed.

        # Structure 2: Main tower on the landing plateau
        struct2_base_x = (landing_plat_peak_start_x + landing_plat_peak_end_x) / 2

        # Layer 1 (Stone Base)
        y_col1_s2 = landing_plat_peak_y + col_h_s / 2
        self.columns.append(Polygon((struct2_base_x - 40, y_col1_s2), col_w_s, col_h_s, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone"))
        self.columns.append(Polygon((struct2_base_x + 40, y_col1_s2), col_w_s, col_h_s, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone"))
        y_beam1_s2 = y_col1_s2 + col_h_s / 2 + beam_h_s / 2
        self.beams.append(Polygon((struct2_base_x, y_beam1_s2), beam_l_s + 20, beam_h_s, self.space, stone_hp, "beams", self.screen_height, self.screen_width, material_type="stone"))
        self.pigs.append(Pig(struct2_base_x - 25+20, y_beam1_s2 + beam_h_s / 2 + pig_r_med, self.space, pig_r_med, "n21"))

        # Layer 2 (Wood Topper)
        y_col2_s2 = y_beam1_s2 + beam_h_s / 2 + col_h_s / 2
        self.columns.append(Polygon((struct2_base_x - 25, y_col2_s2), col_w_s, col_h_s, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood"))
        self.columns.append(Polygon((struct2_base_x + 25, y_col2_s2), col_w_s, col_h_s, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood"))
        y_beam2_s2 = y_col2_s2 + col_h_s / 2 + beam_h_s / 2
        self.beams.append(Polygon((struct2_base_x, y_beam2_s2), beam_l_s, beam_h_s, self.space, wood_hp, "beams", self.screen_height, self.screen_width, material_type="wood"))
        self.pigs.append(Pig(struct2_base_x, y_beam2_s2 + beam_h_s / 2 + pig_r_sml, self.space, pig_r_sml, "n41"))
        # Extra pig
        self.pigs.append(Pig(struct2_base_x + 100, landing_plat_peak_y + pig_r_med, self.space, pig_r_med, "n31"))

        # Add a floating triangle for variety, far off
        self.triangles.append(Polygon((struct2_base_x + 150, landing_plat_peak_y + 80), 30, 30, self.space, ice_hp, "triangles", self.screen_height, self.screen_width, material_type="ice"))

    def build_12(self): # "The Triple Towers"
        self.number = 12
        self.level_birds = ["sahur", "trala", "liri"] # Reduced birds
        self.number_of_birds = 3
        self.one_star = 25000
        self.two_star = 40000
        self.three_star = 55000
        ground_y = 130.0

        # --- Terrain: Relatively flat with small undulations ---
        self._add_static_terrain("poly", [(200, ground_y), (250, ground_y + 15), (300, ground_y)], terrain_tag="hill_low")
        self._add_static_terrain("poly", [(1000, ground_y), (1050, ground_y + 15), (1100, ground_y)], terrain_tag="hill_low")

        col_h_base, col_w_base = 70, 20
        beam_h_base, beam_l_base = 20, 80
        pig_r_med = 12

        # --- Tower 1 (Left, Wood & Ice) ---
        base_x1 = 450
        # Layer 1
        y_col1_t1 = ground_y + col_h_base/2
        self.columns.append(Polygon((base_x1 - 30, y_col1_t1), col_w_base, col_h_base, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood"))
        self.columns.append(Polygon((base_x1 + 30, y_col1_t1), col_w_base, col_h_base, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood"))
        y_beam1_t1 = y_col1_t1 + col_h_base/2 + beam_h_base/2
        self.beams.append(Polygon((base_x1, y_beam1_t1), beam_l_base, beam_h_base, self.space, wood_hp, "beams", self.screen_height, self.screen_width, material_type="wood"))
        self.pigs.append(Pig(base_x1+20, y_beam1_t1 + beam_h_base/2 + pig_r_med, self.space, pig_r_med, "n11"))
        # Layer 2
        y_col2_t1 = y_beam1_t1 + beam_h_base/2 + (col_h_base-10)/2
        self.columns.append(Polygon((base_x1, y_col2_t1), col_w_base-5, col_h_base-10, self.space, ice_hp, "columns", self.screen_height, self.screen_width, material_type="ice"))
        y_beam2_t1 = y_col2_t1 + (col_h_base-10)/2 + (beam_h_base-5)/2
        self.beams.append(Polygon((base_x1, y_beam2_t1), beam_l_base-20, beam_h_base-5, self.space, ice_hp, "beams", self.screen_height, self.screen_width, material_type="ice"))
        self.pigs.append(Pig(base_x1, y_beam2_t1 + (beam_h_base-5)/2 + pig_r_med, self.space, pig_r_med, "n21"))
        # Extra pig for tower 1
        self.pigs.append(Pig(base_x1 - 70, ground_y + pig_r_med, self.space, pig_r_med, "n61"))

        # --- Tower 2 (Center, Stone & Wood) ---
        base_x2 = 700
        # Layer 1
        y_col1_t2 = ground_y + col_h_base/2
        self.columns.append(Polygon((base_x2 - 35, y_col1_t2), col_w_base, col_h_base, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone"))
        self.columns.append(Polygon((base_x2 + 35, y_col1_t2), col_w_base, col_h_base, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone"))
        y_beam1_t2 = y_col1_t2 + col_h_base/2 + beam_h_base/2
        self.beams.append(Polygon((base_x2, y_beam1_t2), beam_l_base + 10, beam_h_base, self.space, stone_hp, "beams", self.screen_height, self.screen_width, material_type="stone"))
        self.pigs.append(Pig(base_x2 - 20, y_beam1_t2 + beam_h_base/2 + pig_r_med, self.space, pig_r_med, "n31"))
        self.pigs.append(Pig(base_x2 + 20, y_beam1_t2 + beam_h_base/2 + pig_r_med, self.space, pig_r_med, "n41"))
        # Layer 2
        y_col2_t2 = y_beam1_t2 + beam_h_base/2 + col_h_base/2
        self.columns.append(Polygon((base_x2 - 25, y_col2_t2), col_w_base-5, col_h_base, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood"))
        self.columns.append(Polygon((base_x2 + 25, y_col2_t2), col_w_base-5, col_h_base, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood"))
        y_beam2_t2 = y_col2_t2 + col_h_base/2 + (beam_h_base-5)/2
        self.beams.append(Polygon((base_x2, y_beam2_t2), beam_l_base-10, beam_h_base-5, self.space, wood_hp, "beams", self.screen_height, self.screen_width, material_type="wood"))
        self.pigs.append(Pig(base_x2, y_beam2_t2 + (beam_h_base-5)/2 + pig_r_med, self.space, pig_r_med, "n51"))

        # --- Tower 3 (Right, Ice & Stone) ---
        base_x3 = 950
        # Layer 1
        y_col1_t3 = ground_y + (col_h_base-10)/2
        self.columns.append(Polygon((base_x3 - 25, y_col1_t3), col_w_base-5, col_h_base-10, self.space, ice_hp, "columns", self.screen_height, self.screen_width, material_type="ice"))
        self.columns.append(Polygon((base_x3 + 25, y_col1_t3), col_w_base-5, col_h_base-10, self.space, ice_hp, "columns", self.screen_height, self.screen_width, material_type="ice"))
        y_beam1_t3 = y_col1_t3 + (col_h_base-10)/2 + (beam_h_base-5)/2
        self.beams.append(Polygon((base_x3, y_beam1_t3), beam_l_base-15, beam_h_base-5, self.space, ice_hp, "beams", self.screen_height, self.screen_width, material_type="ice"))
        self.pigs.append(Pig(base_x3+20, y_beam1_t3 + (beam_h_base-5)/2 + pig_r_med, self.space, pig_r_med, "n11"))
        # Layer 2
        y_col2_t3 = y_beam1_t3 + (beam_h_base-5)/2 + col_h_base/2
        self.columns.append(Polygon((base_x3, y_col2_t3), col_w_base, col_h_base, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone"))
        y_beam2_t3 = y_col2_t3 + col_h_base/2 + beam_h_base/2
        self.beams.append(Polygon((base_x3, y_beam2_t3), beam_l_base-5, beam_h_base, self.space, stone_hp, "beams", self.screen_height, self.screen_width, material_type="stone"))
        self.pigs.append(Pig(base_x3, y_beam2_t3 + beam_h_base/2 + pig_r_med, self.space, pig_r_med, "n21"))
        # Extra pig for tower 3
        self.pigs.append(Pig(base_x3 + 70, ground_y + pig_r_med, self.space, pig_r_med, "n31"))
        # Add an exploding crate
        self.circles.append(Polygon(
            pos=(base_x2 + 150, ground_y + 12),
            length=25, height=25, space=self.space, life=EXPLODING_CRATE_HP,
            element_type="exploding_crate", screen_height=self.screen_height,
            screen_width=self.screen_width, mass=EXPLODING_CRATE_MASS, radius=12,
            image_path=EXPLODING_CRATE_IMG_PATH,
            is_explosive_obj=True, explosion_params=exploding_crate_params_default
        ))

    def build_13(self): # "The Chasm Fortress"
        self.number = 13
        self.level_birds = ["bomb", "patapim"] # Reduced birds
        self.number_of_birds = 2
        self.one_star = 28000
        self.two_star = 45000
        self.three_star = 60000
        ground_y = 130.0

        # --- Terrain: Deep Chasm (Loch) with platforms on either side ---
        launch_plat_end_x = 350
        self._add_static_terrain("poly", [(150, ground_y), (250, ground_y + 40), (launch_plat_end_x, ground_y + 20), (launch_plat_end_x, ground_y)], terrain_tag="hill_platform")

        loch_start_x = launch_plat_end_x + 10
        loch_end_x = 850
        loch_dip_y = 10 # Very deep
        loch_segments_points = [
            ((loch_start_x, ground_y + 20), (loch_start_x + 100, loch_dip_y)),
            ((loch_start_x + 100, loch_dip_y), (loch_end_x - 100, loch_dip_y)),
            ((loch_end_x - 100, loch_dip_y), (loch_end_x, ground_y + 20))
        ]
        for p_start, p_end in loch_segments_points:
            self._add_static_terrain("segment", (p_start, p_end), terrain_tag="loch", radius=3.0)
        self.loch_extent_x = (loch_start_x, loch_end_x)

        landing_plat_start_x = loch_end_x + 10
        # Define the height for the flat part of the platform where the structure will sit
        # This should match struct_ground_y used for placing the fortress.
        platform_flat_top_y = ground_y + 30 
        
        # Define vertices for a platform with a flat top section
        landing_platform_vertices = [
            (landing_plat_start_x, ground_y),                                 # Bottom-left of platform start
            (landing_plat_start_x, platform_flat_top_y),                      # Top-left of platform, rising vertically
            (landing_plat_start_x + 200, platform_flat_top_y),                # End of the flat top section (covers structure width)
            (1150, ground_y)                                                  # Slopes down to the ground on the far right
        ]
        self._add_static_terrain("poly", landing_platform_vertices, terrain_tag="hill_platform")

        # --- Fortress Structure on the Landing Platform ---
        base_x = landing_plat_start_x + 120
        struct_ground_y = ground_y + 30 # Effective ground for structure

        col_h, col_w = 80, 22
        beam_h, beam_l = 22, 90
        pig_r = 13

        # Layer 1 (Stone Walls)
        y_wall1 = struct_ground_y + col_h/2
        self.columns.append(Polygon((base_x - 60, y_wall1), col_w, col_h, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone"))
        self.columns.append(Polygon((base_x + 60, y_wall1), col_w, col_h, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone"))
        y_beam1 = y_wall1 + col_h/2 + beam_h/2
        self.beams.append(Polygon((base_x, y_beam1), beam_l + 40, beam_h, self.space, stone_hp, "beams", self.screen_height, self.screen_width, material_type="stone"))
        self.pigs.append(Pig(base_x - 50, y_beam1 + beam_h/2 + pig_r, self.space, pig_r, "n31"))
        self.pigs.append(Pig(base_x + 50, y_beam1 + beam_h/2 + pig_r, self.space, pig_r, "n41"))

        # Layer 2 (Wood Interior and Topper)
        y_col2 = y_beam1 + beam_h/2 + (col_h-20)/2
        self.columns.append(Polygon((base_x - 20, y_col2), col_w-5, col_h-20, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood"))
        self.columns.append(Polygon((base_x + 20, y_col2), col_w-5, col_h-20, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood"))
        y_beam2 = y_col2 + (col_h-20)/2 + (beam_h-5)/2
        self.beams.append(Polygon((base_x, y_beam2), beam_l, beam_h-5, self.space, wood_hp, "beams", self.screen_height, self.screen_width, material_type="wood"))
        self.pigs.append(Pig(base_x, y_beam2 + (beam_h-5)/2 + pig_r, self.space, pig_r, "n51"))
        # Extra pig
        self.pigs.append(Pig(base_x + 100, struct_ground_y + pig_r, self.space, pig_r, "n11"))

        # Small ice block target
        self.circles.append(Polygon((base_x, struct_ground_y - 20), 30,30, self.space, ice_hp, "circles", self.screen_height, self.screen_width, radius=15, material_type="ice"))
        # Add an exploding crate
        self.circles.append(Polygon(
            pos=(base_x - 150, struct_ground_y + 13),
            length=26, height=26, space=self.space, life=EXPLODING_CRATE_HP,
            element_type="exploding_crate", screen_height=self.screen_height,
            screen_width=self.screen_width, mass=EXPLODING_CRATE_MASS, radius=13,
            image_path=EXPLODING_CRATE_IMG_PATH,
            is_explosive_obj=True, explosion_params=exploding_crate_params_default
        ))

    def _create_template_structure_A(self, base_x, ground_y_offset=0):
        """Template for a moderately complex, stable tower."""
        """Template for a moderately complex, stable tower. Enhanced for more complexity and visual appeal."""
        ground_y = 130.0 + ground_y_offset
        
        # Define dimensions for different layers
        col_h_l1, col_w_l1 = 70, 22  # Layer 1 (Base)
        beam_h_l1, beam_l_l1 = 20, 100

        col_h_l2, col_w_l2 = 60, 18  # Layer 2
        beam_h_l2, beam_l_l2 = 18, 80

        col_h_l3, col_w_l3 = 50, 15  # Layer 3
        beam_h_l3, beam_l_l3 = 15, 60

        col_h_l4, col_w_l4 = 40, 12  # Layer 4 (Topper)
        beam_h_l4, beam_l_l4 = 12, 40
        
        pig_r = 12

        # Layer 1 (Stone Base - Very Stable)
        y_c1 = ground_y + col_h_l1/2
        self.columns.append(Polygon((base_x - 40, y_c1), col_w_l1, col_h_l1, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone"))
        self.columns.append(Polygon((base_x + 40, y_c1), col_w_l1, col_h_l1, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone"))
        y_b1 = y_c1 + col_h_l1/2 + beam_h_l1/2
        self.beams.append(Polygon((base_x, y_b1), beam_l_l1, beam_h_l1, self.space, stone_hp, "beams", self.screen_height, self.screen_width, material_type="stone"))
        self.pigs.append(Pig(base_x, y_b1 + beam_h_l1/2 + pig_r, self.space, pig_r, "m11")) # Strong pig at base

        # Layer 2 (Wood - Still sturdy)
        y_c2 = y_b1 + beam_h_l1/2 + col_h_l2/2
        self.columns.append(Polygon((base_x - 30, y_c2), col_w_l2, col_h_l2, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood"))
        self.columns.append(Polygon((base_x + 30, y_c2), col_w_l2, col_h_l2, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood"))
        y_b2 = y_c2 + col_h_l2/2 + beam_h_l2/2
        self.beams.append(Polygon((base_x, y_b2), beam_l_l2, beam_h_l2, self.space, wood_hp, "beams", self.screen_height, self.screen_width, material_type="wood"))
        self.pigs.append(Pig(base_x, y_b2 + beam_h_l2/2 + pig_r -2, self.space, pig_r - 2, "n21"))

        # Layer 3 (Ice - More fragile)
        y_c3 = y_b2 + beam_h_l2/2 + col_h_l3/2
        self.columns.append(Polygon((base_x - 20, y_c3), col_w_l3, col_h_l3, self.space, ice_hp, "columns", self.screen_height, self.screen_width, material_type="ice"))
        self.columns.append(Polygon((base_x + 20, y_c3), col_w_l3, col_h_l3, self.space, ice_hp, "columns", self.screen_height, self.screen_width, material_type="ice"))
        y_b3 = y_c3 + col_h_l3/2 + beam_h_l3/2
        self.beams.append(Polygon((base_x, y_b3), beam_l_l3, beam_h_l3, self.space, ice_hp, "beams", self.screen_height, self.screen_width, material_type="ice"))

        # Layer 4 (Small Wood Topper with a single pig)
        y_c4 = y_b3 + beam_h_l3/2 + col_h_l4/2
        self.columns.append(Polygon((base_x, y_c4), col_w_l4, col_h_l4, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood"))
        y_b4 = y_c4 + col_h_l4/2 + beam_h_l4/2
        self.beams.append(Polygon((base_x, y_b4), beam_l_l4, beam_h_l4, self.space, wood_hp, "beams", self.screen_height, self.screen_width, material_type="wood"))
        self.pigs.append(Pig(base_x, y_b4 + beam_h_l4/2 + pig_r - 4, self.space, pig_r - 4, "n51")) # Smallest pig on top
        # Extra pig for template A
        self.pigs.append(Pig(base_x + 100, ground_y + pig_r, self.space, pig_r, "n31"))

    def _create_template_structure_B(self, base_x, ground_y_offset=0):
        """Template for a wider, more spread-out structure."""
        """Template for a wider, more spread-out structure. Enhanced for stability and looks."""
        ground_y = 130.0 + ground_y_offset
        col_h_base, col_w_base = 60, 25 # Wider, shorter base columns
        col_h_upper, col_w_upper = 50, 20

        beam_h, beam_l_short, beam_l_long = 22, 70, 150 # Thicker beams
        pig_r_base, pig_r_upper = 14, 12

        # Base Layer (Stone - Very Stable)
        y_c1 = ground_y + col_h_base/2
        self.columns.append(Polygon((base_x - 80, y_c1), col_w_base, col_h_base, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone"))
        self.columns.append(Polygon((base_x, y_c1), col_w_base, col_h_base, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone"))
        self.columns.append(Polygon((base_x + 80, y_c1), col_w_base, col_h_base, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone"))
        y_b1 = y_c1 + col_h_base/2 + beam_h/2
        self.beams.append(Polygon((base_x, y_b1), beam_l_long, beam_h, self.space, stone_hp, "beams", self.screen_height, self.screen_width, material_type="stone"))
        self.pigs.append(Pig(base_x - 60, y_b1 + beam_h/2 + pig_r_base, self.space, pig_r_base, "m21")) # Heavier pig
        self.pigs.append(Pig(base_x + 60, y_b1 + beam_h/2 + pig_r_base, self.space, pig_r_base, "m31")) # Heavier pig

        # Upper Layer (Wood - Lighter, slightly offset for visual interest but still stable)
        y_c2 = y_b1 + beam_h/2 + col_h_upper/2
        self.columns.append(Polygon((base_x - 40, y_c2), col_w_upper, col_h_upper, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood"))
        self.columns.append(Polygon((base_x + 40, y_c2), col_w_upper, col_h_upper, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood"))
        y_b2 = y_c2 + col_h_upper/2 + beam_h/2
        self.beams.append(Polygon((base_x, y_b2), beam_l_short + 20, beam_h, self.space, wood_hp, "beams", self.screen_height, self.screen_width, material_type="wood")) # Wider short beam
        self.pigs.append(Pig(base_x-30, y_b2 + beam_h/2 + pig_r_upper, self.space, pig_r_upper, "n11"))
        

        # Add a small ice triangle decoration on top for visual flair
        tri_base, tri_h = 40, 30
        tri_points = [(-tri_base/2, -tri_h/2), (tri_base/2, -tri_h/2), (0, tri_h/2)]
        y_tri = y_b2 + beam_h/2 + tri_h/2
        self.triangles.append(Polygon((base_x, y_tri), tri_base, tri_h, self.space, ice_hp, "triangles", self.screen_height, self.screen_width, triangle_points=tri_points, material_type="ice"))
        # Extra pigs for template B
        self.pigs.append(Pig(base_x + 150, ground_y + pig_r_base, self.space, pig_r_base, "m11"))
        self.pigs.append(Pig(base_x - 150, ground_y + pig_r_base, self.space, pig_r_base, "n41")) # Added another pig
        self.pigs.append(Pig(base_x-30, ground_y + pig_r_upper, self.space, pig_r_upper, "n51")) # Added another pig

    def build_14(self): # "Ice Bridge"
        self.number = 14
        self.level_birds = ["trala", "trala", "glorbo", "bomb"]
        self.number_of_birds = 4
        self.one_star = 26000
        self.two_star = 42000
        self.three_star = 58000
        ground_y = 130.0

        # --- Terrain: Two flat plateaus separated by a wide rectangular loch ---
        # Launch Plateau (flat top at ground_y + 30)
        launch_plat_y = ground_y # Kept original height for launch side
        self._add_static_terrain("poly", [(150, ground_y), (250, launch_plat_y), (350, launch_plat_y), (350, ground_y)], terrain_tag="hill")

        # Landing Plateau (flat top at ground_y + 30)
        landing_plat_y = ground_y # Kept original height for landing side base
        self._add_static_terrain("poly", [(950, ground_y), (950, landing_plat_y), (1050, landing_plat_y), (1150, ground_y)], terrain_tag="hill")

        loch_start_x, loch_end_x = 400, 940
        loch_dip_y = 20
        # The top of the loch walls will align with the plateau height or ground_y of adjacent terrain.
        # For simplicity, let's assume the loch walls go up to the launch_plat_y / landing_plat_y level.
        # However, the original code had ground_y+30 for the start/end points of the loch segments.
        # Let's make the loch rectangular, with its top edge at launch_plat_y.
        loch_segments_points = [
            # Left wall of the loch
            ((loch_start_x, launch_plat_y), (loch_start_x, loch_dip_y)),
            # Bottom of the loch (flat)
            ((loch_start_x, loch_dip_y), (loch_end_x, loch_dip_y)),
            # Right wall of the loch
            ((loch_end_x, loch_dip_y), (loch_end_x, landing_plat_y))
        ]
        for p_start, p_end in loch_segments_points:
            self._add_static_terrain("segment", (p_start, p_end), terrain_tag="loch", radius=1.0) # Thinner walls for a cleaner look
        self.loch_extent_x = (loch_start_x, loch_end_x)
        self.loch_water_surface_y_override = launch_plat_y # For correct water rendering
        self.loch_rect_bottom_y_for_water_fill = loch_dip_y   # For correct water rendering

        # --- Ice Bridge and its pigs REMOVED ---

        # --- Add a small flat hill on the landing plateau for the structure ---
        structure_hill_base_y = landing_plat_y # Base of this small hill is on the landing plateau
        structure_hill_height = 100
        structure_hill_top_y = structure_hill_base_y + structure_hill_height
        structure_hill_x_start = 950 # Matches landing plateau edge
        structure_hill_x_end = 1050  # Matches landing plateau edge
        
        structure_hill_vertices = [
            (structure_hill_x_start, structure_hill_base_y+30),
            (structure_hill_x_start, structure_hill_top_y+30),
            (structure_hill_x_end, structure_hill_top_y+30),
            (structure_hill_x_end, structure_hill_base_y+30)
        ]
        self._add_static_terrain("poly", structure_hill_vertices, terrain_tag="hill_structure_base")

        # Small stone structure on the far plateau
        self._create_template_structure_A(1000, ground_y_offset=30 + structure_hill_height) # Adjusted offset for the new small hill
        # Add an exploding crate
        self.circles.append(Polygon(
            pos=(700, ground_y + 15), # Centered in the loch area
            length=30, height=30, space=self.space, life=EXPLODING_CRATE_HP,
            element_type="exploding_crate", screen_height=self.screen_height,
            screen_width=self.screen_width, mass=EXPLODING_CRATE_MASS, radius=15,
            image_path=EXPLODING_CRATE_IMG_PATH,
            is_explosive_obj=True, explosion_params=exploding_crate_params_default
        ))

    def build_15(self): # "Stacked Defense"
        self.number = 15
        self.level_birds = ["sahur", "bomb", "patapim"] # Reduced birds
        self.number_of_birds = 3
        self.one_star = 30000
        self.two_star = 48000
        self.three_star = 65000
        ground_y = 130.0

        # --- Terrain: A wide, slightly raised platform ---
        plat_y = ground_y + 10
        self._add_static_terrain("poly", [(300, ground_y), (400, plat_y), (900, plat_y), (1000, ground_y)], terrain_tag="platform")

        # --- Main Structure: Tall, multi-layered ---
        base_x = 650
        self._create_template_structure_A(base_x, ground_y_offset=10) # Main tower

        # Add some smaller, more fragile side elements
        side_col_h, side_col_w = 40, 12
        side_beam_h, side_beam_l = 12, 50
        pig_r_small = 8

        # Left side structure
        y_sc1_l = plat_y + side_col_h/2
        self.columns.append(Polygon((base_x - 120, y_sc1_l), side_col_w, side_col_h, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood"))
        y_sb1_l = y_sc1_l + side_col_h/2 + side_beam_h/2
        self.beams.append(Polygon((base_x - 120, y_sb1_l), side_beam_l, side_beam_h, self.space, wood_hp, "beams", self.screen_height, self.screen_width, material_type="wood"))
        self.pigs.append(Pig(base_x - 120, y_sb1_l + side_beam_h/2 + pig_r_small, self.space, pig_r_small, "n41"))

        # Right side structure (ice)
        y_sc1_r = plat_y + side_col_h/2
        self.columns.append(Polygon((base_x + 120, y_sc1_r), side_col_w, side_col_h, self.space, ice_hp, "columns", self.screen_height, self.screen_width, material_type="ice"))
        y_sb1_r = y_sc1_r + side_col_h/2 + side_beam_h/2
        self.beams.append(Polygon((base_x + 120, y_sb1_r), side_beam_l, side_beam_h, self.space, ice_hp, "beams", self.screen_height, self.screen_width, material_type="ice"))
        self.pigs.append(Pig(base_x + 120, y_sb1_r + side_beam_h/2 + pig_r_small, self.space, pig_r_small, "n51"))
        # Add an exploding crate
        self.circles.append(Polygon(
            pos=(base_x, plat_y +10), # Below the main structure
            length=28, height=28, space=self.space, life=EXPLODING_CRATE_HP,
            element_type="exploding_crate", screen_height=self.screen_height,
            screen_width=self.screen_width, mass=EXPLODING_CRATE_MASS, radius=14,
            image_path=EXPLODING_CRATE_IMG_PATH,
            is_explosive_obj=True, explosion_params=exploding_crate_params_default
        ))


    def build_16(self):
        self.number = 16
        ground_y = 130.0
        self.level_birds = ["liri", "bomb"] # Reduced birds
        self.number_of_birds = 2
        self.one_star = 27000
        self.two_star = 43000
        self.three_star = 59000

        # Basic terrain
        self._add_static_terrain("poly", [(200, ground_y), (300, ground_y + 40), (400, ground_y)], terrain_tag="hill_low")
        self._add_static_terrain("poly", [(900, ground_y), (1000, ground_y + 30), (1100, ground_y)], terrain_tag="hill_low")

        # Stable structure using Template A
        structure_base_x = 700
        self._create_template_structure_A(base_x=structure_base_x)
        # Add a couple of extra pigs around the main structure for variety
        self.pigs.append(Pig(structure_base_x - 100, ground_y + 10, self.space, 12, "n41"))
        self.pigs.append(Pig(structure_base_x + 100, ground_y + 10, self.space, 12, "n51"))
        # Add an exploding crate
        self.circles.append(Polygon(
            pos=(structure_base_x + 150, ground_y + 12),
            length=25, height=25, space=self.space, life=EXPLODING_CRATE_HP,
            element_type="exploding_crate", screen_height=self.screen_height,
            screen_width=self.screen_width, mass=EXPLODING_CRATE_MASS, radius=12,
            image_path=EXPLODING_CRATE_IMG_PATH,
            is_explosive_obj=True, explosion_params=exploding_crate_params_default
        ))

    def build_18(self):
        self.number = 18
        ground_y = 130.0
        self.level_birds = ["trala", "patapim", "liri"] # Reduced birds
        self.number_of_birds = 3
        self.one_star = 28000
        self.two_star = 44000
        self.three_star = 60000

        # Terrain with a small loch
        self._add_static_terrain("poly", [(250, ground_y), (350, ground_y + 20), (450, ground_y)], terrain_tag="hill_low")
        loch_s_x, loch_e_x = 500, 700
        loch_d_y = ground_y - 50
        self._add_static_terrain("segment", ((loch_s_x, ground_y), (loch_s_x + 50, loch_d_y)), terrain_tag="loch")
        self._add_static_terrain("segment", ((loch_s_x + 50, loch_d_y), (loch_e_x - 50, loch_d_y)), terrain_tag="loch")
        self._add_static_terrain("segment", ((loch_e_x - 50, loch_d_y), (loch_e_x, ground_y)), terrain_tag="loch")
        self.loch_extent_x = (loch_s_x, loch_e_x)

        # Stable structure using Template B after the loch
        structure_base_x = 850
        self._create_template_structure_B(base_x=structure_base_x)
        # Add an exploding crate
        self.circles.append(Polygon(
            pos=(structure_base_x - 150, ground_y + 15),
            length=30, height=30, space=self.space, life=EXPLODING_CRATE_HP,
            element_type="exploding_crate", screen_height=self.screen_height,
            screen_width=self.screen_width, mass=EXPLODING_CRATE_MASS, radius=15,
            image_path=EXPLODING_CRATE_IMG_PATH,
            is_explosive_obj=True, explosion_params=exploding_crate_params_default
        ))

    def build_20(self):
        self.number = 20
        ground_y = 130.0
        self.level_birds = ["glorbo", "bomb"] # Reduced birds
        self.number_of_birds = 2
        self.one_star = 29000
        self.two_star = 46000
        self.three_star = 62000

        # Basic terrain
        self._add_static_terrain("poly", [(300, ground_y), (400, ground_y + 30), (500, ground_y)], terrain_tag="hill_low")

        # Adapted from _create_template_structure_A
        base_x = 750
        col_h, col_w = 65, 18
        beam_h = 18
        beam_l_original = 75 # Original beam length from template
        beam_l_first_layer_narrowed = 50 # Narrower beam for the first layer
        pig_r = 11

        # Layer 1 (with narrowed beam)
        y_c1 = ground_y + col_h/2
        self.columns.append(Polygon((base_x - 30, y_c1), col_w, col_h, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood"))
        self.columns.append(Polygon((base_x + 30, y_c1), col_w, col_h, self.space, wood_hp, "columns", self.screen_height, self.screen_width, material_type="wood"))
        y_b1 = y_c1 + col_h/2 + beam_h/2
        self.beams.append(Polygon((base_x, y_b1), beam_l_first_layer_narrowed, beam_h, self.space, wood_hp, "beams", self.screen_height, self.screen_width, material_type="wood"))
        self.pigs.append(Pig(base_x, y_b1 + beam_h/2 + pig_r, self.space, pig_r, "n11"))

        # Layer 2 (using original beam length for variety, or could also be narrowed)
        y_c2 = y_b1 + beam_h/2 + col_h/2
        self.columns.append(Polygon((base_x - 20, y_c2), col_w-4, col_h, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone"))
        self.columns.append(Polygon((base_x + 20, y_c2), col_w-4, col_h, self.space, stone_hp, "columns", self.screen_height, self.screen_width, material_type="stone"))
        y_b2 = y_c2 + col_h/2 + beam_h/2
        self.beams.append(Polygon((base_x, y_b2), beam_l_original-15, beam_h, self.space, stone_hp, "beams", self.screen_height, self.screen_width, material_type="stone"))
        self.pigs.append(Pig(base_x+20, y_b2 + beam_h/2 + pig_r, self.space, pig_r, "n21"))

        # Layer 3 (Topper - can reuse template logic or simplify)
        y_c3 = y_b2 + beam_h/2 + (col_h-15)/2
        self.columns.append(Polygon((base_x, y_c3), col_w-6, col_h-15, self.space, ice_hp, "columns", self.screen_height, self.screen_width, material_type="ice"))
        y_b3 = y_c3 + (col_h-15)/2 + (beam_h-6)/2
        self.beams.append(Polygon((base_x, y_b3), beam_l_original-35, beam_h-6, self.space, ice_hp, "beams", self.screen_height, self.screen_width, material_type="ice"))
        self.pigs.append(Pig(base_x, y_b3 + (beam_h-6)/2 + pig_r, self.space, pig_r, "n31"))
        # Add an exploding crate
        self.circles.append(Polygon(
            pos=(base_x + 150, ground_y + 11),
            length=22, height=22, space=self.space, life=EXPLODING_CRATE_HP,
            element_type="exploding_crate", screen_height=self.screen_height,
            screen_width=self.screen_width, mass=EXPLODING_CRATE_MASS, radius=11,
            image_path=EXPLODING_CRATE_IMG_PATH,
            is_explosive_obj=True, explosion_params=exploding_crate_params_default
        ))

# Placeholder build methods for levels 16-42 using templates
for i in range(17, 43): # Placeholder loop adjusted
    if i == 18: continue # Skip 18 as it's now defined
    if i == 20: continue # Skip 20 as it's now defined
    def _create_placeholder_build_method(level_num):
        def placeholder_build(self):
            self.number = level_num
            ground_y = 130.0
            
            # Basic bird setup, can be randomized further
            # Make bird selection deterministic based on level_num
            bird_options = ["sahur", "liri", "trala", "bomb", "patapim", "glorbo", "palocleves"] # Keep the order consistent
            
            # Determine number of birds based on level_num (e.g., cycles 4, 5, 6)
            # (level_num % 3) gives 0, 1, or 2. Add 4 to get 4, 5, or 6.
            # New logic: 2 or 3 birds for levels > 1
            self.number_of_birds = 2 if level_num % 2 == 0 else 3 # Deterministic 2 or 3 birds
            # Select birds deterministically
            self.level_birds = []
            for i in range(self.number_of_birds):
                # Cycle through bird_options based on level_num and bird index
                bird_index = (level_num + i*2) % len(bird_options) # i*2 for more variation per bird slot
                self.level_birds.append(bird_options[bird_index])

            self.one_star = 20000 + (level_num * 700) 
            self.two_star = 35000 + (level_num * 700)
            self.three_star = 50000 + (level_num * 700)

            # Randomly choose a template or terrain setup
            # Make the choice deterministic based on the level number
            # This ensures that level X will always get the same structure type.
            choice = level_num % 3 # Results in 0, 1, or 2 consistently for a given level_num

            # --- Make random offsets deterministic based on level_num ---
            # We can use level_num to derive consistent "random-like" offsets.
            # Example: offset_x = (level_num * 7) % 101 - 50  (gives a range from -50 to 50)
            #          offset_y = (level_num * 13) % 21      (gives a range from 0 to 20)
            #          chance_for_second_structure = (level_num * 3) % 2 == 0 (True or False consistently)

            deterministic_offset_x1 = (level_num * 7) % 101 - 50 # Range -50 to 50
            deterministic_offset_y1 = (level_num * 13) % 21    # Range 0 to 20
            deterministic_offset_x2 = (level_num * 5) % 61 - 30  # Range -30 to 30
            chance_for_second_structure = (level_num * 3) % 2 == 0 # Consistent True/False

            # Standard explosion parameters for placeholder crates
            current_placeholder_crate_explosion_params = { # Use a distinct name
                "radius": 110 + (level_num % 30) - 15, # Vary radius slightly: 95 to 125
                "damage_pigs": 160 + (level_num % 40) - 20, # Vary damage: 140 to 180
                "damage_polys": 1200 + (level_num % 200) - 100, # Vary damage: 1100 to 1300
                "knockback": 6500 + (level_num % 1000) - 500 # Vary knockback: 6000 to 7000
            }
            crate_added_by_placeholder = False

            if choice == 0: # Use Template A with some terrain
                self._add_static_terrain("poly", [(200, ground_y), (300, ground_y + 30), (400, ground_y)], terrain_tag="hill_low")
                self._create_template_structure_A(base_x=650 + deterministic_offset_x1)
                if chance_for_second_structure: # Chance for a second smaller structure
                    self._create_template_structure_A(base_x=950 + deterministic_offset_x2, ground_y_offset=deterministic_offset_y1)
                    # Scale down the second structure slightly for variety (by reducing col_h, beam_l in a real scenario)
                
                # Add 1-2 crates for choice 0
                self.circles.append(Polygon(
                    pos=(650 + deterministic_offset_x1 - 100, ground_y + 12),
                    length=25, height=25, space=self.space, life=EXPLODING_CRATE_HP,
                    element_type="exploding_crate", screen_height=self.screen_height,
                    screen_width=self.screen_width, mass=EXPLODING_CRATE_MASS, radius=12,
                    image_path=EXPLODING_CRATE_IMG_PATH, is_explosive_obj=True,
                    explosion_params=current_placeholder_crate_explosion_params
                ))
                if (level_num % 4 == 0): # Add a second crate sometimes
                    self.circles.append(Polygon(
                        pos=(650 + deterministic_offset_x1 + 150, ground_y + 12),
                        length=25, height=25, space=self.space, life=EXPLODING_CRATE_HP,
                        element_type="exploding_crate", screen_height=self.screen_height,
                        screen_width=self.screen_width, mass=EXPLODING_CRATE_MASS, radius=12,
                        image_path=EXPLODING_CRATE_IMG_PATH, is_explosive_obj=True,
                        explosion_params=current_placeholder_crate_explosion_params ))
                crate_added_by_placeholder = True

            elif choice == 1: # Use Template B with a loch
                loch_s_x = 400 + deterministic_offset_x1 // 2 # Use a portion of the offset
                loch_e_x = 800 + deterministic_offset_x2 // 2
                loch_d_y = 30 + deterministic_offset_y1 // 2
                # Ensure loch_d_y is not too high, should be below ground_y
                loch_d_y = min(loch_d_y, int(ground_y) - 20) # at least 20 units deep from ground_y

                loch_segments = [
                    ((loch_s_x, ground_y), (loch_s_x + 100, loch_d_y)),
                    ((loch_s_x + 100, loch_d_y), (loch_e_x - 100, loch_d_y)),
                    ((loch_e_x - 100, loch_d_y), (loch_e_x, ground_y))
                ]
                for p_s, p_e in loch_segments:
                    self._add_static_terrain("segment", (p_s, p_e), terrain_tag="loch")
                self.loch_extent_x = (loch_s_x, loch_e_x)
                # Ensure structure after loch is on screen
                struct_b_base_x = loch_e_x + 150 + (deterministic_offset_x1 % 41 - 20)
                struct_b_base_x = min(struct_b_base_x, 1000) # Keep it from going too far right
                self._create_template_structure_B(base_x=struct_b_base_x)

                # Add 1-2 crates for choice 1
                self.circles.append(Polygon(
                    pos=(loch_s_x - 50, ground_y + 12), # On the bank before the loch
                    length=25, height=25, space=self.space, life=EXPLODING_CRATE_HP,
                    element_type="exploding_crate", screen_height=self.screen_height,
                    screen_width=self.screen_width, mass=EXPLODING_CRATE_MASS, radius=12,
                    image_path=EXPLODING_CRATE_IMG_PATH, is_explosive_obj=True,
                    explosion_params=current_placeholder_crate_explosion_params
                ))
                if (level_num % 4 == 1): # Add a second crate sometimes
                    self.circles.append(Polygon(
                        pos=(struct_b_base_x + 100, ground_y + 12), # Near structure B
                        length=25, height=25, space=self.space, life=EXPLODING_CRATE_HP,
                        element_type="exploding_crate", screen_height=self.screen_height,
                        screen_width=self.screen_width, mass=EXPLODING_CRATE_MASS, radius=12,
                        image_path=EXPLODING_CRATE_IMG_PATH, is_explosive_obj=True,
                        explosion_params=current_placeholder_crate_explosion_params ))
                crate_added_by_placeholder = True

            else: # Default to build_0's content if no specific template chosen or for more variety
                # build_0() sets self.number = 1. We must ensure the placeholder's
                # actual level number (level_num) is restored after calling build_0().
                self.build_0() 
                # Add an extra crate if using build_0 as a base for placeholder
                self.circles.append(Polygon(
                    pos=(400, ground_y + 12), # A fixed position for build_0 based placeholders
                    length=25, height=25, space=self.space, life=EXPLODING_CRATE_HP,
                    element_type="exploding_crate", screen_height=self.screen_height, screen_width=self.screen_width, mass=EXPLODING_CRATE_MASS, radius=12, image_path=EXPLODING_CRATE_IMG_PATH, is_explosive_obj=True, explosion_params=current_placeholder_crate_explosion_params))
                # If build_0's pigs are too many/few, adjust build_0() or add specific pigs here.
                # Example: Add a few specific pigs if build_0's are cleared or insufficient
                # self.pigs.clear() # If you still want to clear build_0's pigs
                # self.pigs.append(Pig(850, ground_y + 20, self.space, 12, "n11"))
                # self.pigs.append(Pig(950, ground_y + 50, self.space, 14, "n21"))
                # For now, we will keep the pigs from build_0() for this case.
                # If build_0() places pigs randomly, that randomness will persist here.
                # The build_0() provided places pigs in a specific area (800-1100 x).
            
            # Crucially, ensure self.number is the correct placeholder level number
            # before this build method finishes.
            if self.number != level_num:
                self.number = level_num
            
            # Add a few more random pigs for all placeholder types, EXCEPT for level 17
            if level_num != 17:
                for _ in range(random.randint(1, 3)): # Add 1 to 3 extra pigs
                    px = random.randint(400, 1100)
                    py = ground_y + random.randint(10, 100) # Place them on ground or slightly elevated
                    self.pigs.append(Pig(px, py, self.space, random.choice([10,12,15]), random.choice(["n11","n21","n31"])))

            if crate_added_by_placeholder:
                print(f"Loaded template-based placeholder for level {level_num} and added a crate.")
            else:
                print(f"Loaded template-based placeholder for level {level_num} (crate might be from build_0).")
        return placeholder_build
    setattr(Level, f"build_{i}", _create_placeholder_build_method(i))
