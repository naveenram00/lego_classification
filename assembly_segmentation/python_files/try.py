#-------------- imports --------------
import pygame
from pygame.locals import *
import cv2
import numpy as np
import sys
import os
import pygameMenu
from Screenshotter import cropper
from pygameMenu.locals import *
import math
from PIL import Image, ImageChops
import numpy as np

#--------------- mainmenu_background --------------------

def mainmenu_background():
    """
    Background color of the main menu, on this function user can plot
    images, play sounds, etc.
    """
    screen.fill((40, 0, 40))

#----------------- help information ----------------------

HELP1 = [ '       ',
          'Currently in Object Capture',
          '+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+',
          'Press SPACEBAR to capture camera image',
          'Escape this window by EXIT in menu',
          '       ' ]

HELP2 = [ 'Currently in Node Selection',
          '+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+',
          'Press LEFT/RIGHT to change modes',
          '  Create: CLICK to create nodes',
          '  Select: Delete nodes with BACKSPACE',
          '  Order: CLICK nodes to connect them',
          '  Move: CLICK to move node location' ]

#--------------- part identification instructions --------------------

global part
parts = {0 : "Red 2x1", 
         1 : "Grey 4x1", 
         2 : "Black Tire", 
         3 : "Grey 8x2", 
         4 : "Grey 6x2", 
         5 : "Yellow Corner", 
         6 : "Yellow Head", 
         7 : "Grey Handle", 
         8 : "Yellow Axle", 
         9 : "Blue Stud"}
global instructions
instructions = {0 : "replace with newer design (part 3004)", 
                1 : "needs cleaning/maintanence", 
                2 : "check tire pressure", 
                3 : "replace with two 3x2s", 
                4 : "replace with two 4x2s", 
                5 : "reinforce with more brackets", 
                6 : "add hat", 
                7 : "replace with more visible color",
                8 : "check allignment", 
                9 : "remove and reapply"}

#--------------- starting information -------------------- 

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

cam = cv2.VideoCapture(0)

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'

for m in HELP1:
    print(m)
for m in HELP2:
    print(m)
    
pygame.display.set_caption("Screencapture")
screen = pygame.display.set_mode([640,480])

#-------------- node class --------------------

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

#----------- distance equation --------------------

def distance(p0, p1):
        return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

#------------ select function ------------------
    
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

#-------------- text objects -------------------

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

#--------------- message display -------------------

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText, BLACK)
    TextRect.center = ((640/2),(505))
    screen.blit(TextSurf, TextRect)
    
#---------------- button settings -----------------

def buttons(screen):
    largeText = pygame.font.Font('freesansbold.ttf', 50)
    smallText = pygame.font.Font("freesansbold.ttf",20)
    mouse = pygame.mouse.get_pos()
    if 0 < mouse[0] < 100 and 480+50 > mouse[1] > 480:
        pygame.draw.rect(screen, L_PURPLE,(0,480,100,50))
    else:
        pygame.draw.rect(screen, PURPLE,(0,480,100,50))
    if 540 < mouse[0] < 640 and 480+50 > mouse[1] > 480:
        pygame.draw.rect(screen, L_PURPLE,(540,480,100,50))
    else:
        pygame.draw.rect(screen, PURPLE,(540,480,100,50)) 
       
    TextSurf, TextRect = text_objects(modes[mode_index%len(modes)].upper(), largeText, BLACK)
    
    TextRect.center = ((640/2),(506))
    screen.blit(TextSurf, TextRect)    
    textSurf, textRect = text_objects("<", smallText, WHITE)
    textRect.center = ( (0+(100/2)), (480+(50/2)) )
    screen.blit(textSurf, textRect)
    textSurf, textRect = text_objects(">", smallText, WHITE)
    textRect.center = ( (540+(100/2)), (480+(50/2)) )
    screen.blit(textSurf, textRect)
        
#---------- polyrnn ---------------

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

#---------- first_sequence() -----------------

def first_sequence(screen):
    intro = True
    while intro == True:
        ret, frame = cam.read()
        screen.fill(WHITE)
        rect = pygame.Rect(0,0,640,480)
        sub = screen.subsurface(rect) 
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        print("cv2.cvtCOlor")
        frame = np.rot90(frame)
        print("np.rot90")
        frame = pygame.surfarray.make_surface(frame)
        screen.blit(frame, (0,0))
        pygame.display.update()
        events = pygame.event.get()    
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    pygame.image.save(sub, "crop.jpg")
                    intro = False
                if event.key == K_ESCAPE:
                    menu1.enable()

        
        menu1.mainloop(events)

        pygame.display.flip()
        
#--------- second_sequence() [broken] -----------------

def second_sequence():
    mode_index = 1000000
    pygame.display.set_caption("Node Selection")
    background = pygame.image.load("crop.jpg")
    imagerect = background.get_rect()
    screen = pygame.display.set_mode((640, 530))   # This line makes the stuttering 
    screen.fill(WHITE)
    #screen.blit(background, imagerect)
    n = 0
    select_radius = 60
    selected = []
    ending = True

    while ending == True:


        largeText = pygame.font.Font('freesansbold.ttf', 50)
        smallText = pygame.font.Font("freesansbold.ttf", 20)
        mouse = pygame.mouse.get_pos()
        pygame.draw.rect(screen, WHITE,(0,480,530,50))
        mode = modes[mode_index % len(modes)]
        #set mouse type
        if mode == "move":
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)
            
       #++++++++++++ select option +++++++++++++  
    
#         elif mode == "select":
#             pygame.mouse.set_cursor(*pygame.cursors.diamond)

       #++++++++++++ select option +++++++++++++ 
    
        elif mode == "order":
            pygame.mouse.set_cursor(*pygame.cursors.arrow)
        else:
            pygame.mouse.set_cursor(*pygame.cursors.tri_left)
        events = pygame.event.get()    
        for event in events:

            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()


            if event.type == pygame.MOUSEBUTTONDOWN: #This checks for the mouse press event


                if mouse[1] > 480:

                    if 0 < mouse[0] < 100:

                        print("Mode: " + modes[mode_index % len(modes)])
                        mode_index = abs(mode_index - 1)
                        print(mode_index)
                    elif 540 < mouse[0] < 640 :    
                        print("Mode: " + modes[mode_index % len(modes)])
                        mode_index += 1

                else:

                    if mode == "create":

                        nodes.append(Node(x_init=pygame.mouse.get_pos()[0], y_init=pygame.mouse.get_pos()[1])) #Gets the mouse position
                        #pygame.draw.circle(screen, BLUE, (nodes[n]), 4, 0) #Draws a circle at the mouse position!
                        #print(circ[n])
                        #n += 1


                    if mode == "select":
                        for node in nodes:
                            print(node.is_selected)
                        select_node(pygame.mouse.get_pos(), screen)

                    if mode == "order":
                        selected = 0
                        for node in nodes:
                            if node.is_selected:
                                selected = node
                        if selected == 0:
                            select_node(pygame.mouse.get_pos(), screen)
                        else:
                            selected.next_node = select_node(pygame.mouse.get_pos(), screen)

                    if mode == "move":

                        node_selected = False

                        for node in nodes:
                            if node.is_selected:
                                node_selected = True
                        if not node_selected:
                            select_node(pygame.mouse.get_pos(), screen)
                        else:

                            for node in nodes:
                                if node.is_selected:

                                    node.move_to(pygame.mouse.get_pos())
                                    node.deselect()


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    mode_index += 1
                    print("Mode: " + modes[mode_index % len(modes)])
                elif event.key == pygame.K_LEFT:
                    mode_index = abs(mode_index-1)
                    print("Mode: " + modes[mode_index % len(modes)])
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    for node in nodes:
                        if node.is_selected:

                            nn = node.next_node
                            pn = None

                            for node2 in nodes:
                                if node2.next_node == node:
                                    pn = node2
                            if (nn == None and pn == None):
                                nodes.remove(node)
                            elif ((not nn == None) and pn == None):
                                node.next_node = None
                                nodes.remove(node)
                                nn.is_selected = True
                            elif ((not pn == None) and nn == None):
                                pn.next_node = None
                                nodes.remove(node)
                            else:
                                pn.next_node = nn
                                nodes.remove(node)
                                nn.is_selected = True
                if event.key == pygame.K_ESCAPE:
                    menu2.enable()
                if event.key == pygame.K_RETURN:
                    print(nodes)
    #                     for node in nodes:
    #                         if node.next_node == None:
    #                             nodes.remove(node)
    #                     print(nodes)

                    nodes_copy = [x for x in nodes if not x.next_node == None]

                    print(nodes_copy) 
                    for node in nodes_copy:
                        print(node.next_node)

                    ordered_nodes = [nodes_copy[0].get_pos()]
                    #nodes_copy = nodes
                    node = nodes_copy[0]
                    while len(nodes_copy) > 0:
                        ordered_nodes.append(node.next_node.get_pos())
                        nodes_copy.remove(node)
                        node = node.next_node
                    del nodes[:]
                    nodes.extend(nodes_copy)


    #                     print(ordered_nodes)

                    cropper(ordered_nodes)
                    background = pygame.image.load("out.png")

                    sys.path.append("/usr/src/lego_classification/part_recognition")
                    import lego_class_module as classifier
                    part_number = classifier.classify("out.png")[0]
                    print ("--------------")
                    print ("Part Number: " + str(part_number))
                    print("Part: " + parts[part_number])
                    print("Repair Instructions: " + instructions[part_number])

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((255,255,255))
        screen.blit(background, imagerect)
        buttons(screen)
        for node in nodes:
            #print(screen)
            node.draw(screen)

        menu2.mainloop(events)
        pygame.display.flip()
        pygame.display.update()

#--------------- menu settings ----------------------

menu1 = pygameMenu.TextMenu(screen,
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
                       window_height=int(H_SIZE - 110), # Higher number moves menu up
                       window_width=int(W_SIZE + 43) # Higher number moves menu right
                       )

menu2 = pygameMenu.TextMenu(screen,
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
                       window_width=int(W_SIZE + 43)
                       )

#-------------- menu extras ----------------------

for m in HELP1:
    menu1.add_line(m)
for m in HELP2:
    menu2.add_line(m)

menu1.add_option('Exit', PYGAME_MENU_EXIT)  # Add exit function
menu2.add_option('Exit', PYGAME_MENU_EXIT)

#-----------------  init1()  ------------------

def init1():
    global modes
    modes = ["create", "select", "order", "move"]
    global mode_index
    mode_index = 1000000 
    select_radius = 60
    n = 0
    selected = []

#------------------ start of run ------------------

init1()            
first_sequence(screen)
#segment_screenshot()

#----------second_sequence()--------------------------------------

mode_index = 1000000
pygame.display.set_caption("Node Selection")
background = pygame.image.load("crop.jpg")
imagerect = background.get_rect()
screen = pygame.display.set_mode((640, 530))   # This line makes the stuttering 
screen.fill(WHITE)
#screen.blit(background, imagerect)
n = 0
select_radius = 60
selected = []
ending = True

    # ============== while loop =====================
    
while ending == True:


    largeText = pygame.font.Font('freesansbold.ttf', 50)
    smallText = pygame.font.Font("freesansbold.ttf", 20)
    mouse = pygame.mouse.get_pos()
    pygame.draw.rect(screen, WHITE,(0,480,530,50))
    mode = modes[mode_index % len(modes)]
    
    # -=-=-=-=-=-=- set mouse type -=-=-=-=-=-=-=-=-=-
    
    if mode == "move":
        pygame.mouse.set_cursor(*pygame.cursors.broken_x)
        
    #++++++++++++ select option +++++++++++++  
    
    elif mode == "select":
        pygame.mouse.set_cursor(*pygame.cursors.diamond)

    #++++++++++++ select option +++++++++++++ 
    
    elif mode == "order":
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
    else:
        pygame.mouse.set_cursor(*pygame.cursors.tri_left)
        
    # -=-=-=-=-=-=-=- set mouse type -=-=-=-=-=-=-=-=-=-
    
    events = pygame.event.get() 
    
    # ==-==-==-==-== mouse and button events ==-==-==-==-==
    
    for event in events:

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()


        if event.type == pygame.MOUSEBUTTONDOWN: #This checks for the mouse press event


            if mouse[1] > 480:

                if 0 < mouse[0] < 100:

                    print("Mode: " + modes[mode_index % len(modes)])
                    mode_index = abs(mode_index - 1)
                    print(mode_index)
                elif 540 < mouse[0] < 640 :    
                    print("Mode: " + modes[mode_index % len(modes)])
                    mode_index += 1

            else:

                if mode == "create":

                    nodes.append(Node(x_init=pygame.mouse.get_pos()[0], y_init=pygame.mouse.get_pos()[1])) #Gets the mouse position
                    #pygame.draw.circle(screen, BLUE, (nodes[n]), 4, 0) #Draws a circle at the mouse position!
                    #print(circ[n])
                    #n += 1

        #++++++++++++ select option +++++++++++++ 
        
                if mode == "select":
                    for node in nodes:
                        print(node.is_selected)
                    select_node(pygame.mouse.get_pos(), screen)

        #++++++++++++ select option +++++++++++++ 

                if mode == "order":
                    selected = 0
                    for node in nodes:
                        if node.is_selected:
                            selected = node
                    if selected == 0:
                        select_node(pygame.mouse.get_pos(), screen)
                    else:
                        selected.next_node = select_node(pygame.mouse.get_pos(), screen)

                if mode == "move":

                    node_selected = False

                    for node in nodes:
                        if node.is_selected:
                            node_selected = True
                    if not node_selected:
                        select_node(pygame.mouse.get_pos(), screen)
                    else:

                        for node in nodes:
                            if node.is_selected:

                                node.move_to(pygame.mouse.get_pos())
                                node.deselect()


        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_RIGHT:
                mode_index += 1
                print("Mode: " + modes[mode_index % len(modes)])
            elif event.key == pygame.K_LEFT:
                mode_index = abs(mode_index-1)
                print("Mode: " + modes[mode_index % len(modes)])
            if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                for node in nodes:
                    if node.is_selected:
                        
                        nn = node.next_node
                        pn = None

                        for node2 in nodes:
                            if node2.next_node == node:
                                pn = node2
                        if (nn == None and pn == None):
                            nodes.remove(node)
                        elif ((not nn == None) and pn == None):
                            node.next_node = None
                            nodes.remove(node)
                            nn.is_selected = True
                        elif ((not pn == None) and nn == None):
                            pn.next_node = None
                            nodes.remove(node)
                        else:
                            pn.next_node = nn
                            nodes.remove(node)
                            nn.is_selected = True
            if event.key == pygame.K_ESCAPE:
                menu2.enable()
                
            if event.key == pygame.K_RETURN:
                print(nodes)

                nodes_copy = [x for x in nodes if not x.next_node == None]

                print(nodes_copy) 
                for node in nodes_copy:
                    print(node.next_node)

                ordered_nodes = [nodes_copy[0].get_pos()]
                #nodes_copy = nodes
                node = nodes_copy[0]
                while len(nodes_copy) > 0:
                    ordered_nodes.append(node.next_node.get_pos())
                    nodes_copy.remove(node)
                    node = node.next_node
                del nodes[:]
                nodes.extend(nodes_copy)
                cropper(ordered_nodes)
                
      # ==-==-==-==-== mouse and button events ==-==-==-==-==
    
      # =========== Part Identifier =============
    
                background = pygame.image.load("out.png")
                sys.path.append("/usr/src/lego_classification/part_recognition")
                import lego_class_module as classifier
                part_number = classifier.classify("out.png")[0]
                print ("--------------")
                print ("Part Number: " + str(part_number))
                print("Part: " + parts[part_number])
                print("Repair Instructions: " + instructions[part_number])
                
      # ============ Part Identifier =============
    
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    screen.fill((255,255,255))
    screen.blit(background, imagerect)
    buttons(screen)
    for node in nodes:
        #print(screen)
        node.draw(screen)
        
    menu2.mainloop(events)
    pygame.display.flip()
    pygame.display.update()
# ============== while loop =====================

#-------------second_sequence()----------------------------------
