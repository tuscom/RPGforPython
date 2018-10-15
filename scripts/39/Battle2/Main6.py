"""
機能
・全てのクラス内関数の把握
・Mainの関数をモード毎に分割。更に、それぞれStart、Updateに分割。

要求version
ObjectClass            : 5
FieldCharacter         : 5
FieldEnemy             : 4
FieldFamily            : 5
IconCharacter          : 3
PieceAnimation         : 4
OneCmdAnim             : 3
AllAnimationController : 4
Button                 : 1
"""


import pygame
from pygame.locals import *
import sys

from Source import *

import Main5 as MainModule

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
        self.SetTargetIconPicture()
        self.SceneParameter()
        self.Action = self.Update

        self.SetFade()

    def Update(self):
        self.DrawBackGround()
        self.MainAllObjects()
        self.DrawTargetIcon()
        self.AllAnimationController.Main()
        self.PanelController()
        self.SceneController()
