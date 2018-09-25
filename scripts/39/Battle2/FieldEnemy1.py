import pygame
from pygame.locals import *
import sys

from Helper import BattleHelper

from Source import FieldCharacter

class FieldEnemy(FieldCharacter):
    def __init__(self, MainClass, kwargs):
        self.GetSource(MainClass)
        self.SetOptions(kwargs)
        self.SetParameter()

        self.OnInstanceFunc()

        self.Action = self.Start

    def SetOptions(self, kwargs):
        self.options = {
            "name" : "名無し",
            "picturepath" : "../../../pictures/mon_016.bmp",
            "position" : pygame.math.Vector2(),
            "scale" : pygame.math.Vector2(100, 100),
            "speed" : 10,
            "hp" : 100,
            "HPbarPicturePath" : "../../../pictures/HPbar.png",
            "HPbarbackPicturePath" : "../../../pictures/HPbar_back.png",
            "HPbarThick" : 10
            }
        if kwargs != None:
            self.options.update(kwargs)

    def Start(self):
        self.LoadMaterial()
        self.Action = self.Update
        self.SetHPbar()

    def SetHPbar(self):
        self.HPbarScale = pygame.math.Vector2(self.scale.x * 0.6, self.options["HPbarThick"])
        self.HPbarPos = pygame.math.Vector2(self.position) + pygame.math.Vector2((self.scale.x - self.HPbarScale.x)/2, self.scale.y)

        self.HPbarPicture = BattleHelper.ScaledPicture(
            self.options["HPbarPicturePath"],
            BattleHelper.Vector2ToIntlist(self.HPbarScale)
            )
        self.HPbarbackPicture = BattleHelper.ScaledPicture(
            self.options["HPbarbackPicturePath"],
            BattleHelper.Vector2ToIntlist(self.HPbarScale)
            )

    def Update(self):
        self.HelperUpdate()
        self.Draw()
        self.BtnUpdate()

    def Draw(self):
        super().Draw()
        self.screen.blit(self.HPbarbackPicture, self.HPbarPos)
        self.screen.blit(self.HPbarPicture, self.HPbarPos)


