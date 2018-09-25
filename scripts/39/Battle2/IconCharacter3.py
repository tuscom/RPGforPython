import pygame
from pygame.locals import *
import sys
import functools

import IconCharacter2 as OldIconCharacter

class IconCharacter(OldIconCharacter.IconCharacter):
    def __init__(self, MainClass, CharaClass, kwargs):
        self.GetSource(MainClass, CharaClass)
        self.SetOptions(kwargs)
        self.ProgramParameter()

        self.OnInstanceFunc()
        self.SetObjAnimDic()

    def GetSource(self, MainClass, CharaClass):
        super().GetSource(MainClass, CharaClass)
        self.battleMenuName = CharaClass.battleMenuName

    def SetOptions(self, kwargs):
        self.options = {
            "name" : "名無し",
            "picturepath" : "../../../pictures/mon_016.bmp",
            "position" : pygame.math.Vector2(),
            "scale" : pygame.math.Vector2(100, 100),
            "btnFunc" : None,
            "bgPicturePath" : "../../../pictures/normalPanel.png",
            "HPbarPicturePath" : "../../../pictures/HPbar.png",
            "HPbarbackPicturePath" : "../../../pictures/HPbar_back.png",
            "HPbarThick" : 10
            }
        if kwargs != None:
            self.options.update(kwargs)

    def SetObjAnimDic(self):
        kwargsShowBattleMenu = {"StartFunc" : lambda : self.MainClass.SelectedSwitch(self.CharaClass)}
        kwargsBackBattleMenu = {"EndFunc" : lambda : self.MainClass.SelectedSwitch(None)}
        self.ObjAnimDic = {
            "jump" : self.OneCmdAnim("jump", self, None),
            "showBattleMenu" : self.OneCmdAnim("showBattleMenu", self, kwargsShowBattleMenu),
            "backBattleMenu" : self.OneCmdAnim("backBattleMenu", self, kwargsBackBattleMenu)
            } # CmdAnimName : OneCmdAnim(class)

    def Start(self):
        self.LoadMaterial()
        self.SetScale()
        self.SetHPbar()
        self.SetHPbarPosition()
        self.SetbgPicture()
        self.SetCharacterPicture()
        self.SetBattleMenu()
        self.Action = self.Update

    def SetBattleMenu(self):
        battleMenuText = self.CharaClass.battleMenuText
        noOfBtn = len(self.battleMenuName)
        scale = pygame.math.Vector2(self.MainClass.battleMenuWidth, self.MainClass.battleMenuHeight)
        y = self.MainClass.windowSize[1] - self.MainClass.battleMenuHeight - self.scale.y
        self.BattleMenuBtnList = []
        for i in range(noOfBtn):
            position = pygame.math.Vector2(0, y) + pygame.math.Vector2(1, 0) * scale.x * i
            func = functools.partial(
                self.BattleMenuBtnOnClick,
                self.battleMenuName[i]
                )
            kwargs = {
                "position" : position,
                "scale" : scale,
                "text" : battleMenuText[i],
                "btnFunc" : func,
                "picturepath" : self.MainClass.charaControllerPanelPicturePath,
                "name" : "battleMenu"
                }
            self.BattleMenuBtnList.append(self.MainClass.Button(self.MainClass, kwargs))

    def Update(self):
        self.HelperUpdate()
        self.Draw()
        self.BtnUpdate()
        self.BattleMenuController()

    #Others
    def BattleMenuBtnOnClick(self, menuName):
        self.CharaClass.AttackName = menuName
        self.MainClass.SelectedFamily = None

    def OnClick(self):
        if self.MainClass.SelectedFamily != self.CharaClass:
            self.AddSingleAnim("showBattleMenu")
        else:
            self.AddSingleAnim("backBattleMenu")

    def BattleMenuController(self):
        if self.MainClass.SelectedFamily == self.CharaClass:
            list(map(
                    lambda battleMenuBtn : self.MainClass.ObjectSetActive(battleMenuBtn, True), self.BattleMenuBtnList
                    ))
        else:
            list(map(
                    lambda battleMenuBtn : self.MainClass.ObjectSetActive(battleMenuBtn, False), self.BattleMenuBtnList
                    ))

        