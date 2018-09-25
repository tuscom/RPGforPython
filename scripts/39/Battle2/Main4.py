"""
機能
・アニメーション追加
・バトルメニューのボタン関数以外、実装

コード記述注意点
・時間によらないアニメーションは外から制御した方が楽。
・AddAnimation実行→OneCmdAnimのUpdateまで→PieceAnimのUpdateの順で実行される。

要求version
ObjectClass            : 4
FieldCharacter         : 4
FieldEnemy             : 3
FieldFamily            : 4
IconCharacter          : 3
PieceAnimation         : 3
OneCmdAnim             : 2
AllAnimationController : 3
Button                 : 1
"""


import pygame
from pygame.locals import *
import sys

from Source import *

import Main3 as MainModule

class MainClass(MainModule.MainClass):
    def __init__(self):
        self.WindowParameter()
        self.FieldParameter()
        self.ControllerPanelParameter()
        self.ProgramParameter()
        self.GetSource()

        self.SetWindow()

    def ControllerPanelParameter(self):
        super().ControllerPanelParameter()
        self.battleMenuHeight = 80
        self.battleMenuWidth = int(self.windowSize[0] / 5)

    def GetSource(self):
        super().GetSource()
        self.Button = Button

    def ProgramParameter(self):
        super().ProgramParameter()
        self.SelectedFamily = None

    def Start(self):
        self.LoadMaterial()
        self.SetFieldCharacter()
        self.SetPanel()
        self.Action = self.Update

    def SetPanel(self):
        self.SetBackPanel()
        self.SetFamilyIcon()
        self.SetAttackBtn()

    def SetBackPanel(self):
        self.charaControllerRect = self.Helper.NormToWorldRect(self.charaControllerLayout)
        kwargs = {
            "position" : pygame.math.Vector2(self.charaControllerRect[0], self.charaControllerRect[1]),
            "scale" : pygame.math.Vector2(self.charaControllerRect[2], self.charaControllerRect[3]),
            "picturepath" : self.charaControllerPanelPicturePath
            }
        self.charaControllerPanel = ObjectClass(self, kwargs)

    def SetFamilyIcon(self):
        self.familyIcons = []
        for i in range(len(self.family)):
            self.familyIcons.append(IconCharacter(self, self.family[i], None))
            self.familyIcons[-1].position = pygame.math.Vector2(
                i * self.charaControllerRect[3],
                self.charaControllerRect[1]
                )
    def SetAttackBtn(self):
        #攻撃ボタン
        attackBtnPos = self.Helper.NormToWorldPos(self.attackBtnLayout)
        kwargs = {
            "picturepath" : self.attackBtnPicturePath,
            "position" : attackBtnPos,
            "scale" : self.attackBtnScale,
            "btnFunc" : self.AttackBtnOnClick
            }
        self.attackBtn = ObjectClass(self, kwargs)

    def Update(self):
        self.DrawBackGround()
        self.MainAllObjects()
        self.AllAnimationController.Main()
        self.PanelController()

    def PanelController(self):
        if self.AllAnimationController.IsEndContinueAnimation("battle"):
            self.attackBtn.enable = True
        else:
            self.attackBtn.enable = False

    #Others
    def AttackBtnOnClick(self):
        Character = self.Family() + self.Enemies()
        Character = sorted(Character, key = lambda Chara:Chara.speed, reverse=True)
        list(map(lambda Chara : Chara.Attack(), Character))

    def ObjectSetActive(self, ObjClass, boolean):
        ObjClass.enable = boolean

    def SelectedSwitch(self, ObjClass):
        self.SelectedFamily = ObjClass

if __name__ == "__main__":
    MainClass().Main()
