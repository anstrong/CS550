import pygame
import random

pipes = ["Pipes_1", "Pipes_2"]

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file):
        pygame.sprite.Sprite.__init__(self)  
        self.image = pygame.image.load(image_file)

    def print(self):
        screen.blit(self.image, (0, 0))

class Avatar(pygame.sprite.Sprite):
    def __init__(self, image_file):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load(image_file)

        self.image =  pygame.transform.scale(image, (35, 35))

        self.x = 50
        self.y = 0

        self.speed_fall = 0
        self.speed_flap = 0

    def print(self):
        screen.blit(self.image, (self.x, self.y))

    def flap(self):
        initial_y = int(self.y)
        flap_height = 10
        target = initial_y - flap_height

        if self.y > target:
            for i in range(-1*(int(self.y) - target), 1):
                self.speed_flap = i/3
                self.y += self.speed_flap

        self.speed_fall = -3

    def fall(self):
        if self.speed_fall > 10:
            self.speed_fall = 10

        if self.y < 320:
            self.y += self.speed_fall

        self.speed_fall += (1/4)

    def crash(self):
        if self.speed_fall > 10:
            self.speed_fall = 10

        if self.y > 0:
            self.y -= self.speed_fall

        self.speed_fall -= (1/4)

class Pipe(object):
    def __init__(self, orientation, height, x):
        pygame.sprite.Sprite.__init__(self)

        self.height = int(height)
        self.orientation = orientation

        self.x = x

        self.pipe_image = pygame.image.load('pipe_shaft.png')
        self.lip_image = pygame.image.load('pipe_head.png')

        self.pipe = pygame.transform.scale(self.pipe_image, (50, self.height))
        self.lip =  pygame.transform.scale(self.lip_image, (50, 30))

        if self.orientation == 1:
            self.pipe_y = (315 - self.height) + 37
            self.lip_y = (315 - self.height) + 37
            
        elif self.orientation == -1:
            self.pipe_y = 0   
            self.lip_y = self.height 

    def print(self, x):
        self.x = x

        screen.blit(self.pipe, (self.x, self.pipe_y))
        screen.blit(self.lip, (self.x, self.lip_y))

class Pipe_Pair(pygame.sprite.Sprite):
    def __init__(self, gap_height, x):
        pygame.sprite.Sprite.__init__(self)
        self.gap_height = gap_height
        self.gap_size = 75

        self.x = x

        self.Bottom_Pipe = Pipe(1, self.gap_height, self.x)
        self.Top_Pipe = Pipe(-1, 315 - (self.gap_size + self.gap_height), self.x)

    def print(self, x):
        self.Bottom_Pipe.print(x)
        self.Top_Pipe.print(x)

    def pan(self):
        if self.x < -100:
            self.x = 650
            self.y = random.randint(100, 315)
        else:
            self.x -= 2


for i in range(0, 5):
    height = random.uniform(30, 200)
    init_position = 550 + (i*150)
    name = "Pipes_%s %i"

    pipes.append(.x)

def print_pipes():


'''
class Obstacles(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.x1 = 550
        self.x2 = 700
        self.x3 = 850
        self.x4 = 1000
        self.x5 = 1150

        self.h1 = random.uniform(30, 200)
        self.h2 = random.uniform(30, 200)
        self.h3 = random.uniform(30, 200)
        self.h4 = random.uniform(30, 200)
        self.h5 = random.uniform(30, 200)

        self.Pipes_1 = Pipe_Pair(self.h1, self.x1)
        self.Pipes_2 = Pipe_Pair(self.h2, self.x2)
        self.Pipes_3 = Pipe_Pair(self.h3, self.x3)
        self.Pipes_4 = Pipe_Pair(self.h4, self.x4)
        self.Pipes_5 = Pipe_Pair(self.h5, self.x5)

    def print(self):
        self.Pipes_1.print(self.x1)
        self.Pipes_2.print(self.x2)
        self.Pipes_3.print(self.x3)
        self.Pipes_4.print(self.x4)
        self.Pipes_5.print(self.x5)

    def pan(self):
        for i in range(1, 6):
            x_num = 'x'+str(i)
            h_num = 'h'+str(i)

            pipe = getattr(self, x_num)

            setattr(self, x_num, pipe - 2)

            if pipe < -100:
                setattr(self, x_num, 650)
                setattr(self, h_num, random.randint(100, 315))
'''



'''
def check_collide():
    Flappy_Rect = Flappy_Bird.image.get_rect()
    Pipes_1_Rect_Top_Lip = Pipes.Pipes_1.Top_Pipe.lip_image.get_rect()
    Pipes_1_Rect_Top_Pipe = Pipes.Pipes_1.Top_Pipe.pipe_image.get_rect()
    Pipes_1_Rect_Bottom_Lip = Pipes.Pipes_1.Bottom_Pipe.lip_image.get_rect()
    Pipes_1_Rect_Bottom_Pipe = Pipes.Pipes_1.Bottom_Pipe.pipe_image.get_rect()

    print(' ')
    print(Flappy_Rect.x)
    print(Pipes_1_Rect_Top_Pipe.x)
    print(Pipes_1_Rect_Bottom_Pipe.x)

    if Flappy_Rect.colliderect(Pipes_1_Rect_Top_Lip) == True or colliderect(Flappy_Rect, Pipes_1_Rect_Bottom_Lip) == True:
        Flappy_Bird.crash()
    if colliderect(Flappy_Rect, Pipes_1_Rect_Top_Pipe) == True or colliderect(Flappy_Rect, Pipes_1_Rect_Bottom_Pipe) == True:
        Flappy_Bird.crash()
'''

pygame.init()
pygame.font.init()

done = False

screen = pygame.display.set_mode((635, 455))

Background = Background('flappy_bkgd.png')
Flappy_Bird = Avatar('flappy-bird.png')

print(pipes[0])
print(pipes[1])

while not done:
    screen.fill([255, 255, 255])

    Background.print()
    Flappy_Bird.print()

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    Flappy_Bird.flap()
    
    pressed = pygame.key.get_pressed()
        
    Flappy_Bird.fall()
    
    pygame.display.flip()
