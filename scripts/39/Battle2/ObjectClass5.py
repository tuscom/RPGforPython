import pygame
from pygame.locals import *
import sys

import ObjectClass4

class ObjectClass(ObjectClass4.ObjectClass):
    def __init__(self, MainClass, kwargs):
        self.GetSource(MainClass)
        self.SetOptions(kwargs)
        self.ProgramParameter()

        self.OnInstanceFunc()
        self.SetObjAnimDic()

    #def ProgramParameter(self):
    #    super().ProgramParameter()
    #    self.enable = True

    def Start(self):
        self.LoadMaterial()
        self.Action = self.Update

    def LoadMaterial(self):
        rect = self.Rect()
        self.picture = pygame.transform.scale(pygame.image.load(self.options["picturepath"]).convert_alpha(), rect[2:])
        self.testMask = pygame.image.load("../../../pictures/9c338508771fd401ada29fba07b34ebf.png").convert_alpha()
        #self.testMask = pygame.mask.from_surface(pygame.image.load("../../../pictures/9c338508771fd401ada29fba07b34ebf.png").convert_alpha())
        #self.picture.blit(self.testMask, (0, 0), special_flags=BLEND_RGBA_MULT)
        #self.picture.blit(self.testMask, (50, 50), special_flags=BLEND_RGBA_MULT)

    def Update(self):
        self.HelperUpdate()
        self.Draw()
        self.BtnUpdate()

    def Draw(self):
        #self.screen.blit(self.picture, self.position)

        self.screen.blit(self.picture, self.position)

        #self.testMask.blit(self.picture, (0, 0), special_flags=BLEND_PREMULTIPLIED)
        #self.screen.blit(self.testMask, self.position)

    def SetObjAnimDic(self):
        kwargsFadeIn = {
            "StartFunc" : lambda : self.SetActive(True),
            "EndFunc" : lambda : self.SetActive(False)
            }
        kwargsFadeOut = {
            "StartFunc" : lambda : self.SetActive(True)
            }
        self.ObjAnimDic = {
            "jump" : self.OneCmdAnim("jump", self, None),
            "FadeIn1" : self.OneCmdAnim("FadeIn1", self, kwargsFadeIn),
            "FadeOut1" : self.OneCmdAnim("FadeOut1", self, kwargsFadeOut)
            } # CmdAnimName : OneCmdAnim(class)

    #====================== Others =====================
    def SetActive(self, boolean):
        self.enable = boolean