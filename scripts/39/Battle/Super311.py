"""
継承構造変化
Base31を要求
"""

import pygame
from pygame.locals import *
import sys

import Helper
from Helper import BattleHelper

import Base31 as Base

class MainClass:
    def __init__(self):
        super().__init__()

        if __name__ == "__main__":
            self.BattleHelper = BattleHelper
            self.ObjectClass = self.Base.ObjectClass
            self.IconCharacterClass = IconCharacterClass
            self.FieldCharacterClass = FieldCharacterClass
            self.FieldEnemyClass = FieldEnemyClass

            self.AllAnimationController = AllAnimationController
            self.ContinueAnimation = ContinueAnimation
            self.OneCommandAnimation = OneCommandAnimation
            self.PieceAnimation = PieceAnimation

            self.Helper = self.BattleHelper(self)

class IconCharacterClass(Super.IconCharacterClass):
    def __init__(self, MainClass, CharaClass, kwargs):
        super().__init__(MainClass, CharaClass, kwargs)

        self.battleMenuHeight = 10
        self.noOfShowBattleMenu = 5


    def SetOptions(self, kwargs):
        self.options = {"name" : "名無し",
                        "picturepath" : "../../../pictures/mon_016.bmp",
                        "position" : pygame.math.Vector2(),
                        "scale" : pygame.math.Vector2(100, 100),
                        "btnFunc" : self.OnClick,
                        "battleMenuName" : ["こうげき", "はねる"],
                        "battleMenuFunc" : []}
        if kwargs != None:
            self.options.update(kwargs)

    def ChangeAttackCommand(self, name):
        self.CharaClass.AttackCommand = self.CharaClass.CommandAnimationDic[name]

class FieldCharacterClass(Super.FieldCharacterClass):
    def __init__(self, MainClass, kwargs):
        super().__init__(MainClass, kwargs)

class FieldEnemyClass(Super.FieldEnemyClass):
    def __init__(self, MainClass, kwargs):
        super().__init__(MainClass, kwargs)

class AllAnimationController(Super.AllAnimationController):
    def __init__(self, ContiAnimList):
        super().__init__(ContiAnimList)

class ContinueAnimation(Super.ContinueAnimation):
    def __init__(self, CommandAnimationList, kwargs):
        super().__init__(CommandAnimationList, kwargs)

class OneCommandAnimation(Super.OneCommandAnimation):
    def __init__(self, name, ObjectClass, kwargs):
        super().__init__(name, ObjectClass, kwargs)

class OneCommandAnimation(Super.OneCommandAnimation):
    def __init__(self, name, ObjectClass, kwargs):
        super().__init__(name, ObjectClass, kwargs)

class PieceAnimation(Super.PieceAnimation):
    def __init__(self, name, ObjectClass, kwargs):
        super().__init__(name, ObjectClass, kwargs)


if __name__ == "__main__":
    MainClass().Main()
