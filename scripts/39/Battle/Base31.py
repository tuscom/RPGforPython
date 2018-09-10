"""
FieldCharacter、FieldFamilyクラス作成
Base3を要求
"""

import pygame
from pygame.locals import *
import sys

import Helper
from Helper import BattleHelper

import Base3 as Base

class FieldCharacter(Base.ObjectClass):
    def __init__(self, MainClass, kwargs):
        super().__init__(MainClass, kwargs)
        self.SetAnimation()

        self.HPbarPicture = None

    def SetOptions(self, kwargs):
        self.options = {"name" : "名無し",
                        "picturepath" : "../../../pictures/mon_016.bmp",
                        "position" : pygame.math.Vector2(),
                        "scale" : pygame.math.Vector2(100, 100),
                        "btnFunc" : self.OnClick,
                        "speed" : 10,
                        "hp" : 100}
        if kwargs != None:
            self.options.update(kwargs)

    def SetParameter(self):
        super().SetParameter()
        self.speed = self.options["speed"]
        self.hp = self.options["hp"]

    def SetAnimation(self):
        self.CommandAnimationDic = {
            "jump" : self.OneCommandAnimation("jump", self, None),
            "mudaniHustle" : self.OneCommandAnimation("mudaniHustle", self, None)
            }

    def Start(self):
        super().Start()

    def AutoSelectAttackCommand(self):
        self.AttackCommand = self.CommandAnimationDic["jump"]