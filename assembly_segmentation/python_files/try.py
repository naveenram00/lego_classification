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
screen = pygame.display.set_mode([630,540])

#-----------------------------------------------

class Node:
    def __init__(self,x_init,y_init):
        self.x = x_init
        self.y = y_init
        self.is_selected = False
        self.next_node = None
    
    def deselect(self):
        self.is_selected = False
    def select(self):
        self.is_selected = True
        
    def get_pos(self):
        return (self.x, self.y)
    
    def shift(self, x, y):
        self.x += x
        self.y += y
    
    def move_to(self, pos):
        self.x = pos[0]
        self.y = pos[1]
    
    def draw(self, screen):
        if self.is_selected:
            pygame.draw.circle(screen, (0, 255, 255), (self.x, self.y), 6, 0)
        else:
            pygame.draw.circle(screen, (0, 5, 255), (self.x, self.y), 4, 0)
        if self.next_node != None:
            pygame.draw.line(screen, (50, 5, 255), (self.x, self.y), self.next_node.get_pos(), 3)
            

    def __repr__(self):
        return "".join(["Node(", str(self.x), ",", str(self.y), ")"])

def distance(p0, p1):
        return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def select_node(pos, screen):
    selected = None
    print(nodes)
    for node in nodes:
        node.deselect()
        print(distance(pos, node.get_pos()))
        if distance(pos, node.get_pos()) < select_radius:
            #set selected to nearest node
            selected = node
            selected.select()
            print("test")
    return selected

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText, BLACK)
    TextRect.center = ((640/2),(505))
    screen.blit(TextSurf, TextRect)

def buttons(screen):
#check events
    #for event in pygame.event.get():
        largeText = pygame.font.Font('freesansbold.ttf', 50)
        TextSurf, TextRect = text_objects(modes[mode_index%len(modes)].upper(), largeText, BLACK)
        TextRect.center = ((640/2),(506))
        screen.blit(TextSurf, TextRect)
        smallText = pygame.font.Font("freesansbold.ttf",20)

        mouse = pygame.mouse.get_pos()
        #pygame.draw.rect(screen, BLACK,(550,450,100,50))
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


def segment_screenshot():
    import resize as re
    #re.resize_square("crop.png", 530)
    #re.resize_square("for_segmentation.png", 224)
    sys.path.append("/usr/src/lego_classification/polyrnn-pp/src")
    import polyrnn_module as pm
    poly = pm.segment_image("for_segmentation.jpg")
    l, w = 640, 640

    for point in poly:
        nodes.append(Node(int(point[0]*l), int((point[1]*w))))
    nodes[-1].next_node=nodes[0]
    for i in range(len(nodes)-1):
        nodes[i].next_node = nodes[i+1]

def init():
    # Initialize game and create a screen object.
#     pygame.init()
#         background = pygame.image.load("crop.jpg")
#         imagerect = background.get_rect()
#         screen = pygame.display.set_mode((640, 530))
    global modes
    modes = ["create", "select", "order", "move"]
    global mode_index
    mode_index = 0 
    select_radius = 60
    n = 0
    selected = []
#     pygame.display.set_caption("Node Selection")

    screen.fill(WHITE)

def first_sequence(frame):
    screen.fill([0,0,0])
    rect = pygame.Rect(0,0,630,480)
    sub = screen.subsurface(rect)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)
    screen.blit(frame, (0,0))
    pygame.display.update()

    events = pygame.event.get()    
    for event in events:
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                pygame.image.save(sub, "crop.png")
                second_sequence()
            if event.key == K_ESCAPE:
                menu.enable()

    menu.mainloop(events)

    pygame.display.flip()
            
def second_sequence():
    background = pygame.image.load("crop.jpg")
    imagerect = background.get_rect()
#     screen = pygame.display.set_mode((640, 530))
    pygame.display.update()
            
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

#-----------------------------------------------

try:
    while True:
        
        ret, frame = cam.read()
        
            
            
        first_sequence(frame)
        
#             screen.fill([0,0,0])
#             rect = pygame.Rect(0,0,630,480)
#             sub = screen.subsurface(rect)
#             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             frame = np.rot90(frame)
#             frame = pygame.surfarray.make_surface(frame)
#             screen.blit(frame, (0,0))
#             pygame.display.update()

#             events = pygame.event.get()    
#             for event in events:
#                 if event.type == KEYDOWN:
#                     if event.key == K_SPACE:
#                         pygame.image.save(sub, "crop.png")
                        
                        
#                     elif event.key == K_ESCAPE:
#                         menu.enable()

#             menu.mainloop(events)

#             pygame.display.flip()
            
        second_sequence()
            

#-----------------------------------------------

except KeyboardInterrupt:
    pygame.quit()
    cv2.destroyAllWindows()