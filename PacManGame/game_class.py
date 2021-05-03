import sys
from settings import *
from player_class import *
from enemy_class import *

pygame.init()

position = pygame.math.Vector2


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "Start"
        self.cellWidth = MAZE_WIDTH // 28
        self.cellHeight = MAZE_HEIGHT // 30
        self.playerPosition = None
        self.walls = []
        self.coins = []
        self.enemies = []
        self.enemiesPosition = []
        self.loadLevel(self.walls, self.coins)
        self.player = Player(self, self.playerPosition)
        self.loadEnemies()

    def run(self):
        while self.running:
            if self.state == "Start":
                self.startEvents()
                self.startUpdate()
                self.startDraw()

            elif self.state == "Play":
                self.playEvents()
                self.playUpdate()
                self.playDraw()

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

    def loadLevel(self, walls, coins):
        self.background = pygame.image.load("background.png")
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))

        # reading walls file and writing the data into walls list
        with open("walls.txt", 'r') as file:
            for y, line in enumerate(file):
                for x, char in enumerate(line):
                    if char == "1":
                        walls.append(Vector2(x, y))
                    elif char == "C":
                        coins.append(Vector2(x, y))
                    elif char == "P":
                        self.playerPosition = Vector2(x, y)
                    elif char in ["2", "3", "4", "5"]:
                        self.enemiesPosition.append(Vector2(x, y))
                    elif char == "B":
                        pygame.draw.rect(self.background, BLACK, (x * self.cellWidth, y * self.cellHeight, self.cellWidth, self.cellHeight))

    def loadEnemies(self):
        for index, enemy in enumerate(self.enemiesPosition):
            self.enemies.append(Enemy(self, enemy, index))

    def drawGrid(self, walls, cellWidth, cellHeight):
        for x in range(WIDTH // self.cellWidth):
            pygame.draw.line(self.background, GRAY, (x * self.cellWidth, 0), (x * self.cellWidth, HEIGHT))

        for y in range(HEIGHT // self.cellHeight):
            pygame.draw.line(self.background, GRAY, (0, y * self.cellHeight), (WIDTH, y * self.cellHeight))

        for wall in walls:
            pygame.draw.rect(self.background, (255, 0, 0),
                             (wall.x * cellWidth, wall.y * cellHeight, cellWidth, cellHeight))

    def drawCoins(self, surface, coins, cellWidth, cellHeight):
        for coin in coins:
            pygame.draw.circle(surface, RED, (int(coin.x * cellWidth) + cellWidth // 2 + TOP_BOTTOM_PADDING // 2,
                                              int(coin.y * cellHeight) + cellHeight // 2 + TOP_BOTTOM_PADDING // 2), 5)

    ##################################### START FUNCTIONS ##################################################################

    def startEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = "Play"
                # pygame.image.save(self.screen, "Test.png")

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

                if event.key == pygame.K_RIGHT:
                    self.player.move(Vector2(1, 0))

                if event.key == pygame.K_UP:
                    self.player.move(Vector2(0, -1))

                if event.key == pygame.K_DOWN:
                    self.player.move(Vector2(0, 1))

    def playUpdate(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()

    def playDraw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BOTTOM_PADDING // 2, TOP_BOTTOM_PADDING // 2))
        self.drawCoins(self.screen, self.coins, self.cellWidth, self.cellHeight)
        # self.drawGrid(self.coins, self.cellWidth, self.cellHeight)
        self.drawText("CURRENT SCORE: {}".format(self.player.currentScore), self.screen, (5, 0), 16, WHITE,
                      START_TEXT_FONT)
        self.drawText("HIGH SCORE: 0", self.screen, (WIDTH / 1.4, 0), 16, WHITE, START_TEXT_FONT)
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()
