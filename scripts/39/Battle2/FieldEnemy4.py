import pygame
from pygame.locals import *
import sys

import FieldEnemy3 as OldFieldEnemy

class FieldEnemy(OldFieldEnemy.FieldEnemy):
    def __init__(self, MainClass, kwargs):
        self.GetSource(MainClass)
        self.SetOptions(kwargs)
        self.ProgramParameter()

        self.OnInstanceFunc()
        self.SetObjAnimDic()

    def SetOptions(self, kwargs):
        self.FieldCharacter = self.MainClass.FieldCharacter
        self.FieldCharacter.SetOptions(self, kwargs)
        self.options.update({
            "HPbarPicturePath" : "../../../pictures/HPbar.png",
            "HPbarbackPicturePath" : "../../../pictures/HPbar_back.png",
            "HPbarThick" : 10,
            })
        if kwargs != None:
            self.options.update(kwargs)

    def SetObjAnimDic(self):
        kwargsAttack = {
            "ContinueName" : "battle",
            "SkipCondition" : lambda : not self.IsAlive}
        kwargsDead = {"EndFunc" : lambda:self.SetActive(False)}
        self.ObjAnimDic = {
            "jump" : self.OneCmdAnim("jump", self, kwargsAttack),
            "stepAttack" : self.OneCmdAnim("enemyStepAttack", self, kwargsAttack),
            "dead" : self.OneCmdAnim("dead", self, kwargsDead)
            } # CmdAnimName : OneCmdAnim(class)

    def Start(self):
        self.Action = self.Update
        self.LoadMaterial()
        self.SetHPbar()
        self.AutoSelectAttackTarget()

    def AutoSelectAttackTarget(self):
        family = self.MainClass.AliveFamily()
        if len(family) > 0:
            self.AttackTarget = family[0]

    def Update(self):
        self.HelperUpdate()
        self.ProgramParameterUpdate()
        self.Draw()
        self.BtnUpdate()
        self.HPEvent()

    def OnClick(self):
        SelectedFamily = self.MainClass.SelectedFamily
        if SelectedFamily != None and self.hp > 0:
            SelectedFamily.AttackTarget = self