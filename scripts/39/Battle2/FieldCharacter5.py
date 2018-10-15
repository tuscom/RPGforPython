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

    def SetOptions(self, kwargs):
        self.options = {
            "name" : "名無し",
            "picturepath" : "../../../pictures/mon_016.bmp",
            "position" : pygame.math.Vector2(),
            "scale" : pygame.math.Vector2(100, 100),
            "btnFunc" : None,
            "speed" : 10,
            "hp" : 100,
            "attack" : 15,
            "block" : 10,
            "battleMenuName" : ["stepAttack", "jump"]
            }
        if kwargs != None:
            self.options.update(kwargs)

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
    #Others
    def IsAliveAttackTarget(self):
        return self.AttackTarget.hp > 0

    def AdjustSelectAttackTarget(self):
        if not self.IsAliveAttackTarget():
            self.AutoSelectAttackTarget()

    def SetActive(self, boolean):
        self.enable = boolean

    def CalcDamage(self, enemyAttackRatio):
        enemyAttack = self.AttackTarget.options["attack"] * enemyAttackRatio
        myBlock = self.options["block"]
        result = enemyAttack - myBlock if enemyAttack > myBlock else 0
        return result