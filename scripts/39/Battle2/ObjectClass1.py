"""
描画
ボタン
"""

import pygame
from pygame.locals import *
import sys

class ObjectClass:
    def __init__(self, MainClass, kwargs):
        self.GetSource(MainClass)
        self.SetOptions(kwargs)
        self.SetParameter()

        self.OnInstanceFunc()

        self.Action = self.Start

    #================== Main =================
    def Main(self):
        if self.Action != None:
            self.Action()

    #================== Start =================
    def Start(self):
        self.LoadMaterial()
        self.Action = self.Update

    def GetSource(self, MainClass):
        self.MainClass = MainClass
        self.Helper = MainClass.Helper
        self.BattleHelper = MainClass.BattleHelper
        self.screen = MainClass.screen
        self.BtnAction = MainClass.HelperModule.ButtonAction(self)
        self.BoolAction = self.BtnAction.IsOnDown

    def SetOptions(self, kwargs):
        self.options = {
            "name" : "名無し",
            "picturepath" : "../../../pictures/mon_016.bmp",
            "position" : pygame.math.Vector2(),
            "scale" : pygame.math.Vector2(100, 100)}
        if kwargs != None:
            self.options.update(kwargs)
    def SetParameter(self):
        self.position = pygame.math.Vector2(self.options["position"])
        self.scale = pygame.math.Vector2(self.options["scale"])

    def LoadMaterial(self):
        rect = self.Rect()
        self.picture = pygame.transform.scale(pygame.image.load(self.options["picturepath"]).convert_alpha(), rect[2:])

    #================== Update ================
    def Update(self):
        self.HelperUpdate()
        self.Draw()
        self.BtnUpdate()

    def HelperUpdate(self):
        self.BtnAction.mousePos = self.Helper.mousePos
        self.BtnAction.mousePressed = self.Helper.mousePressed
        self.BtnAction.previousPressed = self.Helper.previousPressed

    def Draw(self):
        self.screen.blit(self.picture, self.position)
    def BtnUpdate(self):
        if self.BoolAction():
            self.OnClick()

    #================== Button ===============
    def OnClick(self):
        pass

    #================= Others ================
    def Rect(self):
        return[int(self.position.x), int(self.position.y), int(self.scale.x), int(self.scale.y)]

    def OnInstanceFunc(self):
        self.MainClass.AllObjects.append(self)

