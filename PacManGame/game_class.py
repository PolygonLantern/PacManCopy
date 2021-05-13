import sys
from settings import *
from player_class import *
from enemy_class import *
from pygame import mixer

pygame.init()


class PickUp(pygame.sprite.Sprite):
    def __init__(self, game, positionX, positionY, pickUpSprite):
        super().__init__()
        self.Game = game
        self.image = pygame.image.load(pickUpSprite)
        self.rect = self.image.get_rect()
        self.rect.center = [positionX, positionY]
        self.sound = mixer.Sound("Presets/PickUpSound.wav")

    def update(self):
        if pygame.sprite.collide_rect_ratio(.3)(self.Game.player, self):
            self.kill()


class Coin(pygame.sprite.Sprite):
    def __init__(self, game, positionX, positionY, coinSprite):
        super().__init__()
        self.Game = game
        self.image = pygame.image.load(coinSprite)
        self.rect = self.image.get_rect()
        self.rect.center = [positionX, positionY]
        self.sound = mixer.Sound("Presets/CoinSound.wav")

    def update(self):
        if pygame.sprite.collide_rect_ratio(.3)(self.Game.player, self):
            self.kill()
        """"
        if pygame.sprite.spritecollide(self.Game.player, self.Game.allSpritesGroup, True,
                                       pygame.sprite.collide_rect_ratio(.3)):
            self.kill()
"""

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "Start"
        self.cellWidth = CELL_WIDTH
        self.cellHeight = CELL_HEIGHT
        self.playerPosition = None
        self.walls = []
        self.coins = []
        self.coinsSprites = []
        self.enemies = []
        self.enemiesPosition = []
        self.pickUps = []
        self.pickUpSprites = []
        self.loadLevel()
        self.player = Player(self, Vector2(self.playerPosition), "Presets/Player.png")
        self.loadEnemies()
        self.allSpritesGroup = pygame.sprite.Group()
        self.playerSpriteGroup = pygame.sprite.Group()
        self.enemySpriteGroup = pygame.sprite.Group()
        self.coinsGroup = pygame.sprite.Group()
        self.pickUpsGroup = pygame.sprite.Group()
        self.highScore = 0
        self.restartedLevel = False
        self.CoinPrefab = Coin(self, -100, 0, "Presets/CoinSprite.png")
        self.PickUpPrefab = PickUp(self, -100, 0, "Presets/PickUp.png")

    def run(self):
        mixer.music.load("Presets/BackgroundMusic.flac")
        mixer.music.play(-1)
        self.highScore = self.readHighScore()
        self.drawCoins()
        self.drawPickUps()
        while self.running:
            if self.state == "Start":
                self.startEvents()
                self.startUpdate()
                self.startDraw()

            elif self.state == "Play":
                self.playEvents()
                self.playUpdate()
                self.playDraw()

            elif self.state == "Game Over":
                self.GOEvents()
                self.GOUpdate()
                self.GODraw()
            else:
                self.running = False

            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    ##################################### HELPER FUNCTIONS #################################################################

    def drawText(self, _text, screen, _position, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(_text, False, colour)
        textSize = text.get_size()
        if centered:
            _position[0] = _position[0] - textSize[0] // 2
            _position[1] = _position[1] - textSize[1] // 2

        screen.blit(text, _position)

    def loadLevel(self):
        self.background = pygame.image.load("Presets/background.png")
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))

        # reading walls file and writing the data into walls list
        with open("Presets/Files/walls.txt", 'r') as file:
            for y, line in enumerate(file):
                for x, char in enumerate(line):
                    if char == "1":
                        self.walls.append(Vector2(x, y))
                    elif char == "C":
                        self.coins.append(Vector2(x, y))
                    elif char == "P":
                        self.playerPosition = [x, y]
                    elif char == "U":
                        self.pickUps.append([x, y])
                    elif char in ["3", "4", "5"]:
                        self.enemiesPosition.append([x, y])
                    elif char == "B":
                        pygame.draw.rect(self.background, BLACK,
                                         (x * self.cellWidth, y * self.cellHeight, self.cellWidth, self.cellHeight))

    def loadEnemies(self):
        for index, enemy in enumerate(self.enemiesPosition):
            self.enemies.append(Enemy(self, Vector2(enemy), index))

    def drawGrid(self, walls, cellWidth, cellHeight):
        for x in range(WIDTH // self.cellWidth):
            pygame.draw.line(self.background, GRAY, (x * self.cellWidth, 0), (x * self.cellWidth, HEIGHT))

        for y in range(HEIGHT // self.cellHeight):
            pygame.draw.line(self.background, GRAY, (0, y * self.cellHeight), (WIDTH, y * self.cellHeight))

        for wall in walls:
            pygame.draw.rect(self.background, (255, 0, 0),
                             (wall.x * cellWidth, wall.y * cellHeight, cellWidth, cellHeight))

    def drawCoins(self):
        for coin in self.coins:
            self.coinsSprites.append(
                Coin(self, int(coin.x * self.cellWidth) + self.cellWidth // 2 + TOP_BOTTOM_PADDING // 2,
                     int(coin.y * self.cellHeight) + self.cellHeight // 2 + TOP_BOTTOM_PADDING // 2, "Presets/CoinSprite.png"))

        for coinSprite in self.coinsSprites:
            self.allSpritesGroup.add(coinSprite)

    def drawPickUps(self):
        for pickUp in self.pickUps:
            self.pickUpSprites.append(
                PickUp(self, int(pickUp[0] * self.cellWidth) + self.cellWidth // 2 + TOP_BOTTOM_PADDING // 2,
                       int(pickUp[1] * self.cellHeight) + self.cellHeight // 2 + TOP_BOTTOM_PADDING // 2,
                       "Presets/PickUp.png"))

        for pickUpSprite in self.pickUpSprites:
            self.allSpritesGroup.add(pickUpSprite)

    def reset(self):
        self.player.lives = 3
        self.player.currentScore = 0
        self.player.gridPosition = Vector2(self.player.startPosition)
        self.player.pixelPosition = self.player.getPixelPosition()
        self.player.direction *= 0
        self.coins = []
        self.coinsSprites = []
        self.pickUps = []
        self.pickUpSprites = []
        self.allSpritesGroup = pygame.sprite.Group()
        with open("Presets/Files/walls.txt", 'r') as file:
            for y, line in enumerate(file):
                for x, char in enumerate(line):
                    if char == "C":
                        self.coins.append(Vector2(x, y))
                    elif char == "U":
                        self.pickUps.append([x, y])
        self.state = "Play"
        self.highScore = self.readHighScore()
        self.drawCoins()
        self.drawPickUps()


    def saveHighScore(self, highScore):
        file = open("Presets/Files/hs.txt", "w")
        file.write(str(highScore))
        file.close()

    def readHighScore(self):
        file = open("Presets/Files/hs.txt", "r")
        return int(file.readline())

    ##################################### START FUNCTIONS ##################################################################

    def startEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = "Play"

    def startUpdate(self):
        pass

    def startDraw(self):
        self.screen.fill(BLACK)
        self.drawText("Press Space to Start", self.screen, [WIDTH // 2, HEIGHT // 2 - 50], START_TEXT_SIZE,
                      (170, 132, 58),
                      START_TEXT_FONT, centered=True)
        self.drawText("1 Player Only", self.screen, [WIDTH // 2, HEIGHT // 2 + 50], START_TEXT_SIZE, (32, 150, 79),
                      START_TEXT_FONT, centered=True)
        self.drawText("HIGH SCORE", self.screen, [3, 5], START_TEXT_SIZE, WHITE,
                      START_TEXT_FONT)

        pygame.display.update()

    ##################################### PLAY FUNCTIONS #################################################################

    def playEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
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

    def playUpdate(self):
        self.player.Update()
        for enemy in self.enemies:
            enemy.Update()
            if enemy.gridPosition == self.player.gridPosition:
                self.playerLoseLife()

    def playerLoseLife(self):
        self.player.lives -= 1
        bestHighScore = self.readHighScore()
        if self.player.lives == 0:
            self.state = "Game Over"
            if self.player.currentScore >= bestHighScore:
                self.saveHighScore(self.player.currentScore)
        else:
            self.player.gridPosition = Vector2(self.player.startPosition)
            self.player.pixelPosition = self.player.getPixelPosition()
            self.player.direction *= 0
            for enemy in self.enemies:
                enemy.gridPosition = Vector2(enemy.startingPosition)
                enemy.pixelPosition = enemy.getPixelPosition()
                enemy.direction *= 0

    def playDraw(self):
        self.screen.fill(BLACK)
        for enemy in self.enemies:
            enemy.draw()
            self.enemySpriteGroup.add(enemy)

        self.playerSpriteGroup.add(self.player)
        self.screen.blit(self.background, (TOP_BOTTOM_PADDING // 2, TOP_BOTTOM_PADDING // 2))
        self.coinsGroup.draw(self.screen)
        self.pickUpsGroup.draw(self.screen)
        self.allSpritesGroup.draw(self.screen)
        self.enemySpriteGroup.draw(self.screen)
        self.playerSpriteGroup.draw(self.screen)

        self.drawText("CURRENT SCORE: {}".format(self.player.currentScore), self.screen, (5, 0), 16, WHITE,
                      START_TEXT_FONT)
        self.drawText("HIGH SCORE: {}".format(self.highScore), self.screen, (WIDTH / 1.4, 0), 16, WHITE,
                      START_TEXT_FONT)
        self.player.draw()

        pygame.display.update()

    ##################################### Game Over  FUNCTIONS #################################################################

    def GOEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def GOUpdate(self):
        pass

    def GODraw(self):
        self.screen.fill(BLACK)
        quitText = "Press the escape button to QUIT"
        retryText = "Press SPACE bar to PLAY AGAIN"
        self.drawText("GAME OVER", self.screen, [WIDTH // 2, 100], 25, RED, START_TEXT_FONT, centered=True)
        self.drawText(retryText, self.screen, [
            WIDTH // 2, HEIGHT // 2], 25, (190, 190, 190), START_TEXT_FONT, centered=True)
        self.drawText(quitText, self.screen, [
            WIDTH // 2, HEIGHT // 1.5], 25, (190, 190, 190), START_TEXT_FONT, centered=True)
        pygame.display.update()
