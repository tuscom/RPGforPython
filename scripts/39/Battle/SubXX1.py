
"""
継承関係変更

最低要求
Sub = Sub3
SubX = SubX4
"""

import pygame
from pygame.locals import *
import sys
import copy

import Helper
from Helper import BattleHelper

from Source import SubX

class FieldFamilyClass(SubX.FieldCharacterClass):
    def __init__(self, MainClass, kwargs):
        super().__init__(MainClass, kwargs)

    def SetHPbarPicture(self, HPbarPicture):
        self.IconClass.HPbarPicture = HPbarPicture
        self.HPbarPicture = HPbarPicture


class FieldEnemyClass(SubX.FieldCharacterClass):
    def __init__(self, MainClass, kwargs):
        super().__init__(MainClass, kwargs)

    def SetOptions(self, kwargs):
        super().SetOptions(kwargs)
        self.options.update({
            "HPbarPicturePath" : "../../../pictures/HPbar.png",
            "HPbarbackPicturePath" : "../../../pictures/HPbar_back.png",
            "HPbarThick" : 10
            })
        if kwargs != None:
            self.options.update(kwargs)

    def Start(self):
        super().Start()
        self.SetHPbar()

    def SetHPbar(self):
        self.HPbarScale = pygame.math.Vector2(self.scale.x * 0.6, self.options["HPbarThick"])
        self.HPbarPos = pygame.math.Vector2(self.position) + pygame.math.Vector2((self.scale.x - self.HPbarScale.x)/2, self.scale.y)

        self.HPbarPicture = BattleHelper.ScaledPicture(
            self.options["HPbarPicturePath"],
            BattleHelper.Vector2ToIntlist(self.HPbarScale)
            )
        self.HPbarbackPicture = BattleHelper.ScaledPicture(
            self.options["HPbarbackPicturePath"],
            BattleHelper.Vector2ToIntlist(self.HPbarScale)
            )

    def Draw(self):
        super().Draw()
        self.screen.blit(self.HPbarbackPicture, self.HPbarPos)
        self.screen.blit(self.HPbarPicture, self.HPbarPos)

