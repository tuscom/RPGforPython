import pygame
from pygame.locals import *
import sys
import random
import copy
import math

import Helper
from Helper import BattleHelper

import Sub5 as Sub

class ObjectClass(Sub.ObjectClass):
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
        #self.SetAnimationCommand()
        self.Action = self.Update

    def Update(self):
        self.HelperUpdate()

        self.Draw()
        self.BtnUpdate()

