"""
機能
基本的なアニメーション構造追加

要求version
ObjectClass            : 2
FieldCharacter         : 2
FieldEnemy             : 1
FieldFamily            : 2
IconCharacter          : 1
PieceAnimation         : 1
OneCmdAnim             : 1
AllAnimationController : 1
"""


import pygame
from pygame.locals import *
import sys

from Source import *

import Main1

class MainClass(Main1.MainClass):
    def __init__(self):
        self.WindowParameter()
        self.FieldParameter()
        self.ControllerPanelParameter()
        self.ProgramParameter()
        self.GetSource()

        self.SetWindow()

    def GetSource(self):
        super().GetSource()
        self.PieceAnimation = PieceAnimation
        self.AllAnimationController = AllAnimationController(self)

    def Start(self):
        self.LoadMaterial()
        self.SetFieldCharacter()
        self.SetPanel()
        self.Action = self.Update

    def Update(self):
        self.DrawBackGround()
        self.MainAllObjects()
        self.AllAnimationController.Main()

if __name__ == "__main__":
    MainClass().Main()
