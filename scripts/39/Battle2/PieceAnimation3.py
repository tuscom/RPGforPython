import pygame
from pygame.locals import *
import sys

import PieceAnimation2

class PieceAnimation(PieceAnimation2.PieceAnimation):
    def __init__(self, name, ObjectClass): #Animationの最小単位
        self.GetSource(ObjectClass)
        self.ProgramParameter()

        self.SetFunction(name)

    def AfterUsedStart(self):
        self.clock += self.Helper.pygamedeltatime
        if self.clock >= self.delayTime:
            self.Action = self.Update
            if self.AfterUsedStartFunc != None:
                self.AfterUsedStartFunc(self)

    def Update(self):
        self.clock += self.Helper.pygamedeltatime
        if self.EndCondition():
            self.Action = self.End
            self.clock = self.endTime + self.delayTime
        if self.UpdateFunc != None:
            self.UpdateFunc(self)


    #↓静的空間にあるとして扱う
    #バトルメニューボタン移動
    def MoveBattleMenuUpdate(self):
        for i in range(len(self.BattleMenuBtnList)):
            self.BattleMenuBtnList[i].position = self.startPositionList[i] + self.speedList[i]*self.clock
    def MoveBattleMenuFirstUsedStart(self):
        self.BattleMenuBtnList = self.ObjectClass.BattleMenuBtnList
    def DecideParameterForMoveBattleMenu(self):
        self.endTime = 0.2
        self.speedList = [(self.goalPositionList[i] - self.startPositionList[i])/self.endTime for i in range(len(self.BattleMenuBtnList))]
        for i in range(len(self.BattleMenuBtnList)):
            self.BattleMenuBtnList[i].position = pygame.math.Vector2(self.startPositionList[i])
    def MoveBattleMenuAfterUsedStart(self):
        for i in range(len(self.BattleMenuBtnList)):
            self.BattleMenuBtnList[i].position = pygame.math.Vector2(self.startPositionList[i])
    ##戻し
    def BackBattleMenuFirstUsedStart(self):
        self.MoveBattleMenuFirstUsedStart()
        self.startPositionList = [pygame.math.Vector2(btn.position) for btn in self.BattleMenuBtnList]
        self.goalPositionList = [pygame.math.Vector2(self.ObjectClass.position) for i in range(len(self.BattleMenuBtnList))]
        self.DecideParameterForMoveBattleMenu()
    ##表示
    def ShowBattleMenuFirstUsedStart(self):
        self.MoveBattleMenuFirstUsedStart()
        self.goalPositionList = [pygame.math.Vector2(btn.position) for btn in self.BattleMenuBtnList]
        self.startPositionList = [pygame.math.Vector2(self.ObjectClass.position) for i in range(len(self.BattleMenuBtnList))]
        self.DecideParameterForMoveBattleMenu()
