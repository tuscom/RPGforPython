import pygame
from pygame.locals import *
import sys
import functools

import IconCharacter3


class IconCharacter(IconCharacter3.IconCharacter):
    def __init__(self, MainClass, CharaClass, kwargs):
        self.MainClass = MainClass
        self.BattleHelper = MainClass.BattleHelper
        self.Helper = MainClass.Helper
        self.screen = MainClass.screen
        self.CharaClass = CharaClass
        self.OneCommandAnimation = MainClass.OneCommandAnimation

        self.SetOptions(kwargs)
        self.SetParameter()
        self.SetButton()
        self.OnInstanceFunc()
        self.SetAction()

    def Start(self):
        self.LoadMaterial()
        self.Action = self.Update

        self.SetScale()
        self.SetHPbar()
        self.SetHPbarPosition()
        self.SetbgPicture()
        self.SetCharacterPicture()
        self.ReflectToCharaClass()
        self.SetBattleMenu()
        self.SetAnimationCommand()

    def SetAnimationCommand(self):
        kwargs = {
            }
        self.ShowBattleMenuCmd = self.OneCommandAnimation("ShowBattleMenu", self, kwargs)

        kwargs = {
            "EndFunc" : self.MainClass.SelectOFF
            }
        self.BackBattleMenuCmd = self.OneCommandAnimation("BackBattleMenu", self, kwargs)

        self.CommandAnimationDic = {
            "jump" : self.OneCommandAnimation("jump", self, None),
            "ShowBattleMenu" : self.ShowBattleMenuCmd
            }

    def Update(self):
        self.HelperUpdate()

        self.Draw()
        self.BtnUpdate()

    def SetBattleMenu(self):
        battleMenu = self.CharaClass.battleMenu
        battleMenuFunc = self.CharaClass.battleMenuFunc
        noOfBtn = len(battleMenu)
        scale = pygame.math.Vector2(
            self.MainClass.battleMenuWidth,
            self.MainClass.battleMenuHeight
            )
        y = self.MainClass.windowSize[1] - self.MainClass.battleMenuHeight - self.scale.y
        self.BattleMenuBtnList = []
        for i in range(noOfBtn):
            position = pygame.math.Vector2(0, y) + pygame.math.Vector2(1, 0) * scale.x * i
            kwargs = {
                "position" : position,
                "scale" : scale,
                "text" : battleMenu[i],
                "btnFunc" : functools.partial(self.BattleMenuBtnOnClick, battleMenuFunc[i]),
                "picturepath" : self.MainClass.charaControllerPanelPicturePath,
                "name" : "battleMenu"
                }
            self.BattleMenuBtnList.append(self.MainClass.ButtonClass(self.MainClass, kwargs))


    def DrawBattleMenu(self):
        list(map(lambda btn : btn.Main(), self.BattleMenuBtnList))

    def SetBattleMenuSwitch(self, boolean):
        self.battleMenuSwitch = boolean

    #==================Button===================
    def OnClick(self):

        if self.MainClass.SelectedFamily != self.CharaClass:
            ShowBattleMenuContiAnim = self.MainClass.ShowBattleMenuContiAnim
            ShowBattleMenuContiAnim.CommandAnimationList = [self.ShowBattleMenuCmd]
            ShowBattleMenuContiAnim.PlayON()

            self.MainClass.SelectedFamily = self.CharaClass
        else:
            ShowBattleMenuContiAnim = self.MainClass.ShowBattleMenuContiAnim
            ShowBattleMenuContiAnim.CommandAnimationList = [self.BackBattleMenuCmd]
            ShowBattleMenuContiAnim.PlayON()

    def BattleMenuBtnOnClick(self, IndividualFunc):
        IndividualFunc()
        self.MainClass.SelectedFamily = None
