import pygame
from pygame.locals import *
import sys


from Source import ObjectClass

class IconCharacter(ObjectClass):
    def __init__(self, MainClass, CharaClass, kwargs):
        self.GetSource(MainClass, CharaClass)
        self.SetOptions(kwargs)
        self.SetParameter()

        self.OnInstanceFunc()

        self.Action = self.Start

    def GetSource(self, MainClass, CharaClass):
        super().GetSource(MainClass)
        self.CharaClass = CharaClass

    def SetOptions(self, kwargs):
        self.options = {
            "name" : "名無し",
            "picturepath" : "../../../pictures/mon_016.bmp",
            "position" : pygame.math.Vector2(),
            "scale" : pygame.math.Vector2(100, 100),
            "bgPicturePath" : "../../../pictures/normalPanel.png",
            "HPbarPicturePath" : "../../../pictures/HPbar.png",
            "HPbarbackPicturePath" : "../../../pictures/HPbar_back.png",
            "HPbarThick" : 10
            }
        if kwargs != None:
            self.options.update(kwargs)

    #Start
    def Start(self):
        self.LoadMaterial()
        self.Action = self.Update

        self.SetScale()
        self.SetHPbar()
        self.SetHPbarPosition()
        self.SetbgPicture()
        self.SetCharacterPicture()

    def SetScale(self):
        self.charaControllerRect = self.MainClass.Helper.NormToWorldRect(self.MainClass.charaControllerLayout)
        self.scale = pygame.math.Vector2(self.charaControllerRect[3], self.charaControllerRect[3])
    def SetHPbar(self):
        self.HPbarScale = pygame.math.Vector2(self.scale.x, self.options["HPbarThick"])
        self.HPbarPos = pygame.math.Vector2()
        self.HPbarPicture = self.BattleHelper.ScaledPicture(
            self.options["HPbarPicturePath"],
            (int(self.HPbarScale.x), int(self.HPbarScale.y))
            )
        self.HPbarbackPicture = self.BattleHelper.ScaledPicture(
            self.options["HPbarbackPicturePath"],
            (int(self.HPbarScale.x), int(self.HPbarScale.y))
            )
        self.CharaClass.SetHPbarPicture(self.HPbarPicture)
    def SetbgPicture(self):
        self.bgPicture = self.BattleHelper.ScaledPicture(
            self.options["bgPicturePath"],
            (self.charaControllerRect[3], self.charaControllerRect[3])
            )
    def SetCharacterPicture(self):
        self.picture = pygame.transform.scale(self.CharaClass.picture, (self.charaControllerRect[3], self.charaControllerRect[3]))

    def SetHPbarPosition(self):
        self.HPbarPos = self.position + pygame.math.Vector2(0, 1) * (self.scale.y - self.HPbarScale.y)

    #Update
    def Update(self):
        self.HelperUpdate()
        self.Draw()
        self.BtnUpdate()

    def Draw(self):
        self.screen.blit(self.bgPicture, self.position)
        self.screen.blit(self.picture, self.position)
        self.screen.blit(self.HPbarbackPicture, self.HPbarPos)
        self.screen.blit(self.HPbarPicture, self.HPbarPos)

