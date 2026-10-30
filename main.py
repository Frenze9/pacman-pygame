import pygame
pygame.init()
from random import randint, choice
import os

def path(file):
    return os.path.join(os.path.dirname(__file__), file)

# base class
class Sprite:
    def __init__(self, x, y, img, w=24, h=24):
        self.img = pygame.image.load(path(img))
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, surface):
        surface.blit(self.img, (self.rect.x, self.rect.y))

class Enemy(Sprite):
    def __init__(self, x, y, img):
        super().__init__(x, y, img)
        self.dx, self.dy = 2, 0  
        self.dr = [-2,2]
    def move(self, maze):

        self.rect.x += self.dx
        self.rect.y += self.dy
        for wall in maze.walls:
            if self.rect.colliderect(wall):
                self.dx *= -1
                self.dy *= -1
                self.rect.x += self.dx
                self.rect.y += self.dy
        if randint(1, 30) == 1:
            self.change_dir()

    def change_dir(self):
        if self.dx != 0:
            self.dx = 0
            self.dy = choice(self.dr)
        else:
            self.dx = choice(self.dr)
            self.dy = 0

class Player(Sprite):
    def __init__(self, x, y):
        super().__init__(x, y, 'pR_open.png')
        self.anim = 'pR_open.png'
        self.dx, self.dy = 0, 0
        self.count_anim = 0
        self.dots = 0
        self.hp = 5

    def animate(self):
        self.count_anim += 1
        if self.count_anim >= 5:
            self.count_anim = 0
            if self.dx  > 0:
                if self.anim == 'pR_open.png':
                    self.anim = 'pR_close.png'
                else:
                    self.anim = 'pR_open.png'
            elif self.dx < 0:
                if self.anim == 'pL_open.png':
                    self.anim = 'pL_close.png'
                else:
                    self.anim = 'pL_open.png'

            elif self.dy > 0:
                if self.anim == 'pD_open.png':
                    self.anim = 'pD_close.png'
                else:
                    self.anim = 'pD_open.png'
            elif self.dy < 0:
                if self.anim == 'pU_open.png':
                    self.anim = 'pU_close.png'
                else:
                    self.anim = 'pU_open.png'
            self.img = pygame.image.load(path(f'{self.anim}'))

    def update(self, maze):
        self.animate()
        self.move()
        obj = self.collide_maze(maze.dots)
        if obj:
            maze.dots.remove(obj)
            self.dots -= 1

        if self.collide_maze(maze.walls):
            self.rect.x -= self.dx
            self.rect.y -= self.dy

        if self.collide_maze(enemies):
            self.rect.x, self.rect.y = 40, 430
            self.hp -= 1

    def collide_maze(self, list_obj):
        for obj in list_obj:
            if self.rect.colliderect(obj):
                return obj
        return False

    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.dx = -2
            self.dy = 0
        elif key[pygame.K_RIGHT]:
            self.dx = 2
            self.dy = 0
        elif key[pygame.K_UP]:
            self.dx = 0
            self.dy = -2
        elif key[pygame.K_DOWN]:
            self.dx = 0
            self.dy = 2
        else:
            self.dx, self.dy = 0, 0

        self.rect.x += self.dx
        self.rect.y += self.dy
                   
class Maze:
    def __init__(self):
        
        '''Лабіринт із стінами'''
        self.walls = []
        self.dots = []
        self.w = pygame.image.load(path('wall.png'))
        self.d = pygame.image.load(path('dot.png'))
        self.create_wall()

    def create_wall(self):
        x, y = 10,10
        count = 0
        for line in maze_map:
            for num in line:
                if num == "1":
                    self.walls.append(pygame.Rect(x, y, 32, 32))
                elif num == "0":
                    self.dots.append(pygame.Rect(x+6, y+6, 18, 18))
                elif num == "2":
                    enemies.append(Enemy(x, y,  f'g{count+1}.png'))
                    count += 1
                x += 32
            y += 32
            x = 10

    def draw(self, surface):
        for wall in self.walls:
            surface.blit(self.w, (wall.x, wall.y))
        for dot in self.dots:
            surface.blit(self.d, (dot.x, dot.y))

class Label:
    def __init__(self, x, y,img , text, font_size=30, color=(255,255,255)):
        self.font = pygame.font.SysFont('Arial', font_size)
        self.font.bold = True
        self.img = pygame.image.load(path(img))
        self.text = text
        self.color = color
        self.x = x
        self.y = y

    def update(self, text):
        self.text = text

    def draw(self, surface):
        img = self.font.render(self.text, True, self.color)
        surface.blit(img, (self.x, self.y))
        surface.blit(self.img, (self.x - 20, self.y+4))
# labyrinth map
maze_map = [
        "111111111111111",
        "100000001000001",
        "101101101011011",
        "100000000000001",
        "110010111010111",
        "100010010010001",
        "110011000110111",
        "100000020000001",
        "110001121100111",
        "100101222100001",
        "110001111100111",
        "100100000001001",
        "101101111101101",
        "130000010000001",
        "111111111111111"]

# initialize game
screen = pygame.display.set_mode((500, 500))
FON = (17, 12, 92)
clock = pygame.time.Clock()
running = True

enemies = []
maze = Maze()

pacman = Player(40, 430)    
pacman.dots = len(maze.dots)
hp = Label(40, 10, 'hp.png', f'HP: {pacman.hp}', 20)
dots = Label(440, 10, 'dot.png', f'Dots: {pacman.dots}', 20)
end = pygame.image.load(path('end.png'))
font = pygame.font.SysFont('Arial', 45)
font.bold = True
end_game = False

btn_start = Sprite(200, 200, 'btn_start.png', 128, 128)
text_start = font.render('PACMAN', True, (255, 245, 48))
start_game = False
#main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not start_game:
            if btn_start.rect.collidepoint(event.pos):
                start_game = True

    if not start_game:
        screen.fill(FON)
        btn_start.draw(screen)
        screen.blit(text_start, (170, 150))
    else:

        if end_game:
            screen.blit(end, (0, 0))
            screen.blit(text, (110, 430))
        else:
            screen.fill(FON)
            maze.draw(screen)
            hp.draw(screen)
            dots.draw(screen)
            hp.update(f': {pacman.hp}')
            dots.update(f': {pacman.dots}')
            pacman.update(maze)
            pacman.draw(screen)
            for enemy in enemies:
                enemy.move(maze)
                enemy.draw(screen)

            if pacman.hp <= 0:
                end_game = True
                text = font.render('GAME OVER', True, (255,0,0))

            if pacman.dots == 0:
                end_game = True
                text = font.render('YOU WIN!', True, (0,255,0))    

    pygame.display.flip()
    clock.tick(40)

pygame.quit()
