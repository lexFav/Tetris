import pygame
import numpy as np
import os
pygame.init()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

TILE_SIZE = 48

OG_PALETTE = [(168, 168, 168), (96, 96, 96), (248, 248, 248), (0, 0, 0)]

pieces_image = pygame.image.load('assets/images/pieces.png')
font_image = pygame.image.load('assets/images/font.png')

a_type_UI = pygame.image.load('assets/images/UI/a-type-UI.png')
b_type_UI = pygame.image.load('assets/images/UI/b-type-UI.png')
game_over_screen = pygame.image.load('assets/images/UI/game-over.png')
pause_screen = pygame.image.load('assets/images/UI/pause.png')
title = pygame.image.load('assets/images/UI/title.png')
select_mode = pygame.image.load('assets/images/UI/select-mode.png')
a_type = pygame.image.load('assets/images/UI/a-type.png')
b_type = pygame.image.load('assets/images/UI/b-type.png')
selector = pygame.image.load('assets/images/UI/selector.png')

def swap_palettes(image, palette_0, palette_1):
    for idx in range(len(palette_0)):
        if palette_0[idx] == palette_1[idx]:
            continue
        
        arr = pygame.surfarray.pixels3d(image)
        t_color = np.array(palette_0[idx])
        r_color = np.array(palette_1[idx])
        mask = np.all(arr == t_color, axis=-1)
        arr[mask] = r_color
        del arr

def set_palette(palette):
    if palette == OG_PALETTE:
        return
    
    for image in [pieces_image, font_image, title, select_mode, a_type, b_type, selector, a_type_UI, b_type_UI, game_over_screen, pause_screen]:
        swap_palettes(image, OG_PALETTE, palette)
