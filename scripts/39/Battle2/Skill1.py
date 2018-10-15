import pygame
from pygame.locals import *
import sys

class Skill:
    def __init__(self, TargetObject, kwargs):
        self.GetSource(TargetObject)
        self.SetOptions(kwargs)

    def GetSource(self, TargetObject):
        self.TargetObject = TargetObject

    def SetOptions(self, kwargs):
        self.options = {
            "ratio" : 1,
            "CmdAnimNameList" : "jump"
            }
        if kwargs != None:
            self.options.update(kwargs)

    def Start(self):
        pass

    def Update(self):
        pass

    def Main(self):
        pass
