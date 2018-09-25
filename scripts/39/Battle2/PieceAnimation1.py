"""
Pygameの描画の特徴（仮定）
・おそらく、現在と少し前の描画が同時に行われる。
"""
import pygame
from pygame.locals import *
import sys

class PieceAnimation:
    def __init__(self, name, ObjectClass): #Animationの最小単位
        self.GetSource(ObjectClass)
        self.ProgramParameter()

        self.SetFunction(name)


    def GetSource(self, ObjectClass):
        self.ObjectClass = ObjectClass
        self.MainClass = ObjectClass.MainClass
        self.AnimController = self.MainClass.AllAnimationController
        self.PieceAnimDic = self.AnimController.PieceAnimDic
        self.Helper = self.MainClass.Helper
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
        if self.UpdateFunc != None:
            self.UpdateFunc(self)

        if self.EndCondition():
            self.Action = self.End

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


    #↓静的空間にあるとして扱う
    #左ステップ
    #def LeftStep(self):
    #    self.endTime = 1
    #    self.width = 100
    #    self.StartFunc = self.LeftStepStart
    #    self.UpdateFunc = self.LeftStepUpdate
    #def LeftStepStart(self):
    #    pass
    #def LeftStepUpdate(self):
    #    pass

    #ジャンプ
    #def Jump(self):
    #    self.endTime = 1
    #    self.height = 100

    #    self.StartFunc = self.JumpStart
    #    self.UpdateFunc = self.JumpUpdate
    #def JumpStart(self):
    #    self.firstPosition = self.ObjectClass.position
    def JumpUpdate(self):
        y = -(self.clock - self.endTime/2)**2 * (4*self.endTime*self.height) + self.height
        y = self.startPosition.y - y #y軸が逆向き

        position = pygame.math.Vector2(self.startPosition.x, y)
        self.ObjectClass.position = pygame.math.Vector2(position)
    def JumpFirstUsedStart(self):
        self.endTime = 1
        self.height = 100
    def JumpAfterUsedStart(self):
        self.startPosition = self.ObjectClass.position

    #HP変動
    #def HPmove(self):
    #    self.endTime = 0.5
    #    self.delayTime = 0.5
    #    self.StartFunc = self.HPmoveStart
    #    self.UpdateFunc = self.HPmoveUpdate
    #def HPmoveStart(self):
    #    damage=10
    #    self.HPbarPicture = self.ObjectClass.HPbarPicture
    #    self.pictureScale = self.HPbarPicture.get_size()
    #    pictureScaleRatio = self.pictureScale[0] / self.ObjectClass.hp
    #    self.speed = damage * pictureScaleRatio / self.endTime
    #    self.ObjectClass.hp -= damage
    #def HPmoveUpdate(self):
    #    clock = self.clock - self.delayTime
    #    pictureScale = (
    #        self.pictureScale[0]-self.speed*clock,
    #        self.pictureScale[1])
    #    self.ObjectClass.HPbarPicture = pygame.transform.scale(
    #        self.HPbarPicture,
    #        [int(pictureScale[0]), int(pictureScale[1])]
    #        )


