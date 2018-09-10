"""
・ボタンの導入
・戦闘メニュー導入

最低要求
Sub = Sub4
"""
import pygame
from pygame.locals import *
import sys
import copy
import functools

import Helper
from Helper import BattleHelper

from Source import Sub
import SubX4

class FieldCharacterClass(SubX4.FieldCharacterClass):
    def __init__(self, MainClass, kwargs):
        self.MainClass = MainClass
        self.BattleHelper = MainClass.BattleHelper
        self.Helper = MainClass.Helper
        self.screen = MainClass.screen
        self.OneCommandAnimation = MainClass.OneCommandAnimation

        self.SetOptions(kwargs)
        self.SetParameter()
        self.SetButton()
        self.OnInstanceFunc()
        self.SetAction()

    def SetOptions(self, kwargs):
        super().SetOptions(kwargs)
        self.options.update({
            "menu" : ["ぶつかる", "ジャンプ", "おどる"],
            "menuFunc" : [lambda:self.ChangeAttackCmd("leftAttackStep"),lambda:self.ChangeAttackCmd("jump"), lambda:self.ChangeAttackCmd("mudaniHustle")]
            })
        if kwargs != None:
            self.options.update(kwargs)

    def SetParameter(self):
        super().SetParameter()
        self.battleMenu = self.options["menu"]
        self.battleMenuFunc = self.options["menuFunc"]
        self.name = self.options["name"]

    def ChangeAttackCmd(self, name):
        self.AttackCommand = self.CommandAnimationDic[name]

    def Start(self):
        self.LoadMaterial()
        self.Action = self.Update
        self.SetAnimationCommand()
        self.AutoSelectAttackTarget()

    def SetAnimationCommand(self):
        BattleLog = self.MainClass.BattleLog

        jumpKwargs = {
            "StartFunc" : lambda:BattleLog.ChangeText("{}はジャンプした！".format(self.name)),
            "EndFunc" : BattleLog.ResetText
            }
        mudaniHustleKwargs = {
            "StartFunc" : lambda:BattleLog.ChangeText("{}はむだにはっするした！".format(self.name)),
            "EndFunc" : BattleLog.ResetText
            }
        leftAttackStepKwargs = {
            "StartFunc" : lambda:BattleLog.ChangeText("{}はこうげきした！".format(self.name)),
            "EndFunc" : BattleLog.ResetText
            }
        rightAttackStep = {
            "StartFunc" : lambda:BattleLog.ChangeText("{}はこうげきした！".format(self.name)),
            "EndFunc" : BattleLog.ResetText
            }

        self.CommandAnimationDic = {
            "jump" : self.OneCommandAnimation("jump", self, jumpKwargs),
            "mudaniHustle" : self.OneCommandAnimation("mudaniHustle", self, mudaniHustleKwargs),
            "leftAttackStep" : self.OneCommandAnimation("leftAttackStep", self, leftAttackStepKwargs),
            "rightAttackStep" : self.OneCommandAnimation("rightAttackStep", self, rightAttackStep)
            }

        self.AttackCommand = self.CommandAnimationDic["mudaniHustle"]

    def AutoSelectAttackTarget(self):
        pass

    def Update(self):
        self.HelperUpdate()

        self.Draw()
        self.BtnUpdate()

class IconCharacterClass(SubX4.IconCharacterClass):
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

class ButtonClass(Sub.ObjectClass):
    def __init__(self, MainClass, kwargs):
        self.MainClass = MainClass
        self.BattleHelper = MainClass.BattleHelper
        self.Helper = MainClass.Helper
        self.screen = MainClass.screen
        self.OneCommandAnimation = MainClass.OneCommandAnimation

        self.SetOptions(kwargs)
        self.SetAnimationCommand()
        self.SetParameter()
        self.SetButton()
        self.SetText()
        self.OnInstanceFunc()
        self.SetAction()

    def SetText(self):
        self.font = pygame.font.Font(self.options["font"], int(self.scale.y * 0.9))
        self.words = self.font.render(self.options["text"], True, self.options["textColor"])

    def SetOptions(self, kwargs):
        super().SetOptions(kwargs)
        self.options.update({
            "font" : "../../../documents/IPAexfont00301/ipaexg.ttf",
            "text" : "ボタン",
            "textColor" : pygame.Color("BLACK")
            })
        if kwargs != None:
            self.options.update(kwargs)

    def Start(self):
        self.LoadMaterial()
        self.Action = self.Update

    def Update(self):
        self.HelperUpdate()

        self.Draw()
        self.DrawText()
        self.BtnUpdate()

    def DrawText(self):
        self.screen.blit(self.words, self.position)

    def ChangeText(self, text):
        self.words = self.font.render(text, True, self.options["textColor"])

    def ResetText(self):
        self.words = self.font.render(self.options["text"], True, self.options["textColor"])
