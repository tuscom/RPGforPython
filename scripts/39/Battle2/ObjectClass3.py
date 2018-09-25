import pygame
from pygame.locals import *
import sys

import ObjectClass2

class ObjectClass(ObjectClass2.ObjectClass):
    def __init__(self, MainClass, kwargs):
        self.GetSource(MainClass)
        self.SetOptions(kwargs)
        self.ProgramParameter()

        self.OnInstanceFunc()
        self.SetObjAnimDic()

    def ProgramParameter(self):
        self.position = pygame.math.Vector2(self.options["position"])
        self.scale = pygame.math.Vector2(self.options["scale"])
        self.Action = self.Start

    def Start(self):
        self.LoadMaterial()
        self.Action = self.Update

    def Update(self):
        self.HelperUpdate()
        self.Draw()
        self.BtnUpdate()
