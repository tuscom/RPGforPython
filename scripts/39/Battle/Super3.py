"""
ターンシステム導入
Base3を要求
"""

import pygame
from pygame.locals import *
import sys

import Helper
from Helper import BattleHelper

import Super2 as Super

class MainClass(Super.MainClass):
    def __init__(self):
        super().__init__()

        if __name__ == "__main__":
            self.BattleHelper = BattleHelper
            self.IconCharacterClass = IconCharacterClass
            self.FieldCharacterClass = FieldCharacterClass
            self.FieldEnemyClass = FieldEnemyClass

            self.AllAnimationController = AllAnimationController
            self.ContinueAnimation = ContinueAnimation
            self.OneCommandAnimation = OneCommandAnimation
            self.PieceAnimation = PieceAnimation

            self.Helper = self.BattleHelper(self)

        self.AllObjectList = []

        self.AttackAnimContiList = []
        self.AttackCharacterList = []

    def Start(self):
        self.Action = self.Update

        self.LoadMaterial()
        self.SetFieldCharacter()
        self.SetPanel()
        
        self.ObjectStart()
        
        self.SetAnimation()

    def ObjectStart(self):
        list(map(lambda objectClass : objectClass.Start(), self.AllObjectList))

    def SetFieldCharacter(self):
        super().SetFieldCharacter()
        self.allCharacters = self.family + self.enemies

    def SetAnimation(self):
        self.AttackCharacterList = self.allCharacters
        commandAnimList = [target.AttackCommand for target in self.AttackCharacterList]
        kwargs={"isRepeat" : False}
        AttackContiAnim = self.ContinueAnimation(commandAnimList, kwargs)

        continueAnimList = [AttackContiAnim]

        self.AnimationController = self.AllAnimationController(continueAnimList)

class IconCharacterClass(Super.IconCharacterClass):
    def __init__(self, MainClass, Character, kwargs):
        super().__init__(MainClass, Character, kwargs)

class FieldCharacterClass(Super.FieldCharacterClass):
    def __init__(self, MainClass, kwargs):
        super().__init__(MainClass, kwargs)
        self.AttackCommand = None

    def Start(self):
        super().Start()
        self.AutoSelectAttackCommand()

    def AutoSelectAttackCommand(self):
        self.AttackCommand = self.CommandAnimationDic["jump"]

class FieldEnemyClass(Super.FieldEnemyClass):
    def __init__(self, MainClass, kwargs):
        super().__init__(MainClass, kwargs)
        self.AttackCommand = None

    def Start(self):
        super().Start()
        self.AutoSelectAttackCommand()

    def AutoSelectAttackCommand(self):
        self.AttackCommand = self.CommandAnimationDic["jump"]

class AllAnimationController(Super.AllAnimationController):
    def __init__(self, ContiAnimList):
        super().__init__(ContiAnimList)

class ContinueAnimation(Super.ContinueAnimation):
    def __init__(self, CommandAnimationList, kwargs):
        super().__init__(CommandAnimationList, kwargs)

class OneCommandAnimation(Super.OneCommandAnimation):
    def __init__(self, name, ObjectClass, kwargs):
        super().__init__(name, ObjectClass, kwargs)

class PieceAnimation(Super.PieceAnimation):
    def __init__(self, name, ObjectClass, kwargs):
        super().__init__(name, ObjectClass, kwargs)

if __name__ == "__main__":
    MainClass().Main()
