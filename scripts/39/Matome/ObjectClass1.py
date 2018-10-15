import pygame
from pygame.locals import *
import sys

class ObjectClass:
    def __init__(self, MainClass, kwargs):
        self.GetSource(MainClass)
        self.SetOptions(kwargs)
        self.TransformParameter()

        self.ProgramParameter()
        self.AppendToModeClass()

    def GetSource(self, MainClass):
        self.MainClass = MainClass
        self.screen = MainClass.screen
        self.Helper = MainClass.Helper
        self.HelperModule = MainClass.HelperModule

    def SetOptions(self, kwargs):
        self.options = {"name" : "名無し",
                        "picturepath" : "../../../pictures/mon_016.bmp",
                        "position" : pygame.math.Vector2(0, 0),
                        "scale" : pygame.math.Vector2(1, 1),
                        "ModeClass" : None}
        if kwargs != None:
            self.options.update(kwargs)

    def ProgramParameter(self):
        self.picture = self.HelperModule.ScaledPicture(
            self.options["picturepath"], 
            size=[int(self.scale.x), int(self.scale.y)])
        self.Action = self.Start

    def AppendToModeClass(self):
        self.options["ModeClass"].AllObjects.append(self)

    def TransformParameter(self):
        self.position = self.options["position"]
        self.scale = self.options["scale"]

    def Start(self):
        self.Action = self.Update

    def Update(self):
        self.Draw()

    def Draw(self):
        self.screen.blit(self.picture, self.position)

    def Main(self):
        if self.Action != None:
            self.Action()
