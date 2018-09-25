import pygame
from pygame.locals import *
import sys

import FieldCharacter2

class FieldCharacter(FieldCharacter2.FieldCharacter):
    def __init__(self, MainClass, kwargs):
        self.GetSource(MainClass)
        self.SetOptions(kwargs)
        self.ProgramParameter()

        self.OnInstanceFunc()
        self.SetObjAnimDic()

    def ProgramParameter(self):
        super().ProgramParameter()
        self.AttackTarget = None
        self.speed = self.options["speed"]
        self.hp = self.options["hp"]


    def Start(self):
        self.Action = self.Update
        self.LoadMaterial()
        self.AutoSelectAttackTarget()

    def AutoSelectAttackTarget(self):
        pass

    def Update(self):
        self.HelperUpdate()
        self.Draw()
        self.BtnUpdate()
