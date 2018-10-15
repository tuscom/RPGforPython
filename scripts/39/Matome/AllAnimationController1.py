import pygame
from pygame.locals import *
import sys
import copy

"""
ここに全てのOneCommandAnimを登録する
"""

class AllAnimationController:
    def __init__(self, MainClass):
        self.GetSource(MainClass)
        self.ProgramParameter()
        
    def GetSource(self, MainClass):
        self.MainClass = MainClass
        self.OneCmdAnim = MainClass.OneCmdAnim
        self.PieceAnimation = MainClass.PieceAnimation

    def ProgramParameter(self):
        self.ContinueAnimListDic = {
            "battle" : []
            } # AnimName : OneCmdAnim
        self.keyList = [*self.ContinueAnimListDic]
        #self.PlayList = copy.deepcopy(self.keyList) #OneCmdAnimのリスト
        self.PlaySingleList = [] #OneCmdAnimのリスト
        self.PlayContinueList = [None for i in range(len(self.keyList))]
        self.Action = self.Start
        self.PieceAnimDic = {
            "leftstep" : [self.PieceAnimation.LeftStepFirstUsedStart,
                          self.PieceAnimation.StepAfterUsedStart,
                          self.PieceAnimation.StepUpdate],
            "rightstep" : [self.PieceAnimation.RightStepFirstUsedStart,
                           self.PieceAnimation.StepAfterUsedStart,
                           self.PieceAnimation.StepUpdate],
            }# PieceAnimName : [FirstUsedStart, AfterUsedStart, Update]
        self.CmdAnimNameDic = {
            "familyStep" : ["leftstep"],
            "enemyStep" : ["rightstep"]
            } #CmdAnimName : [PieceAnimName, PieceAnimName, ...]

        self.CmdAnimKwargs = {
            }

    def Main(self):
        if self.Action != None:
            self.Action()

    #Start系
    def Start(self):
        self.LoadMaterial()
        self.Action = self.Update

    def LoadMaterial(self):
        self.stepAttackEffectPicturePath = "../../../pictures/attack.png"
        self.stepAttackEffectPicture = self.MainClass.BattleHelper.ScaledPicture(
            self.stepAttackEffectPicturePath,
            self.MainClass.charaSize
            )
        self.framePicturePath = "../../../pictures/frame.png"
        self.framePicture = self.MainClass.BattleHelper.ScaledPicture(
            self.framePicturePath,
            [80, 80]
            )
        self.blackboltPicturePath = "../../../pictures/blackbolt.png"
        self.blackboltPicture = self.MainClass.BattleHelper.ScaledPicture(
            self.blackboltPicturePath,
            self.MainClass.charaSize
            )    #Update系

    #Update系
    def Update(self):
        self.Play()
        self.AutoChangePlaySingleList()
        self.AutoChangeContinuePalyList()
    def Play(self):
        list(map(lambda anim:anim.Main(), self.PlaySingleList))
        list(map(lambda anim:anim.Main() if anim != None else None, self.PlayContinueList))
    def AutoChangePlaySingleList(self):
        popIndex = None
        for i in range(len(self.PlaySingleList)):
            if self.PlaySingleList[i].IsEndOfAnimation():
                popIndex = i
        if popIndex != None:
            self.PlaySingleList.pop(popIndex)
    def AutoChangeContinuePalyList(self):
        for i in range(len(self.PlayContinueList)):
            self.ChangeContiPlayList(i)
    def ChangeContiPlayList(self, index):
        if self.PlayContinueList[index] == None:
            pass
        elif self.PlayContinueList[index].IsEndOfAnimation():
            key = self.keyList[index]
            if len(self.ContinueAnimListDic[key]) > 0:
                NextObj = self.ContinueAnimListDic[key][0]
                self.ContinueAnimListDic[key].pop(0)
            else:
                NextObj = None

            self.PlayContinueList[index] = NextObj

    def AddContinueAnim(self, ContiAnimName, OneCmdAnim):
        key = self.keyList.index(ContiAnimName)
        OneCmdAnim.PlayON()
        if self.PlayContinueList[key] != None:
            self.ContinueAnimListDic[ContiAnimName].append(OneCmdAnim)
        else:
            self.PlayContinueList[key] = OneCmdAnim

    def AddSingleAnim(self, OneCmdAnim):
        OneCmdAnim.PlayON()
        self.PlaySingleList.append(OneCmdAnim)

    def ChangeContiPlayList(self, index):
        IsSkip = False
        if self.PlayContinueList[index] == None:
            pass
        elif self.PlayContinueList[index].IsEndOfAnimation():
            key = self.keyList[index]
            if len(self.ContinueAnimListDic[key]) > 0:
                NextObj = self.ContinueAnimListDic[key][0]
                IsSkip = NextObj.SkipCondition()
                self.ContinueAnimListDic[key].pop(0)
            else:
                NextObj = None

            if not IsSkip:
                self.PlayContinueList[index] = NextObj

    #Others
    def IsEndContinueAnimation(self, name):
        key = self.keyList.index(name)
        result = self.PlayContinueList[key] == None
        return result