"""
最低要求条件
Sub = Sub4
SubX = SubX5
"""
import pygame
from pygame.locals import *
import sys
import copy

import Helper
from Helper import BattleHelper

import SubXX2 as SubXX

class FieldFamilyClass(SubXX.FieldFamilyClass):
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
        self.AutoSelectAttackTarget()
        
        self.Action = self.Update
        #self.SetAnimationCommand()

    def Update(self):
        self.HelperUpdate()

        self.Draw()
        self.BtnUpdate()
        self.HPEvent()

class FieldEnemyClass(SubXX.FieldEnemyClass):
    def __init__(self, MainClass, kwargs):
        self.MainClass = MainClass
        self.BattleHelper = MainClass.BattleHelper
        self.Helper = MainClass.Helper
        self.screen = MainClass.screen
        #self.OneCommandAnimation = MainClass.OneCommandAnimation

        self.SetOptions(kwargs)
        self.SetParameter()
        self.SetButton()
        self.OnInstanceFunc()
        self.SetAction()

    def Start(self):
        self.LoadMaterial()
        self.AutoSelectAttackTarget()
        self.SetHPbar()

        self.Action = self.Update
        #self.SetAnimationCommand()

    def Update(self):
        self.HelperUpdate()

        self.Draw()
        self.BtnUpdate()
