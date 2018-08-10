import pygame
from pygame.locals import *
import sys

import __Main

#=================ver0.0.1==================
class MainClass(__Main.BaseMainClass):
    def __init__(self):
        super().__init__()

        self.Helper = HelperClass(self)
        self.Window = StageClass(self)

class ObjectClass(__Main.BaseObjectClass):
    def __init__(self, MainClass, **kwargs):
        super().__init__(MainClass, kwargs)

class PlayerClass(__Main.BasePlayerClass):
    def __init__(self, MainClass, **kwargs):
        super().__init__(MainClass, kwargs)

        self.speedFactor = 1

        self.HorizontalDirection = self.Helper.nowPressed[K_RIGHT] - self.Helper.nowPressed[K_LEFT]
        self.VerticalDirection = self.Helper.nowPressed[K_UP] - self.Helper.nowPressed[K_DOWN]

        self.nextPos = pygame.math.Vector2(self.position)
        self.goalDirection = self.nextPos - self.position
        self.movingDirection = self.nextPos - self.position
        if (self.movingDirection.x**2 + self.movingDirection.y**2)**(1/2) != 0:
            self.deltaPos = self.movingDirection.normalize() * self.speedFactor
        else:
            self.deltaPos = pygame.math.Vector2(0, 0)
        self.DeltaPositionVectorDot = self.movingDirection.dot(self.goalDirection)

    def ConditionPos(self):
        result = False

        #変数更新
        self.HorizontalDirection = self.Helper.nowPressed[K_RIGHT] - self.Helper.nowPressed[K_LEFT]
        self.VerticalDirection = self.Helper.nowPressed[K_UP] - self.Helper.nowPressed[K_DOWN]
        self.movingDirection = self.nextPos - self.position
        if (self.movingDirection.x**2 + self.movingDirection.y**2)**(1/2) != 0:
            self.deltaPos = self.movingDirection.normalize() * self.speedFactor
        else:
            self.deltaPos = pygame.math.Vector2(0, 0)
        self.DeltaPositionVectorDot = self.movingDirection.dot(self.goalDirection)

        #移動条件
        if self.DeltaPositionVectorDot > 0:
            result = True

        #移動目的地の設定 : 入力はあるけど到着している→出発の瞬間
        if self.DeltaPositionVectorDot <= 0:
                
            self.position = pygame.math.Vector2(self.nextPos)
                    
            if self.ConditionArea():
                self.nextPos += (self.HorizontalDirection * pygame.math.Vector2(1, 0) + self.VerticalDirection * pygame.math.Vector2(0, -1)) * self.MainClass.squareSize

            self.goalDirection = self.nextPos - self.position

        return result

    def ReflectPos(self):
        self.position += self.deltaPos

    def ConditionArea(self):
        deltaNewPos = (self.HorizontalDirection * pygame.math.Vector2(1, 0) + self.VerticalDirection * pygame.math.Vector2(0, -1)) * self.MainClass.squareSize
        result = all(list(map(lambda point : self.MainClass.Window.IsInArea(point), self.Area(deltaNewPos+self.nextPos))))
        return result

class StageClass(__Main.BaseStageClass):
    def __init__(self, MainClass, **kwargs):
        super().__init__(MainClass, kwargs)

        #プレイヤー配置
        self.player = PlayerClass(MainClass)
        #障害物配置
        self.objects = [ObjectClass(MainClass, name="木", picturepath="../../pictures/2a39c2a648133318340ed5bd1fb9a762.png", position=pygame.math.Vector2(5, 3)*MainClass.squareSize, scale=pygame.math.Vector2(1, 1)),
                        ObjectClass(MainClass, name="木", picturepath="../../pictures/2a39c2a648133318340ed5bd1fb9a762.png", position=pygame.math.Vector2(10, 3)*MainClass.squareSize, scale=pygame.math.Vector2(3, 3)),
                        ObjectClass(MainClass, name="木", picturepath="../../pictures/2a39c2a648133318340ed5bd1fb9a762.png", position=pygame.math.Vector2(20, 10)*MainClass.squareSize, scale=pygame.math.Vector2(10, 10)),
                        ObjectClass(MainClass, name="木", picturepath="../../pictures/2a39c2a648133318340ed5bd1fb9a762.png", position=pygame.math.Vector2(10, 10)*MainClass.squareSize, scale=pygame.math.Vector2(20, 20))]
        self.enemies = [ObjectClass(MainClass, name="トラバチ", picturepath="../../pictures/9c338508771fd401ada29fba07b34ebf.png", position=pygame.math.Vector2(3, 3)*MainClass.squareSize, scale=pygame.math.Vector2(1, 1))]

        #配置条件
        self.availableArea = {}
        self.gridWindowSize = self.Helper.WorldToGridPos(pygame.math.Vector2(MainClass.windowSize[0], MainClass.windowSize[1]))
        self.AddArea(pygame.math.Vector2(), self.gridWindowSize)
        list(map(lambda obj : self.RemoveArea(obj.position, obj.position+pygame.math.Vector2(1,1).elementwise()*obj.scale*MainClass.squareSize), self.objects))


    def AddArea(self, fromVector2, toVector2):
        gridCountV2 = (toVector2 - fromVector2) // self.MainClass.squareSize
        noOfArea = int(gridCountV2.x * gridCountV2.y)

        for i in range(noOfArea):
            x = i%gridCountV2.x * self.MainClass.squareSize
            y = i//gridCountV2.x * self.MainClass.squareSize
            pointV2 = pygame.math.Vector2(x, y)
            self.availableArea[(int(pointV2.x), int(pointV2.y))] = True

    def RemoveArea(self, fromVector2, toVector2):
        gridCountV2 = (toVector2 - fromVector2) // self.MainClass.squareSize
        noOfArea = int(gridCountV2.x * gridCountV2.y)

        for i in range(noOfArea):
            x = i%gridCountV2.x * self.MainClass.squareSize
            y = i//gridCountV2.x * self.MainClass.squareSize
            pointV2 = pygame.math.Vector2(x, y)
            pointV2 += fromVector2
            self.availableArea[(int(pointV2.x), int(pointV2.y))] = False

    def IsInArea(self, targetV2):
        result = False
        try:
            result = self.availableArea[(int(targetV2.x), int(targetV2.y))]
        except KeyError:
            result = False

        return result

class HelperClass(__Main.BaseHelperClass):
    def __init__(self, MainClass):
        super().__init__(MainClass)

#====================実行部分=================
MainClass().Main()