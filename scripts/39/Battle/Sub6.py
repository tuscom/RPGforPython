import pygame
from pygame.locals import *
import sys
import random
import copy
import math

import Helper
from Helper import BattleHelper

import Sub5 as Sub

class ObjectClass(Sub.ObjectClass):
    def __init__(self, MainClass, kwargs):
        self.MainClass = MainClass
        self.BattleHelper = MainClass.BattleHelper
        self.Helper = MainClass.Helper
        self.screen = MainClass.screen
        self.OneCommandAnimation = MainClass.OneCommandAnimation

        self.LoadMaterial()
        self.SetOptions(kwargs)
        self.SetParameter()
        self.SetButton()
        self.OnInstanceFunc()
        self.SetAction()

    def SetParameter(self):
        super().SetParameter()
        self.enable = True

    def Start(self):
        self.SetAnimationCommand()
        self.Action = self.Update

    def Update(self):
        self.HelperUpdate()
        self.BtnUpdate()
        if not self.enable:
            self.Action = self.End

        #最後に描画
        self.Draw()

    def End(self):
        self.Action = None

#class AllAnimationController(Sub.AllAnimationController):
#    def __init__(self, ContiAnimList):
#        self.ContiAnimList = ContiAnimList
#        self.Action = self.Start

#    def Start(self):
#        self.Action = self.Update

#    def Update(self):
#        self.PlayContiAnim()

#class ContinueAnimation(Sub.ContinueAnimation):
#    def __init__(self, CommandAnimationList, kwargs):
#        self.SetOptions(kwargs)
#        self.SetAction()

#        self.CommandAnimationList = CommandAnimationList

#    def SetOptions(self, kwargs):
#        self.options = {
#            "isRepeat" : False,
#            "isAutoStart" : True}
#        if kwargs != None:
#            self.options.update(kwargs)

#        self.UpdateFunc = self.RepeatUpdate if self.options["isRepeat"] else self.AutoEndUpdate

#    def SetAction(self):
#        if self.options["isAutoStart"]:
#            self.Action = self.Start
#            self.PlayON()
#        else:
#            self.Action = None


#    def Start(self):
#        self.noOfComAnim = len(self.CommandAnimationList)
#        self.Action = self.Update
#        self.indexOfAnimation = 0

#    def Update(self):
#        self.UpdateFunc()

#    def RepeatUpdate(self):
#        comAnim = self.CommandAnimationList[self.indexOfAnimation]
#        comAnim.Main()
#        if comAnim.IsEndOfAnimation():
#            self.indexOfAnimation += 1
#            self.indexOfAnimation %= self.noOfComAnim

#            if self.indexOfAnimation == 0:
#                self.PlayON()

#    def AutoEndUpdate(self):
#        comAnim = self.CommandAnimationList[self.indexOfAnimation]

#        comAnim.Main()
#        if comAnim.IsEndOfAnimation():
#            self.indexOfAnimation += 1

#            if self.EndCondition():
#                self.Action = self.End

#    #================= Others ===================
#    def PlayON(self):
#        list(map(lambda comAnim : comAnim.PlayON(), self.CommandAnimationList))

#        if self.IsEndOfAnimation():
#            self.Action = self.Start

#    def EndCondition(self):
#        return self.indexOfAnimation % self.noOfComAnim == 0

#    def IsEndOfAnimation(self):
#        return self.Action == None


class ContinueAnimation:
    def __init__(self):
        self.Action = self.Start

    def Main(self):
        if self.Action != None:
            self.Action()
    def Start(self):
        self.Action = self.Update

    def SetCommandAnimationList(self):
        self.ContiCmdAnimationList = []
        self.AttackCmdList = []
        self.AttackCmdList.pop()

    def Update(self):
        pass

class OneCommandAnimation(Sub.OneCommandAnimation): 
    def __init__(self, name, ObjectClass, kwargs):
        self.ObjectClass = ObjectClass
        self.PieceAnimation = ObjectClass.MainClass.PieceAnimation
        
        self.SetOptions(kwargs)
        self.SelectAnimation(name)
        self.PieceAnimationList = None
        self.Action = None


    def SetOptions(self, kwargs):
        self.options = {
            "PlayCondition" : None,
            "StartFunc" : None,
            "UpdateFunc" : None,
            "EndFunc" : None}
        if kwargs != None:
            self.options.update(kwargs)
        self.StartFunc = self.options["StartFunc"]
        self.UpdateFunc = self.options["UpdateFunc"]
        self.EndFunc = self.options["EndFunc"]

    def SelectAnimation(self, name):
        self.indexDict = {
            "leftAttackStep" : self.LeftAttackStep,
            "rightAttackStep" : self.RightAttackStep,
            "jump" : self.Jump,
            "mudaniHustle" : self.MudaniHustle,
            "ShowBattleMenu" : self.ShowBattleMenu}

        self.indexDict[name]()


    def Start(self):
        if self.StartFunc != None:
            self.StartFunc()

        self.SendLogMessage()
        self.Action = self.Update

    def SendLogMessage(self):
        pass

    def Update(self):
        if self.UpdateFunc != None:
            self.UpdateFunc()
        list(map(lambda pieceAnime : pieceAnime.Main(), self.PieceAnimationList))
        if self.EndCondition():
            self.Action = self.End

    def End(self):
        self.Action = None

    def IsEndOfAnimation(self):
        return self.Action == None

    def EndCondition(self):
        boolList = list(map(lambda pieceAnim : pieceAnim.IsEndOfAnimation(), self.PieceAnimationList))
        return all(boolList)

    def PlayON(self):
        if self.IsEndOfAnimation():
            self.Action = self.Start
            list(map(lambda pieceAnim : pieceAnim.PlayON(), self.PieceAnimationList))

    #================= Play Condition ================
    def NowPlayCondition(self):
        return True


class PieceAnimation(Sub.PieceAnimation):
    def __init__(self, name, ObjectClass, kwargs): 
        self.ObjectClass = ObjectClass
        self.MainClass = ObjectClass.MainClass
        self.Helper = self.MainClass.Helper

        self.SetOptions(kwargs)

        self.isEndOfAnimation = False
        self.StartFunc = None
        self.UpdateFunc = None
        self.clock = 0

        self.delayTime = 0

        self.Action = None

        self.SelectAnimation(name)

    def Start(self):
        self.clock += self.Helper.pygamedeltatime
        if self.clock >= self.delayTime:

            if self.StartFunc != None:
                self.StartFunc()

            self.isEndOfAnimation = False
            self.Action = self.Update

    def Update(self):
        self.clock += self.Helper.pygamedeltatime
        if self.UpdateFunc != None:
            self.UpdateFunc()

        if self.EndCondition():
            self.Action = self.End
