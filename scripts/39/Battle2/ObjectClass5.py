import pygame
from pygame.locals import *
import sys
import random
import copy
import math

import Helper
from Helper import BattleHelper

import ObjectClass4

class ObjectClass(ObjectClass4.ObjectClass):
    def __init__(self, MainClass, kwargs):
        self.MainClass = MainClass
        self.BattleHelper = MainClass.BattleHelper
        self.Helper = MainClass.Helper
        self.screen = MainClass.screen
        self.OneCommandAnimation = MainClass.OneCommandAnimation

        self.LoadMaterial()
        self.SetOptions(kwargs)
        self.SetParameter()
        self.SetButton()
        self.OnInstanceFunc()
        self.SetAction()

    def SetParameter(self):
        super().SetParameter()
        self.enable = True

    def Start(self):
        self.SetAnimationCommand()
        self.Action = self.Update

    def Update(self):
        self.HelperUpdate()
        self.BtnUpdate()
        if not self.enable:
            self.Action = self.End

        #最後に描画
        self.Draw()

    def End(self):
        self.Action = None

