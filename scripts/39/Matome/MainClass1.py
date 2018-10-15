"""
・FirstUsedStartとAfterUsedStartは同時に実行
"""


import pygame
from pygame.locals import *
import sys

from Source1 import *

class MainClass:
    def __init__(self):
        self.WindowParameter()
        self.FunctionParameter()
        self.GetSource()
        self.SetMode()

        self.SetWindow()

    def WindowParameter(self):
        self.windowSize = [1500, 800]
        self.pageColor = (255,255,255)
        self.squareSize = 32
        self.windowName = "Matome"
        self.screen = pygame.display.set_mode(self.windowSize)

    def FunctionParameter(self):
        self.Action = self.Start

    def GetSource(self):
        self.HelperModule = Helper
        self.MoveModeObjectClass = MoveModeObjectClass
        self.ObjectClass = ObjectClass
        self.Stage = Stage
        self.OneCmdAnim = OneCmdAnim
        self.PieceAnimation = PieceAnimation

        self.Helper = Helper(self)
        self.AllAnimationController = AllAnimationController(self)

    def SetMode(self):
        self.MoveMode = MoveMode(self)
        self.Mode = self.MoveMode

    def SetWindow(self):
        pygame.init()
        pygame.display.set_caption(self.windowName)

    def Start(self):
        self.Action = self.Update

    def Update(self):
        self.Helper.Update()
        self.PygameEventUpdate()
        self.ModeUpdate()
        self.AllAnimationController.Update()

    def PygameEventUpdate(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

    def ModeUpdate(self):
        if self.Mode != None:
            self.Mode.Main()

    def Main(self):
        while True:
            if self.Action != None:
                self.Action()

if __name__ == "__main__":
    MainClass().Main()
