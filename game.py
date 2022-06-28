import pygame
import random

pygame.init()
curentTime = 0
clock = pygame.time.Clock()

GAMELENGTH = 600
GAMEWIDTH = 300
LENGTH = 650 # vertical
WIDTH = 500 # horizontal
BLOCKWIDTH = 30
startValue_y = (LENGTH - GAMELENGTH) // 2
startValue_x = startValue_y

WIN = pygame.display.set_mode((WIDTH, LENGTH))
pygame.display.set_caption("TETRIS")

# COLORS

BACKGROUND = (139,125,107)          # For Background
ORANGE = (255,97,3)             #for game bocks    
PARROTGREEN = (102,205,0)       #for game bocks
SKYBLUE = (152,245,255)         #for game bocks
BLUE = (100,149,237)            #for game bocks
ORCHID = (153,50,204)           #for game bocks
SEAGREEN = (180,238,180)        #for game bocks
GRAY = (161, 161, 161)        # For grid lines
MAROON = (128,0,0)

# Shapes

Z = [
        [
            ".....",
            ".00..", 
            "..00.",
            ".....",
            ".....",
        ],
        [
            ".....",
            "...0.",
            "..00.",
            "..0..",
            ".....",
        ]
    ]
L = [
        [
            ".....",
            "..0..",
            "..0..",
            "..00.",
            ".....",
        ],        
        [
            ".....",
            "...0.",
            ".000.",
            ".....",
            ".....",
        ],
        [
            ".....",
            "..00.",
            "...0.",
            "...0.",
            ".....",
        ],
        [
            ".....",
            ".000.",
            ".0...",
            ".....",
            ".....", 
        ], 
    ]
J = [
        [
            ".....",
            ".....",
            ".000.",
            "...0.",
            ".....",
        ],
        [
            ".....",
            "...0.",
            "...0.",
            "..00.",
            ".....",
        ],
        [
            ".....",
            ".....",
            ".0...",
            ".000.",
            ".....",
        ],
        [
            ".....",
            ".00..",
            ".0...",
            ".0...",
            ".....",
        ],
    ]
I = [
        [
            ".....",
            ".....",
            ".0000",
            ".....",
            ".....",
        ],
        [
            "..0..",
            "..0..",
            "..0..",
            "..0..",
            ".....",
        ],
    ]
T = [
        [
            ".....",
            ".....",
            ".000.",
            "..0..",
            ".....",
        ],
        [
            ".....",
            ".0..",
            ".00.",
            ".0..",
            ".....",
        ],
        [
            ".....",
            ".....",
            "..0..",
            ".000.",
            ".....",
        ],
        [
            ".....",
            "..0..",
            ".00..",
            "..0.."
            ".....",
        ]
    ]
O = [
        [
            ".....",
            ".....",
            "..00.",
            "..00.",
            ".....",

        ],
    ]
S = [
        [
            ".....",
            "..00.",
            ".00.",
            ".....",
            ".....",
        ],
        [
            ".....",
            ".0...",
            ".00..",
            "..0..",
            ".....",
        ]
    ]

# CLASS FOR RECTANGLE BLOCKS

class Block:
    def __init__(self, x, y, shape, color):
        self.x = x
        self.y = y
        self.color = color
        self.rotation = 0
        self.shape = shape
        self.fall = True
        self.end = ()


# To draw grid lines
def drawGrid(win, rows, columns):
    for i in range(rows):
        pygame.draw.line(win, GRAY, (startValue_x, startValue_y + i * BLOCKWIDTH), (startValue_x + GAMEWIDTH, startValue_y + i * BLOCKWIDTH), 1)
        for j in range(columns):
            pygame.draw.line(win, GRAY, (startValue_x + j * BLOCKWIDTH, startValue_y), (startValue_x + j * BLOCKWIDTH, startValue_y + GAMELENGTH), 1)
    pygame.draw.line(win, GRAY, (startValue_x, startValue_y + rows * BLOCKWIDTH), (startValue_x + GAMEWIDTH, startValue_y + rows * BLOCKWIDTH), 1)
    pygame.draw.line(win, GRAY, (startValue_x + columns * BLOCKWIDTH, startValue_y), (startValue_x + columns * BLOCKWIDTH, startValue_y + GAMELENGTH), 1)

# To create place to store blocks
def createSpace(rows, columns, lockedPosition):
    space = [[(0,0,0) for j in range(columns)] for i in range(rows)]
    for i in range(len(space)):
        for j in range(len(space[i])):
            if (j, i) in lockedPosition:
                value = lockedPosition[(j, i)]
                space[i][j] = value
    return space

def getRandom(value):
    return random.choice(value)

# To generate block
def createBlock(shapes, color):
    block  = Block(5, 0, getRandom(shapes), getRandom(color))
    return block

# To draw Block 
def getShape(block):
    formate = []
    shape = block.shape[ block.rotation % len(block.shape)]
    for i, item in enumerate(shape):
        items =list(item)
        for j, ite in enumerate(items):
            if ite == "0":
                formate.append((block.x + j - 3, block.y + i - 4))
    return formate

def draw_everything(win, grid, rows, columns):
    win.fill(MAROON)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(win, grid[i][j], (startValue_x + j * BLOCKWIDTH, startValue_y + i * BLOCKWIDTH, BLOCKWIDTH, BLOCKWIDTH))
    drawGrid(win, rows, columns)
    pygame.display.update()

# To check position to move or not
def checkValidPosition(grid,currentBlock):
    position = []
    for i in range(len(grid)):
        position.append([])
        for j in range(len(grid[i])):
            if grid[i][j] ==(0,0,0):
                position[i].append((j, i))
    position = [j for i in position for j in i]
    currentFormatedBlock = getShape(currentBlock)
    for item in currentFormatedBlock:
        if (item[0] , item[1] + 1) not in position:
            if item[1] > -1:
                return False
    return True

def deleteRows(lockedPosition, grid):
    toFall = {}
    booleans = False
    count = 0
    place = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        # print(row)
        if (0,0,0) not in row: 
            booleans = True
            count += 1
            place = i
            for j in range(len(grid[i]) - 1, -1, -1):
                del lockedPosition[(j,i)]
    toFall = lockedPosition
    if count > 0:
        for item in list(lockedPosition):
            x, y = item
            if y < place:
                key = (x, y + 1)
                lockedPosition[key] = lockedPosition.pop(item)
    return booleans

def checkScore(win, grid, score):
    font  = pygame.font.Font("freesansbold.ttf", 24)
    text = font.render(f"SCORE : {score}", True, (0,0,0),(0, 12, 213) )
    textRect = text.get_rect()
    textRect.center = (14 * 30 - 4, 10 * 30)
    win.blit(text, textRect)
    pygame.display.update()

# To check if lost or not
def checkLost(lockedPosition):
    for item in lockedPosition:
        if item[1] < 1:
            return True
    return False

def draw_nextBlock(win, nextBlock):
    font  = pygame.font.Font("freesansbold.ttf", 24)
    text = font.render("NEXT SHAPE", True, (0,0,0),(0, 12, 213) )
    textRect = text.get_rect()
    textRect.center = (14 * 30 - 4, 4 * 30)
    win.blit(text, textRect)
    shape = getShape(nextBlock)
    for item in shape:
        pygame.draw.rect(win, nextBlock.color, ((item[0] + 9) * BLOCKWIDTH, (item[1] + 8) * BLOCKWIDTH, BLOCKWIDTH - 1, BLOCKWIDTH - 1))

def forDisplayOfText(win, text, color, backgroundColor, font, startPoint, endPoint):
    font = pygame.font.Font("freesansbold.ttf", font)
    text = font.render(text, True, color, backgroundColor)
    textRect = text.get_rect()
    textRect.center = (startPoint, endPoint)
    win.blit(text, textRect)

def displayTheTitle(win):
    win.fill(MAROON)
    forDisplayOfText(win, "WELCOME TO TETRIS GAME", (0,0,0), MAROON, 26, 250, 200)
    forDisplayOfText(win, "PRESS \'S\' TO PLAY", GRAY, MAROON, 26, 250, 250)
    forDisplayOfText(win, "PRESS \'Q\' TO EXIT", GRAY, MAROON, 26, 250, 300)
    forDisplayOfText(win, "ARROW KEY TO CHANGE AND MOVE BLOCK", GRAY, MAROON, 20, 250, 350)
    pygame.display.update()


# Main Function That Runs First
def main(win):
    ROWS = 20
    COLUMNS = 10
    shapes = [Z, L, I, T, O, S, J]
    colors = [ORANGE, PARROTGREEN, BLUE, ORCHID, SEAGREEN]
    running = True
    lockedPosition = {}
    currentBlock = createBlock(shapes, colors)
    nextBlock = createBlock(shapes, colors)
    fallSpeed = 0.31 
    fallTime = 0
    score = 0
    while running:
        grid =createSpace(ROWS,COLUMNS, lockedPosition)
        fallTime += clock.get_rawtime()
        clock.tick()
        if fallTime / 1000 > fallSpeed and currentBlock.fall:
            fallTime = 0
            if checkValidPosition(grid,currentBlock):
                currentBlock.y += 1
            else:
                currentBlock.fall = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    currentBlock.rotation += 1
                    if not(checkValidPosition(grid,currentBlock)):
                        currentBlock.rotation -=1
                if event.key == pygame.K_RIGHT:
                    currentBlock.x += 1     
                    if not(checkValidPosition(grid,currentBlock)):
                        currentBlock.x -= 1 
                if event.key == pygame.K_DOWN:
                    currentBlock.y += 1
                    if not(checkValidPosition(grid,currentBlock)):
                        currentBlock.y -= 1
                if event.key == pygame.K_LEFT:
                    currentBlock.x -= 1
                    if not(checkValidPosition(grid,currentBlock)):
                        currentBlock.x += 1
                if event.key == pygame.K_t:
                    pygame.time.delay(10000000)

        currentFormatedBlock = getShape(currentBlock)

        for i in range(len(currentFormatedBlock)):
            x, y = currentFormatedBlock[i] 
            if y > -1:
                grid[y][x] = currentBlock.color
        for item in currentFormatedBlock:
            if item[1] >= ROWS - 1:
                currentBlock.fall = False
        # if checkLost(lockedPosition):
            # running = False
        if not currentBlock.fall:
            score += 1
            for item in currentFormatedBlock:
                a = (item[0], item[1])
                lockedPosition[a] = currentBlock.color
            if checkLost(lockedPosition):
                running = False
            currentBlock = nextBlock
            nextBlock = createBlock(shapes, colors)
            deleted = deleteRows(lockedPosition, grid)
            if deleted:
                score += 10 
        checkScore(win, grid, score)
        draw_everything(win, grid, ROWS, COLUMNS)
        draw_nextBlock(win, nextBlock)
        pygame.display.update()
    pygame.quit()

def firstMain(win):
    running = True
    while running:
        displayTheTitle(win)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    main(win)
                if event.key == pygame.K_q:
                    running = False
    pygame.display.quit()

firstMain(WIN)