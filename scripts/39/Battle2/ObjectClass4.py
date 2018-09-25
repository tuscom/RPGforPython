import pygame
from pygame.locals import *
import sys

import ObjectClass3

class ObjectClass(ObjectClass3.ObjectClass):
    def __init__(self, MainClass, kwargs):
        self.GetSource(MainClass)
        self.SetOptions(kwargs)
        self.ProgramParameter()

        self.OnInstanceFunc()
        self.SetObjAnimDic()

    def SetOptions(self, kwargs):
        self.options = {
            "name" : "名無し",
            "picturepath" : "../../../pictures/mon_016.bmp",
            "position" : pygame.math.Vector2(),
            "scale" : pygame.math.Vector2(100, 100),
            "btnFunc" : None}
        if kwargs != None:
            self.options.update(kwargs)

    def ProgramParameter(self):
        super().ProgramParameter()
        self.btnFunc = self.options["btnFunc"]
        self.enable = True

    def Main(self):
        if self.Action != None and self.enable:
            self.Action()

    def Start(self):
        self.LoadMaterial()
        self.Action = self.Update

    def Update(self):
        self.HelperUpdate()
        self.Draw()
        self.BtnUpdate()

    def BtnUpdate(self):
        if self.BoolAction():
            self.OnClick()
            if self.btnFunc != None:
                self.btnFunc()