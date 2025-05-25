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
        self.pigs.clear()
        self.columns.clear()
        self.beams.clear()
        self.circles.clear()
        self.triangles.clear()
        
    

    def build_0(self):
        self.number = 1
        self.level_birds = ["sahur","liri","trala","palocleves","bomb","patapim","glorbo"]
        self.number_of_birds = 7
        locked = False
        min_y = 150  
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
        self.number = 1
        self.level_birds = ["sahur","sahur","liri","trala","palocleves","bomb","patapim","glorbo"]
        self.number_of_birds = 8
        locked = False
        
        # --- Structure 1: Simple Tower ---
        base_x1 = 700
        # Ground floor
        self.columns.append(Polygon(self.scale_pos(base_x1 - 30, 150), 20, 85, self.space, wood_hp, "columns", self.screen_height, self.screen_width))
        self.columns.append(Polygon(self.scale_pos(base_x1 + 30, 150), 20, 85, self.space, wood_hp, "columns", self.screen_height, self.screen_width))
        self.beams.append(Polygon(self.scale_pos(base_x1, 198), 85, 20, self.space, wood_hp, "beams", self.screen_height, self.screen_width))
        self.pigs.append(Pig(self.scale_pos(base_x1, 220)[0], self.scale_pos(base_x1, 220)[1], self.space, 12,"n11"))

        # Second floor
        self.columns.append(Polygon(self.scale_pos(base_x1 - 25, 250), 20, 85, self.space, ice_hp, "columns", self.screen_height, self.screen_width))
        self.columns.append(Polygon(self.scale_pos(base_x1 + 25, 250), 20, 85, self.space, ice_hp, "columns", self.screen_height, self.screen_width))
        self.beams.append(Polygon(self.scale_pos(base_x1, 298), 70, 20, self.space, ice_hp, "beams", self.screen_height, self.screen_width))
        self.pigs.append(Pig(self.scale_pos(base_x1, 320)[0], self.scale_pos(base_x1, 320)[1], self.space, 10,"n21"))

        # --- Structure 2: Wider Platform with a Topper ---
        base_x2 = 950
        # Lower platform
        self.columns.append(Polygon(self.scale_pos(base_x2 - 50, 150), 20, 85, self.space, stone_hp, "columns", self.screen_height, self.screen_width))
        self.columns.append(Polygon(self.scale_pos(base_x2, 150), 20, 85, self.space, stone_hp, "columns", self.screen_height, self.screen_width))
        self.columns.append(Polygon(self.scale_pos(base_x2 + 50, 150), 20, 85, self.space, stone_hp, "columns", self.screen_height, self.screen_width))
        self.beams.append(Polygon(self.scale_pos(base_x2 - 25, 198), 85, 20, self.space, stone_hp, "beams", self.screen_height, self.screen_width))
        self.beams.append(Polygon(self.scale_pos(base_x2 + 25, 198), 85, 20, self.space, stone_hp, "beams", self.screen_height, self.screen_width))
        self.pigs.append(Pig(self.scale_pos(base_x2 - 25, 220)[0], self.scale_pos(base_x2 - 25, 220)[1], self.space, 10,"n31"))
        self.pigs.append(Pig(self.scale_pos(base_x2 + 25, 220)[0], self.scale_pos(base_x2 + 25, 220)[1], self.space, 10,"n41"))

        # Topper
        self.columns.append(Polygon(self.scale_pos(base_x2, 250), 20, 85, self.space, wood_hp, "columns", self.screen_height, self.screen_width))
        self.beams.append(Polygon(self.scale_pos(base_x2, 298), 70, 20, self.space, wood_hp, "beams", self.screen_height, self.screen_width))
        self.pigs.append(Pig(self.scale_pos(base_x2, 330)[0], self.scale_pos(base_x2, 330)[1], self.space, 15,"n51"))

        # --- Some floating/precarious elements ---
        self.circles.append(Polygon(self.scale_pos(base_x1 + 100, 350), 20, 20, self.space, ice_hp, "circles", self.screen_height, self.screen_width, radius=20))
        self.triangles.append(Polygon(self.scale_pos(base_x2 - 100, 300), 30, 30, self.space, wood_hp, "triangles", self.screen_height, self.screen_width))

        if self.bool_space:
            self.number_of_birds = 8
            
        


    def build_2(self):
        self.number = 2
        self.level_birds = ["sahur","liri","sahur","palocleves","palocleves"]
        self.number_of_birds = 5 
        locked = True

        # --- Tall Stone Tower with Wooden Top ---
        base_x = 850
        current_y = 150

        # Layer 1 (Stone Base)
        self.columns.append(Polygon(self.scale_pos(base_x - 40, current_y), 20, 85, self.space, stone_hp, "columns", self.screen_height, self.screen_width))
        self.columns.append(Polygon(self.scale_pos(base_x + 40, current_y), 20, 85, self.space, stone_hp, "columns", self.screen_height, self.screen_width))
        self.beams.append(Polygon(self.scale_pos(base_x, current_y + 48), 100, 20, self.space, stone_hp, "beams", self.screen_height, self.screen_width))
        self.pigs.append(Pig(self.scale_pos(base_x, current_y + 70)[0], self.scale_pos(base_x, current_y + 70)[1], self.space, 13, "n11"))
        current_y += 100

        # Layer 2 (Ice Middle)
        self.columns.append(Polygon(self.scale_pos(base_x - 30, current_y), 20, 85, self.space, ice_hp, "columns", self.screen_height, self.screen_width))
        self.columns.append(Polygon(self.scale_pos(base_x + 30, current_y), 20, 85, self.space, ice_hp, "columns", self.screen_height, self.screen_width))
        self.beams.append(Polygon(self.scale_pos(base_x, current_y + 48), 80, 20, self.space, ice_hp, "beams", self.screen_height, self.screen_width))
        self.pigs.append(Pig(self.scale_pos(base_x, current_y + 70)[0], self.scale_pos(base_x, current_y + 70)[1], self.space, 10, "n21"))
        current_y += 100

        # Layer 3 (Wood Top)
        self.columns.append(Polygon(self.scale_pos(base_x - 20, current_y), 20, 85, self.space, wood_hp, "columns", self.screen_height, self.screen_width))
        self.columns.append(Polygon(self.scale_pos(base_x + 20, current_y), 20, 85, self.space, wood_hp, "columns", self.screen_height, self.screen_width))
        self.beams.append(Polygon(self.scale_pos(base_x, current_y + 48), 60, 20, self.space, wood_hp, "beams", self.screen_height, self.screen_width))
        self.pigs.append(Pig(self.scale_pos(base_x, current_y + 70)[0], self.scale_pos(base_x, current_y + 70)[1], self.space, 15, "n31"))

        # --- Small side structure with triangles ---
        side_x = 600
        self.columns.append(Polygon(self.scale_pos(side_x, 150), 20, 85, self.space, wood_hp, "columns", self.screen_height, self.screen_width))
        # Triangle points for a small roof
        triangle_points = [(-25, 0), (25, 0), (0, 25)] # Scaled by Polygon class
        self.triangles.append(Polygon(self.scale_pos(side_x, 205), 50, 25, self.space, wood_hp, "triangles", self.screen_height, self.screen_width, triangle_points=triangle_points))
        self.pigs.append(Pig(self.scale_pos(side_x, 160)[0], self.scale_pos(side_x, 160)[1], self.space, 10, "n41"))

        # self.number_of_birds = 4 # This was already 5 above, keeping it at 5
        if self.bool_space:
            self.number_of_birds = 8
    
    
    def build_3(self):
        self.number = 3
        self.level_birds = ["sahur","liri","sahur","palocleves","palocleves"] 
        self.number_of_birds = 5
        locked = True
        pig1 = Pig(980,230,self.space,13, "n11")
        pig2 = Pig(985,130,self.space,31, "n21") #

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
        self.number = 4
        self.level_birds = ["sahur","liri","sahur","palocleves","palocleves"]
        self.number_of_birds = 5 
        locked = True
        pig1 = Pig(980,230,self.space,31, "n11")
        pig2 = Pig(985,130,self.space,13, "n21") 

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
        self.number = 5
        self.level_birds = ["sahur","liri","sahur","palocleves","palocleves"] 
        self.number_of_birds = 5
        locked = True
        pig1 = Pig(980,230,self.space,13, "n11") 
        pig2 = Pig(985,130,self.space,31, "n21")

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
        self.number = 6
        self.level_birds = ["sahur","liri","sahur","palocleves","palocleves"] 
        self.number_of_birds = 5
        locked = True
        pig1 = Pig(980,230,self.space,13, "n11") 
        pig1.life = 40
        pig2 = Pig(985,130,self.space,31, "n21") 

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
        self.number = 7
        self.level_birds = ["sahur","liri","sahur","palocleves","palocleves"] 
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
        self.number = 8
        self.level_birds = ["sahur", "liri", "sahur", "palocleves", "palocleves"]  
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
        try:
            build_name = "build_" + str(self.number)
            if hasattr(self, build_name):
                getattr(self, build_name)()
            else:
                print(f"Warning: Level-Build-Methode '{build_name}' nicht gefunden. Lade Standard-Level.")
                self.number = 1
                self.build_1() 
        except AttributeError as e:
            print(f"Fehler beim Laden des Levels: {e}")
            self.number = 1
            self.load_level() 
