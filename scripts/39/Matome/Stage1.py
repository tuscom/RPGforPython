import pygame
from pygame.locals import *
import sys

class Stage:
    def __init__(self, MainClass, kwargs):
        self.GetSource(MainClass)
        self.SetOptions(kwargs)
        self.FunctionParameter()

    def GetSource(self, MainClass):
        self.MainClass = MainClass
        self.screen = MainClass.screen
        self.Helper = MainClass.Helper
        self.HelperModule = MainClass.HelperModule
        self.MoveModeObjectClass = MainClass.MoveModeObjectClass
        self.ObjectClass = MainClass.ObjectClass

        self.MoveMode = MainClass.MoveMode

    def SetOptions(self, kwargs):
        self.options={"name" : "TestStage",
                      "picture" : None}
        if kwargs != None:
            self.options.update(kwargs)

    def FunctionParameter(self):
        self.Start = self.FirstUsedStart
        self.Action = self.Start
        self.availableArea = []

    def Main(self):
        if self.Action != None:
            self.Action()

    def ObjectsParameter(self):
        self.picturepath = None

    #Start系
    def FirstUsedStart(self):
        self.SetObjects()
        self.BackgroundParameter()
        self.AfterUsedStart()
        self.Start = self.AfterUsedStart

    def AfterUsedStart(self):
        self.Action = self.Update

    def SetObjects(self):
        #配置するもの。
        stageDic = {"TestStage" : self.TestStage}
        bgDic = {"TestStage" : "../../../pictures/stage.png"}
        
        stageDic[self.options["name"]]()
        self.picturepath = bgDic[self.options["name"]]

    def BackgroundParameter(self):
        windowSize = self.MainClass.windowSize
        #self.picture = self.HelperModule.ScaledPicture(self.picturepath, windowSize)
        bgKwargs = {
            "picturepath" : self.picturepath,
            "scale" : pygame.math.Vector2(windowSize[0], windowSize[1]),
            "ModeClass" : self.MoveMode
            }
        self.bgObject = self.ObjectClass(self.MainClass, bgKwargs)

    #Update系
    def Update(self):
        self.Draw()

    def Draw(self):

        list(map(lambda object:object.Update(), self.objects))
        list(map(lambda enemies:enemies.Update(), self.enemies))
        if self.player != None:
            self.player.Update()

    #Others系
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

    def Reset(self):
        self.player.ResetPosition()
        list(map(lambda object:object.ResetPosition(), self.objects))
        list(map(lambda enemy:enemy.ResetPosition(), self.enemies))

    def ChangeStage(self, StageClass):
        self.Reset()
        self.MainClass.Window = StageClass

    #Stage登録
    def TestStage(self):
        self.player = None
        self.objects = []
        self.enemies = []

