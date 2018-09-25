import ObjectClass1


"""
アニメーションの構造
"""

import pygame
from pygame.locals import *
import sys

class ObjectClass(ObjectClass1.ObjectClass):
    def __init__(self, MainClass, kwargs):
        self.GetSource(MainClass)
        self.SetOptions(kwargs)
        self.SetParameter()

        self.OnInstanceFunc()
        self.SetObjAnimDic()

        self.Action = self.Start

    def GetSource(self, MainClass):
        super().GetSource(MainClass)
        self.OneCmdAnim = MainClass.OneCmdAnim
        self.AllAnimationController = MainClass.AllAnimationController

    def SetObjAnimDic(self):
        self.ObjAnimDic = {
            "jump" : self.OneCmdAnim("jump", self, None)
            } # CmdAnimName : OneCmdAnim(class)

    def Start(self):
        self.LoadMaterial()
        self.Action = self.Update

    def Update(self):
        self.HelperUpdate()
        self.Draw()
        self.BtnUpdate()

    #Others
    def AddContinueAnim(self, ContiAnimName, CmdAnimName):
        CmdAnim = self.ObjAnimDic[CmdAnimName]
        self.AllAnimationController.AddContinueAnim(ContiAnimName, CmdAnim)

    def AddSingleAnim(self, CmdAnimName):
        CmdAnim = self.ObjAnimDic[CmdAnimName]
        self.AllAnimationController.AddSingleAnim(CmdAnim)
