import pygame
from pygame.locals import *
import sys

class MoveModePlayer:
    def __init__(self, MainClass, kwargs):
        super().__init__(MainClass, kwargs)

        self.MoveParameter()

    def MoveParameter(self):
        self.speedFactor = 1
        self.animPos = pygame.math.Vector2(self.position)

    #Update系
    def Draw(self):
        self.screen.blit(self.picture, self.animPos)

    def Move(self):
        pass

    def InputPos(self):
        self.HorizontalDirection = self.Helper.intHorizontalKey
        self.VerticalDirection = self.Helper.intVerticalKey

    def ConditionMove(self):
        result = False

        #止まっているとき→アニメーションが終わっているとき