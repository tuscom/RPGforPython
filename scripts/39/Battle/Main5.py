"""
コードの書き方
１．同じ系列のファイルであれば、飛んで継承することもOK 
２．Start、Update、__init__は必ずOverrideする。
３．Subシリーズには最低限要求するSub下位シリーズ番号を記述する
４．下位シリーズのimportはバージョン管理のため、Source.pyからとする。

対応ver
[Sub, SubX, SubXX] = [4, 6, 2], [5, 5, 2]
"""

import pygame
from pygame.locals import *
import sys
import copy

import Helper
from Helper import BattleHelper

from Source import Sub
from Source import SubX
from Source import SubXX
import Main4 as MainModule

class MainClass(MainModule.MainClass):
    def __init__(self):
        #画面設定
        self.windowSize = [1500, 800]
        self.squareSize = 32
        self.windowName = "Battle"
        self.screen = pygame.display.set_mode(self.windowSize)

        #フィールド
        self.bgPicturePath = "../../../pictures/keimusyo_niwa001.jpg"
        self.charaSize = [250, 250]
        self.familyPos = pygame.math.Vector2(900, 50)
        self.enemyPos = pygame.math.Vector2(350, self.familyPos.y)

        #キャラコントローラーパネル
        self.charaControllerLayout = [0, 0.8, 1, 0.2]
        self.attackBtnLayout = pygame.math.Vector2(0.8, 0.7)
        self.attackBtnScale = pygame.math.Vector2(200, 200)
        self.attackBtnPicturePath = "../../../pictures/attackButton.png"
        self.charaControllerPanelPicturePath = "../../../pictures/normalPanel.png"
        self.battleMenuHeight = 80
        self.noOfBattleMenu = 5
        self.targetIconPicturePath = "../../../pictures/targetIcon.png"
        self.targetIconSize = copy.deepcopy(self.charaSize)
        self.BattleLogPicturePath = "../../../pictures/logPicture.png"
        self.BattleLogLayout = [0, 0, 0.4, 0.04]

        #アニメーション
        self.normalAttackPicturePath = "../../../pictures/attack.png"
        self.normalAttackScale = copy.copy(self.charaSize)

        #派生実装
        if __name__ == "__main__":
            self.BattleHelper = BattleHelper
            self.IconCharacterClass = SubX.IconCharacterClass
            self.FieldCharacterClass = SubXX.FieldFamilyClass
            self.FieldEnemyClass = SubXX.FieldEnemyClass
            self.ObjectClass = Sub.ObjectClass
            self.ButtonClass = SubX.ButtonClass

            self.AllAnimationController = Sub.AllAnimationController
            self.ContinueAnimation = Sub.ContinueAnimation
            self.OneCommandAnimation = Sub.OneCommandAnimation
            self.PieceAnimation = Sub.PieceAnimation

            self.Helper = self.BattleHelper(self)

        self.Action = None
        self.AllObjectsList = []
        #self.SelectedEnemy = None
        self.SelectedFamily = None
        self.ShowBattleMenuAnimSwitch = False

    def Start(self):
        self.Action = self.Update

        self.SetWindow()
        self.LoadMaterial()
        self.SetFieldCharacter()
        self.SetBattleMenu()
        self.SetPanel()
        self.SetAnimation()
        self.SetAttackBtn()
        self.SetBattleLog()

    def LoadMaterial(self):
        super().LoadMaterial()
        self.normalAttackPicture = self.BattleHelper.ScaledPicture(self.normalAttackPicturePath, self.normalAttackScale)
        self.targetIconPicture = self.BattleHelper.ScaledPicture(self.targetIconPicturePath, self.targetIconSize)

    def SetAnimation(self):
        super().SetAnimation()
        kwargs = {
            "isRepeat" : False,
            "isAutoStart" : False
            }
        self.ShowBattleMenuContiAnim = self.ContinueAnimation([], kwargs)
        self.ContinueAnimList.append(self.ShowBattleMenuContiAnim)

    def SetWindow(self):
        pygame.init()
        pygame.display.set_caption(self.windowName)

    def SetBattleMenu(self):
        self.battleMenuWidth = int(self.windowSize[0] / self.noOfBattleMenu)

    def SetBattleLog(self):
        rect = self.Helper.NormToWorldRect(self.BattleLogLayout)
        kwargs = {
            "position" : pygame.math.Vector2(rect[0], rect[1]),
            "scale" : pygame.math.Vector2(rect[2], rect[3]),
            "picturepath" : "../../../pictures/logPicture.png",
            "textColor" : pygame.Color("WHITE"),
            "text" : ""
            }
        self.BattleLog = self.ButtonClass(self, kwargs)

    def Update(self):
        self.DrawBackGround()
        self.DrawFieldCharacter()
        self.DrawPanel()
        self.DrawTargetIcon()
        self.DrawBattleMenu()
        self.AnimationUpdate()

    def SetPanel(self):
        charaControllerRect = self.Helper.NormToWorldRect(self.charaControllerLayout)
        kwargs = {
            "position" : pygame.math.Vector2(charaControllerRect[0], charaControllerRect[1]),
            "scale" : pygame.math.Vector2(charaControllerRect[2], charaControllerRect[3]),
            "picturepath" : self.charaControllerPanelPicturePath
            }
        self.charaControllerPanel = self.ObjectClass(self, kwargs)

        self.familyIcons = []
        for i in range(len(self.family)):
            kwargs = {
                "position" : pygame.math.Vector2(
                    i * charaControllerRect[3],
                    charaControllerRect[1]
                    )
                }
            self.familyIcons.append(self.IconCharacterClass(self, self.family[i], kwargs))


    def DrawTargetIcon(self):
        if self.SelectedFamily != None:
            TargetClass = self.SelectedFamily.AttackTarget
            self.screen.blit(self.targetIconPicture, TargetClass.position)

    def DrawBattleMenu(self):
        if self.SelectedFamily != None and self.ShowBattleMenuAnimSwitch:
            IconClass = self.SelectedFamily.IconClass
            IconClass.DrawBattleMenu()
        elif self.SelectedFamily == None:
            self.ShowBattleMenuAnimSwitch = False

    def DrawPanel(self):
        super().DrawPanel()
        self.BattleLog.Main()

    #===================Button====================
    def AttackBtnOnClick(self):
        super().AttackBtnOnClick()
        self.SelectedFamily = None
    def SelectOFF(self):
        #self.SelectedEnemy = None
        self.SelectedFamily = None

if __name__ == "__main__":
    MainClass().Main()

