import pygame
from pygame.locals import *
import sys

from Source import ObjectClass

class FieldCharacter(ObjectClass):
    def __init__(self, MainClass, kwargs):
        self.GetSource(MainClass)
        self.SetOptions(kwargs)
        self.SetParameter()

        self.OnInstanceFunc()

        self.Action = self.Start

    def SetOptions(self, kwargs):
        self.options = {
            "name" : "名無し",
            "picturepath" : "../../../pictures/mon_016.bmp",
            "position" : pygame.math.Vector2(),
            "scale" : pygame.math.Vector2(100, 100),
            "speed" : 10,
            "hp" : 100
            }
        if kwargs != None:
            self.options.update(kwargs)

    def SetParameter(self):
        super().SetParameter()
        self.speed = self.options["speed"]
        self.hp = self.options["hp"]

    def Start(self):
        self.LoadMaterial()
        self.Action = self.Update

    def Update(self):
        self.HelperUpdate()
        self.Draw()
        self.BtnUpdate()

    #Others
    def SetHPbarPicture(self, HPbarPicture):
        self.HPbarPicture = HPbarPicture
