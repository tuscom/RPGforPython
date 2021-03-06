
import pygame
from pygame.locals import *
import sys

import FieldCharacter3

class FieldCharacter(FieldCharacter3.FieldCharacter):
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
            "battleMenuName" : ["stepAttack", "jump"]
            }
        if kwargs != None:
            self.options.update(kwargs)

    def ProgramParameter(self):
        super().ProgramParameter()
        self.AttackName = "stepAttack"
        self.battleMenuName = self.options["battleMenuName"]

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

    #Others
    def Attack(self):
        self.AddContinueAnim("battle", self.AttackName)
