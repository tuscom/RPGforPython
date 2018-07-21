import pygame
from pygame.locals import *
import sys

class test:
    def __init__(self):
        #parameter
        self.windowSize = [1500, 800]
        self.pageColor = (200,200,200)
        self.windowName = "test"
        self.screen = pygame.display.set_mode(self.windowSize)

    def Main(self):
        pygame.display.set_caption(self.windowName)

        while True:
            self.screen.fill(self.pageColor)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

test().Main()