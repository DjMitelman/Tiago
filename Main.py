from pygame import Rect, init, QUIT, quit, K_ESCAPE, KEYDOWN, K_p
from pygame.display import set_caption, set_mode, flip
from pygame.transform import scale
from pygame.image import load
from pygame.time import Clock
from pygame.event import get

from random import randint, random
from sys import exit as leave
from time import sleep
from os.path import join


TITLE = "IM LOOKIN FOR SOME GRUB"
TILES_HORIZONTAL = 10
TILES_VERTICAL = 10
TILESIZE = 80
WINDOW_WIDTH = TILESIZE * TILES_HORIZONTAL
WINDOW_HEIGHT = TILESIZE * TILES_VERTICAL
LIGHTGREY = (200, 200, 200)
MYINCR = .05
GRASS = "grass.png"
TIGER = "tiger.png"
RABBIT = "rabbit.png"
ENEMY = "gorilla.jpg"


def in_range(value1, value2):
    diff = abs(value1 - value2)
    if diff <= MYINCR:
        return True
    return False

     
class Entities:
    def __init__(self, surface):
        self.surface = surface
        self.inner = []
        self.current_entity = None
        self.listX = []
        self.listY = []
        self.winX = []
        self.winY = []
        self.numOfRabbits = 0
        self.id = 1
        new_entity = Tiger(0, 0, 0)
        self.inner.append(new_entity)
        self.spawnRabbit()

    def getNumRabbits(self): return self.numOfRabbits

    def numRabbitsZero(self): self.numOfRabbits = 0    

    def setWinX(self, element):
        self.winX.remove(element)
        
    def setWinY(self, element):
        self.winY.remove(element)
        
    def getEntityByCoords(self, x, y):
        for elem in self.inner:
            if elem.x == x and elem.y == y and type(elem) != Tiger:
                return elem
        return None
    
    def getEntityByType(self, _type):
        for elem in self.inner:
            if type(elem) == _type:
                return elem

    def format_xy(self):
        for elem in self.inner:
            elem.x = round(elem.x)
            elem.y = round(elem.y)

    def has_collided(self, mouse_pos):
        for elem in self.inner:
            myrect = Rect(elem.x * TILESIZE, elem.y * TILESIZE, \
                                                  TILESIZE, TILESIZE)
            if myrect.collidepoint(mouse_pos[0], mouse_pos[1]) == 1:
                return elem.x, elem.y
        return None, None

    def draw(self, surface):
        if len(self.inner) == 0:
            raise ValueError("No tiles to display.")
        for elem in self.inner:
            if not elem.isEaten():
                myrect = Rect(elem.x * TILESIZE, elem.y * TILESIZE, TILESIZE, TILESIZE)
                self.surface.blit(elem.image, myrect)

    def debug_print(self):
        for elem in self.inner:
            elem.debug_print()
        print(self.winX, self.winY, "Num of Rabbits = ", self.numOfRabbits)
        
    def spawnRabbit(self):
        rx, ry = randint(4, 6), randint(4, 6)
        new_entity = Rabbit(self.id, rx, ry)
        self.inner.append(new_entity)
        self.id += 1
        
        self.winX.append(rx), self.winY.append(ry)
        self.numOfRabbits = 1

class Rabbit(Entities):
    def __init__(self, id, x, y):
        self.id = id
        self.x, self.y = int(x), int(y)
        self.entity_image = RABBIT
        self.eaten = False
        image_path = join("data", "images")
        self.image = load(join(image_path, self.entity_image)).convert_alpha()
        self.image = scale(self.image, (TILESIZE, TILESIZE))
    
    def move(self, x, y):
        if x < 10 and x > -1:
            if not in_range(self.x, x):
                if self.x < x:
                    self.x += 3
                elif self.x > x:
                    self.x -= 3
                else:
                    self.x = x
        if y < 10 and y > -1:
            if not in_range(self.y, y):
                if self.y < y:
                    self.y += 3
                elif self.y > y:
                    self.y -= 3
                else:
                    self.y = y
        print(self.x, self.y, " - Rabbits coord after moving")
                    
    def Eaten(self): 
        self.eaten = True
        super().numRabbitsZero()
    
    def isEaten(self): return self.eaten
    
    def debug_print(self):
        print("type: {}, id: {}, x: {}, y: {}" \
                                  .format("Rabbit", self.id, self.x, self.y))
        
    def getX(self): return self.x
    
    def getY(self): return self.y
    
class Tiger:
    def __init__(self, id, x, y):
        self.id = id
        self.x, self.y = int(x), int(y)
        self.entity_image = TIGER
        self.wellFed = False
        image_path = join("data", "images")
        self.image = load(join(image_path, self.entity_image)).convert_alpha()
        self.image = scale(self.image, (TILESIZE, TILESIZE))
        self.master = .0

    def move(self, x, y, f = 0):
        if f: 
            self.x = x
            self.y = y
            return
        if x < 10 and x > -1:
            if not in_range(self.x, x):
                if self.x < x:
                    self.x += 1
                elif self.x > x:
                    self.x -= 1
                else:
                    self.x = x
        if y < 10 and y > -1:
            if not in_range(self.y, y):
                if self.y < y:
                    self.y += 1
                elif self.y > y:
                    self.y -= 1
                else:
                    self.y = y
    def isEaten(self): return False
    
    def tryingCatch(self):
        tigerOdds, rabbitOdds = random() + self.master, random()
        print("tigerOdds = {}, rabbitodds = {}".format(tigerOdds, rabbitOdds))
        if tigerOdds > rabbitOdds: return True
        else : 
            self.master += .10
            return False
    
    def getX(self): return self.x
    
    def getY(self): return self.y
    
    def isFed(self): return self.wellFed
    
    def oneMoreEaten(self): self.wellFed = True
    
    def debug_print(self):
        print("type: {}, id: {}, x: {}, y: {}" \
                                     .format("Tiger", self.id, self.x, self.y))


class Tile:
    def __init__(self, id, x, y, kind_of_tile):
        filename = ""
        self.id = id
        self.x = int(x)
        self.y = int(y)
        self.kind_of_tile = kind_of_tile
        if kind_of_tile == "0": filename = GRASS
        else: raise ValueError("Error! kind of tile: ", kind_of_tile)
        self.rect = Rect(self.x * TILESIZE, self.y * TILESIZE, TILESIZE, TILESIZE)
        image_path = join("data", "images")
        self.image = load(join(image_path, filename)).convert_alpha()
        self.image = scale(self.image, (TILESIZE, TILESIZE))

    def debug_print(self):
        print("id: {}, x: {}, y: {}, kind: {}".format(self.id, self.x, self.y, self.kind_of_tile))

class Tiles:
    def __init__(self, screen):
        self.screen = screen
        self.inner = []
        self.current_tile = None
        self._load_data()

    def _load_data(self):
        self.inner = []
        filepath = join("data", "grid.txt")
        with open(filepath, "r") as f:
            mylines = f.readlines()
            mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
        id = 0
        for count_i, myline in enumerate(mylines):
            temp_list = myline.split(" ")
            temp_list = [i.strip() for i in temp_list if len(i.strip()) > 0]
            for count_j, elem in enumerate(temp_list):
                new_tile = Tile(id, count_j, count_i, elem)
                self.inner.append(new_tile)
                id += 1

    def getTileByCoords(self, x, y):
        for elem in self.inner:
            if elem.x == x:
                if elem.y == y:
                    return elem
        return None

    def has_collided(self, mouse_pos):
        for elem in self.inner:
            if elem.rect.collidepoint(mouse_pos) == 1:
                return elem.x, elem.y
        return None, None

    def draw(self, surface):
        if len(self.inner) == 0:
            raise ValueError("No tiles to display")
        for elem in self.inner:
            self.screen.blit(elem.image, elem.rect)

    def debug_print(self):
        for elem in self.inner:
            elem.debug_print()


class Game:
    def __init__(self):
        init()
        self.clock = Clock()
        set_caption(TITLE)
        self.surface = set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.BG_COLOR = LIGHTGREY
        self.keep_looping = True
        self.tiles = Tiles(self.surface)
        self.entities = Entities(self.surface)
        self.entities.debug_print()
        self.main()


    def events(self):
        for event in get():
            if event.type == QUIT:
                self.keep_looping = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.keep_looping = False
                if event.key == K_p:
                    print("\n\tPAUSE BREAK\n")
                    sleep(5)

    def updatee(self, tiger, rabbit):
        dx, dy = randint(-1, 1), randint(-1, 1)
        tiger.move(tiger.getX() + dx, tiger.getY() + dy)
        tigerX = round(tiger.getX())
        tigerY = round(tiger.getY())
        rabbitX = round(rabbit.getX())
        rabbitY = round(rabbit.getY())
        if tiger.isFed(): 
            print("Time for a siesta -- gonna base")
            tiger.move(0, 0, 1)
            return True
        if not tiger.isFed() and abs(tigerX-rabbitX) < 3 and abs(tigerY - rabbitY) < 3:
            print("Hang on! Imma commin for u...")
            if tiger.tryingCatch():
                tiger.move(rabbitX, rabbitY)
                self.entities.getEntityByType(Rabbit).Eaten()
                tiger.oneMoreEaten()
                print("Tiger full - {}".format(tiger.isFed()))
            else:
                if random() < 0.5:
                    rabbit.move(rabbitX + 3, rabbitY)
                else: rabbit.move(rabbitX, rabbitY + 3)
                return False


    def draw(self):
        self.surface.fill(self.BG_COLOR)
        self.tiles.draw(self.surface)
        self.entities.draw(self.surface)
        flip()

    
    
    def main(self):
        while self.keep_looping:
            tiger = self.entities.getEntityByType(Tiger)
            rabbit = self.entities.getEntityByType(Rabbit)
            self.events()
            if self.updatee(tiger, rabbit):
                self.draw()
                print("You won\n\n")
                self.__init__()
            else: 
                self.draw()
            self.clock.tick_busy_loop(10)
            
        quit()
        leave()
        



if __name__ == "__main__":
    mygame = Game()