# level.py

from character import Pig
from Polygon import Polygon
import random
import time


wood_hp = 20
stone_hp = 30
ice_hp = 10

class Level():
    
    def __init__(self, pigs, columns, beams, circles, triangles, space, screen_height, screen_width):
        """
        Initializes a Level object.

        Args:
            pigs (list): List to store Pig objects.
            columns (list): List to store Polygon objects representing columns.
            beams (list): List to store Polygon objects representing beams.
            circles (list): List to store Polygon objects representing circles.
            triangles (list): List to store Polygon objects representing triangles.
            space: The space object.
        """
        self.pigs = pigs
        self.columns = columns
        self.beams = beams
        self.circles = circles
        self.triangles = triangles
        self.space = space
        self.number = 0
        self.number_of_birds = 4
        self.bool_space = False
        self.locked = ["","","build_2","build_3","build_4","build_5","build_6","build_7","build_8"] # Corrected indexing to start from 0
        
        # lower limit
        self.one_star = 20000
        self.two_star = 32500
        self.three_star = 45000
        
        self.bool_space = False
        
        self.screen_height = screen_height
        self.screen_width = screen_width
        
        self.base_width, self.base_height = 1200, 650
        self.scale_x = self.screen_width / self.base_width
        self.scale_y = self.screen_height / self.base_height
    
    

    def scale_pos(self, x, y):
        return x * self.scale_x, y * self.scale_y


    def clear_level(self):
        """Clears all pigs, columns, and beams from the lists."""
        self.pigs.clear()
        self.columns.clear()
        self.beams.clear()
        self.circles.clear()
        self.triangles.clear()
        self.number_of_birds = 4  # Reset the number of birds

    

    def build_0(self):
        self.number = 1
        self.level_birds = ["sahur","liri","trala","palocleves","bomb","patapim","glorbo"]
        self.number_of_birds = 7
        locked = False
        # Define the range for the random y-coordinates, including negative values
        min_y = 150  # Changed to negative
        max_y = 600
        min_x = 0
        max_x = self.screen_width
        
        pig1 = Pig(random.randint(min_x, max_x), random.randint(min_y, max_y), self.space, 10, "n11")
        #pig1_2 = Pig(random.randint(min_x, max_x), random.randint(min_y, max_y), self.space, 10, "n12")
        pig2 = Pig(random.randint(min_x, max_x), random.randint(min_y, max_y), self.space, 12, "n21")
        #pig2_2 = Pig(random.randint(min_x, max_x), random.randint(min_y, max_y), self.space, 10, "n22")
        pig3 = Pig(random.randint(min_x, max_x), random.randint(min_y, max_y), self.space, 10, "n31")
        #pig3_2 = Pig(random.randint(min_x, max_x), random.randint(min_y, max_y), self.space, 10, "n32")
        pig4 = Pig(random.randint(min_x, max_x), random.randint(min_y, max_y), self.space, 15, "n41")
        #pig4_2 = Pig(random.randint(min_x, max_x), random.randint(min_y, max_y), self.space, 10, "n42")
        pig5 = Pig(random.randint(min_x, max_x), random.randint(min_y, max_y), self.space, 10, "n51")
        #pig5_2 = Pig(random.randint(min_x, max_x), random.randint(min_y, max_y), self.space, 10, "n52")
        pig6 = Pig(random.randint(min_x, max_x), random.randint(min_y, max_y), self.space, 10, "n11")
        #pig1_2 = Pig(random.randint(min_x, max_x), random.randint(min_y, max_y), self.space, 10, "n12")
        pig7 = Pig(random.randint(min_x, max_x), random.randint(min_y, max_y), self.space, 12, "n21")
        #pig2_2 = Pig(random.randint(min_x, max_x), random.randint(min_y, max_y), self.space, 10, "n22")
        pig8 = Pig(random.randint(min_x, max_x), random.randint(min_y, max_y), self.space, 10, "n31")
        #pig3_2 = Pig(random.randint(min_x, max_x), random.randint(min_y, max_y), self.space, 10, "n32")
        pig9 = Pig(random.randint(min_x, max_x), random.randint(min_y, max_y), self.space, 15, "n41")
        #pig4_2 = Pig(random.randint(min_x, max_x), random.randint(min_y, max_y), self.space, 10, "n42")
        pig10 = Pig(random.randint(min_x, max_x), random.randint(min_y, max_y), self.space, 10, "n51")
        #pig5_2 = Pig(random.randint(min_x, max_x), random.randint(min_y, max_y), self.space, 10, "n52")

        piggs = [pig1,pig2,pig3,pig4,pig5,pig6,pig7,pig8,pig9,pig10]   
        
        
             

        for pig in piggs:
            self.pigs.append(pig)
            
        

        

    def build_1(self):
        """Builds level 1."""

        self.number = 1
        self.level_birds = ["sahur","liri","sahur","palocleves","palocleves","trala"]
        self.number_of_birds = 6
        locked = False
        pig1 = Pig(400,130,self.space,10,"n11")
        pig2 = Pig(450,130,self.space,12,"n21")
        pig3 = Pig(500,130,self.space,10,"n31")
        pig4 = Pig(550,130,self.space,15,"n41")
        pig5 = Pig(600,130,self.space,10,"n51")

        self.pigs.append(pig1)
        self.pigs.append(pig2)
        self.pigs.append(pig3)
        self.pigs.append(pig4)
        self.pigs.append(pig5)
        
        self.number_of_birds = 4

        # create beam and column

        p = self.scale_pos(950,150)
        self.columns.append(Polygon(p,20,85,self.space, wood_hp, "columns", self.screen_height, self.screen_width))
        
        p = self.scale_pos(900,150)
        self.columns.append(Polygon(p,20,85,self.space, ice_hp, "columns", self.screen_height, self.screen_width))
        
        p = self.scale_pos(950,260)
        self.columns.append(Polygon(p,20,85,self.space, wood_hp , "columns", self.screen_height, self.screen_width))
        
        p = self.scale_pos(900,220)
        self.beams.append(Polygon(p,85,20,self.space,wood_hp , "beams", self.screen_height, self.screen_width))
        p = self.scale_pos(800,220)
        self.beams.append(Polygon(p,85,20,self.space,ice_hp , "beams", self.screen_height, self.screen_width))
        p = self.scale_pos(700,220)
        self.beams.append(Polygon(p,85,20,self.space,stone_hp , "beams", self.screen_height, self.screen_width))


        

        p = self.scale_pos(700,510)
        self.circles.append(Polygon(p,20,20,self.space, wood_hp , "circles", self.screen_height, self.screen_width))
        p = self.scale_pos(600,510)
        self.circles.append(Polygon(p,20,20,self.space, stone_hp , "circles", self.screen_height, self.screen_width))
        p = self.scale_pos(550,510)
        self.circles.append(Polygon(p,20,20,self.space, ice_hp , "circles", self.screen_height, self.screen_width))
        
        p = self.scale_pos(200,320)
        self.triangles.append(Polygon(p, 30, 30, self.space, stone_hp, "triangles", self.screen_height, self.screen_width))
        p = self.scale_pos(200,370)
        self.triangles.append(Polygon(p, 30, 30, self.space, ice_hp, "triangles", self.screen_height, self.screen_width))
        p = self.scale_pos(150,350)
        self.triangles.append(Polygon(p, 30, 30, self.space, wood_hp, "triangles", self.screen_height, self.screen_width))
        p = self.scale_pos(200,320)
        self.triangles.append(Polygon(p, 30, 30, self.space, stone_hp, "triangles", self.screen_height, self.screen_width))
        p = self.scale_pos(200,370)
        self.triangles.append(Polygon(p, 30, 30, self.space, ice_hp, "triangles", self.screen_height, self.screen_width))
        p = self.scale_pos(220,350)
        self.triangles.append(Polygon(p, 30, 30, self.space, wood_hp, "triangles", self.screen_height, self.screen_width))

        if self.bool_space:
            self.number_of_birds = 8
            
        


    def build_2(self):
        """Builds level 2."""
        self.number = 2
        self.level_birds = ["sahur","liri","sahur","palocleves","palocleves"] # Added level birds
        self.number_of_birds = 5 # added number of birds
        locked = True
        pig1 = Pig(800,230,self.space,13, "n11") # Added id
        #pig2 = Pig(985,130,self.space)
        
        self.pigs.append(pig1)
        #self.pigs.append(pig2)

        # create beam and column

        p = (900,150)
        self.columns.append(Polygon(p,20,85,self.space,wood_hp, "columns", self.screen_height, self.screen_width))
        
        p = (1010,150)
        self.columns.append(Polygon(p,20,85,self.space,wood_hp , "columns", self.screen_height, self.screen_width))
        
        p = (950,260)
        self.columns.append(Polygon(p,20,85,self.space,wood_hp , "columns", self.screen_height, self.screen_width))
        
        p = (1010,260)
        self.columns.append(Polygon(p,20,85,self.space,wood_hp , "columns", self.screen_height, self.screen_width))


        p = (980,220)
        self.beams.append(Polygon(p,85,20,self.space,wood_hp , "beams", self.screen_height, self.screen_width))
        
        p = (980,310)
        self.beams.append(Polygon(p,85,20,self.space,wood_hp , "beams", self.screen_height, self.screen_width))

        self.number_of_birds = 4
        if self.bool_space:
            self.number_of_birds = 8
    
    
    def build_3(self):
        """Builds level 3."""
        self.number = 3
        self.level_birds = ["sahur","liri","sahur","palocleves","palocleves"] # Added level birds
        self.number_of_birds = 5 # added number of birds
        locked = True
        pig1 = Pig(980,230,self.space,13, "n11") # Added id
        pig2 = Pig(985,130,self.space,31, "n21") # Added id

        self.pigs.append(pig1)
        self.pigs.append(pig2)

        # create beam and column

        p = (950,150)
        self.columns.append(Polygon(p,20,85,self.space,wood_hp , "columns", self.screen_height, self.screen_width))
        
        p = (1010,150)
        self.columns.append(Polygon(p,20,85,self.space,wood_hp , "columns", self.screen_height, self.screen_width))
        
        p = (900,260)
        self.columns.append(Polygon(p,20,85,self.space,wood_hp , "columns", self.screen_height, self.screen_width))
        
        p = (1010,260)
        self.columns.append(Polygon(p,20,85,self.space,wood_hp , "columns", self.screen_height, self.screen_width))


        p = (980,220)
        self.beams.append(Polygon(p,85,20,self.space,wood_hp , "beams", self.screen_height, self.screen_width))
        
        p = (980,310)
        self.beams.append(Polygon(p,85,20,self.space,wood_hp , "beams", self.screen_height, self.screen_width))

        self.number_of_birds = 4
        if self.bool_space:
            self.number_of_birds = 8
    
    
    
    def build_4(self):
        """Builds level 4."""
        self.number = 4
        self.level_birds = ["sahur","liri","sahur","palocleves","palocleves"] # Added level birds
        self.number_of_birds = 5 # added number of birds
        locked = True
        pig1 = Pig(980,230,self.space,31, "n11") # Added id
        pig2 = Pig(985,130,self.space,13, "n21") # Added id

        self.pigs.append(pig1)
        self.pigs.append(pig2)

        # create beam and column

        p = (950,150)
        self.columns.append(Polygon(p,20,85,self.space,wood_hp , "columns", self.screen_height, self.screen_width))
        
        p = (1010,150)
        self.columns.append(Polygon(p,20,85,self.space,wood_hp , "columns", self.screen_height, self.screen_width))
        
        p = (950,260)
        self.columns.append(Polygon(p,20,85,self.space,wood_hp , "columns", self.screen_height, self.screen_width))
        
        p = (1010,260)
        self.columns.append(Polygon(p,20,85,self.space,wood_hp , "columns", self.screen_height, self.screen_width))


        p = (900,220)
        self.beams.append(Polygon(p,85,20,self.space,wood_hp , "beams", self.screen_height, self.screen_width))
        
        p = (980,310)
        self.beams.append(Polygon(p,85,20,self.space,wood_hp , "beams", self.screen_height, self.screen_width))

        self.number_of_birds = 4
        if self.bool_space:
            self.number_of_birds = 8
    
    
    
    def build_5(self):
        """Builds level 5."""
        self.number = 5
        self.level_birds = ["sahur","liri","sahur","palocleves","palocleves"] # Added level birds
        self.number_of_birds = 5 # added number of birds
        locked = True
        pig1 = Pig(980,230,self.space,13, "n11") # Added id
        pig2 = Pig(985,130,self.space,31, "n21") # Added id

        self.pigs.append(pig1)
        self.pigs.append(pig2)

        # create beam and column

        p = (950,150)
        self.columns.append(Polygon(p,20,85,self.space,wood_hp , "columns", self.screen_height, self.screen_width))
        
        p = (1010,150)
        self.columns.append(Polygon(p,20,85,self.space,wood_hp , "columns", self.screen_height, self.screen_width))
        
        p = (950,260)
        self.columns.append(Polygon(p,20,85,self.space,wood_hp , "columns", self.screen_height, self.screen_width))
        
        p = (1010,260)
        self.columns.append(Polygon(p,20,85,self.space,wood_hp , "columns", self.screen_height, self.screen_width))


        p = (980,250)
        self.beams.append(Polygon(p,85,20,self.space,wood_hp , "beams", self.screen_height, self.screen_width))
        
        p = (980,310)
        self.beams.append(Polygon(p,85,20,self.space,wood_hp , "beams", self.screen_height, self.screen_width))

        self.number_of_birds = 4
        if self.bool_space:
            self.number_of_birds = 8
    
    
    
    def build_6(self):
        """Builds level 6."""
        self.number = 6
        self.level_birds = ["sahur","liri","sahur","palocleves","palocleves"] # Added level birds
        self.number_of_birds = 5 # added number of birds
        locked = True
        pig1 = Pig(980,230,self.space,13, "n11") # Added id
        pig1.life = 40
        pig2 = Pig(985,130,self.space,31, "n21") # Added id

        self.pigs.append(pig1)
        self.pigs.append(pig2)
        

        # create beam and column

        p = (950,150)
        self.columns.append(Polygon(p,20,85,self.space,wood_hp , "columns", self.screen_height, self.screen_width))
        
        p = (1010,150)
        self.columns.append(Polygon(p,20,85,self.space,wood_hp , "columns", self.screen_height, self.screen_width))
        
        p = (950,260)
        self.columns.append(Polygon(p,20,85,self.space,wood_hp , "columns", self.screen_height, self.screen_width))
        
        p = (810,260)
        self.columns.append(Polygon(p,20,85,self.space,wood_hp , "columns", self.screen_height, self.screen_width))


        p = (980,220)
        self.beams.append(Polygon(p,85,20,self.space,wood_hp , "beams", self.screen_height, self.screen_width))
        
        p = (980,310)
        self.beams.append(Polygon(p,85,20,self.space,wood_hp , "beams", self.screen_height, self.screen_width))

        self.number_of_birds = 4
        if self.bool_space:
            self.number_of_birds = 8

    def build_7(self):
        """Builds level 7."""
        self.number = 7
        self.level_birds = ["sahur","liri","sahur","palocleves","palocleves"]  # Added level birds
        self.number_of_birds = 5
        locked = True

        # Pigs
        pig1 = Pig(750, 100, self.space, 15, "n11")
        pig2 = Pig(850, 100, self.space, 15, "n21")
        pig3 = Pig(800, 150, self.space, 20, "n31")

        self.pigs.extend([pig1, pig2, pig3])

        # Columns
        col1 = Polygon((700, 200), 20, 100, self.space, wood_hp, "columns", self.screen_height, self.screen_width)
        col2 = Polygon((900, 200), 20, 100, self.space, wood_hp, "columns", self.screen_height, self.screen_width)
        col3 = Polygon((700, 350), 20, 100, self.space, stone_hp, "columns", self.screen_height, self.screen_width)
        col4 = Polygon((900, 350), 20, 100, self.space, stone_hp, "columns", self.screen_height, self.screen_width)

        self.columns.extend([col1, col2, col3, col4])

        # Beams
        beam1 = Polygon((800, 250), 200, 20, self.space, wood_hp, "beams", self.screen_height, self.screen_width)
        beam2 = Polygon((800, 400), 200, 20, self.space, stone_hp, "beams", self.screen_height, self.screen_width)

        self.beams.extend([beam1, beam2])

        # Circles
        circle1 = Polygon((750, 480), 30, 30, self.space, ice_hp, "circles", self.screen_height, self.screen_width)
        circle2 = Polygon((850, 480), 30, 30, self.space, ice_hp, "circles", self.screen_height, self.screen_width)
        self.circles.extend([circle1, circle2])

        self.number_of_birds = 4
        if self.bool_space:
            self.number_of_birds = 8

    def build_8(self):
        """Builds level 8."""
        self.number = 8
        self.level_birds = ["sahur", "liri", "sahur", "palocleves", "palocleves"]  # Added level birds.
        self.number_of_birds = 5
        locked = True

        # Pigs
        pig1 = Pig(600, 100, self.space, 10, "n11")
        pig2 = Pig(650, 150, self.space, 12, "n21")
        pig3 = Pig(700, 100, self.space, 10, "n31")
        pig4 = Pig(625, 200, self.space, 15, "n41")
        pig5 = Pig(675, 200, self.space, 15, "n51")

        self.pigs.extend([pig1, pig2, pig3, pig4, pig5])

        # Columns
        col1 = Polygon((550, 300), 20, 120, self.space, ice_hp, "columns", self.screen_height, self.screen_width)
        col2 = Polygon((750, 300), 20, 120, self.space, ice_hp, "columns", self.screen_height, self.screen_width)
        col3 = Polygon((650, 450), 20, 100, self.space, stone_hp, "columns", self.screen_height, self.screen_width)

        self.columns.extend([col1, col2, col3])

        # Beams
        beam1 = Polygon((650, 350), 200, 20, self.space, wood_hp, "beams", self.screen_height, self.screen_width)
        beam2 = Polygon((650, 500), 200, 20, self.space, stone_hp, "beams", self.screen_height, self.screen_width)

        self.beams.extend([beam1, beam2])

        # Triangles
        triangle1 = Polygon((575, 250), 20, 20, self.space, wood_hp, "triangles", self.screen_height, self.screen_width,
                                triangle_points=[(565, 260), (575, 240), (585, 260)])
        triangle2 = Polygon((725, 250), 20, 20, self.space, wood_hp, "triangles", self.screen_height, self.screen_width,
                                triangle_points=[(715, 260), (725, 240), (735, 260)])
        self.triangles.extend([triangle1, triangle2])

        self.number_of_birds = 4
        if self.bool_space:
            self.number_of_birds = 8
    
    def load_level(self):
        """Loads the level based on the current level number."""
        
        
        
        
        try:
            build_name = "build_" + str(self.number)
            if hasattr(self, build_name):
                getattr(self, build_name)()
            else:
                print(f"Warning: Level-Build-Methode '{build_name}' nicht gefunden. Lade Standard-Level.")
                self.number = 1
                self.build_1()  # Call build_1 to load a default level.  Important!
        except AttributeError as e:
            print(f"Fehler beim Laden des Levels: {e}")
            self.number = 1
            self.load_level() # Recursive call to try loading level 1 if there is an error
