import sys
import pygame
import math
from Screenshotter import run, cropper

try:
    # for Python2
    from Tkinter import *
    import Tkinter, Tkconstants, tkFileDialog## notice capitalized T in Tkinter 
    
except ImportError:
    # for Python3
    from tkinter import filedialog
    from tkinter import *
    
global nodes
nodes = []
select_radius = 15
objects = []

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
           

            

def node_selection():
    # Initialize game and create a screen object.
    pygame.init()
    background = pygame.image.load("crop.png")
    imagerect = background.get_rect()
    screen = pygame.display.set_mode((1500, 700))
    modes = ["create", "select", "order"]
    mode_index = 0
    select_radius = 50
    n = 0
    selected = []
    pygame.display.set_caption("Node Selection")
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    screen.fill(WHITE)
    
 # Start the main loop for the game.
    while True:
        mode = modes[mode_index % len(modes)]
        #set mouse type
        if mode == "move":
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)
        elif mode == "select":
            pygame.mouse.set_cursor(*pygame.cursors.diamond)
        else:
            pygame.mouse.set_cursor(*pygame.cursors.arrow)
            
        #check events
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN: #This checks for the mouse press event
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
                        
                    
                                   
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    mode_index += 1
                    print("Mode: " + modes[mode_index % len(modes)])
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    for node in nodes:
                        if node.is_selected:
                            nodes.remove(node)
                if event.key == pygame.K_RETURN:
                    ordered_nodes = [nodes[0].get_pos()]
                    nodes_copy = nodes
                    node = nodes[0]
                    while len(nodes_copy) > 0:
                        ordered_nodes.append(node.next_node.get_pos())
                        nodes.remove(node)
                        node = node.next_node
                        
                    
                    print(ordered_nodes)
                    
                    cropper(ordered_nodes)
                    background = pygame.image.load("out.png")
                        
                        
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        #Draw objects
        screen.fill((255,255,255))
        screen.blit(background, imagerect)
        for node in nodes:
            #print(screen)
            node.draw(screen)
        
        # Make the most recently drawn screen visible.
        pygame.display.flip()
        pygame.display.update()
run()

node_selection()
#node_selection()