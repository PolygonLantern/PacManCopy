from settings import *
from Utilities import *


# The player's class

class Player(pygame.sprite.Sprite):
    # The constructor for the class, with the game and position parameters
    def __init__(self, game, position):
        # the parent class constructor
        super().__init__()
        # set the class' game variable
        self.Game = game
        # set the starting position of the player to the given coordinates
        self.startPosition = [position.x, position.y]
        # set the grid position of the player to the Vector2 that is passed from the parameters
        self.gridPosition = position
        # calculate the pixel position of the player
        self.pixelPosition = self.getPixelPosition()
        # set the direction of the player when initialised
        self.direction = Vector2(0, 0)
        # variable that remembers what was the last direction that was input by the player
        self.storedDirection = None
        # boolean if the player can move
        self.ableToMove = True
        # variable for the current score
        self.currentScore = 0
        # variable for the lives and the speed of the player
        self.lives = 3
        self.speed = 2
        # lists for the animation sprites
        self.spritesMoveUp = []
        self.spritesMoveDown = []
        self.spritesMoveLeft = []
        self.spritesMoveRight = []
        # variable for the speed of the animation
        self.animationSpeed = .3
        # load all the sprites using the Utility function
        loadSprites("Presets/PlayerSprites/Walk/WalkUp/", self.spritesMoveUp)
        loadSprites("Presets/PlayerSprites/Walk/WalkDown/", self.spritesMoveDown)
        loadSprites("Presets/PlayerSprites/Walk/WalkLeft/", self.spritesMoveLeft)
        loadSprites("Presets/PlayerSprites/Walk/WalkRight/", self.spritesMoveRight)
        # set the booleans by default to false
        self.movingUp = False
        self.movingDown = False
        self.movingLeft = False
        self.movingRight = False
        # variable that shows which is the current sprite that is being displayed
        self.currentSprite = 0
        # the displayed sprite on the screen for the player, by default set to move right
        self.image = self.spritesMoveRight[self.currentSprite]
        # rect of the image, to manipulate the player's sprite
        self.rect = self.image.get_rect()

    # function for the player update
    def Update(self):
        # check if the player can move
        if self.ableToMove:
            # change the pixel position based on the direction and the speed
            self.pixelPosition += self.direction * self.speed

        # setting the grid position in ref to the pixel position
        if self.timeToMove():
            # check if the stored position is not none
            if self.storedDirection is not None:
                # change the direction based on the stored position
                self.direction = self.storedDirection
            # set able to move based on the check in the canMove function
            self.ableToMove = self.canMove()

        # set the x grid position to the pixel position x - the padding and half of the cell width, i dont quite get how this works
        # but it works :D
        self.gridPosition[0] = (self.pixelPosition[
                                    0] - TOP_BOTTOM_PADDING + self.Game.cellWidth // 2) // self.Game.cellWidth + 1
        # same for the y
        self.gridPosition[1] = (self.pixelPosition[
                                    1] - TOP_BOTTOM_PADDING + self.Game.cellHeight // 2) // self.Game.cellHeight + 1

        # check on collision with a coin
        if self.onCoin():
            # collect the coin
            self.collectCoin()
            # remove the coin from the screen
            for coin in self.Game.coinsSprites:
                coin.update()

        # check on collision with a pick up
        if self.onPickUp():
            # collect the pickup
            self.collectPickUp()
            # remove the pick up from the screen
            for pickUp in self.Game.pickUpSprites:
                pickUp.update()

    # pygame sprite update
    def update(self):
        # check in which direction the player is going and play respectively the animation
        if self.movingUp:
            playWalkUp(self, self.animationSpeed)
        elif self.movingDown:
            playWalkDown(self, self.animationSpeed)
        elif self.movingLeft:
            playWalkLeft(self, self.animationSpeed)
        elif self.movingRight:
            playWalkRight(self, self.animationSpeed)

        # set the center of the sprite to the position of the player
        self.rect.center = (int(self.pixelPosition.x), int(self.pixelPosition.y))

    # the player draw function used to display the lives remaining
    def draw(self):
        self.update()
        # draw player lives
        for x in range(self.lives):
            pygame.draw.circle(self.Game.screen, PLAYER_COLOUR, (15 + 35 * x, HEIGHT - 15), 10)

    # function for on collision with a coin
    def onCoin(self):
        # if the position of the player matches a position in the coins list, means the player might be colliding with a coin
        if self.gridPosition in self.Game.coins:

            # checks for the x and y pixel position to make sure that the player is colliding with the coin, and if that's the case then return true
            if int(self.pixelPosition.x + TOP_BOTTOM_PADDING // 2) % self.Game.cellWidth == 0:
                if self.direction == Vector2(1, 0) or self.direction == Vector2(-1, 0):
                    return True

            if int(self.pixelPosition.y + TOP_BOTTOM_PADDING // 2) % self.Game.cellHeight == 0:
                if self.direction == Vector2(0, 1) or self.direction == Vector2(0, -1):
                    return True
        else:
            # else return false
            return False

    # function for the coin collection
    def collectCoin(self):
        # when the player collides with a coin, remove that coin from the list based on the position of the player
        self.Game.coins.remove(self.gridPosition)
        # increase the current score
        self.currentScore += 1
        # play the coin sound
        self.Game.CoinPrefab.sound.play()

    # function for the pick up collision
    def onPickUp(self):
        #  if the player's position is in the pickups list then it might be colliding with a pick up
        if self.gridPosition in self.Game.pickUps:
            # check if the player is colliding based on the x and y pixel position
            if int(self.pixelPosition.x + TOP_BOTTOM_PADDING // 2) % self.Game.cellWidth == 0:
                if self.direction == Vector2(1, 0) or self.direction == Vector2(-1, 0):
                    return True

            if int(self.pixelPosition.y + TOP_BOTTOM_PADDING // 2) % self.Game.cellHeight == 0:
                if self.direction == Vector2(0, 1) or self.direction == Vector2(0, -1):
                    return True
        else:
            return False

    # function for the collection of the pick up
    def collectPickUp(self):
        # remove the pickup based on the player's position
        self.Game.pickUps.remove(self.gridPosition)
        # increase the score
        self.currentScore += 5
        # play the pick up sound
        self.Game.PickUpPrefab.sound.play()

    # function that sets the stored direction to the passed direction
    def move(self, direction):
        self.storedDirection = direction

    # helper function that returns the pixel position of the player. I do not know what maths are happening here..
    def getPixelPosition(self):
        return Vector2((self.gridPosition.x * self.Game.cellWidth) + TOP_BOTTOM_PADDING // 2 + self.Game.cellWidth // 2,
                       (
                               self.gridPosition.y * self.Game.cellHeight) + TOP_BOTTOM_PADDING // 2 + self.Game.cellHeight // 2)

    # helper function, I have no idea what it really does
    def timeToMove(self):
        # checks if the player's direction is either left or right, or none and if that's the case returns true
        if int(self.pixelPosition.x + TOP_BOTTOM_PADDING // 2) % self.Game.cellWidth == 0:
            if self.direction == Vector2(1, 0) or self.direction == Vector2(-1, 0) or self.direction == Vector2(0, 0):
                return True

        # same for the y axis
        if int(self.pixelPosition.y + TOP_BOTTOM_PADDING // 2) % self.Game.cellHeight == 0:
            if self.direction == Vector2(0, 1) or self.direction == Vector2(0, -1) or self.direction == Vector2(0, 0):
                return True

    # function that checks if the player is colliding with a wall
    def canMove(self):
        for wall in self.Game.walls:
            if Vector2(self.gridPosition + self.direction) == wall:
                return False
        return True
