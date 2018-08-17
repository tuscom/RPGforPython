import pygame
from pygame.locals import *
import sys

import Base2

#========================ver0.0.2===================
class MainClass(Base2.BaseMainClass):
    def __init__(self):
        super().__init__()
        self.Helper = HelperClass(self)

        #First Stage
        player = PlayerClass(self, name="餃子")
        objects = [ObjectClass(self, name="木", picturepath="../../pictures/2a39c2a648133318340ed5bd1fb9a762.png", position=pygame.math.Vector2(5, 3)*self.squareSize, scale=pygame.math.Vector2(1, 1)),
                        ObjectClass(self, name="木", picturepath="../../pictures/2a39c2a648133318340ed5bd1fb9a762.png", position=pygame.math.Vector2(10, 3)*self.squareSize, scale=pygame.math.Vector2(3, 3)),
                        ObjectClass(self, name="木", picturepath="../../pictures/2a39c2a648133318340ed5bd1fb9a762.png", position=pygame.math.Vector2(20, 10)*self.squareSize, scale=pygame.math.Vector2(10, 10)),
                        ObjectClass(self, name="木", picturepath="../../pictures/2a39c2a648133318340ed5bd1fb9a762.png", position=pygame.math.Vector2(10, 10)*self.squareSize, scale=pygame.math.Vector2(20, 20))]
        enemies = [TouchEventClass(self, name="トラバチ", picturepath="../../pictures/9c338508771fd401ada29fba07b34ebf.png", position=pygame.math.Vector2(3, 3)*self.squareSize, scale=pygame.math.Vector2(1, 1), func=lambda:print("touch!")),

                   TouchEventClass(self, name="BlackHole", picturepath="../../pictures/b8b25fb3b973b764dd6f1e40c0125952_t.jpg", position=pygame.math.Vector2(10, 0)*self.squareSize, scale=pygame.math.Vector2(1,1), func=lambda: self.Window.ChangeStage(self.SecondStage))]
        picture = HelperClass.ScaledPicture("../../pictures/stage.png", size=self.windowSize)
        self.FirstStage = StageClass(self, player=player, objects=objects, enemies=enemies, picture=picture)

        #Second Stage
        player = PlayerClass(self, name="餃子")
        objects = [ObjectClass(self, name="木", picturepath="../../pictures/2a39c2a648133318340ed5bd1fb9a762.png", position=pygame.math.Vector2(5, 3)*self.squareSize, scale=pygame.math.Vector2(1, 1)),
                        ObjectClass(self, name="木", picturepath="../../pictures/2a39c2a648133318340ed5bd1fb9a762.png", position=pygame.math.Vector2(10, 3)*self.squareSize, scale=pygame.math.Vector2(3, 3)),
                        ObjectClass(self, name="木", picturepath="../../pictures/2a39c2a648133318340ed5bd1fb9a762.png", position=pygame.math.Vector2(20, 10)*self.squareSize, scale=pygame.math.Vector2(10, 10)),
                        ]
        enemies = [TouchEventClass(self, name="BlackHole", picturepath="../../pictures/b8b25fb3b973b764dd6f1e40c0125952_t.jpg", position=pygame.math.Vector2(10, 0)*self.squareSize, scale=pygame.math.Vector2(1,1), func=lambda:self.Window.ChangeStage(self.FirstStage))]
        picture = HelperClass.ScaledPicture("../../pictures/stage.png", size=self.windowSize)
        self.SecondStage = StageClass(self, player=player, objects=objects, enemies=enemies, picture=picture)

        self.Window = self.FirstStage
class ObjectClass(Base2.BaseObjectClass):
    def __init__(self, MainClass, **kwargs):
        super().__init__(MainClass, kwargs)

class TouchEventClass(Base2.BaseTouchEventClass):
    def __init__(self, MainClass, **kwargs):
        super().__init__(MainClass, kwargs)

class PlayerClass(Base2.BasePlayerClass):
    def __init__(self, MainClass, **kwargs):
        super().__init__(MainClass, kwargs)

    def ResetPosition(self):
        self.position = self.options["position"]
        self.nextPos = pygame.math.Vector2(self.position)

class StageClass(Base2.BaseStageClass):
    def __init__(self, MainClass, **kwargs):
        super().__init__(MainClass, kwargs)

class HelperClass(Base2.BaseHelperClass):
    def __init__(self, MainClass):
        super().__init__(MainClass)

#========================実行部分====================
MainClass().Main()