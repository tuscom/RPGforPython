import pygame
from pygame.locals import *
import sys

import FieldCharacter1

class FieldCharacter(FieldCharacter1.FieldCharacter):
    def __init__(self, MainClass, kwargs):
        self.GetSource(MainClass)
        self.SetOptions(kwargs)
        self.SetParameter()

        self.OnInstanceFunc()
        self.SetObjAnimDic()

        self.Action = self.Start

    def Start(self):
        self.LoadMaterial()
        self.Action = self.Update

    def Update(self):
        self.HelperUpdate()
        self.Draw()
        self.BtnUpdate()
