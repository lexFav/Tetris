from pygame.locals import *
from images import *
import pygame
import random
import os
pygame.init()
pygame.mixer.init()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

WIDTH, HEIGHT = TILE_SIZE * 20, TILE_SIZE * 18
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris - Game Boy")

# Constants
CENTER = (WIDTH / 2, HEIGHT / 2)
CENTER_X, CENTER_Y = CENTER
FPS = 60
VOLUME = 0.3
KEYMAP = {
    'UP': K_w,
    'LEFT': K_a,
    'DOWN': K_s,
    'RIGHT': K_d,
    'B': K_b,
    'A': K_n,
    'START': K_RETURN,
    'SELECT': K_LSHIFT,
}
#     'UP': K_UP,
#     'LEFT': K_LEFT,
#     'DOWN': K_DOWN,
#     'RIGHT': K_RIGHT,
#     'B': K_b,
#     'A': K_SPACE,
#     'START': K_RETURN,
#     'SELECT': K_LSHIFT,
# }
JOYSTICKS = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

# Addresses
piece_addresses = {
    'O': 0x00,
    'T': 0x30,
    'S': 0x10,
    'Z': 0x01,
    'J': 0x10,
    'L': 0x20,
    'I-0': 0x11,
    'I-1': 0x21,
    'I-2': 0x31,
    'I-3': 0x02,
    'I-4': 0x12,
    'I-5': 0x22,
}
text_addresses = {
    'A': 0x00, 'B': 0x10, 'C': 0x20, 'D': 0x30, 'E': 0x40, 'F': 0x50, 'G': 0x60, 'H': 0x70, 'I': 0x80, 'J': 0x90,
    'K': 0x01, 'L': 0x11, 'M': 0x21, 'N': 0x31, 'O': 0x41, 'P': 0x51, 'Q': 0x61, 'R': 0x71, 'S': 0x81, 'T': 0x91,
    'U': 0x02, 'V': 0x12, 'W': 0x22, 'X': 0x32, 'Y': 0x42, 'Z': 0x52, 'a': 0x62, 'b': 0x72, 'c': 0x82, 'd': 0x92,
    'e': 0x03, 'f': 0x13, 'g': 0x23, 'h': 0x33, 'i': 0x43, 'j': 0x53, 'k': 0x63, 'l': 0x73, 'm': 0x83, 'n': 0x93,
    'p': 0x04, 'q': 0x14, 'r': 0x24, 's': 0x34, 't': 0x44, 'u': 0x54, 'v': 0x64, 'w': 0x74, 'x': 0x84, 'y': 0x94,
    'z': 0x05, '1': 0x15, '2': 0x25, '3': 0x35, '4': 0x45, '5': 0x55, '6': 0x65, '7': 0x75, '8': 0x85, '9': 0x95,
    '0': 0x06, '.': 0x16, ',': 0x26, '"': 0x36, '`': 0x46, "'": 0x56, '~': 0x66, '?': 0x76, '!': 0x86, '@': 0x96,
    '_': 0x07, '*': 0x17, '#': 0x27, '$': 0x37, '%': 0x47, '&': 0x57, '(': 0x67, ')': 0x77, '+': 0x87, '-': 0x97,
    '/': 0x08, ':': 0x18, ';': 0x28, '<': 0x38, '>': 0x48, '=': 0x58, '[': 0x68, '\\': 0x78, ']': 0x88, '^': 0x98,
    '|': 0x09, '©': 0x19,
}
logo_addresses = [
    0x29, 0x39, 0x49, 0x59, 0x69, 0x79, 0x39,
]
high_score_name_addresses = [
    0x62, 0x72, 0x82, 0x92, 0x03, 0x13, 0x23, 0x33, 0x43, 0x53, 0x63, 0x73, 0x83, 0x93, 0x06,
    0x04, 0x14, 0x24, 0x34, 0x44, 0x54, 0x64, 0x74, 0x84, 0x94, 0x05, 0x16, 0x97, 0x47,
]

# Palletes
PALETTE_0 = [(168, 168, 168), (96, 96, 96), (248, 248, 248), (0, 0, 0)] # Light Gray, Dark Gray, White, Black (Black & White (Emulator) Palette)
PALETTE_1 = [(253, 207, 137), (217, 64, 67), (248, 248, 248), (0, 0, 0)] # Yellow, Red, White, Black (Switch Palette)
PALETTE_2 = [(105, 148, 29), (64, 107, 39), (136, 171, 40), (32, 66, 46)] # Light Green, Dark Green, Lighter Green, Darker Green (OG Gameboy Palette)

PALETTE = PALETTE_1
set_palette(PALETTE)

# Sounds
move_piece_sound = pygame.mixer.Sound('assets/sounds/move-piece.wav')
rotate_piece_sound = pygame.mixer.Sound('assets/sounds/rotate-piece.wav')
piece_landed_sound = pygame.mixer.Sound('assets/sounds/piece-landed.wav')
new_piece_sound = pygame.mixer.Sound('assets/sounds/new-piece.wav')
line_clear_sound = pygame.mixer.Sound('assets/sounds/line-clear.wav')
tetris_clear_sound = pygame.mixer.Sound('assets/sounds/tetris-clear.wav')
level_up_sound = pygame.mixer.Sound('assets/sounds/level-up.wav')
game_over_sound = pygame.mixer.Sound('assets/sounds/game-over-sound.wav')
menu_select = pygame.mixer.Sound('assets/sounds/menu-select.wav')
move_piece_sound = pygame.mixer.Sound('assets/sounds/move-piece.wav')

move_piece_sound.set_volume(VOLUME)
rotate_piece_sound.set_volume(VOLUME)
piece_landed_sound.set_volume(VOLUME)
new_piece_sound.set_volume(VOLUME)
line_clear_sound.set_volume(VOLUME)
tetris_clear_sound.set_volume(VOLUME)
level_up_sound.set_volume(VOLUME)
game_over_sound.set_volume(VOLUME)
menu_select.set_volume(VOLUME)

def get_image(address, VRAM, sender=None):
    x = int(address / 16) * 8
    y = (address % 16) * 8

    image = VRAM.copy().subsurface([x, y, 8, 8]).copy()

    if VRAM == pieces_image:
        if not sender == None:
            if sender == 'piece':
                if piece.shape == 'J':
                    swap_palettes(image, PALETTE, [PALETTE[1], PALETTE[0], *PALETTE[2:]])
            elif sender == 'grid':
                if grid.tile - 1 == 4:
                    swap_palettes(image, PALETTE, [PALETTE[1], PALETTE[0], *PALETTE[2:]])
            elif sender == 'UI':
                if piece.next_shape == 'J':
                    swap_palettes(image, PALETTE, [PALETTE[1], PALETTE[0], *PALETTE[2:]])

    return image

def draw_text(text, pos):
    lines = [text]
    if '\n' in text:
        lines = text.splitlines()
    
    x = 0
    y = 0

    for line in lines:
        for c in line:
            if not c in [' ', '🎮']:
                offset = 0

                if c == 'o':
                    c = '0'
                elif c == '"':
                    if lines.index(line) < 1:
                        offset += 2
                    else:
                        offset -= 4

                address = text_addresses[c]
                img = get_image(address, font_image)

                if c in ['.', ',', "'", '~', '!', ':', ';', '=', '©']:
                    offset -= 2

                screen.blit(img, [pos[0] + x + offset, pos[1] + y])
            elif c == '🎮':
                x += 2

                for address in logo_addresses:
                    img = get_image(address, font_image)
                    screen.blit(img, [pos[0] + x, pos[1] + y])
                    x += 7

                    if logo_addresses.index(address) in [1, 2]:
                        x -= 2

                x -= 8

            x += 8

        y += 8
        x = 0

class Piece:
    def __init__(self):
        self.drop_speed = 53
        self.joy_x = 0
        self.joy_y = 0

        self.joy_motion = [0, 0]
        self.rows = []
        self.score_data = [0, 0, 0, 0, 0]
        self.shapes = {
            'O': [(0, 0), (1, 0), (0, 1), (1, 1)],
            'T': [(-1, 0), (0, 0), (1, 0), (0, 1)],
            'S': [(0, 0), (1, 0), (-1, 1), (0, 1)],
            'Z': [(-1, 0), (0, 0), (0, 1), (1, 1)],
            'J': [(-1, 0), (0, 0), (1, 0), (1, 1)],
            'L': [(-1, 0), (0, 0), (1, 0), (-1, 1)],
            'I': [(-1, 0), (0, 0), (1, 0), (2, 0)],
        }
        self.drop_speed_table = [
            53, 49, 45, 41, 37, 33, 28, 22, 17, 11,
            10, 9, 8, 7, 6, 5, 5, 4, 4,
        ]

        self.next_shape = random.choice(list(self.shapes.keys()))

        self.reset()

    def reset(self):
        self.x = 5
        self.y = 0
        self.shape = self.next_shape
        self.next_shape = random.choice(list(self.shapes.keys()))
        self.frame = 0
        self.move_frame = 0
        self.direction = 0
        self.game_over = False
        self.dropping = 0
        self.drop_rate = 0
        self.held = True

        self.positions = self.shapes[self.shape]
        
        if self.handle_collisions():
            self.game_over = True
            self.frame = -1
            pygame.mixer.music.stop()
            game_over_sound.play()

    def draw(self):
        if len(self.rows) > 0:
            return
        
        if not self.shape == 'I':
            for x, y in self.positions:
                screen.blit(get_image(piece_addresses[self.shape], pieces_image, sender='piece'), [(self.x + x) * 8 + 16, (self.y + y) * 8])
        else:
            for idx, pos in enumerate(self.positions):
                x, y = pos
                direction = 1 - self.direction

                image = f'I-{(direction * 3) + 1}'

                if idx < 1:
                    image = f'I-{direction * 3}'
                elif pos == self.positions[-1]:
                    image = f'I-{(direction * 3) + 2}'
                    
                if self.direction > 0:
                    image = image[:-1] + str(2 - int(image[-1]))

                screen.blit(get_image(piece_addresses[image], pieces_image), [(self.x + x) * 8 + 16, (self.y + y) * 8])

    def handle_controls(self):
        keys = pygame.key.get_pressed()

        if len(JOYSTICKS) < 1:
            self.joy_x = keys[KEYMAP['RIGHT']] - keys[KEYMAP['LEFT']]
        else:
            self.joy_x = self.joy_motion[0]

        if not self.held:
            if len(JOYSTICKS) < 1:
                self.joy_y = keys[KEYMAP['DOWN']]
            else:
                self.joy_y = self.joy_motion[1] > 0
            
            # Dropping 0: Can drop to get points
            # Dropping 1: Currently dropping to get points
            # Dropping -1: Tried dropping but cannot get points

            if self.joy_y:
                if self.dropping > -1:
                    self.dropping = 1
            elif self.dropping == 1:
                self.dropping = -1
                self.drop_rate = 0
        else:
            self.joy_y = 0

        if not (keys[KEYMAP['DOWN']] or self.joy_motion[1] > 0):
            self.held = False

        if ui.key_pressed(KEYMAP['START']):
            ui.pause = 1

    def handle_placement(self):
        if not self.shape == 'I':
            tile = list(self.shapes.keys()).index(self.shape) + 1
            
            for x, y in self.positions:
                grid.grid[grid.height - (self.y + y)][self.x + x] = tile
        else:
            for idx, pos in enumerate(self.positions):
                x, y = pos
                direction = 1 - self.direction

                tile = (direction * 3) + 1

                if idx < 1:
                    tile = direction * 3
                elif pos == self.positions[-1]:
                    tile = (direction * 3) + 2
                    
                if self.direction > 0:
                    tile = 2 - tile

                try:
                    grid.grid[grid.height - (self.y + y)][self.x + x] = tile + 7
                except:
                    pass

        for idx, row in enumerate(grid.grid):
            if row.count(0) < 1:
                self.rows.append(idx)
                self.frame = 0

        if self.drop_rate > 0:
            if ui.mode == 0:
                ui.score += self.drop_rate - 1
            else:
                self.score_data[4] += 1

    def handle_boundaries(self):
        offset_0 = 0
        for x, _ in self.positions:
            offset_0 = max(offset_0, -self.x - x)

        offset_1 = 0
        for x, _ in self.positions:
            offset_1 = max(offset_1, self.x + x - grid.width + 1)

        return offset_0 - offset_1

    def handle_collisions(self):
        for x, y in self.positions:
            if self.y + y < 0:
                continue

            tile = grid.grid[grid.height - (self.y + y) - 1][self.x + x]

            if tile > 0:
                return True
            
        return False

    def handle_horizontal_movement(self):
        if self.joy_x == 0:
            self.move_frame = 0
            return

        old_x = self.x

        if self.move_frame < 1 or self.move_frame == 16:
            self.x += self.joy_x
        elif self.move_frame > 16:
            if (self.move_frame - 16) % 6 == 0:
                self.x += self.joy_x

        self.move_frame += 1

        self.x += self.handle_boundaries()

        if self.handle_collisions():
            self.x -= self.joy_x

        if not old_x == self.x:
            move_piece_sound.play()

    def handle_falling(self):
        if self.joy_y == 0 or not self.joy_x == 0:
            if self.frame % self.drop_speed == 0:
                self.y += 1
        elif self.frame % 2 == 0:
            self.y += 1

            if self.dropping == 1:
                self.drop_rate += 1

        for x, y in self.positions:
            if not self.y + y < grid.height:
                self.handle_placement()

                self.reset()
                self.y += 1
                piece_landed_sound.play()
                break

            if self.y + y > 0:
                row = grid.height - (self.y + y) - 1
                tile = grid.grid[row][self.x + x]
                if tile > 0:
                    self.handle_placement()

                    self.reset()
                    self.y += 1
                    self.joy_y = 0
                    piece_landed_sound.play()
                    break

    def handle_game_over(self):
        if self.frame < grid.height:
            grid.grid[self.frame] = [13] * grid.width
        elif self.frame == grid.height:
            self.frame = 100
        elif self.frame - 100 == 60:
            self.frame = 199
        elif not self.frame < 200:
            if self.frame - 200 < grid.height:
                grid.grid[self.frame - 200] = [0] * grid.width

            if grid.grid[-1][0] == 0:
                screen.blit(game_over_screen, [16, 0])

                if ui.key_pressed(KEYMAP['A']) or ui.key_pressed(KEYMAP['START']):
                    if ui.last_mode == 0:
                        scores = ui.high_scores[ui.chosen_level].copy()
                        scores.reverse()
                        ui.place = len(scores)

                        for name, score in scores:
                            if ui.score > score:
                                ui.place -= 1

                        if ui.place < 3:
                            ui.high_score = True

                            if not len(scores) < 3:
                                ui.high_scores[ui.chosen_level].pop(2)

                            ui.high_scores[ui.chosen_level].insert(ui.place, ['a', ui.score])
                            ui.selected = ui.chosen_level

                    ui.title = True
                    ui.level = 4 + ui.last_mode
                    ui.score = 0
                    ui.temp = 0
                    ui.letter = 0
                    ui.frame = 0
                    self.game_over = False
                    self.score_data = [0, 0, 0, 0, 0]

                    if not ui.high_score:
                        ui.load_music(f'{['a', 'b', 'c'][ui.music]}-type-music')
                    else:
                        ui.load_music('high-score', 0)
            elif grid.grid[-2][0] == 0:
                ui.load_music('game-over', 0)

        self.frame += 1

    def rotate(self, direction):
        if len(self.rows) > 0 or ui.title or ui.pause > 0 or ui.win:
            return
        
        rotate_piece_sound.play()

        if self.shape == 'O':
            return
        
        if self.shape == 'I':
            self.y += 1

            cannot_rotate = False

            if self.handle_collisions():
                cannot_rotate = True

            self.y -= 1

            if cannot_rotate:
                return
        
        self.direction += direction

        if self.shape in ['S', 'Z', 'I']:
            if self.shape == 'I':
                direction = -direction

            if '2' in str(self.direction):
                self.direction = 0
                direction = -direction
            elif self.direction < 0:
                self.direction = 1
                direction = -direction

        self.direction %= 4
        
        new_pos = []
        for x, y in self.positions:
            new_pos.append((-y * direction, x * direction))

        old_pos = self.positions
        self.positions = new_pos

        if not self.handle_boundaries() == 0 or self.handle_collisions():
            self.positions = old_pos

            self.direction = 1

    def update(self):
        if self.game_over:
            self.handle_game_over()
            return
        elif len(self.rows) > 0:
            if self.frame == 1:
                if len(self.rows) < 4:
                    line_clear_sound.play()
                else:
                    tetris_clear_sound.play()

            if int(self.frame / 10) % 2 == 0:
                for row in self.rows:
                    pygame.draw.rect(screen, PALETTE[0], [16, ((grid.height) - row - 1) * 8, grid.width * 8, 8])

            self.frame += 1

            if self.frame > 80:
                ui.lines += len(self.rows)

                if ui.mode == 0:
                    ui.score += ui.points[len(self.rows) - 1] * (ui.level + 1)

                    if not ui.lines < 10:
                        last_level = ui.level
                        ui.level = int(str(ui.lines)[:-1])

                        if ui.level > last_level:
                            level_up_sound.play()

                        if ui.level < 20:
                            self.drop_speed = self.drop_speed_table[ui.level]
                        else:
                            self.drop_speed = 3
                else:
                    self.score_data[len(self.rows) - 1] += 1

                self.rows.sort()
                self.rows.reverse()

                for row in self.rows:
                    grid.grid.pop(row)
                    grid.grid.append([0] * grid.width)

                self.frame = 0
                self.rows = []
                new_piece_sound.play()
            return

        self.handle_controls()
        self.handle_falling()
        self.handle_horizontal_movement()

        self.frame += 1

        self.draw()

class Grid:
    def __init__(self):
        self.width = 10
        self.height = 18
        self.tile = 0

        self.grid = [[0] * self.width for _ in range(self.height)]

    def spawn_garbage(self, height):
        if height < 1:
            return
        
        rows = (height * 2) + random.randint(-1, 1)

        for row in range(rows):
            for block in range(10):
                if random.random() < 2 / 3:
                    tile = 0
                    while tile in [0, 8, 9, 10, 11, 12]:
                        tile = random.randrange(1, 13)

                    self.grid[row][block] = tile

            if self.grid[row].count(0) < 1:
                self.grid[row][random.randrange(0, 10)] = 0

    def update(self):
        pygame.draw.rect(screen, PALETTE[2], [16, 0, self.width * 8, self.height * 8])
        if piece.game_over and self.grid[-1][0] > 12:
            screen.blit(game_over_screen, [16, 0])

        for x in range(2):
            for y in range(int(self.height * 1.5)):
                screen.blit(get_image(0x32, pieces_image), [((x * (self.width + 1)) * 8) + 8, y * 6])

        pygame.draw.line(screen, PALETTE[2], [7, 0], [7, HEIGHT * (8 / TILE_SIZE)])

        for y in range(self.height):
            for x in range(self.width):
                self.tile = self.grid[y][x]

                if 0 < self.tile < len(piece_addresses.values()) + 1:
                    screen.blit(get_image(list(piece_addresses.values())[self.tile - 1], pieces_image, sender='grid'), [(x + 2) * 8, (self.height - y - 1) * 8])
                elif self.tile == 13:
                    screen.blit(get_image(0x03, pieces_image, sender='grid'), [(x + 2) * 8, (self.height - y - 1) * 8])

class UI:
    def __init__(self):
        self.score = 0
        self.level = 0
        self.lines = 0
        self.x = (grid.width * 8) + 24
        self.title = True
        self.win = False
        self.frame = 0
        self.selected = 0
        self.mode = 0
        self.music = 0
        self.height = 0
        self.temp = 0
        self.last_mode = 0
        self.pause = 0
        self.chosen_level = 0
        self.high_score = False
        self.letter = 0
        self.place = 0
        self.button = 0
        self.joy_press_motion = [0, 0]
        self.current_score_data = [0, 0, 0, 0, 0]
        self.keys = pygame.key.get_pressed()

        self.points = [40, 100, 300, 1200]
        self.high_scores = []
        self.read_high_scores()

    def load_music(self, filename, loops=-1, start=0.0):
        pygame.mixer.music.load(f'assets/sounds/{filename}.mp3')
        pygame.mixer.music.play(loops, start)

    def stop_music(self):
        pygame.mixer.music.stop()

    def read_high_scores(self):
        with open('high-scores.txt', 'r') as f:
            lines = f.readlines()
            
            for line in lines:
                if len(line) < 3:
                    self.high_scores.append([])
                    continue

                level_scores = []

                for level in line.split('_'):
                    name, score = level.split('-')
                    full_name = ''
                    hex_num = name.replace('0x', '')

                    for c_idx in range(6):
                        c = int(hex_num[(c_idx * 2):((c_idx + 1) * 2)], 16)

                        if c == 255:
                            continue

                        if c < len(high_score_name_addresses):
                            address = high_score_name_addresses[c]
                            full_name += list(text_addresses.keys())[list(text_addresses.values()).index(address)]
                        else:
                            full_name += ' '

                    level_scores.append([full_name, int(score, 16)])

                self.high_scores.append(level_scores)

    def save_high_score(self):
        level_idx = 0
        high_scores_save = ''

        for level in self.high_scores:
            if level == []:
                high_scores_save += ' \n'
                continue

            level_code = ''
            idx = 0

            for name, score in level:
                decoded_name = '0x'

                for c in name:
                    address = 0

                    if c == ' ':
                        address = len(high_score_name_addresses)
                    else:
                        address = high_score_name_addresses.index(text_addresses[c])

                    decoded_name += f'{address:0{2}X}'

                while len(decoded_name) < 14:
                    decoded_name += 'FF'

                decoded_score = f'0x{score:0{6}X}'

                if idx < len(level) - 1:
                    level_code += f'{decoded_name}-{decoded_score}_'
                else:
                    level_code += f'{decoded_name}-{decoded_score}'
                
                idx += 1

            if level_idx < len(self.high_scores) - 1:
                high_scores_save += f'{level_code}\n'
            else:
                high_scores_save += level_code

            level_idx += 1
        
        with open('high-scores.txt', 'w') as f:
            f.write(high_scores_save)

        self.high_score = False
        self.letter = 0
        self.frame = 0
        self.stop_music()
        self.load_music(f'{['a', 'b', 'c'][self.music]}-type-music')

    def key_pressed(self, key):
        keys = pygame.key.get_pressed()
        key_check = keys[key] and not self.keys[key]
        return key_check or self.button == key

    def handle_selected(self, width):
        sfx = False

        if self.key_pressed(KEYMAP['LEFT']) or self.joy_press_motion[0] < 0:
            if self.selected % width > 0:
                self.selected -= 1
                sfx = True
        elif self.key_pressed(KEYMAP['RIGHT']) or self.joy_press_motion[0] > 0:
            if self.selected % width < width - 1:
                self.selected += 1
                sfx = True

        if self.key_pressed(KEYMAP['UP']) or self.joy_press_motion[1] < 0:
            if self.selected > width - 1:
                self.selected -= width
                sfx = True
        elif self.key_pressed(KEYMAP['DOWN']) or self.joy_press_motion[1] > 0:
            if self.selected < width:
                self.selected += width
                sfx = True

        if sfx:
            menu_select.play()

    def handle_mode_select(self):
        keys = pygame.key.get_pressed()

        screen.blit(select_mode, [0, 0])

        if self.level == 2:
            self.mode = -1
            last_selected = self.selected
            if keys[KEYMAP['LEFT']] or piece.joy_motion[0] < 0:
                self.selected = 0
            elif keys[KEYMAP['RIGHT']] or piece.joy_motion[0] > 0:
                self.selected = 1

            if not self.selected == last_selected:
                if self.key_pressed(KEYMAP['LEFT']) or self.key_pressed(KEYMAP['RIGHT']) or not self.joy_press_motion[0] == 0:
                    menu_select.play()

            if int(self.frame / 16) % 2 == 0:
                if self.selected < 1:
                    draw_text('a-type', [8 * 3, 8 * 5])
                else:
                    draw_text('b-type', [8 * 11, 8 * 5])
        else:
            self.music = -1
            old_select = self.selected
            self.handle_selected(width=2)
            if not self.selected == old_select:
                if self.selected < 3:
                    self.load_music(f'{str('abc')[self.selected]}-type-music')
                else:
                    self.stop_music()

            if int(self.frame / 16) % 2 == 0:
                if self.selected == 0:
                    draw_text('a-type', [8 * 3, 8 * 12])
                elif self.selected == 1:
                    draw_text('b-type', [8 * 11, 8 * 12])
                elif self.selected == 2:
                    draw_text('c-type', [8 * 3, 8 * 14])
                elif self.selected == 3:
                    draw_text(' off', [8 * 11, 8 * 14])

        if self.mode > -1:
            draw_text(f'{['a', 'b'][self.mode]}-type', [8 * (3 + (8 * self.mode)), 8 * 5])

        if self.music > -1:
            if self.music < 2:
                draw_text(f'{['a', 'b'][self.music]}-type', [8 * (3 + (8 * (self.music))), 8 * 12])
            else:
                draw_text(['c-type', ' off'][self.music - 2], [8 * (3 + (8 * (self.music - 2))), 8 * 14])

        self.frame += 1

    def update(self):
        if self.win:
            if not pygame.mixer.music.get_busy():
                if self.temp < 0:
                    if self.frame < 18:
                        grid.grid[self.frame] = [0] * grid.width
                    else:
                        self.temp = 0
                elif self.temp > 4:
                    if self.key_pressed(KEYMAP['START']) or self.key_pressed(KEYMAP['A']):
                        
                        scores = self.high_scores[10 + (self.chosen_level * 5) + self.height].copy()
                        scores.reverse()
                        self.place = len(scores)

                        for name, score in scores:
                            if self.score > score:
                                self.place -= 1

                        if self.place < 3:
                            self.high_score = True

                            if not len(scores) < 3:
                                self.high_scores[10 + (self.chosen_level * 5) + self.height].pop(2)

                            self.high_scores[10 + (self.chosen_level * 5) + self.height].insert(self.place, ['a', self.score])
                            self.selected = self.chosen_level

                        self.title = True
                        self.level = 4 + self.last_mode
                        self.score = 0
                        self.temp = 0
                        self.letter = 0
                        self.frame = -1
                        self.win = False
                        self.current_score_data = [0, 0, 0, 0, 0]
                        piece.game_over = False
                        piece.score_data = [0, 0, 0, 0, 0]
                        
                        if not ui.high_score:
                            ui.load_music(f'{['a', 'b', 'c'][ui.music]}-type-music')
                        else:
                            ui.load_music('high-score', 0)
                else:
                    if not self.frame < 0:
                        if piece.score_data[self.temp] == self.current_score_data[self.temp]:
                            self.temp += 1
                            self.frame = -40
                        elif self.frame % 5 == 0 or self.temp == 4:
                            self.current_score_data[self.temp] += 1
                            move_piece_sound.play()
                            data = self.current_score_data
                            self.score = (data[0] * 40) + (data[1] * 100) + (data[2] * 300) + (data[3] * 1200) + data[4]

                draw_text(f'single\n{' ' * (not len(str(self.current_score_data[0])) > 1)}{self.current_score_data[0]} % 40', [8 * 2, 0])
                draw_text(str(self.current_score_data[0] * 40), [8 * 11 - (len(str(self.current_score_data[0] * 40)) * 8), 8 * 2])

                draw_text(f'double\n{' ' * (not len(str(self.current_score_data[1])) > 1)}{self.current_score_data[1]} % 100', [8 * 2, 8 * 3])
                draw_text(str(self.current_score_data[1] * 100), [8 * 11 - (len(str(self.current_score_data[1] * 100)) * 8), 8 * 5])

                draw_text(f'triple\n {self.current_score_data[2]} % 300', [8 * 2, 8 * 6])
                draw_text(str(self.current_score_data[2] * 300), [8 * 11 - (len(str(self.current_score_data[2] * 300)) * 8), 8 * 8])

                draw_text(f'tetris\n {self.current_score_data[3]} % 1200', [8 * 2, 8 * 9])
                draw_text(str(self.current_score_data[3] * 300), [8 * 11 - (len(str(self.current_score_data[3] * 300)) * 8), 8 * 11])

                draw_text('drops', [8 * 2, 8 * 12])
                draw_text(str(self.current_score_data[4]), [8 * 11 - (len(str(self.current_score_data[4])) * 8), 8 * 13])

                for x in range(8 * 2, 8 * 12, 2):
                    pygame.draw.rect(screen, PALETTE[3], [x, 8 * 15, 1, 1])

                draw_text('this stage', [8 * 2, 8 * 16])
                draw_text(str(self.score), [8 * 11 - (len(str(self.score)) * 8), 8 * 17])

                if self.temp < 0:
                    pygame.draw.rect(screen, PALETTE[2], [8 * 2, 0, 8 * 10, (18 - self.frame) * 8])

                self.frame += 1

            screen.blit(b_type_UI, [self.x, 0])

            draw_text(str(self.level), [8 * 17 - (len(str(self.level)) * 8), 8 * 2])
            draw_text(str(self.height), [8 * 17 - (len(str(self.height)) * 8), 8 * 5])
            draw_text(str(25 - self.lines), [8 * 18 - (len(str(25 - self.lines)) * 8), 8 * 10])

            self.keys = pygame.key.get_pressed()
            return

        if not self.title:
            if self.mode == 0:
                screen.blit(a_type_UI, [self.x, 0])

                if self.score > 999999:
                    self.score = 999999

                draw_text(str(self.score), [8 * 20 - (len(str(self.score)) * 8), 8 * 3])
                draw_text(str(self.level), [8 * 19 - (len(str(self.level)) * 8), 8 * 7])
                draw_text(str(self.lines), [8 * 19 - (len(str(self.lines)) * 8), 8 * 10])
            else:
                screen.blit(b_type_UI, [self.x, 0])

                draw_text(str(self.level), [8 * 17 - (len(str(self.level)) * 8), 8 * 2])
                draw_text(str(self.height), [8 * 17 - (len(str(self.height)) * 8), 8 * 5])
                draw_text(str(25 - self.lines), [8 * 18 - (len(str(25 - self.lines)) * 8), 8 * 10])

                if 25 - self.lines < 1:
                    self.win = True
                    self.lines = 25
                    self.stop_music()
                    self.load_music('b-type-win', 0)
                    self.frame = 0
                    self.temp = -1

            if self.pause > 0:
                screen.blit(pause_screen, [16, 0])

                if self.pause > 1:
                    if self.key_pressed(KEYMAP['START']):
                        self.pause = 0
                else:
                    self.pause = 2
            else:
                # Draw next piece
                if not piece.next_shape == 'I':
                    for x, y in piece.shapes[piece.next_shape]:
                        screen.blit(get_image(piece_addresses[piece.next_shape], pieces_image, sender='UI'), [(WIDTH * (8 / TILE_SIZE)) + (x * 8) - (8 * 4), (y * 8) + (8 * 14)])
                else:
                    screen.blit(get_image(0x02, pieces_image), [(WIDTH * (8 / TILE_SIZE)) - (8 * 5), 8 * 14])
                    screen.blit(get_image(0x12, pieces_image), [(WIDTH * (8 / TILE_SIZE)) - (8 * 4), 8 * 14])
                    screen.blit(get_image(0x12, pieces_image), [(WIDTH * (8 / TILE_SIZE)) - (8 * 3), 8 * 14])
                    screen.blit(get_image(0x22, pieces_image), [(WIDTH * (8 / TILE_SIZE)) - (8 * 2), 8 * 14])
        else:
            if self.level == 0: # Beginning Credits
                screen.fill(PALETTE[2])
                draw_text('"tm and ©1987 elorg,\n tetris licensed to\n    bullet-proof\n    software and\n   sub-licensed to\n      notendo.', [0, 8])
                draw_text('©1989 bullet-proof\n     software.\n  ©1989 🎮', [8, 8 * 8])
                draw_text('all rights reserved.\n \n  original concept,\n design and program\nby alexey pazhitnov."', [0, 8 * 12])

                self.frame += 1
                if self.frame > 60 * 4:
                    if self.frame > 60 * 8 or self.key_pressed(KEYMAP['START']):
                        self.frame = 0
                        self.selected = 0
                        self.level = 1
                        self.load_music('title')
            elif self.level == 1: # Title Screen
                screen.blit(title, [0, 0])
                draw_text('©1989 🎮', [8 * 4, 8 * 16])

                if self.key_pressed(KEYMAP['LEFT']) or self.joy_press_motion[0] < 0:
                    self.selected = 0
                elif self.key_pressed(KEYMAP['RIGHT']) or self.joy_press_motion[0] > 0:
                    self.selected = 1

                if self.key_pressed(KEYMAP['SELECT']):
                    self.selected = 1 - self.selected
                
                if self.key_pressed(KEYMAP['START']):
                    if self.selected > 0:
                        self.selected = 0
                    else:
                        self.level = 2
                        self.load_music('a-type-music')

                screen.blit(selector, [((WIDTH * (4 / TILE_SIZE)) * self.selected) + 8, 14 * 8])
            elif self.level < 4: # Gameplay Selection
                # Level 2: Gameplay Selection
                # Level 3: Music Selection
                
                self.handle_mode_select()

                if self.key_pressed(KEYMAP['START']):
                    if self.level == 2:
                        self.mode = self.selected
                        self.music = 0
                    else:
                        self.music = self.selected

                    self.selected = 0
                    self.level = 4 + self.mode

                    if self.music < 3:
                        self.load_music(f'{str('abc')[self.music]}-type-music')

                if self.key_pressed(KEYMAP['A']):
                    if self.level == 2:
                        self.mode = self.selected
                        self.selected = self.music
                    else:
                        self.music = self.selected
                        self.selected = 0

                        if self.music < 3:
                            self.load_music(f'{str('abc')[self.music]}-type-music')

                    if self.level < 3:
                        self.level += 1
                    else:
                        self.level = 4 + self.mode
                elif self.key_pressed(KEYMAP['B']):
                    if self.level == 3:
                        self.music = self.selected
                        self.selected = self.mode
                        self.level = 2
            elif self.level == 4: # A type
                screen.blit(a_type, [0, 0])

                if not self.high_score:
                    self.handle_selected(width=5)
                else:
                    if self.key_pressed(KEYMAP['A']):
                        self.letter += 1

                        if self.letter > 5:
                            self.save_high_score()
                        elif self.letter == len(self.high_scores[self.chosen_level][self.place][0]):
                            self.high_scores[self.chosen_level][self.place][0] += 'a'
                    elif self.key_pressed(KEYMAP['B']):
                        self.letter -= 1

                        if self.letter < 0:
                            self.letter = 0
                    elif self.key_pressed(KEYMAP['START']) and self.frame > 0:
                        self.save_high_score()

                    if not self.high_scores[self.chosen_level][self.place][0][self.letter] == ' ':
                        c = high_score_name_addresses.index(text_addresses[self.high_scores[self.chosen_level][self.place][0][self.letter]])
                    else:
                        c = len(high_score_name_addresses)

                    if len(JOYSTICKS) < 1:
                        c += self.key_pressed(KEYMAP['UP']) - self.key_pressed(KEYMAP['DOWN'])
                    else:
                        c -= self.joy_press_motion[1]
                        
                    c %= len(high_score_name_addresses) + 1

                    if c < len(high_score_name_addresses):
                        c = list(text_addresses.keys())[list(text_addresses.values()).index(high_score_name_addresses[c])]
                    else:
                        c = ' '

                    string = ''
                    for letter in self.high_scores[self.chosen_level][self.place][0]:
                        if len(string) == self.letter:
                            string += c
                        else:
                            string += letter

                    self.high_scores[self.chosen_level][self.place][0] = string

                    if not pygame.mixer.music.get_busy():
                        self.load_music('high-score', -1, 1.7)

                if len(self.high_scores[self.selected]) > 0:
                    idx = 0

                    for name, score in self.high_scores[self.selected]:
                        pygame.draw.rect(screen, PALETTE[2], [8 * 4, 8 * (13 + idx), len(name) * 8, 8])

                        draw_text(name, [8 * 4, 8 * (13 + idx)])

                        if self.high_score and idx == self.place and int(self.frame / 16) % 2 > 0:
                            pygame.draw.rect(screen, PALETTE[2], [8 * (4 + self.letter), 8 * (13 + idx), 8, 8])

                        pygame.draw.rect(screen, PALETTE[2], [(8 * 18) - (len(str(score)) * 8), 8 * (13 + idx), len(str(score)) * 8, 8])
                        draw_text(str(score), [(8 * 18) - (len(str(score)) * 8), 8 * (13 + idx)])
                        
                        idx += 1

                if int(self.frame / 16) % 2 == 0:
                    draw_text(str(self.selected), [(8 * 5) + ((self.selected % 5) * 16), (8 * 6) + (int(self.selected / 5) * 16)])

                if self.frame > 0 and not self.high_score:
                    if self.key_pressed(KEYMAP['START']) or self.key_pressed(KEYMAP['A']):
                        self.level = self.selected
                        self.chosen_level = self.level
                        self.title = False
                        self.selected = 0
                    elif self.key_pressed(KEYMAP['B']):
                        self.level = 2
                        self.selected = 0

                self.last_mode = 0
                self.frame += 1
            elif self.level < 7: # B type
                screen.blit(b_type, [0, 0])

                self.last_mode = 1

                if self.level == 5: # Choose Level
                    self.temp = -1

                    if not self.high_score:
                        self.handle_selected(width=5)
                    else:
                        if self.key_pressed(KEYMAP['A']):
                            self.letter += 1

                            if self.letter > 5:
                                self.save_high_score()
                            elif self.letter == len(self.high_scores[10 + (self.chosen_level * 5) + self.height][self.place][0]):
                                self.high_scores[10 + (self.chosen_level * 5) + self.height][self.place][0] += 'a'
                        elif self.key_pressed(KEYMAP['B']):
                            self.letter -= 1

                            if self.letter < 0:
                                self.letter = 0
                        elif self.key_pressed(KEYMAP['START']) and self.frame > 0:
                            self.save_high_score()

                        if not self.high_scores[10 + (self.chosen_level * 5) + self.height][self.place][0][self.letter] == ' ':
                            c = high_score_name_addresses.index(text_addresses[self.high_scores[10 + (self.chosen_level * 5) + self.height][self.place][0][self.letter]])
                        else:
                            c = len(high_score_name_addresses)

                        if len(JOYSTICKS) < 1:
                            c += self.key_pressed(KEYMAP['UP']) - self.key_pressed(KEYMAP['DOWN'])
                        else:
                            c -= self.joy_press_motion[1]
                        c %= len(high_score_name_addresses) + 1

                        if c < len(high_score_name_addresses):
                            c = list(text_addresses.keys())[list(text_addresses.values()).index(high_score_name_addresses[c])]
                        else:
                            c = ' '

                        string = ''
                        for letter in self.high_scores[10 + (self.chosen_level * 5) + self.height][self.place][0]:
                            if len(string) == self.letter:
                                string += c
                            else:
                                string += letter

                        self.high_scores[10 + (self.chosen_level * 5) + self.height][self.place][0] = string

                    if not pygame.mixer.music.get_busy():
                        self.load_music('high-score', -1, 1.7)

                    if int(self.frame / 16) % 2 == 0:
                        draw_text(str(self.selected), [(8 * 2) + ((self.selected % 5) * 16), (8 * 6) + (int(self.selected / 5) * 16)])
                else: # Choose height
                    self.height = -1
                    self.handle_selected(width=3)

                    if int(self.frame / 16) % 2 == 0:
                        draw_text(str(self.selected), [(8 * 13) + ((self.selected % 3) * 16), (8 * 6) + (int(self.selected / 3) * 16)])

                if self.level == 5:
                    scores_list = self.high_scores[10 + (self.selected * 5) + self.height]
                else:
                    scores_list = self.high_scores[10 + (self.temp * 5) + self.selected]

                if len(scores_list) > 0:
                    idx = 0

                    for name, score in scores_list:
                        pygame.draw.rect(screen, PALETTE[2], [8 * 4, 8 * (13 + idx), len(name) * 8, 8])

                        draw_text(name, [8 * 4, 8 * (13 + idx)])

                        if self.high_score and idx == self.place and int(self.frame / 16) % 2 > 0:
                            pygame.draw.rect(screen, PALETTE[2], [8 * (4 + self.letter), 8 * (13 + idx), 8, 8])

                        pygame.draw.rect(screen, PALETTE[2], [(8 * 18) - (len(str(score)) * 8), 8 * (13 + idx), len(str(score)) * 8, 8])
                        draw_text(str(score), [(8 * 18) - (len(str(score)) * 8), 8 * (13 + idx)])
                        
                        idx += 1

                if self.temp > -1:
                    draw_text(str(self.temp), [(8 * 2) + ((self.temp % 5) * 16), (8 * 6) + (int(self.temp / 5) * 16)])
                else:
                    draw_text(str(self.height), [(8 * 13) + ((self.height % 3) * 16), (8 * 6) + (int(self.height / 3) * 16)])

                if not self.high_score:
                    if self.key_pressed(KEYMAP['START']) and self.frame > 1:
                        if self.level == 5:
                            self.temp = self.selected
                            self.height = 0
                        else:
                            self.height = self.selected

                        self.selected = 0
                        self.level = self.temp
                        self.chosen_level = self.level
                        self.title = False
                        grid.spawn_garbage(self.height)

                    if self.key_pressed(KEYMAP['A']) and self.frame:
                        if self.level == 5:
                            self.temp = self.selected
                            self.selected = self.height
                            self.level = 6
                        else:
                            self.height = self.selected
                            self.selected = 0
                            self.level = self.temp
                            self.chosen_level = self.level
                            self.title = False
                            grid.spawn_garbage(self.height)
                    elif self.key_pressed(KEYMAP['B']):
                        if self.level == 5:
                            self.level = 2
                            self.selected = 0
                        else:
                            self.height = self.selected
                            self.selected = self.temp
                            self.level = 5

                self.frame += 1

        self.keys = pygame.key.get_pressed()


def draw():
    screen.fill(PALETTE[3])

    if not ui.title:
        grid.update()

        if not (ui.pause > 0 or ui.win):
            piece.update()

    ui.update()

    surf = screen.subsurface([0, 0, WIDTH * (8 / TILE_SIZE), HEIGHT * (8 / TILE_SIZE)])
        
    surf = pygame.transform.scale(surf, [WIDTH, HEIGHT])
    screen.blit(surf, (0, 0))

clock = pygame.time.Clock()
pygame.mixer.music.set_volume(VOLUME)

grid = Grid()
piece = Piece()
ui = UI()

run = True
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
            pygame.quit()
            quit()

        if event.type == KEYDOWN:
            if event.key == KEYMAP['B']:
                piece.rotate(-1)

            if event.key == KEYMAP['A']:
                piece.rotate(1)

        if event.type == JOYHATMOTION:
            piece.joy_motion = list(event.value)
            piece.joy_motion[1] = -piece.joy_motion[1]
            ui.joy_press_motion = list(event.value)
            ui.joy_press_motion[1] = -ui.joy_press_motion[1]
            
        if event.type == JOYBUTTONDOWN:
            if event.button in [0, 1, 6, 7]:
                ui.button = KEYMAP[{0: 'B', 1: 'A', 6: 'SELECT', 7: 'START'}[event.button]]

                if event.button < 2:
                    if event.button == 0:
                        piece.rotate(-1)
                    else:
                        piece.rotate(1)
    
    draw()
    ui.joy_press_motion = [0, 0]
    ui.button = 0

    pygame.display.flip()
