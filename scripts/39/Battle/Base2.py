"""
アニメーションの構造
"""

import pygame
from pygame.locals import *
import sys

import Helper
from Helper import BattleHelper

import Base1 as Base

class ObjectClass(Base.ObjectClass):
    def __init__(self, MainClass, kwargs):
        super().__init__(MainClass, kwargs)
        self.Helper = MainClass.Helper

        self.OneCommandAnimation = MainClass.OneCommandAnimation

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

