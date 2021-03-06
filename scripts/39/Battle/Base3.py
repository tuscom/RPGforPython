"""
ボタン機能追加
"""

import pygame
from pygame.locals import *
import sys

import Helper
from Helper import BattleHelper

import Base2 as Base

class ObjectClass(Base.ObjectClass):
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
        self.MainClass.AllObjectList.append(self)
    def SetAction(self):
        self.Action = self.Update
        
    def Update(self):
        self.HelperUpdate()

        self.Draw()
        self.BtnUpdate()

    def HelperUpdate(self):
        self.BtnAction.mousePos = self.Helper.mousePos
        self.BtnAction.mousePressed = self.Helper.mousePressed
        self.BtnAction.previousPressed = self.Helper.previousPressed

    def AnimationUpdate(self):
        if self.Animation != None:
            self.Animation()

