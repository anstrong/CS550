'''
Annabelle Strong
11/15/2017

This program runs a Flappy Bird game with a couple theme/character variation options

Upon my honor, I have neither given nor recieved unauthorized aid.
'''
import pygame
import random
import time

######################### CLASSES ##########################
### AVATAR ###
class Avatar(pygame.sprite.Sprite):
    def __init__(self, avatar_type):
        # Define as a sprite for collision detection
        pygame.sprite.Sprite.__init__(self)

        # Define avatar type for character-based alterations
        self.type = avatar_type

        # Load avatar image
        image = pygame.image.load('Resources/Characters/' + self.type +'.png')

        # Scale avatar image as needed for each character
        if self.type == 'flappy-bird':
            self.image =  pygame.transform.scale(image, (35, 35))
        if self.type == 'nyan-cat':
            self.image =  pygame.transform.scale(image, (38, 25))
        elif self.type == 'unicorn':
            self.image =  pygame.transform.scale(image, (48, 35))
        elif self.type == 'fish':
            self.image =  pygame.transform.scale(image, (35, 30))

        # Set default values for screen position
        self.x = 50
        self.y = 50
        self.ground = 455

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
        # Change ground height for Flappy Bird mode
        if self.type == 'flappy-bird':
            self.ground = 320

        # Set slower gravitational acceleration for fish mode (to give water-like lag effect)
        if self.type == 'fish':
            self.acceleration = 1/5
        else: # Set regular gravity-based acceleration 
            self.acceleration = 1/3

        # Set terminal velocity
        if self.speed_fall > 10:
            self.speed_fall = 10

        # Accelerate avatar towards ground
        if self.rect.y < self.ground:
            self.rect.y += self.speed_fall

        # Accelerate fall until terminal valocity is reached
        self.speed_fall += (self.acceleration)

    def crash(self):
        # Fall faster than normal
        self.acceleration = 2/3
        self.fall()

        # Switch Flappy Bird avatar to nosedive version (other avatars' images didn't work well for this but I made sure to include it for the Classic mode)
        if self.type == 'flappy-bird':
            image = pygame.image.load('Resources/Characters/' + self.type + '_crash.png')
            self.image =  pygame.transform.scale(image, (35, 35))

 ### BACKGROUND ###
class Background_Image():
    def __init__(self, avatar_type):
        # Load background image
        self.image = pygame.image.load('Resources/Characters/' + avatar_type + '_bkgd.png')

    def print(self):
        # Send image to screen
        screen.blit(self.image, (0, 0))

### PIPES ###
class Pipe_Component():
    def __init__(self, orientation, height, x, avatar_type):
        # Set pipe height
        self.height = int(height)

        # Set pipe orientation (1 = bottom pipe, -1 = top pipe)
        self.orientation = orientation

        # Set initial x-axis position
        self.x = x

        # Place pipe based on mode (since Classic has higher ground limit)
        if avatar_type == 'flappy-bird':
            if self.orientation == 1:
                self.y = (315 - self.height) + 37
            elif self.orientation == -1:
                self.y = 0
        else:
            if self.orientation == 1:
                self.y = (455 - self.height)
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

class Shaft(Pipe_Component):
    def __init__(self, orientation, height, x, avatar_type):
        # Initialize parent class
        Pipe_Component.__init__(self, orientation, height, x, avatar_type)

        # Load and scale image
        image = pygame.image.load('Resources/Characters/' + avatar_type + '_pipe_shaft.png')
        self.image = pygame.transform.scale(image, (50, self.height)) 


class Lip(Pipe_Component):
    def __init__(self, orientation, height, x, avatar_type):
        # Initialize parent class
        Pipe_Component.__init__(self, orientation, height, x, avatar_type)
        
        # Load and scale image
        image = pygame.image.load('Resources/Characters/' + avatar_type + '_pipe_lip.png')
        self.image = pygame.transform.scale(image, (50, 30))

        if self.orientation == -1: 
            self.y = self.height

class Pipe():
    def __init__(self, orientation, height, x, avatar_type):
        # Set pipe height
        self.height = int(height)

        # Set pipe orientation (1 = bottom pipe, -1 = top pipe)
        self.orientation = orientation

        # Set initial x-axis position
        self.x = x

        # Define pipe shaft and lip based on above parameters
        self.shaft = Shaft(self.orientation, self.height, self.x, avatar_type)
        self.lip = Lip(self.orientation, self.height, self.x, avatar_type)

    def print(self, x):
        # Update x value
        self.x = x

        # Send newly positioned images to screen
        self.shaft.print(self.x)
        self.lip.print(self.x)
  
class Pipe_Pair():
    def __init__(self, gap_height, x, avatar_type):
        # Define gap height (y position where gap occurs) and size
        self.gap_height = gap_height

        # Set ground height and gap based on mode (since Classic has higher ground limit and fish mode is slower and requires a larget pipe gap)
        if avatar_type == 'flappy-bird':
            self.ground = 315
            self.gap_size = 90
        elif avatar_type == 'fish':
            self.ground = 455
            self.gap_size = 145
        else:
            self.ground = 455
            self.gap_size = 135

        # Set initial x-axis position     
        self.x = x

        # Define top and bottom pipe based on above parameters
        self.Bottom_Pipe = Pipe(1, self.gap_height, self.x, avatar_type)
        self.Top_Pipe = Pipe(-1, self.ground - (self.gap_size + self.gap_height), self.x, avatar_type)

    def print(self, x):
        # Update x value
        self.x = x

        # Send newly positioned images to screen
        self.Bottom_Pipe.print(self.x)
        self.Top_Pipe.print(self.x)

class Obstacles(pygame.sprite.Sprite):
    def __init__(self, avatar_type):
        # Define as a sprite for collision detection
        pygame.sprite.Sprite.__init__(self)

        # Set avatar type for character-based modifications
        self.avatar_type = avatar_type

        # Change pipe distance for fish mode due to speed difference
        if self.avatar_type == 'fish':
            self.pipe_distance = 175
        else:
            self.pipe_distance = 150

        # Define arrays to hold pipe pairs and corresponding x-values
        self.pipes = []
        self.x = []

        # Set minimum and maximum heights for pipes based on mode's ground limit
        self.min = 50
        if self.avatar_type == 'flappy-bird':
            self.max = 225
        elif self.avatar_type == 'fish':
            self.max = 300
        else:
            self.max = 310

        # Create pipe pairs, define height and initial position, and save info to arrays
        for i in range(0, 5):
            x = 550 + (self.pipe_distance*i)
            h = random.uniform(self.min, self.max)

            self.pipes.append(Pipe_Pair(h, x, self.avatar_type))
            self.x.append(x)

    def pan(self):
        # Cycle through pipes and move each slightly to the left
        for i in range(0, 5):
            self.x[i] -= 2

            # Reset a pipe off to the right after it passed the screen and reassign a new height
            if self.x[i] < -100:
                self.x[i] = (5*self.pipe_distance) -100
                self.pipes[i] = Pipe_Pair(random.randint(self.min, self.max), self.x[i], self.avatar_type)

    def print(self):
        # Send newly positioned images to screen
        for i in range(0, 5):
            self.pipes[i].print(self.x[i])

class Menu_Button():
    def __init__(self, x, y, button_type):
        global mode 

        # Set up size and position variables
        self.x = x
        self.y = y
        self.w = 125
        self.h = 45

        # Load and scale button image
        image = pygame.image.load('Resources/General/' + button_type + '.png')
        self.image =  pygame.transform.scale(image, (self.w, self.h))

        # Shortcuts to get position and state of mouse
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # Check to see if mouse is over button
        if (self.x + self.w) > mouse[0] > self.x and (self.y + self.h) > mouse[1] > self.y:
            # If button is clicked, restart play mode or switch to main menu depending on button
            if click[0] == 1:
                # Navigate accordingly
                if button_type == 'replay':
                    game_init(Character.type) # Reset game with chosen character

                if button_type == 'home':
                    mode = 'home'

    def print(self):
        # Send image of button to screen
        screen.blit(self.image, (self.x, self.y))

class Avatar_Button():
    def __init__(self, x, y, avatar_type):
        global character
        global mode

        # Set up size and position variables
        self.x = x
        self.y = y

        # Change height and width for each image as necessary
        if avatar_type == 'flappy-bird':
            self.w = 45
            self.h = 45
        elif avatar_type == 'nyan-cat':
            self.w = 65
            self.h = 45
        elif avatar_type == 'unicorn':
            self.w = 75
            self.h = 65
        elif avatar_type == 'fish':
            self.w = 52
            self.h = 45

        # Load and scale button image
        image = pygame.image.load('Resources/Characters/' + avatar_type + '.png')
        self.image =  pygame.transform.scale(image, (self.w, self.h))

        # Shortcuts to get position and state of mouse
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # Check to see if mouse is over button
        if (self.x + self.w) > mouse[0] > self.x and (self.y + self.h) > mouse[1] > self.y:
            # If button is hovered over, display title of theme
            if click[0] != 1:
                print_home(avatar_type)
            # If button is clicked, start game with chosen avatar
            if click[0] == 1:
                game_init(avatar_type)
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
                file = 'Resources/General/bronze.png'
            if self.color == 'silver':
                file = 'Resources/General/silver.png'
            if self.color == 'gold':
                file = 'Resources/General/gold.png'
            if self.color == 'platinum':
                file = 'Resources/General/platinum.png'

            # Load and scale image
            image = pygame.image.load(file)
            self.image =  pygame.transform.scale(image, (85, 85))

    def print(self):
        # Send image to screen
        if self.color != 'none':
            screen.blit(self.image, (168, 150))

######################### FUNCTIONS ##########################
def game_init(avatar_type): # Initialize, reset, or switch game objects
    global score
    global cycles
    global tutorial
    global alive
    global start

    global Character
    global Background
    global Pipes

    # Reset score
    score = 0
    cycles = 0
    tutorial = True

    # Revive avatar
    alive = True

    # Reset timer
    start = time.time()
        
    # Define or redifine/reset character and objects based on theme chosen
    Character = Avatar(avatar_type)
    Background = Background_Image(avatar_type)
    Pipes = Obstacles(avatar_type)

def print_home(avatar_type):
    # Reset screen (to erase previous captions)
    screen.fill([255, 255, 255])

    # Print background and game objects with current positions
    Background.print()

     # Load and print title image
    title_image = pygame.image.load('Resources/General/title.png')
    title =  pygame.transform.scale(title_image, (350, 100))
    screen.blit(title, (125, 50))

    # Define caption text based on selected avatar
    mode_title = 'Pick an avatar!'
    y_value = 180
    if avatar_type == 'flappy-bird':
        mode_title = 'Classic'
        y_value = 245
    elif avatar_type == 'nyan-cat':
        mode_title = 'Nyan Cat'
        y_value = 245
    elif avatar_type == 'unicorn':
        mode_title = 'Unicorn'
        y_value = 245
    elif avatar_type == 'fish':
        mode_title = 'Fish'
        y_value = 245

    # Define caption color based on selected avatar's background
    if Character.type == 'unicorn':
        color = (0, 0, 0)
    else:
        color = (255, 255, 255)

    # Print default caption
    font = pygame.font.Font("Resources/General/Flappy.ttf", 35)
    text = font.render(mode_title, True, color)
    screen.blit(text, (y_value, 400))

def home():
    print_home('none')

    # Create avatar buttons
    Flappy_Bird_Button = Avatar_Button(235, 175, 'flappy-bird')
    Nyan_Cat_Button = Avatar_Button(135, 175, 'nyan-cat')
    Unicorn_Button = Avatar_Button(410, 160, 'unicorn')
    Fish_Button = Avatar_Button(320, 175, 'fish')

    # Send buttons to screen
    Flappy_Bird_Button.print()
    Nyan_Cat_Button.print()
    Unicorn_Button.print()
    Fish_Button.print()

def game_over():
    global score
    global high_score

    # Resize flappy bird font
    font = pygame.font.Font("Resources/General/Flappy.ttf", 35)

    # Crash the avatar
    Character.crash()

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
    title_image = pygame.image.load('Resources/General/game_over.png')
    title =  pygame.transform.scale(title_image, (350, 100))
    screen.blit(title, (140, 15))

    # Load, scale, and print scoreboard
    scoreboard_image = pygame.image.load('Resources/General/scoreboard.png')
    scoreboard =  pygame.transform.scale(scoreboard_image, (350, 175))
    screen.blit(scoreboard, (135, 100))

    # Print medal on top of scoreboard
    medal.print()

    # Create replay and home buttons
    replay = Menu_Button(150, 275, 'replay')
    home = Menu_Button(350, 275, 'home')

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

    # End game if avatar touches ground after first 1/10 second
    if Character.rect.y >=  Character.ground and (start-now) > .1:
        alive = False
        game_over()

    # Check for collision with any of the pipes and crash if contact occurs
    for i in range(0, 5):
        Pipe_X = Pipes.pipes[i]

        Character_Rect = Character.rect
        Top_Lip = Pipe_X.Top_Pipe.shaft.rect
        Top_Pipe = Pipe_X.Top_Pipe.lip.rect
        Bottom_Lip = Pipe_X.Bottom_Pipe.shaft.rect
        Bottom_Pipe = Pipe_X.Bottom_Pipe.lip.rect

        if Character_Rect.colliderect(Top_Lip) or Character_Rect.colliderect(Bottom_Lip) or Character_Rect.colliderect(Top_Pipe) or Character_Rect.colliderect(Bottom_Pipe):
            alive = False
            game_over()

def update_score():
    global score
    global alive

    # Add to score if avatar crossed a value of x that can be found in the list of current pipe locations
    if Character.rect.x in Pipes.x and alive == True:
        score += 1

    # Change the score counter color for the unicorn theme's light background
    if Character.type == 'unicorn':
        color = (0, 0, 0)
    else:
        color = (255, 255, 255)

    # Resize flappy bird font
    font = pygame.font.Font("Resources/General/Flappy.ttf", 60)

    # Update text to reflect new score
    text = font.render(str(score), True, color)
    screen.blit(text, (318, 390))

######################### GAME LOGIC ##########################
# Initialize Pygame modules
pygame.init()
pygame.font.init()

# Initialize screen
screen = pygame.display.set_mode((635, 455))

# Set window title
pygame.display.set_caption("Flappy Bird")

# Set window icon
icon = pygame.image.load('Resources/Characters/flappy-bird.png')
pygame.display.set_icon(icon)

# Set font
font = pygame.font.Font("Resources/General/Flappy.ttf", 60)

# Set default score and create high score variable
score = 0
high_score = 0

# Set default game-control bools and modes
done = False
alive = True
tutorial = True

mode = 'home'
avatar_type = 'flappy-bird'

# Set up game objects based on character choice
game_init(avatar_type)

# Start timer
start = time.time()

while not done:
    # Check for user input
    key = pygame.key.get_pressed()

    # Home screen
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

    # Game mode
    if mode == 'play':
        # Create black background canvas
        screen.fill([255, 255, 255])

        # Print background and game objects with current positions
        Background.print()
        Pipes.print()
        Character.print()

        # Check to see if game is still going 
        check_alive()

        # Pause movement until player hits spacebar
        if alive and tutorial == True:
            # Resize flappy bird font
            font = pygame.font.Font("Resources/General/Flappy.ttf", 20)

            # Update text to reflect new score
            text = font.render('press the spacebar to play', True, (255, 255, 255))
            screen.blit(text, (105, 58))

            # Monitor buttons and keys for user input
            for event in pygame.event.get():
                    # End session if red close button is clicked
                    if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                        done = True
                    # Flap if spacebar is pressed and game is still active
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        tutorial = False
                        Character.flap()

        # Resume moement
        if alive and tutorial == False:
            # Monitor buttons and keys for user input
            for event in pygame.event.get():
                    # End session if red close button is clicked
                    if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                        done = True
                    # Flap if spacebar is pressed and game is still active
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        Character.flap()
            
            # Move objects
            Character.fall()
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

    # Update screen
    pygame.display.flip()
