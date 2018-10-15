import pygame
from pygame.locals import *
import sys

class Helper:
    def __init__(self, MainClass):
        self.GetSource(MainClass)
        self.ProgramParameter()
        self.GridLineParameter()
        self.KeyBoardParameter()

    def GetSource(self, MainClass):
        self.MainClass = MainClass
        self.screen = MainClass.screen

    def ProgramParameter(self):
        self.Action = self.Start

    def GridLineParameter(self):
        self.gridLineColor = pygame.Color("BLACK")
        self.noOfGridLine = pygame.math.Vector2(self.MainClass.windowSize[0]/self.MainClass.squareSize, self.MainClass.windowSize[1]/self.MainClass.squareSize)

    def KeyBoardParameter(self):
        #key
        self.nowPressed = pygame.key.get_pressed()
        self.previousPressed = self.nowPressed

        #left, right, up and down
        self.intHorizontalKey = self.nowPressed[K_RIGHT] - self.nowPressed[K_LEFT]
        self.intVerticalKey = self.nowPressed[K_UP] - self.nowPressed[K_DOWN]

    #Main
    def Main(self):
        if self.Action != None:
            self.Action()

    #Start系
    def Start(self):
        self.Action = self.Update

    #Update系
    def Update(self):
        self.KeyBoardUpdate()

    def KeyBoardUpdate(self):
        self.previousPressed = self.nowPressed

        #key
        self.nowPressed = pygame.key.get_pressed()

        #left, right, up, down
        self.intHorizontalKey = self.nowPressed[K_RIGHT] - self.nowPressed[K_LEFT]
        self.intVerticalKey = self.nowPressed[K_UP] - self.nowPressed[K_DOWN]

    def DrawGridLine(self):
        for i in range(int(self.noOfGridLine.x)):
            pygame.draw.line(self.screen, self.gridLineColor, ((i+1)*self.MainClass.squareSize, 0), ((i+1)*self.MainClass.squareSize, self.MainClass.windowSize[1]))

        for i in range(int(self.noOfGridLine.y)):
            pygame.draw.line(self.screen, self.gridLineColor, (0, (i+1)*self.MainClass.squareSize), (self.MainClass.windowSize[0], (i+1)*self.MainClass.squareSize))


    #Other系
    def WorldToGridPos(self, worldPos):
        remainder = pygame.math.Vector2(worldPos.x%self.MainClass.squareSize, worldPos.y%self.MainClass.squareSize)
        return worldPos - remainder

    def MakeArea(self, fromV2, toV2):
        result = []
        posV2 = toV2 - fromV2
        noOfArea = int(posV2.x * posV2.y)

        for i in range(noOfArea):
            x = i%posV2.x * self.MainClass.squareSize
            y = i//posV2.x * self.MainClass.squareSize
            pointV2 = pygame.math.Vector2(x, y)
            
            result.append(pointV2)

        return result

    def ScaledPicture(picturepath, size=(100, 100)):
        picture = pygame.transform.scale(pygame.image.load(picturepath).convert_alpha(), size)
        return picture

