import pygame

"""
    This class takes care of most of the animation processing. I have combined all those methods in once class to prevent
    from copy pasting the same thing over the player and the enemy class.
"""


# Function that loads the 6 frame animation sprites

def loadSprites(path, spriteList):
    for i in range(0, 6):
        spriteList.append(pygame.image.load(path + "tile_" + str(i) + ".png"))


# Function that sets' the character's current image to play the walk up sequence of sprites

def playWalkUp(self, speed):
    # Variable that helps controlling the speed of the sprites that are being displayed on the screen
    # this will start with 0 and it will add .3 or the speed parameter, and it will increment every time the function is called
    # there fore it will hold the 0th frame for about 3 seconds and then will switch to frame 1
    self.currentSprite += speed

    # if the variable is greater or equal to 6 (the last frame in the animation)
    if self.currentSprite >= len(self.spritesMoveUp):
        # reset the variable
        self.currentSprite = 0

    # display the frame by changing the image of the character
    self.image = self.spritesMoveUp[int(self.currentSprite)]


# Same as the function above with the exception that it changes the sprites for the walk down animation

def playWalkDown(self, speed):
    self.currentSprite += speed

    if self.currentSprite >= len(self.spritesMoveDown):
        self.currentSprite = 0

    self.image = self.spritesMoveDown[int(self.currentSprite)]


# Same as the function above with the exception that it changes the sprites for the walk left animation

def playWalkLeft(self, speed):
    self.currentSprite += speed

    if self.currentSprite >= len(self.spritesMoveLeft):
        self.currentSprite = 0

    self.image = self.spritesMoveLeft[int(self.currentSprite)]


# Same as the function above with the exception that it changes the sprites for the walk right animation

def playWalkRight(self, speed):
    self.currentSprite += speed

    if self.currentSprite >= len(self.spritesMoveRight):
        self.currentSprite = 0

    self.image = self.spritesMoveRight[int(self.currentSprite)]


# Function that changes the animation state of the character
# Every character has 4 booleans that play the corresponding animation
# The parameters set everything to false by default

def animationBool(self, movingUp=False, movingDown=False, movingLeft=False, movingRight=False):
    # Then sets the class boolean variables to the ones passed to the function
    self.movingUp = movingUp
    self.movingDown = movingDown
    self.movingLeft = movingLeft
    self.movingRight = movingRight
