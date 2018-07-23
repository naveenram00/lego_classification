# import pygame
# import pygameMenu
# from pygameMenu.locals import *

# background_colour = (255,255,255)
# (width, height) = (700,700)
# screen = pygame.display.set_mode((width, height))

# screen.fill(background_colour)
# pygame.display.flip()
# pygameMenu.Menu(screen, width, height, "Arial", "Tutorial 1")
# running = True
# while running:
    
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

# Import pygame and libraries
# from pygame.locals import *
# from random import randrange
# import os
# import pygame

# # Import pygameMenu
# import pygameMenu
# from pygameMenu.locals import *

# ABOUT = ['PygameMenu {0}'.format(pygameMenu.__version__),
#          'Author: {0}'.format(pygameMenu.__author__),
#          PYGAMEMENU_TEXT_NEWLINE,
#          'Email: {0}'.format(pygameMenu.__email__)]
# COLOR_BACKGROUND = (128, 0, 128)
# COLOR_BLACK = (0, 0, 0)
# COLOR_WHITE = (255, 255, 255)
# FPS = 60.0
# MENU_BACKGROUND_COLOR = (228, 55, 36)
# WINDOW_SIZE = (640, 480)

# # -----------------------------------------------------------------------------
# # Init pygame
# pygame.init()
# os.environ['SDL_VIDEO_CENTERED'] = '1'

# # Create pygame screen and objects
# surface = pygame.display.set_mode(WINDOW_SIZE)
# pygame.display.set_caption('PygameMenu example 2')
# clock = pygame.time.Clock()
# dt = 1 / FPS

# # Global variables
# DIFFICULTY = ['EASY']


# # -----------------------------------------------------------------------------

# def change_difficulty(d):
#     """
#     Change difficulty of the game.
    
#     :return: 
#     """
#     print ('Selected difficulty: {0}'.format(d))
#     DIFFICULTY[0] = d


# def random_color():
#     """
#     Return random color.
    
#     :return: Color tuple
#     """
#     return randrange(0, 255), randrange(0, 255), randrange(0, 255)


# def play_function(difficulty, font):
#     """
#     Main game function
    
#     :param difficulty: Difficulty of the game
#     :param font: Pygame font
#     :return: None
#     """
#     difficulty = difficulty[0]
#     assert isinstance(difficulty, str)

#     if difficulty == 'EASY':
#         f = font.render('Playing as baby', 1, COLOR_WHITE)
#     elif difficulty == 'MEDIUM':
#         f = font.render('Playing as normie', 1, COLOR_WHITE)
#     elif difficulty == 'HARD':
#         f = font.render('Playing as god', 1, COLOR_WHITE)
#     else:
#         raise Exception('Unknown difficulty {0}'.format(difficulty))

#     # Draw random color and text
#     bg_color = random_color()
#     f_width = f.get_size()[0]

#     # Reset main menu and disable
#     # You also can set another menu, like a 'pause menu', or just use the same
#     # main_menu as the menu that will check all your input.
#     main_menu.disable()
#     main_menu.reset(1)

#     while True:

#         # Clock tick
#         clock.tick(60)

#         # Application events
#         playevents = pygame.event.get()
#         for e in playevents:
#             if e.type == QUIT:
#                 exit()
#             elif e.type == KEYDOWN:
#                 if e.key == K_ESCAPE:
#                     if main_menu.is_disabled():
#                         main_menu.enable()

#                         # Quit this function, then skip to loop of main-menu on line 197
#                         return

#         # Pass events to main_menu
#         main_menu.mainloop(playevents)

#         # Continue playing
#         surface.fill(bg_color)
#         surface.blit(f, ((WINDOW_SIZE[0] - f_width) / 2, WINDOW_SIZE[1] / 2))
#         pygame.display.flip()


# def main_background():
#     """
#     Function used by menus, draw on background while menu is active.
    
#     :return: None
#     """
#     surface.fill(COLOR_BACKGROUND)


# # -----------------------------------------------------------------------------
# # PLAY MENU
# play_menu = pygameMenu.Menu(surface,
#                             bgfun=main_background,
#                             color_selected=COLOR_WHITE,
#                             font=pygameMenu.fonts.FONT_BEBAS,
#                             font_color=COLOR_BLACK,
#                             font_size=30,
#                             menu_alpha=100,
#                             menu_color=MENU_BACKGROUND_COLOR,
#                             menu_height=int(WINDOW_SIZE[1] * 0.6),
#                             menu_width=int(WINDOW_SIZE[0] * 0.6),
#                             onclose=PYGAME_MENU_DISABLE_CLOSE,
#                             option_shadow=False,
#                             title='Play menu',
#                             window_height=WINDOW_SIZE[1],
#                             window_width=WINDOW_SIZE[0]
#                             )
# # When pressing return -> play(DIFFICULTY[0], font)
# play_menu.add_option('Start', play_function, DIFFICULTY,
#                      pygame.font.Font(pygameMenu.fonts.FONT_FRANCHISE, 30))
# play_menu.add_selector('Select difficulty', [('Easy', 'EASY'),
#                                              ('Medium', 'MEDIUM'),
#                                              ('Hard', 'HARD')],
#                        onreturn=None,
#                        onchange=change_difficulty)
# play_menu.add_option('Return to main menu', PYGAME_MENU_BACK)

# # ABOUT MENU
# about_menu = pygameMenu.TextMenu(surface,
#                                  bgfun=main_background,
#                                  color_selected=COLOR_WHITE,
#                                  font=pygameMenu.fonts.FONT_BEBAS,
#                                  font_color=COLOR_BLACK,
#                                  font_size_title=30,
#                                  font_title=pygameMenu.fonts.FONT_8BIT,
#                                  menu_color=MENU_BACKGROUND_COLOR,
#                                  menu_color_title=COLOR_WHITE,
#                                  menu_height=int(WINDOW_SIZE[1] * 0.6),
#                                  menu_width=int(WINDOW_SIZE[0] * 0.6),
#                                  onclose=PYGAME_MENU_DISABLE_CLOSE,
#                                  option_shadow=False,
#                                  text_color=COLOR_BLACK,
#                                  text_fontsize=20,
#                                  title='About',
#                                  window_height=WINDOW_SIZE[1],
#                                  window_width=WINDOW_SIZE[0]
#                                  )
# for m in ABOUT:
#     about_menu.add_line(m)
# about_menu.add_line(PYGAMEMENU_TEXT_NEWLINE)
# about_menu.add_option('Return to menu', PYGAME_MENU_BACK)

# # MAIN MENU
# main_menu = pygameMenu.Menu(surface,
#                             bgfun=main_background,
#                             color_selected=COLOR_WHITE,
#                             font=pygameMenu.fonts.FONT_BEBAS,
#                             font_color=COLOR_BLACK,
#                             font_size=30,
#                             menu_alpha=100,
#                             menu_color=MENU_BACKGROUND_COLOR,
#                             menu_height=int(WINDOW_SIZE[1] * 0.6),
#                             menu_width=int(WINDOW_SIZE[0] * 0.6),
#                             onclose=PYGAME_MENU_DISABLE_CLOSE,
#                             option_shadow=False,
#                             title='Main menu',
#                             window_height=WINDOW_SIZE[1],
#                             window_width=WINDOW_SIZE[0]
#                             )
# main_menu.add_option('Play', play_menu)
# main_menu.add_option('About', about_menu)
# main_menu.add_option('Quit', PYGAME_MENU_EXIT)

# # -----------------------------------------------------------------------------
# # Main loop
# while True:

#     # Tick
#     clock.tick(60)

#     # Application events
#     events = pygame.event.get()
#     for event in events:
#         if event.type == QUIT:
#             exit()

#     # Main menu
#     main_menu.mainloop(events)

#     # Flip surface
#     pygame.display.flip()

# coding=utf-8
"""
EXAMPLE 1
Example file, timer clock with in-menu options.
Copyright (C) 2017-2018 Pablo Pizarro @ppizarror
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

# Import pygame and libraries
from random import randrange
import datetime
import os
import pygame
from pygame.locals import *

# Import pygameMenu
import pygameMenu
from pygameMenu.locals import *

# -----------------------------------------------------------------------------
# Constants and global variables
ABOUT = ['PygameMenu {0}'.format(pygameMenu.__version__),
         'Author: {0}'.format(pygameMenu.__author__),
         PYGAMEMENU_TEXT_NEWLINE,
         'Email: {0}'.format(pygameMenu.__email__)]
COLOR_BLUE = (12, 12, 200)
COLOR_BACKGROUND = [128, 0, 128]
COLOR_WHITE = (255, 255, 255)
FPS = 60
H_SIZE = 540  # Height of window size
HELP = ['Press ESC to enable/disable Menu',
        'Press ENTER to access a Sub-Menu or use an option',
        'Press UP/DOWN to move through Menu',
        'Press LEFT/RIGHT to move through Selectors']
W_SIZE = 630  # Width of window size

# -----------------------------------------------------------------------------
# Init pygame
pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Write help message on console
for m in HELP:
    print(m)

# Create window
surface = pygame.display.set_mode((W_SIZE, H_SIZE))
pygame.display.set_caption('PygameMenu example')

# Main timer and game clock
clock = pygame.time.Clock()
timer = [0.0]
dt = 1.0 / FPS
timer_font = pygame.font.Font(pygameMenu.fonts.FONT_NEVIS, 100)


# -----------------------------------------------------------------------------
def mainmenu_background():
    """
    Background color of the main menu, on this function user can plot
    images, play sounds, etc.
    """
    surface.fill((40, 0, 40))


def reset_timer():
    """
    Reset timer
    """
    timer[0] = 0


def change_color_bg(c, **kwargs):
    """
    Change background color
    
    :param c: Color tuple
    """
    if c == (-1, -1, -1):  # If random color
        c = (randrange(0, 255), randrange(0, 255), randrange(0, 255))
    if kwargs['write_on_console']:
        print('New background color: ({0},{1},{2})'.format(*c))
    COLOR_BACKGROUND[0] = c[0]
    COLOR_BACKGROUND[1] = c[1]
    COLOR_BACKGROUND[2] = c[2]


# -----------------------------------------------------------------------------
# Timer menu
timer_menu = pygameMenu.Menu(surface,
                             dopause=False,
                             font=pygameMenu.fonts.FONT_FRANCHISE,
                             menu_alpha=85,
                             menu_color=(0, 0, 0),  # Background color
                             menu_color_title=(0, 0, 0),
                             menu_height=480,
                             menu_width=600,
                             onclose=PYGAME_MENU_RESET,  # If this menu closes (press ESC) back to main
                             title='Timer Menu',
                             title_offsety=5,  # Adds 5px to title vertical position
                             window_height=H_SIZE,
                             window_width=W_SIZE
                             )
timer_menu.add_option('Reset timer', reset_timer)

# Adds a selector (element that can handle functions)
timer_menu.add_selector('Change bgcolor',
                        # Values of selector, call to change_color_bg
                        [('Random', (-1, -1, -1)),
                         ('Default', (128, 0, 128)),
                         ('Black', (0, 0, 0)),
                         ('Blue', COLOR_BLUE)],
                        onchange=None,  # Action when changing element with left/right
                        onreturn=change_color_bg,  # Action when pressing return on a element
                        default=1,  # Optional parameter that sets default item of selector
                        write_on_console=True  # Optional parametrs to change_color_bg function
                        )
timer_menu.add_option('Return to Menu', PYGAME_MENU_BACK)
timer_menu.add_option('Close Menu', PYGAME_MENU_CLOSE)

# -----------------------------------------------------------------------------
# Help menu
help_menu = pygameMenu.TextMenu(surface,
                                dopause=False,
                                font=pygameMenu.fonts.FONT_FRANCHISE,
                                menu_color=(30, 50, 107),  # Background color
                                menu_color_title=(120, 45, 30),
                                onclose=PYGAME_MENU_DISABLE_CLOSE,  # Pressing ESC button does nothing
                                title='Help',
                                window_height=H_SIZE,
                                window_width=W_SIZE
                                )
help_menu.add_option('Return to Menu', PYGAME_MENU_BACK)
for m in HELP:
    help_menu.add_line(m)

# -----------------------------------------------------------------------------
# About menu
about_menu = pygameMenu.TextMenu(surface,
                                 dopause=False,
                                 font=pygameMenu.fonts.FONT_FRANCHISE,
                                 font_size_title=30,
                                 font_title=pygameMenu.fonts.FONT_8BIT,
                                 menu_color_title=COLOR_BLUE,
                                 onclose=PYGAME_MENU_DISABLE_CLOSE,  # Disable menu close (ESC button)
                                 text_fontsize=20,
                                 title='About',
                                 window_height=H_SIZE,
                                 window_width=W_SIZE
                                 )
about_menu.add_option('Return to Menu', PYGAME_MENU_BACK)
for m in ABOUT:
    about_menu.add_line(m)
about_menu.add_line(PYGAMEMENU_TEXT_NEWLINE)

# -----------------------------------------------------------------------------
# Main menu, pauses execution of the application
menu = pygameMenu.Menu(surface,
                       bgfun=mainmenu_background,
                       enabled=False,
                       font=pygameMenu.fonts.FONT_FRANCHISE,
                       menu_alpha=90,
                       onclose=PYGAME_MENU_CLOSE,
                       title='Main Menu',
                       title_offsety=5,
                       window_height=H_SIZE,
                       window_width=W_SIZE
                       )
menu.add_option(timer_menu.get_title(), timer_menu)  # Add timer submenu
menu.add_option(help_menu.get_title(), help_menu)  # Add help submenu
menu.add_option(about_menu.get_title(), about_menu)  # Add about submenu
menu.add_option('Exit', PYGAME_MENU_EXIT)  # Add exit function

# -----------------------------------------------------------------------------
# Main loop
while True:

    # Tick clock
    clock.tick(60)
    timer[0] += dt

    # Paint background
    surface.fill(COLOR_BACKGROUND)

    # Application events
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                menu.enable()

    # Draw timer
    time_string = str(datetime.timedelta(seconds=int(timer[0])))
    time_blit = timer_font.render(time_string, 1, COLOR_WHITE)
    time_blit_size = time_blit.get_size()
    surface.blit(time_blit, (
        W_SIZE / 2 - time_blit_size[0] / 2, H_SIZE / 2 - time_blit_size[1] / 2))

    # Execute main from principal menu if is enabled
    menu.mainloop(events)

    # Flip surface
    pygame.display.flip()