import pygame
from pygame.locals import *
import sys

from testHelper import Character, Grid, KeyBoard, Time

class test:
    def __init__(self):
        #parameter
        self.windowSize = [1500, 800]
        self.pageColor = (255,255,255)
        self.squareSize = 32
        self.windowName = "test"
        self.screen = pygame.display.set_mode(self.windowSize)
        self.KeyBoard = KeyBoard()
        self.Time = Time()
        #順序注意
        self.Player = Character(self, picturepath="../../pictures/mon_016.bmp", mode="player")
        self.Window = Window(self)
        self.Grid = Grid(self)
        

    def Main(self):
        pygame.display.set_caption(self.windowName)
        pygame.init()

        while True:
            self.EarlyUpdate()

            self.Window.Update()
            self.Grid.Update()

            self.LaterUpdate()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

    def EarlyUpdate(self):
        self.screen.fill(self.pageColor)
        self.KeyBoard.EarlyUpdate()
        self.Time.EarlyUpdate()

    def LaterUpdate(self):
        self.KeyBoard.LaterUpdate()


class Window:
    def __init__(self, MainClass):
        self.mainClass = MainClass
        self.screen = self.mainClass.screen
        self.Update = self.TestWindow

        self.player = self.mainClass.Player

    def TestWindow(self):
        self.player.Update()

test().Main()