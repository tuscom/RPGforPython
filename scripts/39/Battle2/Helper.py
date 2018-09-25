import pygame
from pygame.locals import *
import sys

import BaseHelper

class Button:
    def __init__(self, screen, **kwargs):
        self.screen = screen

        self.options = {"rect" : [0, 0, 300, 100],
                        "type" : "IsOnDown",
                        "func" : lambda:print("Btn pushed!"),
                        "picturename" : "../../../pictures/normalPanel.png",
                        "font" : "../../../documents/IPAexfont00301/ipaexg.ttf",
                        "text" : "ボタン",
                        "textColor" : pygame.Color("BLACK")}
        self.options.update(kwargs)

        self.rect = self.options["rect"]
        self.position = pygame.math.Vector2(self.rect[0], self.rect[1])
        self.scale = pygame.math.Vector2(self.rect[2], self.rect[3])
        self.picture = pygame.transform.scale(pygame.image.load(self.options["picturename"]).convert_alpha(), (self.rect[2], self.rect[3]))
        self.BtnAction = ButtonAction(self)
        self.BtnAction.rect = self.rect
        self.actiondict = {"IsOnDown" : self.BtnAction.IsOnDown}
        self.BoolAction = self.actiondict[self.options["type"]]
        self.Func = self.options["func"]
        #text
        self.font = pygame.font.Font(self.options["font"], self.rect[3])
        self.words = self.font.render(self.options["text"], True, self.options["textColor"])

    def Update(self):
        self.BtnAction.mousePos = pygame.mouse.get_pos()
        self.BtnAction.mousePressed = pygame.mouse.get_pressed()

        self.screen.blit(self.picture, (self.rect[0], self.rect[1]))
        if self.BoolAction():
            self.Func()
        self.screen.blit(self.words, (self.rect[0], self.rect[1]))

        self.BtnAction.previousPressed = self.BtnAction.mousePressed

class ButtonAction:
    def __init__(self, ParentClass):
        self.ParentClass = ParentClass
        self.rect = (0, 0, 0, 0)
        self.mousePos = (0, 0)
        self.mousePressed = (0, 0, 0)
        self.previousPressed = (1, 1, 1)

    def IsOnDown(self):
        result = False
        self.rect = self.Rect()
        
        if self.mousePressed[0] and not self.previousPressed[0]:
            if self.rect[0] <= self.mousePos[0] <= self.rect[0]+self.rect[2] and self.rect[1] <= self.mousePos[1] <= self.rect[1]+self.rect[3]:
                result = True

        return result

    def Rect(self):
        #rect 計算
        return (self.ParentClass.position.x, self.ParentClass.position.y, self.ParentClass.scale.x, self.ParentClass.scale.y)

class BattleHelper(BaseHelper.BattleHelper):
    def __init__(self, MainClass):
        super().__init__(MainClass)

        #Fade In 001
        self.pictureSize001 = (self.windowSize[0]+350, self.windowSize[1])
        self.fadePicture001 = BattleHelper.ScaledPicture("../../../pictures/myFade.png", size=self.pictureSize001)
        self.position001 = pygame.math.Vector2(-300, 0)

    def FadeIn001(self):
        if self.windowSize[0] - self.position001.x > 0:
            self.screen.blit(self.fadePicture001, self.position001)
            self.position001 += pygame.math.Vector2(10, 0)
