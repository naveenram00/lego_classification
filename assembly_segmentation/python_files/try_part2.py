import pygame
from pygame.locals import *
import cv2
import numpy as np
import sys
import os
import pygameMenu
from pygameMenu.locals import *

#-----------------------------------------------

def mainmenu_background():
    """
    Background color of the main menu, on this function user can plot
    images, play sounds, etc.
    """
    screen.fill((40, 0, 40))

HELP = ['       ',
        'Currently in Object Capture',
        '-----------------------------',
        'Press SPACEBAR to capture camera image',
        'Escape this window by EXIT in menu',
        '       ',
        
#         'Press LEFT/RIGHT to change modes',
#         '  Create: Click to create nodes',
#         '  Select: Click to select node (Delete with BACKSPACE)',
#         '  Order: Click on two existing nodes to connect them',
#         '  Move: Click to move selected node to location'
       ]

global nodes
nodes = []
first = []
select_radius = 15
objects = []
BLUE = (12, 12, 200)
COLOR_BACKGROUND = [128, 0, 128]
WHITE = (255, 255, 255)
PURPLE = (69, 61, 85)
L_PURPLE =(69,61, 150)
BLACK = (0, 0, 0)
H_SIZE = 600  # Height of window size
W_SIZE = 600  # Width of window size

#-----------------------------------------------

cam = cv2.VideoCapture(0)

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'

for m in HELP:
    print(m)
    
pygame.display.set_caption("Screencapture")
screen = pygame.display.set_mode([630,480])

#-----------------------------------------------

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def buttons(screen):
#check events
    for event in pygame.event.get():
        largeText = pygame.font.Font('freesansbold.ttf', 50)
        TextSurf, TextRect = text_objects(modes[mode_index%len(modes)].upper(), largeText, BLACK)
        TextRect.center = ((640/2),(506))
        screen.blit(TextSurf, TextRect)
        smallText = pygame.font.Font("freesansbold.ttf",20)

        mouse = pygame.mouse.get_pos()
#         pygame.draw.rect(screen, BLACK,(550,450,100,50))
        if 0 < mouse[0] < 100 and 480+50 > mouse[1] > 480:
            pygame.draw.rect(screen, L_PURPLE,(0,480,100,50))
        else:
            pygame.draw.rect(screen, PURPLE,(0,480,100,50))


        if 540 < mouse[0] < 640 and 480+50 > mouse[1] > 480:
            pygame.draw.rect(screen, L_PURPLE,(540,480,100,50))
        else:
            pygame.draw.rect(screen, PURPLE,(540,480,100,50))

        
        textSurf, textRect = text_objects("<", smallText, WHITE)
        textRect.center = ( (0+(100/2)), (480+(50/2)) )
        screen.blit(textSurf, textRect)
        textSurf, textRect = text_objects(">", smallText, WHITE)
        textRect.center = ( (540+(100/2)), (480+(50/2)) )
        screen.blit(textSurf, textRect)
        
#-----------------------------------------------

help_menu = pygameMenu.TextMenu(screen,
                                bgfun=mainmenu_background,
                                dopause=True,
                                font=pygameMenu.fonts.FONT_FRANCHISE,
                                text_fontsize=25,
                                font_size_title=60,
                                menu_color=(0,0,0),  # Background color
                                menu_color_title=(69, 61, 85),
                                onclose=PYGAME_MENU_DISABLE_CLOSE,  # Pressing ESC button does nothing
                                title='Help',
                                menu_height=int(H_SIZE * .6),
                                menu_width=int(W_SIZE * .9),
                                window_height=int(H_SIZE - 55),
                                window_width=int(W_SIZE + 27)
                                )
help_menu.add_option('Return to Menu', PYGAME_MENU_BACK)
# for m in HELP:
#     menu.add_line(m)

#-----------------------------------------------

menu = pygameMenu.TextMenu(screen,
                       bgfun=mainmenu_background,
                       enabled=False,
                       font=pygameMenu.fonts.FONT_NEVIS,
                       text_fontsize=17,
                       menu_alpha=40,
                       menu_color=(0,0,0),  # Background color
                       menu_color_title=(69, 61, 85),
                       onclose=PYGAME_MENU_CLOSE,
                       title='Help',
                       title_offsety=5,
                       menu_height=int(H_SIZE * .6),
                       menu_width=int(W_SIZE * .9),
                       window_height=int(H_SIZE - 55),
                       window_width=int(W_SIZE + 27)
                       )
for m in HELP:
    menu.add_line(m)
# menu.add_option(timer_menu.get_title(), timer_menu)  # Add timer submenu
# menu.add_option(help_menu.get_title(), help_menu)  # Add help submenu
# menu.add_option(about_menu.get_title(), about_menu)  # Add about submenu
menu.add_option('Exit', PYGAME_MENU_EXIT)  # Add exit function

#---------------------------------------------------------------------

def init():
    background = pygame.image.load("crop.jpg")
    imagerect = background.get_rect()
    screen = pygame.display.set_mode((640, 530))   # This line makes the stuttering 
    screen.fill(WHITE)
    screen.blit(background, imagerect)
    
    while True:
        screen.fill(WHITE)
        screen.blit(background, imagerect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
        pygame.display.update()
        
    
init()