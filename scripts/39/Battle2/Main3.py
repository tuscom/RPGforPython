"""
機能
アニメーション追加。HP変動できるようにする

要求version
ObjectClass            : 3
FieldCharacter         : 3
FieldEnemy             : 2
FieldFamily            : 3
IconCharacter          : 2
PieceAnimation         : 2
OneCmdAnim             : 1
AllAnimationController : 2
"""


import pygame
from pygame.locals import *
import sys

from Source import *

import Main2 as MainModule

class MainClass(MainModule.MainClass):
    def __init__(self):
        self.WindowParameter()
        self.FieldParameter()
        self.ControllerPanelParameter()
        self.ProgramParameter()
        self.GetSource()

        self.SetWindow()

    def Start(self):
        self.LoadMaterial()
        self.SetFieldCharacter()
        self.SetPanel()
        self.Action = self.Update

    def Update(self):
        self.DrawBackGround()
        self.MainAllObjects()
        self.AllAnimationController.Main()

    #Others
    def Family(self):
        result = list(filter(lambda ObjClass : type(ObjClass) == self.FieldFamily, self.AllObjects))
        return result

    def Enemies(self):
        result = list(filter(lambda ObjClass:type(ObjClass) == self.FieldEnemy, self.AllObjects))
        return result


if __name__ == "__main__":
    MainClass().Main()
