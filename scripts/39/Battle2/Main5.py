"""
機能
・ターゲットアイコン実装
・アニメーション追加

注意点
・FirstUsedStartとAfterUsedStartを同時に実行するものとしないものが混在している（同時：PieceAnimation）

要求version
ObjectClass            : 4
FieldCharacter         : 5
FieldEnemy             : 4
FieldFamily            : 5
IconCharacter          : 3
PieceAnimation         : 4
OneCmdAnim             : 3
AllAnimationController : 4
Button                 : 1
"""


import pygame
from pygame.locals import *
import sys

from Source import *

import Main4 as MainModule

class MainClass(MainModule.MainClass):
    def __init__(self):
        self.WindowParameter()
        self.FieldParameter()
        self.ControllerPanelParameter()
        self.ProgramParameter()
        self.GetSource()

        self.SetWindow()

    def FieldParameter(self):
        super().FieldParameter()
        self.TargetIconPicturePath = "../../../pictures/targetIcon.png"

    def Start(self):
        self.LoadMaterial()
        self.SetFieldCharacter()
        self.SetPanel()
        self.SetTargetIconPicture()
        self.Action = self.Update

    def SetTargetIconPicture(self):
        self.TargetIconPicture = self.BattleHelper.ScaledPicture(self.TargetIconPicturePath, self.charaSize)

    def Update(self):
        self.DrawBackGround()
        self.MainAllObjects()
        self.DrawTargetIcon()
        self.AllAnimationController.Main()
        self.PanelController()

    def DrawTargetIcon(self):
        if self.SelectedFamily != None:
            position = self.SelectedFamily.AttackTarget.position
            self.screen.blit(self.TargetIconPicture, position)

    #Others
    def AttackBtnOnClick(self):
        Character = self.Family() + self.Enemies()
        Character = sorted(Character, key = lambda Chara:Chara.speed, reverse=True)
        list(map(lambda Chara : Chara.Attack(), Character))
        self.SelectedSwitch(None)

    def AliveFamily(self):
        result = list(filter(lambda ObjClass : type(ObjClass) == self.FieldFamily, self.AllObjects))
        result = list(filter(lambda CharaClass : CharaClass.hp > 0, result))
        return result

    def AliveEnemies(self):
        result = list(filter(lambda ObjClass:type(ObjClass) == self.FieldEnemy, self.AllObjects))
        result = list(filter(lambda CharaClass : CharaClass.hp > 0, result))
        return result


if __name__ == "__main__":
    MainClass().Main()
