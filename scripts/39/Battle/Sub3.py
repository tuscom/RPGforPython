"""
AllObject追加
"""

import pygame
from pygame.locals import *
import sys

import Helper
from Helper import BattleHelper

import Sub2 as Sub

class ObjectClass(Sub.ObjectClass):
    def __init__(self, MainClass, kwargs):
        self.MainClass = MainClass
        self.BattleHelper = MainClass.BattleHelper
        self.Helper = MainClass.Helper
        self.screen = MainClass.screen
        self.OneCommandAnimation = MainClass.OneCommandAnimation

        self.SetOptions(kwargs)
        self.SetParameter()
        self.SetButton()
        self.OnInstanceFunc()
        self.SetAction()

    def SetOptions(self, kwargs):
        self.options = {"name" : "名無し",
                        "picturepath" : "../../../pictures/mon_016.bmp",
                        "position" : pygame.math.Vector2(),
                        "scale" : pygame.math.Vector2(100, 100),
                        "btnFunc" : self.OnClick}
        if kwargs != None:
            self.options.update(kwargs)
    def SetParameter(self):
        self.position = pygame.math.Vector2(self.options["position"])
        self.scale = pygame.math.Vector2(self.options["scale"])
    def SetButton(self):
        self.BtnAction = Helper.ButtonAction(self)
        self.BoolAction = self.BtnAction.IsOnDown
        self.BtnFunc = self.options["btnFunc"]
    def OnInstanceFunc(self):
        self.MainClass.AllObjectsList.append(self)
    def SetAction(self):
        self.Action = self.Start

class AllAnimationController(Sub.AllAnimationController):
    def __init__(self, ContiAnimList):
        super().__init__(ContiAnimList)

class ContinueAnimation(Sub.ContinueAnimation):
    def __init__(self, CommandAnimationList, kwargs):
        super().__init__(CommandAnimationList, kwargs)

class OneCommandAnimation(Sub.OneCommandAnimation): 
    def __init__(self, name, ObjectClass, kwargs):
        super().__init__(name, ObjectClass, kwargs)

class PieceAnimation(Sub.PieceAnimation):
    def __init__(self, name, ObjectClass, kwargs): 
        super().__init__(name, ObjectClass, kwargs)

    def HPmoveUpdate(self):
        clock = self.clock - self.delayTime
        pictureScale = (
            self.pictureScale[0]-self.speed*clock,
            self.pictureScale[1])

        picture = pygame.transform.scale(
            self.HPbarPicture,
            [int(pictureScale[0]), int(pictureScale[1])]
            )

        self.ObjectClass.SetHPbarPicture(picture)