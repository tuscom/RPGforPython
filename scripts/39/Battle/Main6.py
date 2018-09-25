"""
コードの書き方
１．同じ系列のファイルであれば、飛んで継承することもOK 
２．Start、Update、__init__は必ずOverrideする。
３．Mainシリーズには最低限要求するSub下位シリーズ番号を記述する
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
import Main5 as MainModule

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
        self.explosionPicturePath = "../../../pictures/frame.png"
        self.explosionPictureSize = (30, 30)

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

        self.AttackFunction = None

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

    def SetAnimation(self):
        super().SetAnimation()
        kwargs = {
            "isRepeat" : False,
            "isAutoStart" : False
            }
        self.ShowBattleMenuContiAnim = self.ContinueAnimation([], kwargs)
        self.ContinueAnimList.append(self.ShowBattleMenuContiAnim)

        kwargs = {
            "isRepeat" : False,
            "isAutoStart" : False
            }
        self.FieldCharaOtherContiAnim = self.ContinueAnimation([], kwargs)
        self.ContinueAnimList.append(self.FieldCharaOtherContiAnim)


    def Update(self):
        #self.DrawBackGround()
        #self.DrawFieldCharacter()
        #self.DrawPanel()
        #self.DrawTargetIcon()
        #self.DrawBattleMenu()
        self.AnimationUpdate()

        #blitを最後に実行
        self.MainOfAllObjects()

    def MainOfAllObjects(self):
        [list(map(lambda ObjectClass:ObjectClass.Main(), self.AllObjectsList))]

    #=================== Attack's Update ====================
    def Attack(self):
        if self.AttackFunction != None:
            self.AttackFunction()

    def AttackStart(self):
        self.CalcDamageForAttack()
        self.RefReflectDamageForAttack()
        self.SetContinueAttackAnimation()
        self.SetOtherAttackAnimation()

        self.AttackFunction = self.AttackUpdate

    def CalcDamageForAttack(self):
        pass
    def ReflectDamageForAttack(self):
        pass
    def SetContinueAttackAnimation(self):
        pass
    def SetOtherAttackAnimation(self):
        pass

    def AttackUpdate(self):
        if self.EndConditionForAttack():
            self.AttackFunction = self.AttackEnd

    def EndConditionForAttack(self):
        return self.EndAttackAnimation()
    def EndAttackAnimation(self):
        #複数のContinueAnimationが対象となる可能性あり
        return False

    def AttackEnd(self):
        self.AttackFunction = None

    #==================== Attack's Others ===================
    def PlayOfAttack(self):
        self.AttackFunction = self.AttackStart

if __name__ == "__main__":
    MainClass().Main()

