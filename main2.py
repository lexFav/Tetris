from pygame.locals import *
import pygame
import random
import os
pygame.init()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

WIDTH, HEIGHT = 800, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

# Constants
CENTER = (WIDTH / 2, HEIGHT / 2)
CENTER_X, CENTER_Y = CENTER
FPS = 60
FONT = pygame.font.Font('font.ttf', 20)
GAME_WIDTH = 10
GAME_HEIGHT = 20
TILE_SIZE = int(HEIGHT / (GAME_HEIGHT + 3))
NEXT_PIECE = 0
SCORE = 0
offset_x = CENTER_X - (TILE_SIZE * (GAME_WIDTH / 2))
offset_y = CENTER_Y - (TILE_SIZE * (GAME_HEIGHT / 2)) - (TILE_SIZE / 2)

# Lists
GRID = [0] * (GAME_WIDTH * GAME_HEIGHT)
PIECES = ['S', 'Z', 'I', 'O', 'J', 'L', 'T']
NEXT_PIECE = random.choice(PIECES)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (245, 50, 20)
GREEN = (0, 200, 50)
BLUE = (60, 70, 255)
LIGHT_BLUE = (0, 180, 230)
YELLOW = (245, 245, 0)
ORANGE = (255, 171, 25)
GRAY = (128, 128, 128)
LIGHT_GRAY = (230, 230, 230)
PURPLE = (180, 50, 200)
PIECE_COLOR = {
    'S': 1,
    'Z': 2,
    'I': 3,
    'O': 4,
    'J': 5,
    'L': 6,
    'T': 7,
}
colors = {
    1: GREEN,
    2: RED,
    3: LIGHT_BLUE,
    4: YELLOW,
    5: BLUE,
    6: ORANGE,
    7: PURPLE,
}

class Piece:
    def __init__(self, type, shadow=False):
        self.reset(type, shadow)

    def reset(self, type, shadow=False):
        self.type = type
        self.color = PIECE_COLOR[self.type]
        self.grid_x = GAME_WIDTH / 2
        self.grid_y = 22
        self.grid_idx = 0
        self.counter = 0
        self.rotate_counter = 0
        self.height = 0
        self.speed_x = 0
        self.speed_y = 0
        self.shadow = shadow
        self.width = [1, 1]
        self.last_width = [0, 0]
        self.positions = [
            (0, 0)
        ]

        match self.type:
            case 'S':
                self.positions.append((-1, 0))
                self.positions.append((0, 1))
                self.positions.append((1, 1))

            case 'Z':
                self.positions.append((1, 0))
                self.positions.append((0, 1))
                self.positions.append((-1, 1))

            case 'I':
                self.positions.append((0, 1))
                self.positions.append((0, 2))
                self.positions.append((0, 3))
                self.width = [0, 0]

            case 'O':
                self.positions.append((0, 1))
                self.positions.append((1, 0))
                self.positions.append((1, 1))
                self.width = [0, 1]

            case 'J':
                self.positions.append((-1, 0))
                self.positions.append((-1, 1))
                self.positions.append((1, 0))

            case 'L':
                self.positions.append((1, 1))
                self.positions.append((1, 0))
                self.positions.append((-1, 0))

            case 'T':
                self.positions.append((1, 0))
                self.positions.append((0, 1))
                self.positions.append((-1, 0))

    def off_screen(self):
        for x, y in self.positions:
            x += self.grid_x
            y += self.grid_y
            if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
                return True
           
        return False

    def colliding_grid(self, add_y=True):
        try:
            for x, y in self.positions:
                self.gidx = int((self.grid_x + x) + (GAME_WIDTH * (self.grid_y + y)))
                if GRID[self.gidx] > 0:
                    self.grid_y += add_y
                    return True
        except:
            pass
           
        for _, y in self.positions:
            if self.grid_y + y <= 1 - self.shadow:
                return True
           
        return False

    def set_width(self):
        if not self.type == 'I':
            match self.type:
                case 'S':
                    self.width = [1, 1]
                    if (1, 1) in self.positions:
                        self.width = [0, 1]
                    elif (-1, -1) in self.positions:
                        self.width = [1, 0]
                case 'Z':
                    self.width = [1, 1]
                    if (-1, 1) in self.positions:
                        self.width = [0, 1]
                    elif (1, -1) in self.positions:
                        self.width = [1, 0]
                case 'J':
                    self.width = [1, 1]
                    for x, y in self.positions:
                        if (x, y) == (1, -1):
                            self.width = [1, 0]
                        elif (x, y) == (-1, 1):
                            self.width = [0, 1]
                case 'L':
                    self.width = [1, 1]
                    for x, y in self.positions:
                        if (x, y) == (1, 1):
                            self.width = [0, 1]
                        elif (x, y) == (-1, -1):
                            self.width = [1, 0]
                case 'T':
                    self.width = [1, 1]
                    if not (0, -1) in self.positions:
                        self.width = [0, 1]
                    elif not (0, 1) in self.positions:
                        self.width = [1, 0]
        else:
            match self.width:
                case [0, 0]:
                    self.width = [1, 2]
                    self.last_width = [0, 0]
                   
                case [1, 2]:
                    if self.last_width == [0, 0]:
                        self.width = [-1, 1]
                    elif self.last_width == [-1, 1]:
                        self.width = [0, 0]
                   
                case [-1, 1]:
                    self.width = [1, 2]
                    self.last_width = [-1, 1]

    def move(self, direction):
        if not direction[0] == 0 and self.off_screen():
            return

        dir_x, dir_y = direction

        self.grid_x += dir_x

        if self.grid_x < self.width[0]:
            self.grid_x = self.width[0]

        if self.grid_x >= GAME_WIDTH - self.width[1]:
            self.grid_x = GAME_WIDTH - self.width[1] - 1

        if self.colliding_grid(False):
            self.grid_x -= dir_x
           
        if self.counter == FPS * 0.4:
            self.counter = 0

        if self.counter > 0:
            self.counter += 1
            return

        self.grid_y += dir_y

        self.counter += 1

    def rotate(self, degrees):
        if self.type == 'O':
            return
       
        repetitions = {
            -90: 1,
            180: 2,
            90: 3,
        }

        self.set_width()
        if not self.type == 'I':
            for _ in range(repetitions[degrees]):
                positions = []

                for x, y in self.positions:
                    positions.append((-y, x))

                self.positions = positions
        else:
            for _ in range(repetitions[degrees]):
                positions = []
                center = (0.5, 1.5)

                for x, y in self.positions:
                    x1 = x - center[0]
                    y1 = y - center[1]

                    x2 = -y1
                    y2 = x1
                    positions.append((x2 + center[0], y2 + center[1]))

                self.positions = positions

    def handle_keys(self):
        keys = pygame.key.get_pressed()

        if keys[K_DOWN] or keys[K_s]:
            self.speed_y = -2
        else:
            self.speed_y = -1

    def lose(self):
        quit()

    def update(self):
        if not self.shadow:
            global NEXT_PIECE

            if self.colliding_grid():
                for x, y in self.positions:
                    self.gidx = int((self.grid_x + x) + (GAME_WIDTH * (self.grid_y + y)))
                    try:
                        GRID.pop(self.gidx)
                        GRID.insert(self.gidx, self.color)
                    except:
                        self.lose()
                self.reset(NEXT_PIECE)
                shadow.reset(NEXT_PIECE, shadow=True)
                NEXT_PIECE = random.choice(PIECES)

            self.handle_keys()
            self.move((self.speed_x, -1))
        else:
            self.positions = piece.positions
            self.grid_x = piece.grid_x
            self.grid_y = 0
            while self.colliding_grid(False):
                self.grid_y += 1

            if not self.colliding_grid(False):
                self.grid_y -= 1

    def draw(self):
        if self.off_screen():
            return
        
        offset_x = CENTER_X - (TILE_SIZE * (GAME_WIDTH / 2))
        offset_y = CENTER_Y + (TILE_SIZE * (GAME_HEIGHT / 2)) - (TILE_SIZE * 1.5)
        x = offset_x + (self.grid_x * TILE_SIZE)
        y = offset_y - (self.grid_y * TILE_SIZE)
        for x_pos, y_pos in self.positions:
            pos = [x + (x_pos * TILE_SIZE), y - (y_pos * TILE_SIZE)]
            if not self.shadow:
                pygame.draw.rect(screen, colors[self.color], [*pos, TILE_SIZE, TILE_SIZE])
            pygame.draw.rect(screen, BLACK, [pos[0] - 2, pos[1] - 2, TILE_SIZE + 2, TILE_SIZE + 2], 2)


def clear_row():
    global SCORE

    rows = []
    for idx in range(int(len(GRID) / GAME_WIDTH)):
        rows.append(GRID[(idx * GAME_WIDTH):((idx + 1) * GAME_WIDTH)])

    rows.append(rows.pop(0))

    for i, row in enumerate(rows):
        if 0 in row:
            continue

        SCORE += 10
        idxes = []
        gidx = (i + 1) * GAME_WIDTH
        for _ in range(GAME_WIDTH):
            idxes.append(gidx - GAME_WIDTH)
            GRID.pop(gidx)
            GRID.append(0)

def draw_grid():
    for x in range(GAME_WIDTH):
        for y in range(GAME_HEIGHT):
            pygame.draw.rect(screen, WHITE, [x * TILE_SIZE + offset_x - 2, y * TILE_SIZE + offset_y - 2, TILE_SIZE + 4, TILE_SIZE + 4])
            pygame.draw.rect(screen, LIGHT_GRAY, [x * TILE_SIZE + offset_x - 2, y * TILE_SIZE + offset_y - 2, TILE_SIZE + 4, TILE_SIZE + 4], 1)

    for idx, tile in enumerate(GRID):
        if tile == 0:
            continue
       
        x = idx % GAME_WIDTH
        y = GAME_HEIGHT - int(idx / GAME_WIDTH)

        pygame.draw.rect(screen, colors[tile], [x * TILE_SIZE + offset_x, y * TILE_SIZE + offset_y, TILE_SIZE, TILE_SIZE])
        pygame.draw.rect(screen, BLACK, [x * TILE_SIZE + offset_x - 2, y * TILE_SIZE + offset_y - 2, TILE_SIZE + 2, TILE_SIZE + 2], 2)

def draw_next_piece():
    color = PIECE_COLOR[NEXT_PIECE]

    x = offset_x + ((GAME_WIDTH + 2) * TILE_SIZE)
    y = offset_y + TILE_SIZE

    pygame.draw.rect(screen, WHITE, [x - (TILE_SIZE / 2) - 2, y - (TILE_SIZE / 2) - 2, (TILE_SIZE * 4) + 2, (TILE_SIZE * 4) + 2])
    pygame.draw.rect(screen, BLACK, [x - (TILE_SIZE / 2) - 2, y - (TILE_SIZE / 2) - 2, (TILE_SIZE * 4) + 2, (TILE_SIZE * 4) + 2], 3)

    positions = [(0, 0)]
    match color:
        case 1:
            positions.append((-1, 0))
            positions.append((0, 1))
            positions.append((1, 1))

        case 2:
            positions.append((1, 0))
            positions.append((0, 1))
            positions.append((-1, 1))

        case 3:
            positions.append((0, -1))
            positions.append((0, 1))
            positions.append((0, 2))

        case 4:
            positions = []
            positions.append((-0.5, 0))
            positions.append((0.5, 0))
            positions.append((-0.5, 1))
            positions.append((0.5, 1))

        case 5:
            positions.append((-1, 0))
            positions.append((-1, 1))
            positions.append((1, 0))

        case 6:
            positions.append((1, 1))
            positions.append((1, 0))
            positions.append((-1, 0))

        case 7:
            positions.append((1, 0))
            positions.append((0, 1))
            positions.append((-1, 0))

    x += TILE_SIZE
    y += TILE_SIZE * 1.5
    for x_pos, y_pos in positions:
        pos = [x + (x_pos * TILE_SIZE), y - (y_pos * TILE_SIZE)]
        pygame.draw.rect(screen, colors[color], [*pos, TILE_SIZE, TILE_SIZE])
        pygame.draw.rect(screen, BLACK, [pos[0] - 2, pos[1] - 2, TILE_SIZE + 2, TILE_SIZE + 2], 2)

    label = FONT.render('NEXT', 1, GRAY)
    w, h = label.get_size()
    screen.blit(label, [x - (w / 4), y - (h * 4.5)])

def draw():
    screen.fill(LIGHT_GRAY)

    piece.update()
    shadow.update()
    clear_row()

    draw_grid()
    draw_next_piece()

    piece.draw()
    shadow.draw()

    pygame.draw.rect(screen, BLACK, [offset_x - 2, offset_y - 2, GAME_WIDTH * TILE_SIZE + 4, GAME_HEIGHT * TILE_SIZE + 4], 3)

    label = FONT.render(f'SCORE: {SCORE}', 1, GRAY)
    w = label.get_width() / 2
    screen.blit(label, [CENTER_X - w, 10])

clock = pygame.time.Clock()

rand = random.choice(PIECES)
piece = Piece(rand)
shadow = Piece(rand, shadow=True)

run = True
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
            pygame.quit()
            quit()
   
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                piece.speed_x = -1

            elif event.key == K_RIGHT:
                piece.speed_x = 1

            if event.key == K_UP:
                piece.rotate(90)

            if event.key == K_DOWN:
                piece.grid_y -= 1

    draw()
    piece.speed_x = 0

    pygame.display.flip()
    