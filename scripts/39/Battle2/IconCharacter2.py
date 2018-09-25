import pygame
from pygame.locals import *
import sys

import IconCharacter1

class IconCharacter(IconCharacter1.IconCharacter):
    def __init__(self, MainClass, CharaClass, kwargs):
        self.GetSource(MainClass, CharaClass)
        self.SetOptions(kwargs)
        self.ProgramParameter()

        self.OnInstanceFunc()
        self.SetObjAnimDic()

    def OnInstanceFunc(self):
        super().OnInstanceFunc()
        self.CharaClass.IconClass = self

    def Start(self):
        self.LoadMaterial()
        self.SetScale()
        self.SetHPbar()
        self.SetHPbarPosition()
        self.SetbgPicture()
        self.SetCharacterPicture()
        self.Action = self.Update

    def Update(self):
        self.HelperUpdate()
        self.Draw()
        self.BtnUpdate()
