import pygame
from pygame.locals import *
import sys

import FieldEnemy1 

class FieldEnemy(FieldEnemy1.FieldEnemy):
    def __init__(self, MainClass, kwargs):
        self.GetSource(MainClass)
        self.SetOptions(kwargs)
        self.ProgramParameter()

        self.OnInstanceFunc()
        self.SetObjAnimDic()

    def SetObjAnimDic(self):
        self.ObjAnimDic = {
            "jump" : self.OneCmdAnim("jump", self, None),
            "stepAttack" : self.OneCmdAnim("enemyStepAttack", self, None)
            } # CmdAnimName : OneCmdAnim(class)


    def Start(self):
        self.Action = self.Update
        self.LoadMaterial()
        self.SetHPbar()
        self.AutoSelectAttackTarget()
        #self.AddContinueAnim("battle", "stepAttack")

    def Update(self):
        self.HelperUpdate()
        self.Draw()
        self.BtnUpdate()

    def AutoSelectAttackTarget(self):
        family = self.MainClass.Family()
        if len(family) > 0:
            self.AttackTarget = family[0]
