"""
整理
"""

import pygame
from pygame.locals import *
import sys
import copy

import Helper
from Helper import BattleHelper

import SubX2 as Sub

class IconCharacterClass(Sub.IconCharacterClass):
    def __init__(self, MainClass, CharaClass, kwargs):
        self.MainClass = MainClass
        self.BattleHelper = MainClass.BattleHelper
        self.Helper = MainClass.Helper
        self.screen = MainClass.screen
        self.CharaClass = CharaClass
        self.OneCommandAnimation = MainClass.OneCommandAnimation

        self.SetOptions(kwargs)
        self.SetParameter()
        self.SetButton()
        self.OnInstanceFunc()
        self.SetAction()


    def SetOptions(self, kwargs):
        self.options = {
            "name" : "名無し",
            "picturepath" : "../../../pictures/mon_016.bmp",
            "position" : pygame.math.Vector2(),
            "scale" : pygame.math.Vector2(100, 100),
            "btnFunc" : self.OnClick,
            "bgPicturePath" : "../../../pictures/normalPanel.png",
            "HPbarPicturePath" : "../../../pictures/HPbar.png",
            "HPbarbackPicturePath" : "../../../pictures/HPbar_back.png",
            "HPbarThick" : 10
            }
        if kwargs != None:
            self.options.update(kwargs)

    def Start(self):
        self.LoadMaterial()
        self.Action = self.Update

        self.SetScale()
        self.SetHPbar()
        self.SetHPbarPosition()
        self.SetbgPicture()
        self.SetCharacterPicture()
        self.ReflectToCharaClass()

    def ReflectToCharaClass(self):
        self.CharaClass.IconClass = self

    def SetHPbar(self):
        self.HPbarScale = pygame.math.Vector2(self.scale.x, self.options["HPbarThick"])
        self.HPbarPos = pygame.math.Vector2()
        self.HPbarPicture = self.BattleHelper.ScaledPicture(
            self.options["HPbarPicturePath"],
            (int(self.HPbarScale.x), int(self.HPbarScale.y))
            )
        self.HPbarbackPicture = self.BattleHelper.ScaledPicture(
            self.options["HPbarbackPicturePath"],
            (int(self.HPbarScale.x), int(self.HPbarScale.y))
            )
        self.CharaClass.HPbarPicture = self.HPbarPicture

    def SetHPbarPicture(self, HPbarPicture):
        self.CharaClass.HPbarPicture = HPbarPicture
        self.HPbarPicture = HPbarPicture

    def Update(self):
        self.HelperUpdate()

        self.Draw()
        self.BtnUpdate()

class FieldCharacterClass(Sub.FieldCharacterClass):
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
        self.options = {
            "name" : "名無し",
            "picturepath" : "../../../pictures/mon_016.bmp",
            "position" : pygame.math.Vector2(),
            "scale" : pygame.math.Vector2(100, 100),
            "btnFunc" : self.OnClick,
            "speed" : 10,
            "hp" : 100,
            }
        if kwargs != None:
            self.options.update(kwargs)

    def SetParameter(self):
        super().SetParameter()
        self.speed = self.options["speed"]
        self.hp = self.options["hp"]

    def Start(self):
        super().Start()
        self.SetAnimationCommand()

    def SetAnimationCommand(self):
        self.CommandAnimationDic = {
            "jump" : self.OneCommandAnimation("jump", self, None),
            "mudaniHustle" : self.OneCommandAnimation("mudaniHustle", self, None)
            }

        self.AttackCommand = self.CommandAnimationDic["mudaniHustle"]

    def SetHPbarPicture(self, HPbarPicture):
        self.IconClass.HPbarPicture = HPbarPicture
        self.HPbarPicture = HPbarPicture

    def Update(self):
        self.HelperUpdate()

        self.Draw()
        self.BtnUpdate()

class FieldEnemyClass(Sub.FieldEnemyClass):
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
        self.options = {
            "name" : "名無し",
            "picturepath" : "../../../pictures/mon_016.bmp",
            "position" : pygame.math.Vector2(),
            "scale" : pygame.math.Vector2(100, 100),
            "btnFunc" : self.OnClick,
            "speed" : 10,
            "hp" : 100,
            "HPbarPicturePath" : "../../../pictures/HPbar.png",
            "HPbarbackPicturePath" : "../../../pictures/HPbar_back.png",
            "HPbarThick" : 10
            }
        if kwargs != None:
            self.options.update(kwargs)

    def SetParameter(self):
        super().SetParameter()
        self.speed = self.options["speed"]
        self.hp = self.options["hp"]

    def Start(self):
        super().Start()
        self.SetAnimationCommand()

    def SetAnimationCommand(self):
        self.CommandAnimationDic = {
            "jump" : self.OneCommandAnimation("jump", self, None),
            "mudaniHustle" : self.OneCommandAnimation("mudaniHustle", self, None)
            }

        self.AttackCommand = self.CommandAnimationDic["mudaniHustle"]

    def SetHPbarPicture(self, HPbarPicture):
        self.HPbarPicture = HPbarPicture
