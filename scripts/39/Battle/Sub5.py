import pygame
from pygame.locals import *
import sys
import random
import copy
import math

import Helper
from Helper import BattleHelper

import Sub4 as Sub

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

class ContinueAnimation(Sub.ContinueAnimation):
    def __init__(self, CommandAnimationList, kwargs):
        self.SetOptions(kwargs)
        self.SetAction()

        self.CommandAnimationList = CommandAnimationList

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

    def SelectAnimation(self, name):
        self.indexDict = {
            "leftAttackStep" : self.LeftAttackStep,
            "rightAttackStep" : self.RightAttackStep,
            "jump" : self.Jump,
            "mudaniHustle" : self.MudaniHustle,
            "ShowBattleMenu" : self.ShowBattleMenu,
            "BackBattleMenu" : self.BackBattleMenu,
            "explosion" : self.Explosion}

        self.indexDict[name]()

    #バトルメニュー戻し
    def BackBattleMenu(self):
        self.PieceAnimationList = [
            self.PieceAnimation("BackBattleMenu", self.ObjectClass, None)
            ]

    #爆破
    def Explosion(self):
        self.PieceAnimationList = [
            self.PieceAnimation("explosion", self.ObjectClass, None)
            ]

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

    def SelectAnimation(self, name):
        self.indexDic = {
            "leftStep" : self.LeftStep,
            "rightStep" : self.RightStep,
            "jump" : self.Jump,
            "HPmove" : self.HPmove,
            "HPmoveForAttack" : self.HPmoveForAttack,
            "ShowBattleMenu" : self.ShowBattleMenu,
            "BackBattleMenu" : self.BackBattleMenu,
            "NormalAttackEffect" : self.NormalAttackEffect,
            "explosion" : self.Explosion}

        self.indexDic[name]()

    #バトルメニュー表示
    def ShowBattleMenuStart(self):
        super().ShowBattleMenuStart()
        self.MainClass.ShowBattleMenuAnimSwitch = True
        for i in range(len(self.posList)):
            self.targetList[i].position = pygame.math.Vector2(self.posList[i])
        
    #バトルメニュー戻し
    def BackBattleMenu(self):
        self.endTime = 0.2
        self.targetList = self.ObjectClass.BattleMenuBtnList
        self.goalPosition = pygame.math.Vector2(self.ObjectClass.position)
        self.startPosList = [pygame.math.Vector2(btn.position) for btn in self.targetList]

        self.StartFunc = self.BackBattleMenuStart
        self.UpdateFunc = self.ShowBattleMenuUpdate
    def BackBattleMenuStart(self):
        self.speedList = [(self.goalPosition - startPosition) / self.endTime for startPosition in self.startPosList]
        self.posList = [pygame.math.Vector2(startPosition) for startPosition in self.startPosList]

    #爆破
    def Explosion(self):
        self.endTime = 1
        self.range = 10
        self.interval= 0.3
        self.speed = 1
        self.screen = self.MainClass.screen
        self.StartFunc = self.ExplosionStart
        self.UpdateFunc = self.ExplosionUpdate
    def ExplosionStart(self):
        self.centerPos = (pygame.math.Vector2(self.ObjectClass.position) + pygame.math.Vector2(self.ObjectClass.scale)) / 2
        self.pictureList = [copy.deepcopy(self.MainClass.explosionPicture)]
        self.gapV2 = pygame.math.Vector2(random.randint(-self.range, self.range), random.randint(-self.range, self.range))
        self.posList = [self.centerPos+self.gapV2]
    def ExplosionUpdate(self):
        list(map(lambda pos:self.MoveForExplosion(pos), self.posList))
        self.DrawForExplosion()
        if math.ceil(self.clock*10) % int(self.interval*10) == 0:
            self.pictureList.append(copy.deepcopy(self.MainClass.explosionPicture))
            self.gapV2 = pygame.math.Vector2(random.randint(-self.range, self.range), random.randint(-self.range, self.range))
            self.posList.append(self.centerPos+self.gapV2)

    def MoveForExplosion(self, pos):
        deltatime = self.Helper.pygamedeltatime
        pos += self.speed * deltatime * pygame.math.Vector2(0, -1)
    def DrawForExplosion(self):
        for i in range(self.noOfPicture):
            self.screen.blit(self.pictureList[i], self.posList[i])
