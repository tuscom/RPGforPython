import pygame
from pygame.locals import *
import sys

import FieldEnemy2 as OldFieldEnemy

class FieldEnemy(OldFieldEnemy.FieldEnemy):
    def __init__(self, MainClass, kwargs):
        self.GetSource(MainClass)
        self.SetOptions(kwargs)
        self.ProgramParameter()

        self.OnInstanceFunc()
        self.SetObjAnimDic()

    def SetOptions(self, kwargs):
        self.options = {
            "name" : "名無し",
            "picturepath" : "../../../pictures/mon_016.bmp",
            "position" : pygame.math.Vector2(),
            "scale" : pygame.math.Vector2(100, 100),
            "btnFunc" : None,
            "speed" : 10,
            "hp" : 100,
            "HPbarPicturePath" : "../../../pictures/HPbar.png",
            "HPbarbackPicturePath" : "../../../pictures/HPbar_back.png",
            "HPbarThick" : 10,
            "battleMenuName" : ["stepAttack", "jump"]
            }
        if kwargs != None:
            self.options.update(kwargs)

    def Start(self):
        self.Action = self.Update
        self.LoadMaterial()
        self.SetHPbar()
        self.AutoSelectAttackTarget()

    def Update(self):
        self.HelperUpdate()
        self.Draw()
        self.BtnUpdate()

