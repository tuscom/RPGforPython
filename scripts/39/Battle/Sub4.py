"""
アニメーション追加
"""

import pygame
from pygame.locals import *
import sys

import Helper
from Helper import BattleHelper

import Sub3 as Sub

class ObjectClass(Sub.ObjectClass):
    def __init__(self, MainClass, kwargs):
        self.MainClass = MainClass
        self.BattleHelper = MainClass.BattleHelper
        self.Helper = MainClass.Helper
        self.screen = MainClass.screen
        self.OneCommandAnimation = MainClass.OneCommandAnimation

        self.SetOptions(kwargs)
        self.SetParameter()
        self.SetButton()
        self.OnInstanceFunc()
        self.SetAction()

    def Start(self):
        self.LoadMaterial()
        self.SetAnimationCommand()
        self.Action = self.Update

    def SetAnimationCommand(self):
        pass

    def Update(self):
        self.HelperUpdate()

        self.Draw()
        self.BtnUpdate()

class AllAnimationController(Sub.AllAnimationController):
    def __init__(self, ContiAnimList):
        self.ContiAnimList = ContiAnimList
        self.Action = self.Start

    def Start(self):
        self.Action = self.Update

    def Update(self):
        self.PlayContiAnim()

    def PlayContiAnim(self):
        list(map(lambda contiAnim : contiAnim.Main(), self.ContiAnimList))

class ContinueAnimation(Sub.ContinueAnimation):
    def __init__(self, CommandAnimationList, kwargs):
        self.SetOptions(kwargs)
        self.SetAction()

        self.CommandAnimationList = CommandAnimationList

    def SetOptions(self, kwargs):
        self.options = {
            "isRepeat" : False,
            "isAutoStart" : True}
        if kwargs != None:
            self.options.update(kwargs)

        self.UpdateFunc = self.RepeatUpdate if self.options["isRepeat"] else self.AutoEndUpdate

    def SetAction(self):
        if self.options["isAutoStart"]:
            self.Action = self.Start
            self.PlayON()
        else:
            self.Action = None

    def Start(self):
        self.noOfComAnim = len(self.CommandAnimationList)
        self.Action = self.Update
        self.indexOfAnimation = 0

    def Update(self):
        self.UpdateFunc()

class OneCommandAnimation(Sub.OneCommandAnimation): 
    def __init__(self, name, ObjectClass, kwargs):
        self.ObjectClass = ObjectClass
        self.PieceAnimation = ObjectClass.MainClass.PieceAnimation

        self.SetOptions(kwargs)

        self.PieceAnimationList = None

        self.Action = None

        self.SelectAnimation(name)

    def SetOptions(self, kwargs):
        self.options = {
            "StartFunc" : None,
            "UpdateFunc" : None,
            "EndFunc" : None}
        if kwargs != None:
            self.options.update(kwargs)
        self.StartFunc = self.options["StartFunc"]
        self.UpdateFunc = self.options["UpdateFunc"]
        self.EndFunc = self.options["EndFunc"]

    def SelectAnimation(self, name):
        self.indexDict = {
            "leftAttackStep" : self.LeftAttackStep,
            "rightAttackStep" : self.RightAttackStep,
            "jump" : self.Jump,
            "mudaniHustle" : self.MudaniHustle,
            "ShowBattleMenu" : self.ShowBattleMenu}

        self.indexDict[name]()

    #バトルメニュー表示
    def ShowBattleMenu(self):
        self.PieceAnimationList = [
            self.PieceAnimation("ShowBattleMenu", self.ObjectClass, None)
            ]

    #左ステップアタック
    def LeftAttackStep(self):
        self.PieceAnimationList = [
            self.PieceAnimation("leftStep", self.ObjectClass, None),
            self.PieceAnimation("HPmoveForAttack", self.ObjectClass, None),
            self.PieceAnimation("NormalAttackEffect", self.ObjectClass, None)
            ]

    #右ステップアタック
    def RightAttackStep(self):
        self.PieceAnimationList = [
            self.PieceAnimation("rightStep", self.ObjectClass, None),
            self.PieceAnimation("HPmoveForAttack", self.ObjectClass, None),
            self.PieceAnimation("NormalAttackEffect", self.ObjectClass, None)
            ]

    def Start(self):
        if self.StartFunc != None:
            self.StartFunc()

        self.Action = self.Update

    def Update(self):
        if self.UpdateFunc != None:
            self.UpdateFunc()
        list(map(lambda pieceAnime : pieceAnime.Main(), self.PieceAnimationList))
        if self.EndCondition():
            self.Action = self.End

    def End(self):
        super().End()
        if self.EndFunc != None:
            self.EndFunc()

    #=================Others==================

class PieceAnimation(Sub.PieceAnimation):
    def __init__(self, name, ObjectClass, kwargs): 
        self.ObjectClass = ObjectClass
        self.MainClass = ObjectClass.MainClass
        self.Helper = self.MainClass.Helper

        self.SetOptions(kwargs)

        self.isEndOfAnimation = False
        self.StartFunc = None
        self.UpdateFunc = None
        self.clock = 0

        self.delayTime = 0

        self.Action = None

        self.SelectAnimation(name)

    def SetOptions(self, kwargs):
        self.options = {"name" : "名無し"}
        if kwargs != None:
            self.options.update(kwargs)
        self.name = self.options["name"]

    def SelectAnimation(self, name):
        self.indexDic = {
            "leftStep" : self.LeftStep,
            "rightStep" : self.RightStep,
            "jump" : self.Jump,
            "HPmove" : self.HPmove,
            "HPmoveForAttack" : self.HPmoveForAttack,
            "ShowBattleMenu" : self.ShowBattleMenu,
            "NormalAttackEffect" : self.NormalAttackEffect}

        self.indexDic[name]()

    #バトルメニュー表示
    def ShowBattleMenu(self):
        self.endTime = 0.2
        self.targetList = self.ObjectClass.BattleMenuBtnList
        self.startPosition = pygame.math.Vector2(self.ObjectClass.position)
        self.goalPosList = [pygame.math.Vector2(btn.position) for btn in self.targetList]

        self.StartFunc = self.ShowBattleMenuStart
        self.UpdateFunc = self.ShowBattleMenuUpdate
    def ShowBattleMenuStart(self):
        self.speedList = [(goalPosition - self.startPosition) / self.endTime for goalPosition in self.goalPosList]
        self.posList = [pygame.math.Vector2(self.startPosition) for i in range(len(self.speedList))]
    def ShowBattleMenuUpdate(self):
        for i in range(len(self.speedList)):
            self.MoveForShowBattleMenu(self.targetList[i], self.posList[i], self.speedList[i])
    def MoveForShowBattleMenu(self, btn, position, speed):
        deltatime = self.Helper.pygamedeltatime
        position += speed * deltatime
        btn.position = pygame.math.Vector2(position)

    #左ステップ
    def LeftStep(self):
        self.endTime = 1
        self.width = 100
        self.StartFunc = self.LeftStepStart
        self.UpdateFunc = self.StepUpdate
    def LeftStepStart(self):
        self.direction = pygame.math.Vector2(-1, 0)
        self.changeDirectionTime = self.endTime/2
        self.position = self.ObjectClass.position
        self.speed = self.width / self.changeDirectionTime
    def StepUpdate(self):
        deltatime = self.Helper.pygamedeltatime
        if self.clock <= self.changeDirectionTime:
            self.position += self.direction * deltatime * self.speed
        elif self.clock > self.changeDirectionTime:
            self.position += -self.direction * deltatime * self.speed

    #右ステップ
    def RightStep(self):
        self.endTime = 1
        self.width = 100
        self.StartFunc = self.RightStepStart
        self.UpdateFunc = self.StepUpdate
    def RightStepStart(self):
        self.direction = pygame.math.Vector2(-1, 0)
        self.changeDirectionTime = self.endTime/2
        self.position = self.ObjectClass.position
        self.speed = self.width / self.changeDirectionTime

    #ノーマル攻撃エフェクト
    def NormalAttackEffect(self):
        self.endTime = 1
        self.screen = self.MainClass.screen
        self.StartFunc = self.NormalAttackEffectStart
        self.UpdateFunc = self.NormalAttackEffectUpdate
    def NormalAttackEffectStart(self):
        self.TargetClass = self.ObjectClass.AttackTarget
        self.sourcePicture = self.MainClass.normalAttackPicture
        size = self.sourcePicture.get_size()
        self.scale = pygame.math.Vector2(size[0], size[1])
        self.speed = -self.scale / self.endTime
        self.position = pygame.math.Vector2(self.TargetClass.position)
    def NormalAttackEffectUpdate(self):
        deltatime = self.Helper.pygamedeltatime
        self.scale += self.speed * deltatime
        picture = pygame.transform.scale(
            self.sourcePicture,
            [int(self.scale.x), int(self.scale.y)])

        self.position -= self.speed / 2 * deltatime
        self.screen.blit(picture, self.position)

    #攻撃のためのHP変動
    def HPmoveForAttack(self):
        self.endTime = 0.5
        self.delayTime = 0.5
        self.StartFunc = self.HPmoveForAttackStart
        self.UpdateFunc = self.HPmoveForAttackUpdate
    def HPmoveForAttackStart(self):
        self.TargetClass = self.ObjectClass.AttackTarget
        damage=10
        self.HPbarPicture = self.TargetClass.HPbarPicture
        self.pictureScale = self.HPbarPicture.get_size()
        pictureScaleRatio = self.pictureScale[0] / self.TargetClass.hp
        self.speed = damage * pictureScaleRatio / self.endTime
        self.TargetClass.hp -= damage
    def HPmoveForAttackUpdate(self):
        clock = self.clock - self.delayTime
        pictureScale = (
            self.pictureScale[0]-self.speed*clock,
            self.pictureScale[1])
        self.TargetClass.HPbarPicture = pygame.transform.scale(
            self.HPbarPicture,
            [int(pictureScale[0]), int(pictureScale[1])]
            )


    def Start(self):
        self.clock += self.Helper.pygamedeltatime
        if self.clock >= self.delayTime:

            if self.StartFunc != None:
                self.StartFunc()

            self.isEndOfAnimation = False
            self.Action = self.Update

    def Update(self):
        self.clock += self.Helper.pygamedeltatime
        if self.UpdateFunc != None:
            self.UpdateFunc()

        if self.EndCondition():
            self.Action = self.End
