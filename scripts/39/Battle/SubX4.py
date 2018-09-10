
"""
field character class 作成

最低要求
Sub = Sub3
"""

import pygame
from pygame.locals import *
import sys
import copy

import Helper
from Helper import BattleHelper

from Source import Sub
import SubX3


class FieldCharacterClass(Sub.ObjectClass):
    def __init__(self, MainClass, kwargs):
        super().__init__(MainClass, kwargs)

    def SetOptions(self, kwargs):
        super().SetOptions(kwargs)
        self.options.update({
            "speed" : 10,
            "hp" : 100,
            })
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
            "mudaniHustle" : self.OneCommandAnimation("mudaniHustle", self, None),
            "leftAttackStep" : self.OneCommandAnimation("leftAttackStep", self, None),
            "rightAttackStep" : self.OneCommandAnimation("rightAttackStep", self, None)
            }

        self.AttackCommand = self.CommandAnimationDic["mudaniHustle"]

    def SetHPbarPicture(self, HPbarPicture):
        self.HPbarPicture = HPbarPicture

class IconCharacterClass(SubX3.IconCharacterClass):
    def __init__(self, MainClass, CharaClass, kwargs):
        super().__init__(MainClass, CharaClass, kwargs)
