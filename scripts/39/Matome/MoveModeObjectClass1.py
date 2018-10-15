import pygame
from pygame.locals import *
import sys

from Source1 import ObjectClass

class MoveModeObjectClass(ObjectClass):
    def __init__(self,MainClass, kwargs):
        super().__init__(MainClass, kwargs)

    def GetSource(self, MainClass):
        super().GetSource(MainClass)
        self.squareSize = self.MainClass.squareSize

    def TransformParameter(self):
        super().TransformParameter()
        self.scale = self.options["scale"] * self.squareSize

#class MoveObjectClass(ObjectClass):
#    def __init__(self, MainClass, kwargs):
#        super().__init__(MainClass, kwargs)

#        self.MoveParameter()

#    def SetOptions(self, kwargs):
#        super().SetOptions(kwargs)
#        self.options.update({
#            "speedFactor" : 1
#            })
#        if kwargs != None:
#            self.options.update(kwargs)

#    def GetSource(self, MainClass):
#        super().GetSource(MainClass)
#        self.squareSize = MainClass.squareSize

#    def TransformParameter(self):
#        self.position = self.options["position"]
#        scaleRatio = self.options["scale"]
#        self.scale = self.squareSize * scaleRatio

#    def MoveParameter(self):
#        self.speedFactor = 1
#        self.nextPos = pygame.math.Vector2(self.position)
#        self.goalDirection = self.nextPos - self.position
#        self.movingDirection = self.nextPos - self.position
#        if (self.movingDirection.x**2 + self.movingDirection.y**2)**(1/2) != 0:
#            self.deltaPos = self.movingDirection.normalize() * self.speedFactor
#        else:
#            self.deltaPos = pygame.math.Vector2(0, 0)
#        self.DeltaPositionVectorDot = self.movingDirection.dot(self.goalDirection)
#        self.HorizontalDirection = self.Helper.intHorizontalKey
#        self.VerticalDirection = self.Helper.intVerticalKey

#    #Update系
#    def Update(self):
#        super().Update()
#        self.Move()

#    def Move(self):
#        self.InputPos()
#        if self.ConditionPos():
#            self.ReflectPos()

#    def InputPos(self):
#        self.HorizontalDirection = self.Helper.intHorizontalKey
#        self.VerticalDirection = self.Helper.intVerticalKey

#    def ConditionPos(self):
#        result = False
#        #変数更新
#        self.movingDirection = self.nextPos - self.position
#        if (self.movingDirection.x**2 + self.movingDirection.y**2)**(1/2) != 0:
#            self.deltaPos = self.movingDirection.normalize() * self.speedFactor
#        else:
#            self.deltaPos = pygame.math.Vector2(0, 0)
#        self.DeltaPositionVectorDot = self.movingDirection.dot(self.goalDirection)

#        #移動条件
#        if self.DeltaPositionVectorDot > 0:
#            result = True

#        #移動目的地の設定 : 入力はあるけど到着している→出発の瞬間
#        if self.DeltaPositionVectorDot <= 0:
                
#            self.position = pygame.math.Vector2(self.nextPos)
                    
#            if self.ConditionArea():
#                self.nextPos += (self.HorizontalDirection * pygame.math.Vector2(1, 0) + self.VerticalDirection * pygame.math.Vector2(0, -1)) * self.MainClass.squareSize

#            self.goalDirection = self.nextPos - self.position

#        return result

#    def ReflectPos(self):
#        self.position += self.deltaPos

#    def ConditionArea(self):
#        deltaNewPos = (self.HorizontalDirection * pygame.math.Vector2(1, 0) + self.VerticalDirection * pygame.math.Vector2(0, -1)) * self.MainClass.squareSize
#        result = all(list(map(lambda point : self.MainClass.Window.IsInArea(point), self.Area(deltaNewPos+self.nextPos))))
#        return result
