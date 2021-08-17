import sys
from player_class import *
from enemy_class import *
from pygame import mixer

# Initialising pygame
pygame.init()


# Class for the pick Ups in the game
# The class inherits from the pygame sprite class


class PickUp(pygame.sprite.Sprite):
    # the constructor of the class, passing the game class, the x and y position of the object and path to the representing sprite
    def __init__(self, game, positionX, positionY, pickUpSprite):
        # inheriting the methods from the parent class
        super().__init__()
        # Class variables
        # Game is for the main game class that holds the information for the player and all the lists that this class cares about
        self.Game = game
        # image loads the sprite that is passed in the constructor
        self.image = pygame.image.load(pickUpSprite)
        # rect creates a rectangle around the sprite to allow movement and manipulation of the sprite
        self.rect = self.image.get_rect()
        # rect center, centers the sprite to the passed coordinates
        self.rect.center = [positionX, positionY]
        # sound is the sound effect for when the player collects the object
        self.sound = mixer.Sound("Presets/SoundFX/PickUpSound.wav")

    # update is function that is called on every sprite every second

    def update(self):
        # check if the player is colliding with the pick up object and if so, delete the object
        if pygame.sprite.collide_rect_ratio(.3)(self.Game.player, self):
            self.kill()


class Coin(pygame.sprite.Sprite):
    # the constructor of the class, passing the game class, the x and y position of the object and path to the representing sprite
    def __init__(self, game, positionX, positionY, coinSprite):
        # inheriting the methods from the parent class
        super().__init__()
        # Class variables
        # Game is for the main game class that holds the information for the player and all the lists that this class cares about
        self.Game = game
        # image loads the sprite that is passed in the constructor
        self.image = pygame.image.load(coinSprite)
        # rect creates a rectangle around the sprite to allow movement and manipulation of the sprite
        self.rect = self.image.get_rect()
        # rect center, centers the sprite to the passed coordinates
        self.rect.center = [positionX, positionY]
        # sound is the sound effect for when the player collects the object
        self.sound = mixer.Sound("Presets/SoundFX/CoinSound.wav")

    # update is function that is called on every sprite every second

    def update(self):
        # check if the player is colliding with the pick up object and if so, delete the object
        if pygame.sprite.collide_rect_ratio(.3)(self.Game.player, self):
            self.kill()


# Main game class

class Game:
    def __init__(self):
        # set the screen size
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        #set the title of the window
        self.title = pygame.display.set_caption("Dungeon Runaway")
        #set the icon
        self.iconImage = pygame.image.load("Presets/PlayerSprites/Walk/WalkRight/tile_5.png")
        self.icon = pygame.display.set_icon(self.iconImage)
        # set up a clock to control the frames showed per second
        self.clock = pygame.time.Clock()
        # running is a state variable that makes the game run until is not false
        self.running = True
        # game state variable that keeps the current state of the game, this is used to trigger Game Over screen and Main Menu screen
        self.state = "Start"
        # set the game grid's cell width and height to the preset in the settings class
        self.cellWidth = CELL_WIDTH
        self.cellHeight = CELL_HEIGHT
        # set the player position
        self.playerPosition = None
        # list that will hold the position of all the walls
        self.walls = []
        # list that will hold the position of all coins
        self.coins = []
        # list for the coins' sprites
        self.coinsSprites = []
        # list for all the enemies
        self.enemies = []
        # list that will hold all the positions of the enemies
        self.enemiesPosition = []
        # list for the pick ups positions
        self.pickUps = []
        # list for the pick ups' sprites
        self.pickUpSprites = []
        # execute the load level function, that read from the wall.txt file and loads the data
        self.loadLevel()
        # variable that will hold the initially spawned loot number
        self.spawnedLoot = len(self.coins)
        # create an instance of the player and passing the position
        self.player = Player(self, Vector2(self.playerPosition))
        # load the enemies
        self.loadEnemies()
        # create a group for all the sprites in the game. This is not used for all of them but instead only for the collectibles
        self.allSpritesGroup = pygame.sprite.Group()
        # group for the player sprites
        self.playerSpriteGroup = pygame.sprite.Group()
        # group for the enemy sprites
        self.enemySpriteGroup = pygame.sprite.Group()
        # separate group for the collectibles sprites
        self.coinsGroup = pygame.sprite.Group()
        self.pickUpsGroup = pygame.sprite.Group()
        # list of the background sound files, just for ease than having to browse through the code
        self.backgroundMusic = ["Presets/Music/BackgroundMusic.flac", "Presets/Music/beatsMe.wav", "Presets/Music/BackgroundMusic1.wav", "Presets/Music/BackgroundMusic2.mp3", "Presets/Music/BackgroundMusic3.mp3"]
        # event for when a song end
        self.SONG_END = pygame.USEREVENT + 1
        # subscribe to the event
        mixer.music.set_endevent(self.SONG_END)
        # load the game over sound
        self.gameOverSound = mixer.Sound("Presets/SoundFX/GameOver.wav")
        # highscore variable
        self.highScore = 0
        # 2 prefabs of the collectibles, used mainly to play the sound after they are picked up by the player.
        self.CoinPrefab = Coin(self, -100, 0, "Presets/CoinSprite.png")
        self.PickUpPrefab = PickUp(self, -100, 0, "Presets/SpeedPickUp.png")
        # load the first song and play it
        mixer.music.load(self.backgroundMusic[1])
        mixer.music.play()
    # function that makes the game loop
        self.currentlyPlayingSong = None

    def run(self):
        # set the highscore to the number that is written in the hs.txt file
        self.highScore = self.readHighScore()
        # draw the collectibles sprites
        self.drawCoins()
        self.drawPickUps()
        #self.queueMusic()
        # Game loop
        # check for the running variable
        while self.running:
            # check for the state of the game, by default its start
            if self.state == "Start":
                # run all the start state functions
                # every state has 3 functions
                # Events, Update and Draw
                # Events is for the input that is given to pygame
                self.startEvents()
                # Update is for the logic that is running on the background
                self.startUpdate()
                # Draw is displaying everything that is meant to be shown
                self.startDraw()

            elif self.state == "Play":
                self.playEvents()
                self.playUpdate()
                self.playDraw()

            elif self.state == "Level Cleared":
                self.LCEvents()
                self.LCUpdate()
                self.LCDraw()

            elif self.state == "Game Over":
                self.GOEvents()
                self.GOUpdate()
                self.GODraw()
            else:
                # if its none of the states above, stop the game
                self.running = False
            # clock sets the framerate of the game
            self.clock.tick(FPS)
        # close the game and the window
        pygame.quit()
        sys.exit()

    ##################################### HELPER FUNCTIONS #################################################################

    # function that displays text on the screen
    def drawText(self, _text, screen, _position, size, colour, font_name, centered=False):
        # set the font to the passed font
        font = pygame.font.SysFont(font_name, size)
        # set the text to the passed text
        text = font.render(_text, False, colour)
        # set the size of the text
        textSize = text.get_size()

        # position the text if specified
        if centered:
            _position[0] = _position[0] - textSize[0] // 2
            _position[1] = _position[1] - textSize[1] // 2

        # Display the text on the screen
        screen.blit(text, _position)

    # function that reads from the walls.txt and loads the passed data

    def loadLevel(self):
        # set the background image
        self.background = pygame.image.load("Presets/background.png")
        # scale the image based on the screen's width and height
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))

        # reading walls file and writing the data into walls list
        with open("Presets/Files/walls.txt", 'r') as file:
            for y, line in enumerate(file):
                for x, char in enumerate(line):
                    # appends a Vector2 to the walls list with the position of the wall
                    if char == "1":
                        self.walls.append(Vector2(x, y))
                    # appends a Vector2 to the coins list with the position of the coins
                    elif char == "C":
                        self.coins.append(Vector2(x, y))
                    # sets the player's position to the coordinates
                    elif char == "P":
                        self.playerPosition = [x, y]
                    # appends a Vector2 to the pick ups list with the position of the pickup
                    elif char == "U":
                        self.pickUps.append(Vector2(x, y))
                    # appends the position of the enemies to the enemiesPosition list
                    elif char in ["2", "3", "4", "5"]:
                        self.enemiesPosition.append([x, y])
                    # visually representing the entrance of the enemy's spawn else it does not makes sense
                    elif char == "B":
                        pygame.draw.rect(self.background, BLACK,
                                         (x * self.cellWidth, y * self.cellHeight, self.cellWidth, self.cellHeight))

    # Function that loads enemies based on what the loadLevel() has written in the enemiesPosition list

    def loadEnemies(self):
        for index, enemy in enumerate(self.enemiesPosition):
            self.enemies.append(Enemy(self, Vector2(enemy), index))

    # Function that adds coin sprite object to the coinsSprites list and then adds all of the objects to the allSpritesGroup to be displayed

    def drawCoins(self):
        for coin in self.coins:
            self.coinsSprites.append(
                Coin(self, int(coin.x * self.cellWidth) + self.cellWidth // 2 + TOP_BOTTOM_PADDING // 2,
                     int(coin.y * self.cellHeight) + self.cellHeight // 2 + TOP_BOTTOM_PADDING // 2,
                     "Presets/CoinSprite.png"))

        for coinSprite in self.coinsSprites:
            self.allSpritesGroup.add(coinSprite)

    # Function that adds pickUp sprite object to the pickUpsSprites list and then adds all of the objects to the allSpritesGroup to be displayed

    def drawPickUps(self):
        for pickUp in self.pickUps:
            self.pickUpSprites.append(
                PickUp(self, int(pickUp.x * self.cellWidth) + self.cellWidth // 2 + TOP_BOTTOM_PADDING // 2,
                       int(pickUp.y * self.cellHeight) + self.cellHeight // 2 + TOP_BOTTOM_PADDING // 2,
                       "Presets/SpeedPickUp.png"))

        for pickUpSprite in self.pickUpSprites:
            self.allSpritesGroup.add(pickUpSprite)

    # Reset function for when the game ends and the player wants to restart the game.

    def reset(self, resetScore=True, resetLives=True, resetCollectedLoot=True):
        # reset the amount of collected loot if the player dies
        if resetCollectedLoot:
            self.player.collectedLoot = 0
        # set the lives back to 3
        if resetLives:
            self.player.lives = 3
        # reset the score
        if resetScore:
            self.player.currentScore = 0
        # return the player to the starting position
        self.player.gridPosition = Vector2(self.player.startPosition)
        self.player.pixelPosition = self.player.getPixelPosition()
        # set the direction of the player to 0,0 so it does not move in any direction
        self.player.direction *= 0
        # empty the collectibles lists
        self.coins = []
        self.coinsSprites = []
        self.pickUps = []
        self.pickUpSprites = []
        # reset the allSpritesGroup
        self.allSpritesGroup = pygame.sprite.Group()
        # When reset, fill the lists once again from the file
        with open("Presets/Files/walls.txt", 'r') as file:
            for y, line in enumerate(file):
                for x, char in enumerate(line):
                    if char == "C":
                        self.coins.append(Vector2(x, y))
                    elif char == "U":
                        self.pickUps.append(Vector2(x, y))

        # change the state to play
        self.state = "Play"
        # change the highscore if the player has managed to beat the last given
        self.highScore = self.readHighScore()
        # draw the collectibles
        self.drawCoins()
        self.drawPickUps()

    # write to a file the last currentScore
    def saveHighScore(self, highScore):
        file = open("Presets/Files/hs.txt", "w")
        file.write(str(highScore))
        file.close()

    # Read from the file with the highscore

    def readHighScore(self):
        file = open("Presets/Files/hs.txt", "r")
        return int(file.readline())

    def queueMusic(self):
        nextSong = random.choice(self.backgroundMusic)
        while nextSong == self.currentlyPlayingSong:
            nextSong = random.choice(self.backgroundMusic)
        self.currentlyPlayingSong = nextSong
        mixer.music.load(nextSong)
        mixer.music.play()

    ##################################### START FUNCTIONS ##################################################################
    # start events as explained above, contain the input that is passed to the game

    def startEvents(self):

        for event in pygame.event.get():
            if event.type == self.SONG_END:
                self.queueMusic()

            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # if space was pressed, change the state to play
                self.state = "Play"

    # this function is empty because there are none animations or anything that requires updating while on the main menu

    def startUpdate(self):
        pass

    # Draw function

    def startDraw(self):
        # draw the whole window's screen black
        self.screen.fill(BLACK)
        # use the drawText function and display the text
        self.drawText("Press Space to Start", self.screen, [WIDTH // 2, HEIGHT // 2 - 50], START_TEXT_SIZE,
                      (170, 132, 58),
                      START_TEXT_FONT, centered=True)
        self.drawText("1 Player Only", self.screen, [WIDTH // 2, HEIGHT // 2 + 50], START_TEXT_SIZE, (32, 150, 79),
                      START_TEXT_FONT, centered=True)
        self.drawText("HIGH SCORE", self.screen, [3, 5], START_TEXT_SIZE, WHITE,
                      START_TEXT_FONT)

        # update the display
        pygame.display.update()

    ##################################### PLAY FUNCTIONS #################################################################
    # Play events, function that listens to the input that the player gives.

    def playEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

                # if the player inputs any of the arrows, the direction of the player changes and so does the animation
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(Vector2(-1, 0))
                    animationBool(self.player, False, False, True, False)

                if event.key == pygame.K_RIGHT:
                    self.player.move(Vector2(1, 0))
                    animationBool(self.player, False, False, False, True)

                if event.key == pygame.K_UP:
                    self.player.move(Vector2(0, -1))
                    animationBool(self.player, True, False, False, False)

                if event.key == pygame.K_DOWN:
                    self.player.move(Vector2(0, 1))
                    animationBool(self.player, False, True, False, False)
            if event.type == self.SONG_END:
                print(f"gay")
                self.queueMusic()

    # Update runs again every second.

    def playUpdate(self):
                # run the player update function
        if not pygame.mixer.get_busy():
            mixer.music.unpause()
        self.player.Update()
        # run all the enemies update functions
        for enemy in self.enemies:
            enemy.Update()
            # if enemy collides with the player, the player loses life
            if enemy.gridPosition == self.player.gridPosition:
                self.playerLoseLife()

        if self.player.collectedLoot >= self.spawnedLoot:
            self.state = "Level Cleared"
            self.player.collectedLoot = 0

    # Function that decreases the life of the player.
    def playerLoseLife(self):
        # reduce the life
        mixer.music.pause()
        self.player.deathSound.play()

        self.player.lives -= 1
        # read again if the player has managed to beat the highscore and store it for a later check
        bestHighScore = self.readHighScore()
        # if the player's life reach 0 change the state to game over
        if self.player.lives == 0:
            self.state = "Game Over"
            self.gameOverSound.play()
            # if the current score of the player is better than the best highscore
            if self.player.currentScore >= bestHighScore:
                # update the highscore in case the player decides to reset the game
                self.saveHighScore(self.player.currentScore)

        else:
            # if however the player has more lives, reset the position
            self.player.gridPosition = Vector2(self.player.startPosition)
            self.player.pixelPosition = self.player.getPixelPosition()
            # change the direction to 0, 0
            self.player.direction *= 0
            # reset the position of the enemies
            for enemy in self.enemies:
                enemy.gridPosition = Vector2(enemy.startingPosition)
                enemy.pixelPosition = enemy.getPixelPosition()
                enemy.direction *= 0

    # Draw function

    def playDraw(self):
        # make the whole screen black
        self.screen.fill(BLACK)

        # draw all the enemies and add them to their respective spriteGroup
        for enemy in self.enemies:
            enemy.update()
            self.enemySpriteGroup.add(enemy)

        # add the player to the playerSpriteGroup
        self.playerSpriteGroup.add(self.player)
        # display the padding on the screen
        self.screen.blit(self.background, (TOP_BOTTOM_PADDING // 2, TOP_BOTTOM_PADDING // 2))
        # draw all the coins
        self.coinsGroup.draw(self.screen)
        # draw all the pick ups
        self.pickUpsGroup.draw(self.screen)
        # draw all the sprites in the group, not sure entirely why do I need to draw them separately and then all together but it works so I am not going to change it
        self.allSpritesGroup.draw(self.screen)
        # draw all the enemies
        self.enemySpriteGroup.draw(self.screen)
        # draw the player
        self.playerSpriteGroup.draw(self.screen)

        # draw the text to show the current and best highscore
        self.drawText("CURRENT SCORE: {}".format(self.player.currentScore), self.screen, (5, 0), 16, WHITE,
                      START_TEXT_FONT)
        self.drawText("HIGH SCORE: {}".format(self.highScore), self.screen, (WIDTH / 1.4, 0), 16, WHITE,
                      START_TEXT_FONT)
        self.player.draw()

        # update the screen
        pygame.display.update()

    ##################################### Game Over  FUNCTIONS #################################################################
    # Events for the game over screen

    def GOEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # if the player presses space, reset the game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            # if the playe presses the escape, quit the game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def GOUpdate(self):
        pass

    # Game over draw

    def GODraw(self):
        # make the screen black
        self.screen.fill(BLACK)
        # two variables for the text to make it easier to track down in case of possible typos
        quitText = "Press the escape button to QUIT"
        retryText = "Press SPACE bar to PLAY AGAIN"
        # Display the text on the screen
        self.drawText("GAME OVER", self.screen, [WIDTH // 2, 100], 25, RED, START_TEXT_FONT, centered=True)
        self.drawText(retryText, self.screen, [
            WIDTH // 2, HEIGHT // 2], 25, (190, 190, 190), START_TEXT_FONT, centered=True)
        self.drawText(quitText, self.screen, [
            WIDTH // 2, HEIGHT // 1.5], 25, (190, 190, 190), START_TEXT_FONT, centered=True)
        # update the screen
        pygame.display.update()

    ##################################### Level Cleared FUNCTIONS #################################################################

    def LCEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset(False, False, False)

    def LCUpdate(self):
        pass

    def LCDraw(self):
        self.screen.fill(BLACK)
        # two variables for the text to make it easier to track down in case of possible typos
        congratsText = "Congratulations!"
        additionalCongratsText = "You cleared the dungeon without getting caught!"
        evenMoreCongratsText = "You are a true goblin!"
        retryText = "Press Space to continue "
        # Display the text on the screen
        self.drawText("Level Cleared", self.screen, [WIDTH // 2, 100], 25, RED, START_TEXT_FONT, centered=True)
        self.drawText(congratsText, self.screen, [
            WIDTH // 2, HEIGHT // 3], 20, (190, 190, 190), START_TEXT_FONT, centered=True)
        self.drawText(additionalCongratsText, self.screen, [
            WIDTH // 2, HEIGHT // 2.5], 20, (190, 190, 190), START_TEXT_FONT, centered=True)
        self.drawText(evenMoreCongratsText, self.screen, [
            WIDTH // 2, HEIGHT // 2], 20, (190, 190, 190), START_TEXT_FONT, centered=True)

        self.drawText(retryText, self.screen, [
            WIDTH // 2, HEIGHT // 1.5], 25, (190, 190, 190), START_TEXT_FONT, centered=True)
        # update the screen
        pygame.display.update()
