
# coding: utf-8

# In[1]:


import pygame
import pygame.camera
#import VideoCapture
from pygame.locals import *


pygame.init
pygame.camera.init()
pygame.display.init()
pygame.camera.list_cameras()
if pygame.display.get_init() == True:
    print("1")
    

size1= 200, 200
print (pygame.FULLSCREEN)
pygame.display.toggle_fullscreen()
#
pygame.display.set_mode(size1)

