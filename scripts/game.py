import pygame
from pygame.locals import *
import sys

pygame.init()
screen=pygame.display.set_mode((400,600))
pygame.display.set_caption("test")

while(1):
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit(0)
