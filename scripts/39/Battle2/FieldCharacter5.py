import pygame
from pygame.locals import *
import sys

import FieldCharacter4 as OldFieldCharacter

class FieldCharacter(OldFieldCharacter.FieldCharacter):
    def __init__(self, MainClass, kwargs):
        self.GetSource(MainClass)
        self.SetOptions(kwargs)
        self.ProgramParameter()

        self.OnInstanceFunc()
        self.SetObjAnimDic()

    def ProgramParameter(self):
        super().ProgramParameter()
        self.IsAlive = True
        self.IsOnDead = False

    def Start(self):
        self.Action = self.Update
        self.LoadMaterial()
        self.AutoSelectAttackTarget()

    def Update(self):
        self.HelperUpdate()
        self.ProgramParameterUpdate()
        self.Draw()
        self.BtnUpdate()
        self.HPEvent()

    def HPEvent(self):
        if self.IsOnDead:
            self.AddSingleAnim("dead")
            self.IsOnDead = False

    def ProgramParameterUpdate(self):
        oldIsAlive = self.IsAlive
        self.IsAlive = self.hp>0
        if oldIsAlive and not self.IsAlive:
            self.IsOnDead = True

    def IsAliveAttackTarget(self):
        return self.AttackTarget.hp > 0

    def AdjustSelectAttackTarget(self):
        if not self.IsAliveAttackTarget():
            self.AutoSelectAttackTarget()

    #Others
    def SetActive(self, boolean):
        self.enable = boolean