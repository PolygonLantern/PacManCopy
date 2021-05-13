import pygame


def loadSprites(path, spriteList):
    for i in range(0, 6):
        spriteList.append(pygame.image.load(path + "tile_" + str(i) + ".png"))


def playWalkUp(self, speed):
    self.currentSprite += speed

    if self.currentSprite >= len(self.spritesMoveUp):
        self.currentSprite = 0

    self.image = self.spritesMoveUp[int(self.currentSprite)]


def playWalkDown(self, speed):
    self.currentSprite += speed

    if self.currentSprite >= len(self.spritesMoveDown):
        self.currentSprite = 0

    self.image = self.spritesMoveDown[int(self.currentSprite)]


def playWalkLeft(self, speed):
    self.currentSprite += speed

    if self.currentSprite >= len(self.spritesMoveLeft):
        self.currentSprite = 0

    self.image = self.spritesMoveLeft[int(self.currentSprite)]


def playWalkRight(self, speed):
    self.currentSprite += speed

    if self.currentSprite >= len(self.spritesMoveRight):
        self.currentSprite = 0

    self.image = self.spritesMoveRight[int(self.currentSprite)]


def animationBool(self, movingUp=False, movingDown=False, movingLeft=False, movingRight=False):
    self.movingUp = movingUp
    self.movingDown = movingDown
    self.movingLeft = movingLeft
    self.movingRight = movingRight
