"""
機能
・ターゲットアイコン実装
・アニメーション追加

注意点
・FirstUsedStartとAfterUsedStartを同時に実行するものとしないものが混在している（同時：PieceAnimation）

要求version
ObjectClass            : 5(new)
FieldCharacter         : 5(new)
FieldEnemy             : 4(new)
FieldFamily            : 5(new)
IconCharacter          : 3
PieceAnimation         : 4(new)
OneCmdAnim             : 3(new)
AllAnimationController : 4(new)
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

    def ProgramParameter(self):
        super().ProgramParameter()
        self.IsEndBattle = False

    def GetSource(self):
        super().GetSource()
        self.FieldCharacter = FieldCharacter

    def Start(self):
        self.LoadMaterial()
        self.SetFieldCharacter()
        self.SetPanel()
        self.SetTargetIconPicture()
        self.SceneParameter()
        self.Action = self.Update

        self.SetFade()

    def SetTargetIconPicture(self):
        self.TargetIconPicture = self.BattleHelper.ScaledPicture(self.TargetIconPicturePath, self.charaSize)

    def SceneParameter(self):
        kwargs = {
            "name" : "FadeObject",
            "picturepath" : "../../../pictures/myFade.png",
            "position" : pygame.math.Vector2(0, 0),
            "scale" : pygame.math.Vector2(self.windowSize[0]*1.4, self.windowSize[1])
            }
        self.FadeObject = ObjectClass(self, kwargs)
        self.FadeObject.SetActive(False)

    def SetFade(self):
        self.FadeObject.AddSingleAnim("FadeIn1")

    def Update(self):
        self.DrawBackGround()
        self.MainAllObjects()
        self.DrawTargetIcon()
        self.AllAnimationController.Main()
        self.PanelController()
        self.SceneController()

    def DrawTargetIcon(self):
        if self.SelectedFamily != None:
            position = self.SelectedFamily.AttackTarget.position
            self.screen.blit(self.TargetIconPicture, position)

    def SceneController(self):
        OldIsEndBattle = self.IsEndBattle
        self.IsEndBattle = not len(self.AliveFamily()) or not len(self.AliveEnemies())
        if self.IsEndBattle and not OldIsEndBattle:
            self.FadeObject.AddSingleAnim("FadeOut1")

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

    #def FadeInStartFunc(self):
    #    list(map(lambda ObjClass : ObjClass.SetActive(False), self.AllObjects))
    #    self.FadeObject.SetActive(True)

    #def FadeInEndFunc(self):
    #    list(map(lambda ObjClass : ObjClass.SetActive(True), self.AllObjects))
    #    self.FadeObject.SetActive(False)

if __name__ == "__main__":
    MainClass().Main()
