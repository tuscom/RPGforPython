"""
アニメーション機能改善
Base3を要求
"""

import pygame
from pygame.locals import *
import sys
import copy

import Helper
from Helper import BattleHelper

import Super2 as Super

class MainClass(Super.MainClass):
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

        self.AllObjectList = []

        self.AttackAnimContiList = []
        self.AttackCharacterList = []

    def Start(self):
        self.Action = self.Update

        self.LoadMaterial()
        self.SetFieldCharacter()
        self.SetPanel()
        self.SetAttackBtn()
        
        self.ObjectStart()
        
        self.SetAnimation()

    def ObjectStart(self):
        list(map(lambda objectClass : objectClass.Start(), self.AllObjectList))

    def SetFieldCharacter(self):
        super().SetFieldCharacter()
        self.allCharacters = self.family + self.enemies


    def SetPanel(self):
        charaControllerRect = self.Helper.NormToWorldRect(self.charaControllerLayout)
        kwargs = {
            "position" : pygame.math.Vector2(charaControllerRect[0], charaControllerRect[1]),
            "scale" : pygame.math.Vector2(charaControllerRect[2], charaControllerRect[3]),
            "picturepath" : self.charaControllerPanelPicturePath
            }
        self.charaControllerPanel = self.Base.ObjectClass(self, kwargs)

        self.familyIcons = []
        for i in range(len(self.family)):
            self.familyIcons.append(self.IconCharacterClass(self, self.family[i], None))
            self.familyIcons[-1].position = pygame.math.Vector2(
                i * charaControllerRect[3],
                charaControllerRect[1]
                )

    def SetAnimation(self):
        self.AttackCharacterList = copy.copy(self.allCharacters)
        commandAnimList = [target.AttackCommand for target in self.AttackCharacterList]
        kwargs={
            "isRepeat" : False,
            "isAutoStart" : False}
        self.AttackContiAnim = self.ContinueAnimation(commandAnimList, kwargs)

        continueAnimList = [self.AttackContiAnim]

        self.AnimationController = self.AllAnimationController(continueAnimList)

    def SetAttackBtn(self):
        attackBtnPos = self.Helper.NormToWorldPos(self.attackBtnLayout)
        kwargs = {
            "picturepath" : self.attackBtnPicturePath,
            "position" : attackBtnPos,
            "scale" : self.attackBtnScale,
            "btnFunc" : self.AttackBtnOnClick
            }
        self.attackBtn = self.Base.ObjectClass(self, kwargs)

    def AttackBtnOnClick(self):
        self.AttackContiAnim.PlayON()
        self.AttackCharacterList = sorted(self.AttackCharacterList, key=lambda chara:chara.speed, reverse=True)
        commandAnimList = [target.AttackCommand for target in self.AttackCharacterList]
        self.AttackContiAnim.CommandAnimationList = commandAnimList

class IconCharacterClass(Super.IconCharacterClass):
    def __init__(self, MainClass, Character, kwargs):
        super().__init__(MainClass, Character, kwargs)

class FieldCharacterClass(Super.FieldCharacterClass):
    def __init__(self, MainClass, kwargs):
        super().__init__(MainClass, kwargs)
        self.AttackCommand = None

    def SetOptions(self, kwargs):
        self.options = {"name" : "名無し",
                        "picturepath" : "../../../pictures/mon_016.bmp",
                        "position" : pygame.math.Vector2(),
                        "scale" : pygame.math.Vector2(100, 100),
                        "btnFunc" : self.OnClick,
                        "speed" : 10}
        if kwargs != None:
            self.options.update(kwargs)

    def SetParameter(self):
        super().SetParameter()
        self.speed = self.options["speed"]

    def Start(self):
        super().Start()
        self.AutoSelectAttackCommand()

    def AutoSelectAttackCommand(self):
        self.AttackCommand = self.CommandAnimationDic["jump"]

class FieldEnemyClass(Super.FieldEnemyClass):
    def __init__(self, MainClass, kwargs):
        super().__init__(MainClass, kwargs)
        self.AttackCommand = None

    def SetOptions(self, kwargs):
        self.options = {"name" : "名無し",
                        "picturepath" : "../../../pictures/mon_016.bmp",
                        "position" : pygame.math.Vector2(),
                        "scale" : pygame.math.Vector2(100, 100),
                        "btnFunc" : self.OnClick,
                        "speed" : 10}
        if kwargs != None:
            self.options.update(kwargs)

    def SetParameter(self):
        super().SetParameter()
        self.speed = self.options["speed"]

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
        self.options = {
            "isRepeat" : False,
            "isAutoStart" : True}
        if kwargs != None:
            self.options.update(kwargs)
        self.UpdateFunc = self.RepeatUpdate if self.options["isRepeat"] else self.AutoEndUpdate
        self.Action = self.Start if self.options["isAutoStart"] else None

        self.CommandAnimationList = CommandAnimationList
        self.indexOfAnimation = 0

    def Start(self):
        super().Start()
        self.indexOfAnimation = 0

    def RepeatUpdate(self):
        comAnim = self.CommandAnimationList[self.indexOfAnimation]

        comAnim.Main()
        if comAnim.IsEndOfAnimation():
            self.indexOfAnimation += 1
            self.indexOfAnimation %= self.noOfComAnim

            if self.indexOfAnimation == 0:
                self.PlayON()

    def AutoEndUpdate(self):
        comAnim = self.CommandAnimationList[self.indexOfAnimation]

        comAnim.Main()
        if comAnim.IsEndOfAnimation():
            self.indexOfAnimation += 1

            if self.EndCondition():
                self.Action = self.End

    def PlayON(self):
        list(map(lambda comAnim : comAnim.PlayON(), self.CommandAnimationList))

        if self.IsEndOfAnimation():
            self.Action = self.Start

    def EndCondition(self):
        return self.indexOfAnimation % self.noOfComAnim == 0

    def IsEndOfAnimation(self):
        return self.Action == None

class OneCommandAnimation(Super.OneCommandAnimation):
    def __init__(self, name, ObjectClass, kwargs):
        super().__init__(name, ObjectClass, kwargs)

    def Update(self):
        if self.UpdateFunc != None:
            self.UpdateFunc()
        list(map(lambda pieceAnime : pieceAnime.Main(), self.PieceAnimationList))
        if self.EndCondition():
            self.Action = self.End

    def PlayON(self):
        if self.IsEndOfAnimation():
            self.Action = self.Start
            list(map(lambda pieceAnim : pieceAnim.PlayON(), self.PieceAnimationList))
    def IsEndOfAnimation(self):
        return self.Action == None

    def EndCondition(self):
        boolList = list(map(lambda pieceAnim : pieceAnim.IsEndOfAnimation(), self.PieceAnimationList))
        return all(boolList)

class PieceAnimation(Super.PieceAnimation):
    def __init__(self, name, ObjectClass, kwargs):
        super().__init__(name, ObjectClass, kwargs)

    def Update(self):
        self.clock += self.Helper.pygamedeltatime

        if self.UpdateFunc != None:
            self.UpdateFunc()

        if self.EndCondition():
            self.Action = self.End

    def PlayON(self):
        if self.IsEndOfAnimation():
            self.Action = self.Start

    def EndCondition(self):
        return self.clock >= self.endTime + self.delayTime

    def IsEndOfAnimation(self):
        return self.Action == None

if __name__ == "__main__":
    MainClass().Main()
