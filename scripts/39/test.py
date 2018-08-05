import pygame
from pygame.locals import *
import sys

from testHelper import Character, Grid

class test:
    def __init__(self):
        #parameter
        self.windowSize = [1500, 800]
        self.pageColor = (255,255,255)
        self.squareSize = 32
        self.windowName = "test"
        self.screen = pygame.display.set_mode(self.windowSize)


        self.Player = Character(self, picturepath="../../pictures/mon_016.bmp", mode="player")
        self.Window = Window(self)
        self.Grid = Grid(self)

    def Main(self):
        pygame.display.set_caption(self.windowName)

        while True:
            self.screen.fill(self.pageColor)

            self.Window.Update()
            self.Grid.Update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

class Window:
    def __init__(self, MainClass):
        self.mainClass = MainClass
        self.screen = self.mainClass.screen
        self.Update = self.TestWindow

        self.player = self.mainClass.Player

    def TestWindow(self):
        self.player.Update()

test().Main()