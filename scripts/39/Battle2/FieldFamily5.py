import pygame
from pygame.locals import *
import sys

import FieldFamily4 as OldFieldFamily

class FieldFamily(OldFieldFamily.FieldFamily):
    def __init__(self, MainClass, kwargs):
        self.GetSource(MainClass)
        self.SetOptions(kwargs)
        self.ProgramParameter()

        self.OnInstanceFunc()
        self.SetObjAnimDic()

    def SetObjAnimDic(self):
        kwargsAttack = {
            "ContinueName" : "battle",
            "SkipCondition" : lambda : not self.IsAlive}
        kwargsDead = {"EndFunc" : lambda:self.SetActive(False)}
        self.ObjAnimDic = {
            "jump" : self.OneCmdAnim("jump", self, kwargsAttack),
            "stepAttack" : self.OneCmdAnim("familyStepAttack", self, kwargsAttack),
            "dead" : self.OneCmdAnim("dead", self, kwargsDead)
            } # CmdAnimName : OneCmdAnim(class)

    def Start(self):
        self.Action = self.Update
        self.LoadMaterial()
        self.AutoSelectAttackTarget()

    def AutoSelectAttackTarget(self):
        enemies = self.MainClass.AliveEnemies()
        if len(enemies) > 0:
            self.AttackTarget = enemies[0]

    def Update(self):
        self.HelperUpdate()
        self.ProgramParameterUpdate()
        self.Draw()
        self.BtnUpdate()
        self.HPEvent()
