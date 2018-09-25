import pygame
from pygame.locals import *
import sys

import FieldFamily1

class FieldFamily(FieldFamily1.FieldFamily):
    def __init__(self, MainClass, kwargs):
        self.GetSource(MainClass)
        self.SetOptions(kwargs)
        self.SetParameter()

        self.OnInstanceFunc()
        self.SetObjAnimDic()

        self.Action = self.Start

    def Start(self):
        self.LoadMaterial()
        self.AddContinueAnim("battle", "jump")
        self.Action = self.Update

    def Update(self):
        self.HelperUpdate()
        self.Draw()
        self.BtnUpdate()
