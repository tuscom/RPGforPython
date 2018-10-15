import pygame
from pygame.locals import *
import sys

class MoveMode:
    def __init__(self, MainClass):
        self.GetSource(MainClass)
        self.FunctionParameter()

    def GetSource(self, MainClass):
        self.MainClass = MainClass
        self.Stage = MainClass.Stage

    def FunctionParameter(self):
        self.Action = self.Start
        self.AllObjects = []

    def Main(self):
        if self.Action != None:
            self.Action()

    def Start(self):
        self.SetStage()
        self.Action = self.Update

    def SetStage(self):
        self.TestStage = self.Stage(self.MainClass, None)

    def Update(self):
        self.MainOfAllObjects()
        self.TestStage.Main()

    def MainOfAllObjects(self):
        list(map(lambda ObjClass : ObjClass.Main(), self.AllObjects))