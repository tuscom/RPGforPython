"""
描画
ボタン
Sub1を要求
"""

import pygame
from pygame.locals import *
import sys

import Helper
from Helper import BattleHelper

from Source import Sub

class IconCharacterClass(Sub.ObjectClass):
    def __init__(self, MainClass, CharaClass, kwargs):
        super().__init__(MainClass, kwargs)
        self.options.update({
            "bgPicturePath" : "../../../pictures/normalPanel.png",
            "HPbarPicturePath" : "../../../pictures/HPbar.png",
            "HPbarbackPicturePath" : "../../../pictures/HPbar_back.png",
            "HPbarThick" : 10
            })
        self.CharaClass = CharaClass

    def Start(self):
        super().Start()

        self.SetScale()
        self.SetHPbar()
        self.SetHPbarPosition()
        self.SetbgPicture()
        self.SetCharacterPicture()

    def SetScale(self):
        self.charaControllerRect = self.MainClass.Helper.NormToWorldRect(self.MainClass.charaControllerLayout)
        self.scale = pygame.math.Vector2(self.charaControllerRect[3], self.charaControllerRect[3])
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
    def SetbgPicture(self):
        self.bgPicture = self.BattleHelper.ScaledPicture(
            self.options["bgPicturePath"],
            (self.charaControllerRect[3], self.charaControllerRect[3])
            )
    def SetCharacterPicture(self):
        self.picture = pygame.transform.scale(self.CharaClass.picture, (self.charaControllerRect[3], self.charaControllerRect[3]))

    def SetHPbarPosition(self):
        self.HPbarPos = self.position + pygame.math.Vector2(0, 1) * (self.scale.y - self.HPbarScale.y)

    def Draw(self):
        self.screen.blit(self.bgPicture, self.position)
        self.screen.blit(self.picture, self.position)
        self.screen.blit(self.HPbarbackPicture, self.HPbarPos)
        self.screen.blit(self.HPbarPicture, self.HPbarPos)

class FieldCharacterClass(Sub.ObjectClass):
    def __init__(self, MainClass, kwargs):
        super().__init__(MainClass, kwargs)
        self.options.update({
            
            })

class FieldEnemyClass(Sub.ObjectClass):
    def __init__(self, MainClass, kwargs):
        super().__init__(MainClass, kwargs)
        self.options.update({
            "HPbarPicturePath" : "../../../pictures/HPbar.png",
            "HPbarbackPicturePath" : "../../../pictures/HPbar_back.png",
            "HPbarThick" : 10
            })

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


