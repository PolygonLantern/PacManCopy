from settings import *
from pygame import mixer
from Utilities import *

# IMPORTANT FOR ANIMATION FOR THE PLAYER print(((MAZE_WIDTH//2)//10)//2 - 2)

class Player(pygame.sprite.Sprite):
    def __init__(self, game, position, playerSpritePath):
        super().__init__()
        self.Game = game
        self.startPosition = [position.x, position.y]
        self.gridPosition = position
        self.pixelPosition = self.getPixelPosition()
        self.direction = Vector2(0, 0)
        self.storedDirection = None
        self.ableToMove = True
        self.currentScore = 0
        self.lives = 3
        self.speed = 2
        self.spritesMoveUp = []
        self.spritesMoveDown = []
        self.spritesMoveLeft = []
        self.spritesMoveRight = []
        self.animationSpeed = .3
        loadSprites("Presets/PlayerSprites/Walk/WalkUp/", self.spritesMoveUp)
        loadSprites("Presets/PlayerSprites/Walk/WalkDown/", self.spritesMoveDown)
        loadSprites("Presets/PlayerSprites/Walk/WalkLeft/", self.spritesMoveLeft)
        loadSprites("Presets/PlayerSprites/Walk/WalkRight/", self.spritesMoveRight)
        self.movingUp = False
        self.movingDown = False
        self.movingLeft = False
        self.movingRight = False
        self.currentSprite = 0
        self.image = self.spritesMoveRight[self.currentSprite]
        self.rect = self.image.get_rect()


    def Update(self):
        if self.ableToMove:
            self.pixelPosition += self.direction * self.speed

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
            for coin in self.Game.coinsSprites:
                coin.update()

        if self.onPickUp():
            self.collectPickUp()
            for pickUp in self.Game.pickUpSprites:
                pickUp.update()

    def update(self):

        if self.movingUp:
            playWalkUp(self, self.animationSpeed)
        elif self.movingDown:
            playWalkDown(self, self.animationSpeed)
        elif self.movingLeft:
            playWalkLeft(self, self.animationSpeed)
        elif self.movingRight:
            playWalkRight(self, self.animationSpeed)

        self.rect.center = (int(self.pixelPosition.x), int(self.pixelPosition.y))

    def draw(self):
        self.update()
        # draw player lives
        for x in range(self.lives):
            pygame.draw.circle(self.Game.screen, PLAYER_COLOUR, (15 + 35 * x, HEIGHT - 15), 10)

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
        self.Game.CoinPrefab.sound.play()

    def onPickUp(self):
        if self.gridPosition in self.Game.pickUps:
            if int(self.pixelPosition.x + TOP_BOTTOM_PADDING // 2) % self.Game.cellWidth == 0:
                if self.direction == Vector2(1, 0) or self.direction == Vector2(-1, 0):
                    return True

            if int(self.pixelPosition.y + TOP_BOTTOM_PADDING // 2) % self.Game.cellHeight == 0:
                if self.direction == Vector2(0, 1) or self.direction == Vector2(0, -1):
                    return True
        else:
            return False

    def collectPickUp(self):
        self.Game.pickUps.remove(self.gridPosition)
        self.currentScore += 5
        self.Game.PickUpPrefab.sound.play()

    def move(self, direction):
        self.storedDirection = direction

    def getPixelPosition(self):
        return Vector2((self.gridPosition.x * self.Game.cellWidth) + TOP_BOTTOM_PADDING // 2 + self.Game.cellWidth // 2,
                       (self.gridPosition.y * self.Game.cellHeight) + TOP_BOTTOM_PADDING // 2 + self.Game.cellHeight // 2)

    def timeToMove(self):
        if int(self.pixelPosition.x + TOP_BOTTOM_PADDING // 2) % self.Game.cellWidth == 0:
            if self.direction == Vector2(1, 0) or self.direction == Vector2(-1, 0) or self.direction == Vector2(0, 0):
                return True

        if int(self.pixelPosition.y + TOP_BOTTOM_PADDING // 2) % self.Game.cellHeight == 0:
            if self.direction == Vector2(0, 1) or self.direction == Vector2(0, -1) or self.direction == Vector2(0, 0):
                return True

    def canMove(self):
        for wall in self.Game.walls:
            if Vector2(self.gridPosition + self.direction) == wall:
                return False
        return True
