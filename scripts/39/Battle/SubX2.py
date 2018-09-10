"""
アニメーションの構造
Sub2を要求
"""
import pygame
from pygame.locals import *
import sys

import Helper
from Helper import BattleHelper

import SubX1 as Sub



class IconCharacterClass(Sub.IconCharacterClass):
    def __init__(self, MainClass, Character, kwargs):
        super().__init__(MainClass, Character, kwargs)

    def SetHPbar(self):
        super().SetHPbar()
        self.CharaClass.IconClass = self
        self.CharaClass.HPbarPicture = self.HPbarPicture

class FieldCharacterClass(Sub.FieldCharacterClass):
    def __init__(self, MainClass, kwargs):
        super().__init__(MainClass, kwargs)

        self.options.update({
            "hp" : 100
            })

        self.hp = self.options["hp"]
        self.HPbarPicture = None
        self.IconClass = None

        self.CommandAnimationDic = {
            "jump" : self.OneCommandAnimation("jump", self, None),
            "mudaniHustle" : self.OneCommandAnimation("mudaniHustle", self, None)
            }

    def Update(self):
        super().Update()
        self.ReflectHPbarPicture()

    def ReflectHPbarPicture(self):
        self.IconClass.HPbarPicture = self.HPbarPicture

class FieldEnemyClass(Sub.FieldEnemyClass):
    def __init__(self, MainClass, kwargs):
        super().__init__(MainClass, kwargs)

        self.options.update({
            "hp" : 100
            })

        self.hp = self.options["hp"]

        self.CommandAnimationDic = {
            "jump" : self.OneCommandAnimation("jump", self, None),
            "mudaniHustle" : self.OneCommandAnimation("mudaniHustle", self, None)
            }


