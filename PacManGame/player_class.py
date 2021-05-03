import pygame
from settings import *


class Player:
    def __init__(self, game, position):
        self.Game = game
        self.gridPosition = position
        self.pixelPosition = self.getPixelPosition()
        self.direction = Vector2(1, 0)
        self.storedDirection = None
        self.ableToMove = True
        self.currentScore = 0

    def update(self):
        if self.ableToMove:
            self.pixelPosition += self.direction

        # setting the grid position in ref to the pixel position
        if self.timeToMove():
            if self.storedDirection is not None:
                self.direction = self.storedDirection
            self.ableToMove = self.canMove()

        self.gridPosition[0] = (self.pixelPosition[
                                    0] - TOP_BOTTOM_PADDING + self.Game.cellWidth // 2) // self.Game.cellWidth + 1
        self.gridPosition[1] = (self.pixelPosition[
                                    1] - TOP_BOTTOM_PADDING + self.Game.cellHeight // 2) // self.Game.cellHeight + 1

        if self.onCoin():
            self.collectCoin()

    def draw(self):
        pygame.draw.circle(self.Game.screen, PLAYER_COLOUR, (int(self.pixelPosition.x), int(self.pixelPosition.y)),
                           self.Game.cellWidth // 2 - 2)
        # drawing the grid rectangle
        #pygame.draw.rect(self.Game.screen, RED, (self.gridPosition[0] * self.Game.cellWidth + TOP_BOTTOM_PADDING // 2,
        #                                         self.gridPosition[1] * self.Game.cellHeight + TOP_BOTTOM_PADDING // 2,
        #                                        self.Game.cellWidth, self.Game.cellHeight), 1)

    def onCoin(self):
        if self.gridPosition in self.Game.coins:
            if int(self.pixelPosition.x + TOP_BOTTOM_PADDING // 2) % self.Game.cellWidth == 0:
                if self.direction == Vector2(1, 0) or self.direction == Vector2(-1, 0):
                    return True

            if int(self.pixelPosition.y + TOP_BOTTOM_PADDING // 2) % self.Game.cellHeight == 0:
                if self.direction == Vector2(0, 1) or self.direction == Vector2(0, -1):
                    return True
        else:
            return False

    def collectCoin(self):
        self.Game.coins.remove(self.gridPosition)
        self.currentScore += 1

    def move(self, direction):
        self.storedDirection = direction

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

    def canMove(self):
        for wall in self.Game.walls:
            if Vector2(self.gridPosition + self.direction) == wall:
                return False
        return True
