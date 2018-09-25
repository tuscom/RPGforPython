import pygame
from pygame.locals import *
import sys

import FieldFamily2 as OldFieldFamily

class FieldFamily(OldFieldFamily.FieldFamily):
    def __init__(self, MainClass, kwargs):
        self.GetSource(MainClass)
        self.SetOptions(kwargs)
        self.ProgramParameter()

        self.OnInstanceFunc()
        self.SetObjAnimDic()

    def ProgramParameter(self):
        super().ProgramParameter()
        self.IconClass = None

    def SetObjAnimDic(self):
        self.ObjAnimDic = {
            "jump" : self.OneCmdAnim("jump", self, None),
            "stepAttack" : self.OneCmdAnim("familyStepAttack", self, None)
            } # CmdAnimName : OneCmdAnim(class)

    def Start(self):
        self.Action = self.Update
        self.LoadMaterial()
        self.AutoSelectAttackTarget()
        #self.AddContinueAnim("battle", "stepAttack")

    def Update(self):
        self.HelperUpdate()
        self.Draw()
        self.BtnUpdate()

    def AutoSelectAttackTarget(self):
        enemies = self.MainClass.Enemies()
        if len(enemies) > 0:
            self.AttackTarget = enemies[0]

    def SetHPbarPicture(self, HPbarPicture):
        self.HPbarPicture = HPbarPicture
        self.IconClass.HPbarPicture = HPbarPicture