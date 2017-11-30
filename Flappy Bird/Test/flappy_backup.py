import pygame
import random
import time

# Sound effects
# Variations

######################### CLASSES ##########################
 ### BACKGROUND ###
class Background_Image():
    def __init__(self, image_file):

        # Load background image
        self.image = pygame.image.load(image_file)

    def print(self):
        # Send image to screen
        screen.blit(self.image, (0, 0))

 ### AVATAR ###
class Avatar(pygame.sprite.Sprite):
    def __init__(self, image_file):
        # Define as a sprite for collision detection
        pygame.sprite.Sprite.__init__(self)

        # Load and scale down avatar image
        image = pygame.image.load(image_file)
        self.image =  pygame.transform.scale(image, (35, 35))

        # Set default values for screen position
        self.x = 50
        self.y = 50

        # Define image rect: rectangle of space it occupies on the screen
        self.rect = pygame.Rect(self.x, self.y, 35, 35)
 
        # Set up variables for flap and fall speeds
        self.speed_fall = 0
        self.speed_flap = 0

    def print(self):
        # Send avatar image to screen
        screen.blit(self.image, self.rect)

    def flap(self):
        # Set up initial and target heights for flap
        initial_y = int(self.rect.y)
        flap_height = 10
        target = initial_y - flap_height

        # Flap; decrease change in y until peak is reached
        if self.rect.y > target:
            for i in range(-1*(self.rect.y - target), 1):
                self.speed_flap = i/3
                self.rect.y += self.speed_flap

        # "Hover" effect at peak before beginning to fall again
        self.speed_fall = -3

    def fall(self):
        # Set gravity-based acceleration 
        self.acceleration = 1/3

        # Set terminal velocity
        if self.speed_fall > 10:
            self.speed_fall = 10

        # Set ground height
        if self.rect.y < 320:
            self.rect.y += self.speed_fall

        # Accelerate fall until terminal valocity is reached
        self.speed_fall += (self.acceleration)

    def crash(self):
        # Fall faster than normal
        self.acceleration = 2/3
        self.fall()

        # Switch avatar to nosedive version
        image = pygame.image.load('Resources/flappy-crash.png')
        self.image =  pygame.transform.scale(image, (35, 35))

### PIPES ###
class Shaft():
    def __init__(self, orientation, height, x):
        # Set pipe height
        self.height = int(height)

        # Set pipe orientation (1 = bottom pipe, -1 = top pipe)
        self.orientation = orientation

        # Load and scale image
        image = pygame.image.load('Resources/pipe_shaft.png')
        self.image = pygame.transform.scale(image, (50, self.height))

        # Set initial x-axis position
        self.x = x

        # Determine y-axis position based on height and orientation
        if self.orientation == 1:
            self.y = (315 - self.height) + 37
            
        elif self.orientation == -1:
            self.y = 0   

        # Define image rect
        self.rect = pygame.Rect(self.x, self.y, 35, 35)

    def print(self, x):
        # Update x value
        self.x = x

        # Redifine image rect to reflect new position
        self.rect = pygame.Rect(self.x, self.y, 35, 35)

        # Send newly positioned image to screen
        screen.blit(self.image, self.rect)

class Lip():
    def __init__(self, orientation, height, x):
        # Set pipe height
        self.height = int(height)

        # Set pipe orientation (1 = bottom pipe, -1 = top pipe)
        self.orientation = orientation

        # Load and scale image
        image = pygame.image.load('Resources/pipe_head.png')
        self.image = pygame.transform.scale(image, (50, 30))

        # Set initial x-axis position
        self.x = x

        # Determine y-axis position based on height and orientation
        if self.orientation == 1:
            self.y = (315 - self.height) + 37
            
        elif self.orientation == -1:
            self.y = self.height

        # Define image rect
        self.rect = pygame.Rect(self.x, self.y, 35, 35)

    def print(self, x):
        # Update x value
        self.x = x

        # Redifine image rect to reflect new position
        self.rect = pygame.Rect(self.x, self.y, 35, 35)

        # Send newly positioned image to screen
        screen.blit(self.image, self.rect)

class Pipe():
    def __init__(self, orientation, height, x):
        # Set pipe height
        self.height = int(height)

        # Set pipe orientation (1 = bottom pipe, -1 = top pipe)
        self.orientation = orientation

        # Set initial x-axis position
        self.x = x

        # Define pipe shaft and lip based on above parameters
        self.shaft = Shaft(self.orientation, self.height, self.x)
        self.lip = Lip(self.orientation, self.height, self.x)

    def print(self, x):
        # Update x value
        self.x = x

        # Send newly positioned images to screen
        self.shaft.print(self.x)
        self.lip.print(self.x)
  
class Pipe_Pair():
    def __init__(self, gap_height, x):
        # Define gap height (y position where gap occurs) and size
        self.gap_height = gap_height
        self.gap_size = 90

        # Set initial x-axis position     
        self.x = x

        # Define top and bottom pipe based on above parameters
        self.Bottom_Pipe = Pipe(1, self.gap_height, self.x)
        self.Top_Pipe = Pipe(-1, 315 - (self.gap_size + self.gap_height), self.x)

    def print(self, x):
        # Update x value
        self.x = x

        # Send newly positioned images to screen
        self.Bottom_Pipe.print(self.x)
        self.Top_Pipe.print(self.x)

class Obstacles(pygame.sprite.Sprite):
    def __init__(self):
        # Define as a sprite for collision detection
        pygame.sprite.Sprite.__init__(self)

        # Define arrays to hold pipe pairs and corresponding x-values
        self.pipes = []
        self.x = []

        # Set minimum and maximum heights for pipes
        self.min = 30
        self.max = 225

        # Create pipe pairs, define height and initial position, and save info to arrays
        for i in range(0, 5):
            x = 550 + (150*i)
            h = random.uniform(self.min, self.max)

            self.pipes.append(Pipe_Pair(h, x))
            self.x.append(x)

    def pan(self):
        global alive 

        # Only pan if bird hasn't crashed
        if alive == True:
            # Cycle through pipes and move slightly to the left
            for i in range(0, 5):
                self.x[i] -= 2

                # Reset a pipe off to the right after it passed the screen and reassign a new height
                if self.x[i] < -100:
                    self.x[i] = 650
                    self.pipes[i] = Pipe_Pair(random.randint(self.min, self.max), self.x[i])

    def print(self):
        # Send newly positioned images to screen
        for i in range(0, 5):
            self.pipes[i].print(self.x[i])

class Menu_Button():
    def __init__(self, file, x, y, button_type):
        global mode 
        global character 
        global alive

        # Set up size and position variables
        self.x = x
        self.y = y
        self.w = 125
        self.h = 45

        # Load and scale button image
        image = pygame.image.load(file)
        self.image =  pygame.transform.scale(image, (self.w, self.h))

        # Shortcuts to get position and state of mouse
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # Check to see if mouse is over button
        if (self.x + self.w) > mouse[0] > self.x and (self.y + self.h) > mouse[1] > self.y:
            # If button is clicked, restart play mode or switch to main menu depending on button
            if click[0] == 1:
                game_init(character) # Reset game with chosen character

                alive = True # Revive avatar

                # Navigate accordingly
                if button_type == 'replay':
                    mode = 'play'
                if button_type == 'home':
                    mode = 'home'

    def print(self):
        # Send image of button to screen
        screen.blit(self.image, (self.x, self.y))

class Avatar_Button():
    def __init__(self, file, x, y, avatar_type):
        global character
        global mode

        # Set up size and position variables
        self.x = x
        self.y = y
        self.w = 45
        self.h = 45

        # Load and scale button image
        image = pygame.image.load(file)
        self.image =  pygame.transform.scale(image, (self.w, self.h))

        # Shortcuts to get position and state of mouse
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # Check to see if mouse is over button
        if (self.x + self.w) > mouse[0] > self.x and (self.y + self.h) > mouse[1] > self.y:
            # If button is hovered over, display title of theme
            if click[0] != 1:
                display_title(avatar_type)
            # If button is clicked, start game with chosen avatar
            if click[0] == 1:
                character = avatar_type
                game_init(character)
                mode = 'play'

    def print(self):
        # Send image of button to screen
        screen.blit(self.image, (self.x, self.y))

class Medal():
    def __init__(self, color):
        self.color = color

        # Find file corresponding with medal earned
        if self.color != 'none':
            if self.color == 'bronze':
                file = 'Resources/bronze.png'
            if self.color == 'silver':
                file = 'Resources/silver.png'
            if self.color == 'gold':
                file = 'Resources/gold.png'
            if self.color == 'platinum':
                file = 'Resources/platinum.png'

            # Load and scale image
            image = pygame.image.load(file)
            self.image =  pygame.transform.scale(image, (80, 75))

    def print(self):
        # Send image to screen
        if self.color != 'none':
            screen.blit(self.image, (165, 160))

######################### FUNCTIONS ##########################
def game_init(character): # Initialize, reset, or switch game objects
    global Background_Image
    global Avatar
    global Obstacles

    global Background
    global Flappy_Bird
    global Pipes

    global alive
    global start

    global score
    global cycles
    global tutorial

    # Reset score
    score = 0
    cycles = 0
    tutorial = True

    # Revive avatar
    alive = True

    # Reset timer
    start = time.time()
        
    # Define or redifine/reset character and objects based on theme chosen
    if character == 'bird':
        Background = Background_Image('Resources/flappy_bkgd.png')
        Flappy_Bird = Avatar('Resources/flappy-bird.png')
        Pipes = Obstacles()

def display_title(avatar):
    global Background

    # Reset screen (to erase previous captions)
    screen.fill([255, 255, 255])

    # Print background and game objects with current positions
    Background.print()

    # Load and print title image
    title_image = pygame.image.load('Resources/title.png')
    title =  pygame.transform.scale(title_image, (350, 100))
    screen.blit(title, (125, 50))

    # Redefine a resized version of the flappy bird font
    font = pygame.font.Font("Resources/Flappy.ttf", 35)

    # Define caption text based on selected avatar
    if avatar == 'bird':
        mode_title = 'Classic'

    # Send text to screen
    text = font.render(mode_title, True, (255, 255, 255))
    screen.blit(text, (400 * 4/len(mode_title) + 35, 400))

def home():
     # Load and print title image
    title_image = pygame.image.load('Resources/title.png')
    title =  pygame.transform.scale(title_image, (350, 100))
    screen.blit(title, (125, 50))

    # Print default caption
    font = pygame.font.Font("Resources/Flappy.ttf", 35)
    text = font.render('Choose your avatar!', True, (255, 255, 255))
    screen.blit(text, (125, 400))

    # Define and print avatar buttons
    bird = Avatar_Button('Resources/flappy-bird.png', 290, 175, 'bird')
    bird.print()

def game_over():
    global alive
    global score
    global high_score
    global character

    # Resize flappy bird font
    font = pygame.font.Font("Resources/Flappy.ttf", 35)

    # Crash the avatar
    if character == 'bird':
        Flappy_Bird.crash()

    # Check for high score
    if score > high_score:
        high_score = score

    # Define metal earned
    if score < 10:
        medal = Medal('none')
    if 10 <= score < 20:
        medal = Medal('bronze')
    if 20 <= score < 30:
        medal = Medal('silver')
    if 30 <= score < 40:
        medal = Medal('gold')
    if 40 <= score:
        medal = Medal('platinum')

    # Load and print 'game over' banner
    title_image = pygame.image.load('Resources/game_over.png')
    title =  pygame.transform.scale(title_image, (350, 100))
    screen.blit(title, (140, 15))

    # Load, scale, and print scoreboard
    scoreboard_image = pygame.image.load('Resources/scoreboard.png')
    scoreboard =  pygame.transform.scale(scoreboard_image, (350, 175))
    screen.blit(scoreboard, (135, 100))

    # Print medal on top of scoreboard
    medal.print()

    # Create replay and home buttons
    replay = Menu_Button('Resources/replay.png', 150, 275, 'replay')
    home = Menu_Button('Resources/home.png', 350, 275, 'home')

    # Print buttons
    replay.print()
    home.print()

    # Print score data
    score_value = font.render(str(score), True, (255, 255, 255))
    screen.blit(score_value, (420, 145))

    best_value = font.render(str(high_score), True, (255, 255, 255))
    screen.blit(best_value, (420, 210))

def check_alive():
    global start
    global alive

    # Check how much time has passed so avatar isn't dead instantly 
    now = time.time()

    # End game if avatar touches ground after first 1/2 second
    if Flappy_Bird.rect.y <= 315 and (start-now) > .5:
        alive = False
        game_over()

    # Check for collision with any of the pipes and crash if contact occurs
    for i in range(0, 5):
        Pipe_X = Pipes.pipes[i]

        Flappy_Rect = Flappy_Bird.rect
        Top_Lip = Pipe_X.Top_Pipe.shaft.rect
        Top_Pipe = Pipe_X.Top_Pipe.lip.rect
        Bottom_Lip = Pipe_X.Bottom_Pipe.shaft.rect
        Bottom_Pipe = Pipe_X.Bottom_Pipe.lip.rect

        if Flappy_Rect.colliderect(Top_Lip) or Flappy_Rect.colliderect(Bottom_Lip) or Flappy_Rect.colliderect(Top_Pipe) or Flappy_Rect.colliderect(Bottom_Pipe):
            alive = False
            game_over()

def update_score():
    global score
    global alive

    # Add to score if avatar crossed a value of x that can be found in the list of current pipe locations
    if Flappy_Bird.rect.x in Pipes.x and alive == True:
        score += 1

    # Resize flappy bird font
    font = pygame.font.Font("Resources/Flappy.ttf", 60)

    # Update text to reflect new score
    text = font.render(str(score), True, (255, 255, 255))
    screen.blit(text, (318, 390))

######################### GAME LOGIC ##########################
# Initialize Pygame modules
pygame.init()
pygame.font.init()

# Initialize screen
screen = pygame.display.set_mode((635, 455))
end_screen = pygame.display.set_mode((635, 455))

# Set window title
pygame.display.set_caption("Flappy Bird")

# Set window icon
icon = pygame.image.load('Resources/flappy-bird.png')
pygame.display.set_icon(icon)

# Set font
font = pygame.font.Font("Resources/Flappy.ttf", 60)

# Set default score and create list to save scores
score = 0
high_score = 0

# Set default game-control bools
done = False
alive = True
mode = 'home'
character = 'bird'
tutorial = True

# Define cycles variable (to ensure that the 'how-to play' feature only triggers before first cycle)
cycles = 0

# Set up game objects based on character choice
game_init(character)

# Start timer
start = time.time()

while not done:
    # Check for user input
    key = pygame.key.get_pressed()

    if mode == 'home':
        # Create black background canvas
        screen.fill([255, 255, 255])

        # Print background and game objects with current positions
        Background.print()

        # Print home screen
        home()

        # Monitor buttons and keys for user input
        for event in pygame.event.get():
                # End session if red close button is clicked
                if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                        done = True

    if mode == 'play':

        # Create black background canvas
        screen.fill([255, 255, 255])

        # Print background and game objects with current positions
        Background.print()
        Pipes.print()
        Flappy_Bird.print()

        # Check to see if game is still going 
        check_alive()

        if alive and tutorial == True:
            # Resize flappy bird font
            font = pygame.font.Font("Resources/Flappy.ttf", 20)

            # Update text to reflect new score
            text = font.render('press the spacebar to play', True, (255, 255, 255))
            screen.blit(text, (100, 55))

            # Monitor buttons and keys for user input
            for event in pygame.event.get():
                    # End session if red close button is clicked
                    if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                        done = True
                    # Flap if spacebar is pressed and game is still active
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        tutorial = False
                        Flappy_Bird.flap()

        if alive and tutorial == False:
            # Monitor buttons and keys for user input
            for event in pygame.event.get():
                    # End session if red close button is clicked
                    if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                        done = True
                    # Flap if spacebar is pressed and game is still active
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        Flappy_Bird.flap()
            
            # Move objects
            Flappy_Bird.fall()
            Pipes.pan()

            update_score()
        
        if not alive:
            game_over()

            # Monitor buttons and keys for user input
            for event in pygame.event.get():
                    # End session if red close button is clicked
                    if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                            done = True
                    #if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and alive == True:
                    
    cycles += 1

        # Update screen
    pygame.display.flip()
