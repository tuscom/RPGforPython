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

        self.Window = Window(self.screen)

    def Main(self):
        pygame.display.set_caption(self.windowName)

        while True:
            self.screen.fill(self.pageColor)

            self.Window.Update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

class Window:
    def __init__(self, screen):
        self.screen = screen
        self.player = pygame.image.load("../pictures/mon_016.bmp")
        self.Update = self.TestWindow

    def TestWindow(self):
        self.screen.blit(self.player, (0, 0))

test().Main()