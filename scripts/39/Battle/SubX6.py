"""
最低要求
Sub = Sub4
"""
import pygame
from pygame.locals import *
import sys
import copy
import functools

import Helper
from Helper import BattleHelper

from Source import Sub
import SubX5

class FieldCharacterClass(SubX5.FieldCharacterClass):
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

    def Start(self):
        self.LoadMaterial()
        self.Action = self.Update
        self.SetAnimationCommand()
        self.AutoSelectAttackTarget()

    def Update(self):
        self.HelperUpdate()

        self.Draw()
        self.BtnUpdate()

class IconCharacterClass(SubX5.IconCharacterClass):
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

    def Start(self):
        self.LoadMaterial()
        self.Action = self.Update

        self.SetScale()
        self.SetHPbar()
        self.SetHPbarPosition()
        self.SetbgPicture()
        self.SetCharacterPicture()
        self.ReflectToCharaClass()
        self.SetBattleMenu()
        self.SetAnimationCommand()

    def Update(self):
        self.HelperUpdate()

        self.Draw()
        self.DrawBattleMenu()
        self.BtnUpdate()

    def OnClick(self):
        super().OnClick()
        self.MainClass.SelectedEnemy = self.CharaClass.AttackTarget
        self.MainClass.SelectedFamily = self.CharaClass

class ButtonClass(SubX5.ButtonClass):
    def __init__(self, MainClass, kwargs):
        self.MainClass = MainClass
        self.BattleHelper = MainClass.BattleHelper
        self.Helper = MainClass.Helper
        self.screen = MainClass.screen
        self.OneCommandAnimation = MainClass.OneCommandAnimation

        self.SetOptions(kwargs)
        self.SetAnimationCommand()
        self.SetParameter()
        self.SetButton()
        self.SetText()
        self.OnInstanceFunc()
        self.SetAction()

    def Start(self):
        self.LoadMaterial()
        self.Action = self.Update

    def Update(self):
        self.HelperUpdate()

        self.Draw()
        self.DrawText()
        self.BtnUpdate()
