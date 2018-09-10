"""
アニメーションの構造
Sub = Sub2
SubX = SubX2
"""
import pygame
from pygame.locals import *
import sys

import Helper
from Helper import BattleHelper

from Source import Sub
from Source import SubX
import Main1 as MainModule


class MainClass(MainModule.MainClass):
    def __init__(self):
        super().__init__()

        if __name__ == "__main__":
            self.BattleHelper = BattleHelper
            self.IconCharacterClass = SubX.IconCharacterClass
            self.FieldCharacterClass = SubX.FieldCharacterClass
            self.FieldEnemyClass = SubX.FieldEnemyClass
            self.ObjectClass = Sub.ObjectClass

            self.AllAnimationController = Sub.AllAnimationController
            self.ContinueAnimation = Sub.ContinueAnimation
            self.OneCommandAnimation = Sub.OneCommandAnimation
            self.PieceAnimation = Sub.PieceAnimation

            self.Helper = self.BattleHelper(self)

    def Main(self):
        #変数セット
        self.Action = self.Start

        while True:
            self.Helper.EarlyUpdate()

            if self.Action != None:
                self.Action()

            self.Helper.LateUpdate()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

    def Start(self):
        super().Start()
        self.SetAnimation()

    def SetAnimation(self):
        testAnimTarget = self.family + self.enemies
        testComAnimList = [target.CommandAnimationDic["mudaniHustle"] for target in testAnimTarget]
        kwargs = {
            "isRepeat" : True,
            "isAutoStart" : True
            }
        testContiAnim = self.ContinueAnimation(testComAnimList, kwargs)
        testContiAnimList = [testContiAnim]

        self.AnimationController = self.AllAnimationController(testContiAnimList)

    def Update(self):
        super().Update()
        self.AnimationUpdate()

    def AnimationUpdate(self):
        self.AnimationController.Main()

if __name__ == "__main__":
    MainClass().Main()
