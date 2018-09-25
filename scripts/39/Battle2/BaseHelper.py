import pygame
from pygame.locals import *
import sys

class BattleHelper:
    def __init__(self, MainClass):
        self.MainClass = MainClass
        self.windowSize = MainClass.windowSize
        self.screen = MainClass.screen

        self.pygameclock = pygame.time.get_ticks() * 1e-3
        self.pygamedeltatime = 0

        self.mousePos = pygame.mouse.get_pos()
        self.mousePressed = pygame.mouse.get_pressed()
        self.previousPressed = self.mousePressed

    def NormToWorldPos(self, normV2):
        windowSize = self.MainClass.windowSize
        windowSizeV2 = pygame.math.Vector2(windowSize[0], windowSize[1])
        return normV2.elementwise() * windowSizeV2

    def NormToWorldRect(self, rect):
        windowSize = self.MainClass.windowSize
        result = [rect[0]*windowSize[0], rect[1]*windowSize[1], rect[2]*windowSize[0], rect[3]*windowSize[1]]
        result = [int(i) for i in result]
        return result

    def EarlyUpdate(self):
        previousclock = self.pygameclock
        self.pygameclock = pygame.time.get_ticks() * 1e-3
        self.pygamedeltatime = self.pygameclock - previousclock

        self.mousePos = pygame.mouse.get_pos()
        self.mousePressed = pygame.mouse.get_pressed()

    def LateUpdate(self):
        self.previousPressed = self.mousePressed

    def ScaledPicture(picturepath, size=(100, 100)):
        picture = pygame.transform.scale(pygame.image.load(picturepath).convert_alpha(), size)
        return picture

    def Vector2ToIntlist(v2):
        return [int(v2.x), int(v2.y)]

    def FadeIn001(self):
        pass

