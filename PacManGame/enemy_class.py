import random
from settings import *
from Utilities import *

Vector2 = pygame.math.Vector2


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, position, enemyNumber):
        super().__init__()
        self.Game = game
        self.gridPosition = position
        self.startingPosition = [position.x, position.y]
        self.pixelPosition = self.getPixelPosition()
        self.radius = 10
        self.number = enemyNumber
        self.colour = self.setColour()
        self.personality = self.setPersonality()
        self.direction = Vector2(0, 0)
        self.target = None
        self.speed = self.setSpeed()
        self.spritesMoveUp = []
        self.spritesMoveRight = []
        self.spritesMoveLeft = []
        self.spritesMoveDown = []
        self.animationSpeed = .3
        loadSprites("Presets/EnemySprites/Walk/WalkUp/", self.spritesMoveUp)
        loadSprites("Presets/EnemySprites/Walk/WalkDown/", self.spritesMoveDown)
        loadSprites("Presets/EnemySprites/Walk/WalkRight/", self.spritesMoveRight)
        loadSprites("Presets/EnemySprites/Walk/WalkLeft/", self.spritesMoveLeft)
        self.movingUp = False
        self.movingDown = False
        self.movingLeft = False
        self.movingRight = False
        self.currentSprite = 0
        self.image = self.spritesMoveLeft[self.currentSprite]
        self.rect = self.image.get_rect()

    def Update(self):
        self.target = self.setTarget()
        if self.target != self.gridPosition:
            self.pixelPosition += self.direction * self.speed
            if self.timeToMove():
                self.move()

        # Set grid position
        self.gridPosition[0] = (self.pixelPosition[
                                    0] - TOP_BOTTOM_PADDING + self.Game.cellWidth // 2) // self.Game.cellWidth + 1
        self.gridPosition[1] = (self.pixelPosition[
                                    1] - TOP_BOTTOM_PADDING + self.Game.cellHeight // 2) // self.Game.cellHeight + 1

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

    def getPixelPosition(self):
        return Vector2((self.gridPosition.x * self.Game.cellWidth) + TOP_BOTTOM_PADDING // 2 + self.Game.cellWidth // 2,
                       (
                               self.gridPosition.y * self.Game.cellHeight) + TOP_BOTTOM_PADDING // 2 + self.Game.cellHeight // 2)

    def timeToMove(self):
        if int(self.pixelPosition.x + TOP_BOTTOM_PADDING // 2) % self.Game.cellWidth == 0:
            if self.direction == Vector2(1, 0) or self.direction == Vector2(-1, 0) or self.direction == Vector2(0, 0):
                return True

        if int(self.pixelPosition.y + TOP_BOTTOM_PADDING // 2) % self.Game.cellHeight == 0:
            if self.direction == Vector2(0, 1) or self.direction == Vector2(0, -1) or self.direction == Vector2(0, 0):
                return True
        return False

    def setTarget(self):
        if self.personality == "Speedy" or self.personality == "Slow":
            if self.Game.player.gridPosition[0] > CELL_WIDTH // 2 and self.Game.player.gridPosition[
                1] > CELL_HEIGHT // 2:
                animationBool(self, True, False, False, False)

            if self.Game.player.gridPosition[0] > CELL_WIDTH // 2 and self.Game.player.gridPosition[
                1] < CELL_HEIGHT // 2:
                animationBool(self, False, False, False, True)

            if self.Game.player.gridPosition[0] < CELL_WIDTH // 2 and self.Game.player.gridPosition[
                1] > CELL_HEIGHT // 2:
                animationBool(self, False, False, True, False)

            else:
                animationBool(self, False, True, False, False)

            return self.Game.player.gridPosition
        else:
            if self.Game.player.gridPosition[0] > CELL_WIDTH // 2 and self.Game.player.gridPosition[
                1] > CELL_HEIGHT // 2:
                animationBool(self, False, True, False, False)
                return Vector2(1, 1)

            if self.Game.player.gridPosition[0] > CELL_WIDTH // 2 and self.Game.player.gridPosition[
                1] < CELL_HEIGHT // 2:
                animationBool(self, False, False, True, False)
                return Vector2(1, CELL_HEIGHT - 2)

            if self.Game.player.gridPosition[0] < CELL_WIDTH // 2 and self.Game.player.gridPosition[
                1] > CELL_HEIGHT // 2:
                animationBool(self, False, False, False, True)
                return Vector2(CELL_WIDTH - 2, 1)

            else:
                animationBool(self, True, False, False, False)
                return Vector2(CELL_WIDTH - 2, CELL_HEIGHT - 2)

    def move(self):
        if self.personality == "Speedy":
            self.direction = self.getPathDirection(self.target)

        if self.personality == "Random":
            self.direction = self.getRandomDirection()

        if self.personality == "Scared":
            self.direction = self.getPathDirection(self.target)

        if self.personality == "Slow":
            self.direction = self.getPathDirection(self.target)

    def setSpeed(self):
        if self.personality in ["Speedy", "Scared"]:
            speed = 2
        else:
            speed = 1

        return speed

    def getPathDirection(self, target):
        nextCell = self.findNextCellInPath(target)
        xDirection = nextCell[0] - self.gridPosition[0]
        yDirection = nextCell[1] - self.gridPosition[1]

        return Vector2(xDirection, yDirection)

    def findNextCellInPath(self, target):
        path = self.BFS([int(self.gridPosition.x), int(self.gridPosition.y)], [
            int(target[0]), int(target[1])])
        return path[1]

    def BFS(self, start, target):
        grid = [[0 for x in range(28)] for x in range(30)]
        for cell in self.Game.walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1
        queue = [start]
        path = []
        visited = []
        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target:
                break
            else:
                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for neighbour in neighbours:
                    if neighbour[0] + current[0] >= 0 and neighbour[0] + current[0] < len(grid[0]):
                        if neighbour[1] + current[1] >= 0 and neighbour[1] + current[1] < len(grid):
                            nextCell = [neighbour[0] + current[0], neighbour[1] + current[1]]
                            if nextCell not in visited:
                                if grid[nextCell[1]][nextCell[0]] != 1:
                                    queue.append(nextCell)
                                    path.append({"Current": current, "Next": nextCell})
        shortest = [target]
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"])
        return shortest

    def getRandomDirection(self):
        while True:
            number = random.randint(-2, 2)
            if number == -2:
                xDirection, yDirection = 1, 0
                animationBool(self, True, False, False, False)

            elif number == -1:
                xDirection, yDirection = 0, 1
                animationBool(self, False, True, False, False)

            elif number == 0:
                xDirection, yDirection = -1, 0
                animationBool(self, False, False, True, False)

            else:
                xDirection, yDirection = 0, -1
                animationBool(self, False, False, False, True)

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

