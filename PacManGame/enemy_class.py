import pygame
import random
from settings import *

Vector2 = pygame.math.Vector2


class Enemy:
    def __init__(self, game, position, enemyNumber):
        self.Game = game
        self.gridPosition = position
        self.pixelPosition = self.getPixelPosition()
        self.radius = 10
        self.number = enemyNumber
        self.colour = self.setColour()
        self.personality = self.setPersonality()
        self.direction = Vector2(1, 0)

    def update(self):
        self.pixelPosition += self.direction
        if self.timeToMove():
            self.move()

        # Set grid position
        self.gridPosition[0] = (self.pixelPosition[
                                    0] - TOP_BOTTOM_PADDING + self.Game.cellWidth // 2) // self.Game.cellWidth + 1
        self.gridPosition[1] = (self.pixelPosition[
                                    1] - TOP_BOTTOM_PADDING + self.Game.cellHeight // 2) // self.Game.cellHeight + 1

    def draw(self):
        pygame.draw.circle(self.Game.screen, self.colour, (int(self.pixelPosition.x), int(self.pixelPosition.y)),
                           self.radius)

    def getPixelPosition(self):
        return Vector2((self.gridPosition.x * self.Game.cellWidth) + TOP_BOTTOM_PADDING // 2 + self.Game.cellWidth // 2,
                       (self.gridPosition.y * self.Game.cellHeight) + TOP_BOTTOM_PADDING // 2 + self.Game.cellHeight // 2)

    def timeToMove(self):
        if int(self.pixelPosition.x + TOP_BOTTOM_PADDING // 2) % self.Game.cellWidth == 0:
            if self.direction == Vector2(1, 0) or self.direction == Vector2(-1, 0):
                return True

        if int(self.pixelPosition.y + TOP_BOTTOM_PADDING // 2) % self.Game.cellHeight == 0:
            if self.direction == Vector2(0, 1) or self.direction == Vector2(0, -1):
                return True
        return False

    def move(self):
        if self.personality == "Random":
            self.direction = self.getRandomDirection()
    
    def getRandomDirection(self):
        while True:
            number = random.randint(-2, 2)
            if number == -2:
                xDirection, yDirection = 1, 0

            elif number == -1:
                xDirection, yDirection = 0, 1

            elif number == 0:
                xDirection, yDirection = -1, 0

            else:
                xDirection, yDirection = 0, -1
            nextPosition = Vector2(self.gridPosition.x + xDirection, self.gridPosition.y + yDirection)

            if nextPosition not in self.Game.walls:
                break
        return Vector2(xDirection, yDirection)

    def setColour(self):
        if self.number == 0:
            return 255, 0, 0
        if self.number == 1:
            return 0, 255, 0
        if self.number == 2:
            return 0, 0, 255
        if self.number == 3:
            return 255, 0, 255

    def setPersonality(self):
        if self.number == 0:
            return "Speedy"
        elif self.number == 1:
            return "Scared"
        elif self.number == 2:
            return "Random"
        elif self.number == 3:
            return "Slow"

