import sys
import pygame
import math
import os
from PIL import Image, ImageChops 
import numpy as np
from Screenshotter import run, cropper
#from resize import resize_square



# try:
#     # for Python2
#     from Tkinter import *
#     import tkFileDialog as filedialog
#     import Tkconstants, tkFileDialog## notice capitalized T in Tkinter 
    
# except ImportError:
#     # for Python3
#     from tkinter import filedialog
#     from tkinter import *
    

global nodes
nodes = []

select_radius = 15
objects = []

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (69, 61, 85)
L_PURPLE =(69,61, 150)
BLACK = (0, 0, 0)
global part
parts = {0 : "Red 2x1", 1 : "Grey 4x1", 2 : "Black Tire", 3 : "Grey 8x2", 4 : "Grey 6x2", 
        5 : "Yellow Corner", 6 : "Yellow Head", 7 : "Grey Handle", 8 : "Yellow Axle", 9 : "Blue Stud"}
global instructions
instructions = {0 : "replace with newer design (part 3004)", 1 : "needs cleaning/maintanence", 
        2 : "check tire pressure", 3 : "replace with two 3x2s", 4 : "replace with two 4x2s", 
        5 : "reinforce with more brackets", 6 : "add hat", 7 : "replace with more visible color",
        8 : "check allignment", 9 : "remove and reapply"}



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
    re.resize_square("crop.png", 530)
    re.resize_square("for_segmentation.png", 224)
    sys.path.append("/usr/src/lego_classification/polyrnn-pp/src")
    import polyrnn_module as pm
    poly = pm.segment_image("for_segmentation.jpg")
    l, w = 530, 530

    y_offset = 640-530/2
    for point in poly:
        nodes.append(Node(int(point[0]*l), int((point[1]*w))))

def init():
    # Initialize game and create a screen object.
    pygame.init()
    background = pygame.image.load("crop.jpg")
    imagerect = background.get_rect()
    screen = pygame.display.set_mode((640, 530))
    global modes
    modes = ["create", "select", "order", "move"]
    global mode_index
    mode_index = 0 
    select_radius = 60
    n = 0
    selected = []
    pygame.display.set_caption("Node Selection")

    screen.fill(WHITE)

 # Start the main loop for the game.
    while True:
        #for event in pygame.event.get():
        mode = modes[mode_index % len(modes)]
        #set mouse type
        if mode == "move":
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)
        elif mode == "select":
            pygame.mouse.set_cursor(*pygame.cursors.diamond)
        elif mode == "order":
            pygame.mouse.set_cursor(*pygame.cursors.arrow)
        else:
            pygame.mouse.set_cursor(*pygame.cursors.tri_left)
            
        for event in pygame.event.get():
            
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()


            if event.type == pygame.MOUSEBUTTONDOWN: #This checks for the mouse press event

                
                if mouse[1] > 480:
                    
                    if 0 < mouse[0] < 100:
                        #pygame.draw.rect(screen, L_PURPLE,(0,480,100,50))
                        print("Mode: " + modes[mode_index % len(modes)])
                    elif 540 < mouse[0] < 640 :    
                        #pygame.draw.rect(screen, L_PURPLE,(540,480,100,50))
                        mode_index += 1

                else:
                    #pygame.draw.rect(screen, PURPLE,(0,480,100,50))
                    #pygame.draw.rect(screen, PURPLE,(540,480,100,50))
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

    #                             if selected == 0:
    #                                 select_node(pygame.mouse.get_pos(), screen)
    #                             else:
    #                                 selected.next_node = select_node(pygame.mouse.get_pos(), screen)



                                   
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
                            nodes.remove(node)
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
        
        #Draw objects
        screen.fill((255,255,255))
        screen.blit(background, imagerect)
        buttons(screen)
        for node in nodes:
            #print(screen)
            node.draw(screen)
        
        
        # Make the most recently drawn screen visible.
        pygame.display.flip()
        pygame.display.update()



run()
segment_screenshot()
print("test")
init()

#resize_square("out.png", 224)

c#lassifier.classify("/usr/src/lego_classification/assembly_recognition/python_files/out.png")
#node_selection()cd -
