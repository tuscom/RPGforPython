import pygame
from pygame.locals import *
import sys

from Source import ObjectClass

class Button(ObjectClass):
    def __init__(self, MainClass, kwargs):
        self.GetSource(MainClass)
        self.SetOptions(kwargs)
        self.ProgramParameter()

        self.OnInstanceFunc()
        self.SetObjAnimDic()

    def ProgramParameter(self):
        super().ProgramParameter()
        self.font = pygame.font.Font(self.options["font"], int(self.scale.y * 0.9))
        self.words = self.font.render(self.options["text"], True, self.options["textColor"])

    def SetOptions(self, kwargs):
        self.options = {
            "name" : "名無し",
            "picturepath" : "../../../pictures/mon_016.bmp",
            "position" : pygame.math.Vector2(),
            "scale" : pygame.math.Vector2(100, 100),
            "font" : "../../../documents/IPAexfont00301/ipaexg.ttf",
            "text" : "ボタン",
            "textColor" : pygame.Color("BLACK")
            }
        if kwargs != None:
            self.options.update(kwargs)

    def Start(self):
        self.LoadMaterial()
        self.Action = self.Update

    def Update(self):
        self.HelperUpdate()
        self.Draw()
        self.DrawText()
        self.BtnUpdate()

    def DrawText(self):
        self.screen.blit(self.words, self.position)

    #Others
    def ChangeText(self, text):
        self.words = self.font.render(text, True, self.options["textColor"])

    def ResetText(self):
        self.words = self.font.render(self.options["text"], True, self.options["textColor"])
