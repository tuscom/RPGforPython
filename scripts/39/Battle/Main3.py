"""
攻撃ボタンの実装+整理
Sub = Sub3
SubX = SubX3
"""

import pygame
from pygame.locals import *
import sys
import copy

import Helper
from Helper import BattleHelper

from Source import Sub
from Source import SubX
import Main2 as MainModule

class MainClass(MainModule.MainClass):
    def __init__(self):
        super().__init__()

        if __name__ == "__main__":
            self.BattleHelper = BattleHelper
            self.IconCharacterClass = SubX.IconCharacterClass
            self.FieldCharacterClass = SubX.FieldCharacterClass
            self.FieldEnemyClass = SubX.FieldEnemyClass
            self.ObjectClass = Sub.ObjectClass

            self.AllAnimationController = Sub.AllAnimationController
            self.ContinueAnimation = Sub.ContinueAnimation
            self.OneCommandAnimation = Sub.OneCommandAnimation
            self.PieceAnimation = Sub.PieceAnimation

            self.Helper = self.BattleHelper(self)

        self.AllObjectsList = []

    def Start(self):
        super().Start()
        self.SetAttackBtn()

    def SetFieldCharacter(self):
        super().SetFieldCharacter()
        self.AttackCharacterList = self.family + self.enemies


    def SetAttackBtn(self):
        attackBtnPos = self.Helper.NormToWorldPos(self.attackBtnLayout)
        kwargs = {
            "picturepath" : self.attackBtnPicturePath,
            "position" : attackBtnPos,
            "scale" : self.attackBtnScale,
            "btnFunc" : self.AttackBtnOnClick
            }
        self.attackBtn = self.ObjectClass(self, kwargs)

    def AttackBtnOnClick(self):
        self.AttackCharacterList = sorted(self.AttackCharacterList, key=lambda chara:chara.speed, reverse=True)
        commandAnimList = [target.AttackCommand for target in self.AttackCharacterList]
        self.AttackContiAnim.CommandAnimationList = commandAnimList
        self.AttackContiAnim.PlayON()

    def SetAnimation(self):
        kwargs = {
            "isRepeat" : False,
            "isAutoStart" : False
            }
        self.AttackContiAnim = self.ContinueAnimation([], kwargs)

        self.ContinueAnimList = [self.AttackContiAnim]

        self.AnimationController = self.AllAnimationController(self.ContinueAnimList)

    def SetPanel(self):
        charaControllerRect = self.Helper.NormToWorldRect(self.charaControllerLayout)
        kwargs = {
            "position" : pygame.math.Vector2(charaControllerRect[0], charaControllerRect[1]),
            "scale" : pygame.math.Vector2(charaControllerRect[2], charaControllerRect[3]),
            "picturepath" : self.charaControllerPanelPicturePath
            }
        self.charaControllerPanel = self.ObjectClass(self, kwargs)

        self.familyIcons = []
        for i in range(len(self.family)):
            self.familyIcons.append(self.IconCharacterClass(self, self.family[i], None))
            self.familyIcons[-1].position = pygame.math.Vector2(
                i * charaControllerRect[3],
                charaControllerRect[1]
                )

    def Update(self):
        self.DrawBackGround()
        self.MainOfAllObjects()
        self.AnimationUpdate()

    def MainOfAllObjects(self):
        list(map(lambda objectClass : objectClass.Main(), self.AllObjectsList))

if __name__ == "__main__":
    MainClass().Main()
