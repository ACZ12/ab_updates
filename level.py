# level.py

from character import Pig
from Polygon import Polygon

wood_hp = 20
stone_hp = 30
ice_hp = 10

class Level():
    
    def __init__(self,pigs,columns,beams,circles,triangles,space):

        self.pigs = pigs
        self.columns = columns
        self.beams = beams
        self.circles = circles
        self.triangles = triangles
        self.space = space
        self.number = 1
        #self.number_of_birds = 4
        self.bool_space = False
        self.locked = ["","","build_2","build_3","build_4","build_5","","",""]
        
        # lower limit
        self.one_star = 20000
        self.two_star = 32500
        self.three_star = 45000
        
        self.bool_space = False


    def clear_level(self):
        """Clears all pigs, columns, and beams from the lists."""
        self.pigs.clear()
        self.columns.clear()
        self.beams.clear()
        self.circles.clear()
        self.triangles.clear()
        self.number_of_birds = 4  # Reset the number of birds



    def build_1(self):
        # level 0
        self.number = 1
        self.level_birds = ["sahur","liri","sahur","sahur"]
        self.number_of_birds = 5
        locked = False
        pig1 = Pig(400,130,self.space,10,"n11")
        pig2 = Pig(450,130,self.space,60,"n21")
        pig3 = Pig(500,130,self.space,10,"n31")
        pig4 = Pig(550,130,self.space,60,"n41")
        pig5 = Pig(600,130,self.space,10,"n51")

        self.pigs.append(pig1)
        self.pigs.append(pig2)
        self.pigs.append(pig3)
        self.pigs.append(pig4)
        self.pigs.append(pig5)
        
        self.number_of_birds = 4

        # create beam and column

        p = (950,150)
        self.columns.append(Polygon(p,20,85,self.space, wood_hp, "columns"))
        
        p = (900,150)
        self.columns.append(Polygon(p,20,85,self.space, ice_hp, "columns"))
        
        p = (950,260)
        self.columns.append(Polygon(p,20,85,self.space, wood_hp , "columns"))
        
        p = (900,220)
        self.beams.append(Polygon(p,85,20,self.space,wood_hp , "beams"))
        p = (800,220)
        self.beams.append(Polygon(p,85,20,self.space,ice_hp , "beams"))
        p = (700,220)
        self.beams.append(Polygon(p,85,20,self.space,stone_hp , "beams"))


       

        p = (700,510)
        self.circles.append(Polygon(p,20,20,self.space, wood_hp , "circles"))
        p = (600,510)
        self.circles.append(Polygon(p,20,20,self.space, stone_hp , "circles"))
        p = (550,510)
        self.circles.append(Polygon(p,20,20,self.space, ice_hp , "circles"))
        
        p = (700,310)
        self.triangles.append(Polygon(p,20,20,self.space, stone_hp , "triangles", triangle_points=[(p[0]-10,p[1]+10),(p[0],p[1]-10),(p[0]+10,p[1]+10)]))
        p = (500,310)
        self.triangles.append(Polygon(p,20,20,self.space, ice_hp , "triangles", triangle_points=[(p[0]-10,p[1]+10),(p[0],p[1]-10),(p[0]+10,p[1]+10)]))
        p = (650,310)
        self.triangles.append(Polygon(p,20,20,self.space, wood_hp , "triangles", triangle_points=[(p[0]-10,p[1]+10),(p[0],p[1]-10),(p[0]+10,p[1]+10)]))

        if self.bool_space:
            self.number_of_birds = 8
            
        


    def build_2(self):
        # level 1
        self.number = 2
        locked = True
        pig1 = Pig(800,230,self.space,13)
        #pig2 = Pig(985,130,self.space)
        
        self.pigs.append(pig1)
        #self.pigs.append(pig2)

        # create beam and column

        p = (900,150)
        self.columns.append(Polygon(p,20,85,self.space,wood_hp, "columns"))
        
        p = (1010,150)
        self.columns.append(Polygon(p,20,85,self.space,wood_hp , "columns"))
        
        p = (950,260)
        self.columns.append(Polygon(p,20,85,self.space,wood_hp , "columns"))
        
        p = (1010,260)
        self.columns.append(Polygon(p,20,85,self.space,wood_hp , "columns"))


        p = (980,220)
        self.beams.append(Polygon(p,85,20,self.space,wood_hp , "beams"))
        
        p = (980,310)
        self.beams.append(Polygon(p,85,20,self.space,wood_hp , "beams"))

        self.number_of_birds = 4
        if self.bool_space:
            self.number_of_birds = 8
    
    
    def build_3(self):
        # level 2
        self.number = 3
        locked = True
        pig1 = Pig(980,230,self.space,13)
        pig2 = Pig(985,130,self.space,31)

        self.pigs.append(pig1)
        self.pigs.append(pig2)

        # create beam and column

        p = (950,150)
        self.columns.append(Polygon(p,20,85,self.space,wood_hp , "columns"))
        
        p = (1010,150)
        self.columns.append(Polygon(p,20,85,self.space,wood_hp , "columns"))
        
        p = (900,260)
        self.columns.append(Polygon(p,20,85,self.space,wood_hp , "columns"))
        
        p = (1010,260)
        self.columns.append(Polygon(p,20,85,self.space,wood_hp , "columns"))


        p = (980,220)
        self.beams.append(Polygon(p,85,20,self.space,wood_hp , "beams"))
        
        p = (980,310)
        self.beams.append(Polygon(p,85,20,self.space,wood_hp , "beams"))

        self.number_of_birds = 4
        if self.bool_space:
            self.number_of_birds = 8
    
    
    
    def build_4(self):
        # level 3
        self.number = 4
        locked = True
        pig1 = Pig(980,230,self.space,31)
        pig2 = Pig(985,130,self.space,13)

        self.pigs.append(pig1)
        self.pigs.append(pig2)

        # create beam and column

        p = (950,150)
        self.columns.append(Polygon(p,20,85,self.space,wood_hp , "columns"))
        
        p = (1010,150)
        self.columns.append(Polygon(p,20,85,self.space,wood_hp , "columns"))
        
        p = (950,260)
        self.columns.append(Polygon(p,20,85,self.space,wood_hp , "columns"))
        
        p = (1010,260)
        self.columns.append(Polygon(p,20,85,self.space,wood_hp , "columns"))


        p = (900,220)
        self.beams.append(Polygon(p,85,20,self.space,wood_hp , "beams"))
        
        p = (980,310)
        self.beams.append(Polygon(p,85,20,self.space,wood_hp , "beams"))

        self.number_of_birds = 4
        if self.bool_space:
            self.number_of_birds = 8
    
    
    
    def build_5(self):
        # level 4
        self.number = 5
        locked = True
        pig1 = Pig(980,230,self.space,13)
        pig2 = Pig(985,130,self.space,31)

        self.pigs.append(pig1)
        self.pigs.append(pig2)

        # create beam and column

        p = (950,150)
        self.columns.append(Polygon(p,20,85,self.space,wood_hp , "columns"))
        
        p = (1010,150)
        self.columns.append(Polygon(p,20,85,self.space,wood_hp , "columns"))
        
        p = (950,260)
        self.columns.append(Polygon(p,20,85,self.space,wood_hp , "columns"))
        
        p = (1010,260)
        self.columns.append(Polygon(p,20,85,self.space,wood_hp , "columns"))


        p = (980,250)
        self.beams.append(Polygon(p,85,20,self.space,wood_hp , "beams"))
        
        p = (980,310)
        self.beams.append(Polygon(p,85,20,self.space,wood_hp , "beams"))

        self.number_of_birds = 4
        if self.bool_space:
            self.number_of_birds = 8
    
    
    
    def build_6(self):
        # level 5
        self.number = 6
        locked = True
        pig1 = Pig(980,230,self.space,13)
        pig1.life = 40
        pig2 = Pig(985,130,self.space,31)

        self.pigs.append(pig1)
        self.pigs.append(pig2)
        

        # create beam and column

        p = (950,150)
        self.columns.append(Polygon(p,20,85,self.space,wood_hp , "columns"))
        
        p = (1010,150)
        self.columns.append(Polygon(p,20,85,self.space,wood_hp , "columns"))
        
        p = (950,260)
        self.columns.append(Polygon(p,20,85,self.space,wood_hp , "columns"))
        
        p = (810,260)
        self.columns.append(Polygon(p,20,85,self.space,wood_hp , "columns"))


        p = (980,220)
        self.beams.append(Polygon(p,85,20,self.space,wood_hp , "beams"))
        
        p = (980,310)
        self.beams.append(Polygon(p,85,20,self.space,wood_hp , "beams"))

        self.number_of_birds = 4
        if self.bool_space:
            self.number_of_birds = 8
    
    
    


    def load_level(self):
        try:
            build_name = "build_"+str(self.number)
            if hasattr(self, build_name):
                getattr(self, build_name)()
            else:
                print(f"Warnung: Level-Build-Methode '{build_name}' nicht gefunden. Lade Standard-Level.")
                self.number = 1
                self.build() # Rufe die 'build()' Methode direkt auf
        except AttributeError as e:
            print(f"Fehler beim Laden des Levels: {e}")
            self.number = 1
            self.load_level() # Stelle sicher, dass ein Level geladen wird