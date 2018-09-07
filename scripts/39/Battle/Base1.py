"""
描画
ボタン
"""

import pygame
from pygame.locals import *
import sys

import Helper
from Helper import BattleHelper


class ObjectClass:
    def __init__(self, MainClass, kwargs):
        self.MainClass = MainClass
        self.BattleHelper = MainClass.BattleHelper
        self.screen = MainClass.screen
        self.options = {"name" : "名無し",
                        "picturepath" : "../../../pictures/mon_016.bmp",
                        "position" : pygame.math.Vector2(),
                        "scale" : pygame.math.Vector2(100, 100)}
        if kwargs != None:
            self.options.update(kwargs)

        self.position = pygame.math.Vector2(self.options["position"])
        self.scale = pygame.math.Vector2(self.options["scale"])

        self.BtnAction = Helper.ButtonAction(self)
        self.BoolAction = self.BtnAction.IsOnDown
        self.BtnFunc = self.OnClick

        self.Action = self.Start

    #================== Main =================
    def Main(self):
        if self.Action != None:
            self.Action()

    #================== Start =================
    def Start(self):
        self.LoadMaterial()
        self.Action = self.Update

    def LoadMaterial(self):
        rect = self.Rect()
        self.picture = pygame.transform.scale(pygame.image.load(self.options["picturepath"]).convert_alpha(), rect[2:])

    #================== Update ================
    def Update(self):
        self.BtnAction.mousePos = pygame.mouse.get_pos()
        self.BtnAction.mousePressed = pygame.mouse.get_pressed()

        self.Draw()
        self.BtnUpdate()

        self.BtnAction.previousPressed = self.BtnAction.mousePressed

    def Draw(self):
        self.screen.blit(self.picture, self.position)
    def BtnUpdate(self):
        if self.BoolAction():
            self.BtnFunc()

    #================== Button ===============
    def OnClick(self):
        print("btn pushed!")

    #================= Others ================
    def Rect(self):
        return[int(self.position.x), int(self.position.y), int(self.scale.x), int(self.scale.y)]

