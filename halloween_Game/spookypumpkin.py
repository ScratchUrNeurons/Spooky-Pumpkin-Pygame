import random # For generating random numbers
import sys # We will use sys.exit to exit the program
import pygame
from pygame.locals import * # Basic pygame imports
from pygame import mixer
# Global Variables for the game
FPS = 32
SCREENWIDTH = 400
SCREENHEIGHT = 580
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
basey = SCREENHEIGHT * 0.8
game_sprite = {}
game_audio = {}
player = 'gallery/sprites/pumpkin.png'
Background = 'gallery/sprites/Background2.png'
Knife = 'gallery/sprites/knife2.png'
mixer.init()
mixer.music.load("gallery/audio/halloween.mp3")
mixer.music.play(100)
def welcomeScreen():
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - game_sprite['player'].get_height())/2)
    basex = 0
    while True:
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If the user presses space or up key, start the game for them
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(game_sprite['Background'], (0, 0))    
                SCREEN.blit(game_sprite['player'], (playerx, playery))      
                SCREEN.blit(game_sprite['base'], (basex,basey))    
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0
    fps=FPS

    # Create 2 knifes for blitting on the screen
    newKnife1 = getRandomKnife()
    newKnife2 = getRandomKnife()

    # my List of upper knifes
    upperKnifes = [
        {'x': SCREENWIDTH+200, 'y':newKnife1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newKnife2[0]['y']},
    ]
    # my List of lower knifes
    lowerKnifes = [
        {'x': SCREENWIDTH+200, 'y':newKnife1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newKnife2[1]['y']},
    ]

    knifeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerJumpv = -8 # velocity while jumping
    playerJump = False # It is true only when the pumpkin is jumping


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerJumpv
                    playerJump = True
                    game_audio['wing'].play()
                    
                   


        crashTest = isCollide(playerx, playery, upperKnifes, lowerKnifes) # This function will return true if the player is crashed
        if crashTest:
            return     

        #check for score
        playerMidPos = playerx + game_sprite['player'].get_width()/2
        for knife in upperKnifes:
            knifeMidPos = knife['x'] + game_sprite['knife'][0].get_width()/2
            if knifeMidPos<= playerMidPos < knifeMidPos +4:
                score +=1
                if (score % 5 == 0):
                    fps=FPS+4
                    FPSCLOCK.tick(FPS)
                print(f"Your score is {score}") 
                game_audio['point'].play()


        if playerVelY <playerMaxVelY and not playerJump:
            playerVelY += playerAccY

        if playerJump:
            playerJump = False            
        playerHeight = game_sprite['player'].get_height()
        playery = playery + min(playerVelY, basey - playery - playerHeight)

        # move knifes to the left
        for upperKnife , lowerKnife in zip(upperKnifes, lowerKnifes):
            upperKnife['x'] += knifeVelX
            lowerKnife['x'] += knifeVelX
            

        # Add a new knife when the first is about to cross the leftmost part of the screen
        if 0<upperKnifes[0]['x']<5:
            newknife = getRandomKnife()
            upperKnifes.append(newknife[0])
            lowerKnifes.append(newknife[1])

        # if the knife is out of the screen, remove it
        if upperKnifes[0]['x'] < -game_sprite['knife'][0].get_width():
            upperKnifes.pop(0)
            lowerKnifes.pop(0)
        
        # Lets blit our sprites now
        SCREEN.blit(game_sprite['Background'], (0, 0))
        for upperKnife, lowerKnife in zip(upperKnifes, lowerKnifes):
            SCREEN.blit(game_sprite['knife'][0], (upperKnife['x'], upperKnife['y']))
            SCREEN.blit(game_sprite['knife'][1], (lowerKnife['x'], lowerKnife['y']))

        SCREEN.blit(game_sprite['base'], (basex, basey))
        SCREEN.blit(game_sprite['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += game_sprite['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(game_sprite['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += game_sprite['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(fps)

def isCollide(playerx, playery, upperKnifes, lowerKnifes):
    if playery> basey - 25  or playery<0:
        game_audio['hit'].play()
        return True
    
    for knife in upperKnifes:
        knifeHeight = game_sprite['knife'][0].get_height()
        if(playery < knifeHeight + knife['y'] and abs(playerx - knife['x']) < game_sprite['knife'][0].get_width()):
            game_audio['hit'].play()
            return True

    for knife in lowerKnifes:
        if (playery + game_sprite['player'].get_height() > knife['y']) and abs(playerx - knife['x']) < game_sprite['knife'][0].get_width():
            game_audio['hit'].play()
            return True

    return False

def getRandomKnife():
    """
    Generate positions of two knifes(one bottom straight and one top rotated ) for blitting on the screen
    """
    knifeHeight = game_sprite['knife'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - game_sprite['base'].get_height()  - 1.2 *offset))
    knifeX = SCREENWIDTH + 10
    y1 = knifeHeight - y2 + offset
    knife = [
        {'x': knifeX, 'y': -y1}, #upper Knife
        {'x': knifeX, 'y': y2} #lower Knife
    ]
    return knife






if __name__ == "__main__":
    # This will be the main point from where our game will start
    pygame.init() # Initialize all pygame's modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Spooky Pumpkin')
    game_sprite['numbers'] = ( 
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
    )

    game_sprite['base'] =pygame.image.load('gallery/sprites/base2.png').convert_alpha()
    game_sprite['knife'] =(pygame.transform.rotate(pygame.image.load( Knife).convert_alpha(), 180), 
    pygame.image.load(Knife).convert_alpha()
    )

    # Game sounds
    game_audio['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    game_audio['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    game_audio['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    game_audio['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    game_audio['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    game_sprite['Background'] = pygame.image.load(Background).convert()
    game_sprite['player'] = pygame.image.load(player).convert_alpha()

    while True:
        welcomeScreen() # Shows welcome screen to the user until he presses a button
        mainGame() # This is the main game function 