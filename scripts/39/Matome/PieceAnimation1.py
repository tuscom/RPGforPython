import pygame
from pygame.locals import *
import sys

class PieceAnimation:
    def __init__(self, name, ObjectClass, ParentOneCmdAnim): #Animationの最小単位
        self.GetSource(ObjectClass, ParentOneCmdAnim)
        self.ProgramParameter()

        self.SetFunction(name)


    def GetSource(self, ObjectClass, ParentOneCmdAnim):
        self.ObjectClass = ObjectClass
        self.MainClass = ObjectClass.MainClass
        self.AnimController = self.MainClass.AllAnimationController
        self.PieceAnimDic = self.AnimController.PieceAnimDic
        self.Helper = self.MainClass.Helper
        self.ParentOneCmdAnim = ParentOneCmdAnim
    def ProgramParameter(self):
        self.delayTime = 0
        self.endTime = 1
        self.clock = 0
        self.UpdateFunc = None
        self.Action = None
        self.Start = self.FirstUsedStart
    def SetFunction(self, name):
        FuncList = self.PieceAnimDic[name]
        self.FirstUsedStartFunc = FuncList[0]
        self.AfterUsedStartFunc = FuncList[1]
        self.UpdateFunc = FuncList[2]

    #Main
    def Main(self):
        if self.Action != None:
            self.Action()

    def FirstUsedStart(self):
        if self.FirstUsedStartFunc != None:
            self.FirstUsedStartFunc(self)

        self.Start = self.AfterUsedStart
        self.Action = self.Start

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

    def End(self):
        self.clock = 0
        self.Action = None

    #Others
    def PlayON(self):
        if self.IsEndOfAnimation():
            self.Action = self.Start

    def EndCondition(self):
        return self.clock >= self.endTime + self.delayTime

    def IsEndOfAnimation(self):
        return self.Action == None

    #↓静的空間
    #ステップ
    def StepAfterUsedStart(self):
        self.position = self.ObjectClass.position
    def StepUpdate(self):
        deltatime = self.Helper.pygamedeltatime
        if self.clock <= self.changeDirectionTime:
            self.position += self.direction * deltatime * self.speed
        elif self.clock > self.changeDirectionTime:
            self.position += -self.direction * deltatime * self.speed
    #左ステップ
    def LeftStepFirstUsedStart(self):
        self.endTime = 1
        self.changeDirectionTime = self.endTime / 2
        self.width = 100
        self.direction = pygame.math.Vector2(-1, 0)
        self.speed = self.width / self.changeDirectionTime
    #右ステップ
    def RightStepFirstUsedStart(self):
        self.endTime = 1
        self.changeDirectionTime = self.endTime / 2
        self.width = 100
        self.direction = pygame.math.Vector2(1, 0)
        self.speed = self.width / self.changeDirectionTime

    #HP変動
    def HPmoveAfterUsedStart(self):
        damage = 10
        self.HPbarPicture = self.TargetObject.HPbarPicture
        self.pictureScale = self.HPbarPicture.get_size()
        pictureScaleRatio = self.pictureScale[0] / self.TargetObject.hp
        self.speed = damage * pictureScaleRatio / self.endTime
        self.TargetObject.hp -= damage
    def HPmoveUpdate(self):
        clock = self.clock - self.delayTime
        pictureScale = (
            self.pictureScale[0]-self.speed*clock,
            self.pictureScale[1])
        self.TargetObject.HPbarPicture = pygame.transform.scale(
            self.HPbarPicture,
            [int(pictureScale[0]), int(pictureScale[1])]
            )
        self.TargetObject.SetHPbarPicture(
            pygame.transform.scale(
                self.HPbarPicture,
                [int(pictureScale[0]), int(pictureScale[1])]
                )
            )
    #味方HP変動
    def HPmoveOfFamilyFirstUsedStart(self):
        self.TargetObject = self.ObjectClass
        self.endTime = 0.5
        self.delayTime = 0.5
    #敵HP変動
    def HPmoveOfEnemyFirstUsedStart(self):
        self.TargetObject = self.ObjectClass.AttackTarget
        self.endTime = 0.5
        self.delayTime = 0.5

