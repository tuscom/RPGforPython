import pygame
from pygame.locals import *
import sys

import AllAnimationController3 as OldAllAnimationController

class AllAnimationController(OldAllAnimationController.AllAnimationController):
    def __init__(self, MainClass):
        self.GetSource(MainClass)
        self.ProgramParameter()

    def ProgramParameter(self):
        self.ProgramOtherParameter()
        self.ContinueAnimListDic = {
            "battle" : []
            } # AnimName : OneCmdAnim
        self.keyList = [*self.ContinueAnimListDic]
        #self.PlayList = copy.deepcopy(self.keyList) #OneCmdAnimのリスト
        self.PlaySingleList = [] #OneCmdAnimのリスト
        self.PlayContinueList = [None for i in range(len(self.keyList))]
        self.Action = self.Start
        self.PieceAnimDic = {
            "jump" : [self.PieceAnimation.JumpFirstUsedStart,
                      self.PieceAnimation.JumpAfterUsedStart,
                      self.PieceAnimation.JumpUpdate],
            "leftstep" : [self.PieceAnimation.LeftStepFirstUsedStart,
                          self.PieceAnimation.StepAfterUsedStart,
                          self.PieceAnimation.StepUpdate],
            "rightstep" : [self.PieceAnimation.RightStepFirstUsedStart,
                           self.PieceAnimation.StepAfterUsedStart,
                           self.PieceAnimation.StepUpdate],
            "stepAttackEffect" : [self.PieceAnimation.StepAttackEffectFirstUsedStart,
                                  self.PieceAnimation.StepAttackEffectAfterUsedStart,
                                  self.PieceAnimation.StepAttackEffectUpdate],
            "familyHPmove" : [self.PieceAnimation.HPmoveOfFamilyFirstUsedStart,
                              self.PieceAnimation.HPmoveAfterUsedStart,
                              self.PieceAnimation.HPmoveUpdate],
            "enemyHPmove" : [self.PieceAnimation.HPmoveOfEnemyFirstUsedStart,
                             self.PieceAnimation.HPmoveOfEnemyAfterUsedStart,
                             self.PieceAnimation.HPmoveUpdate],
            "showBattleMenu" : [self.PieceAnimation.ShowBattleMenuFirstUsedStart,
                                self.PieceAnimation.MoveBattleMenuAfterUsedStart,
                                self.PieceAnimation.MoveBattleMenuUpdate],
            "backBattleMenu" : [self.PieceAnimation.BackBattleMenuFirstUsedStart,
                                self.PieceAnimation.MoveBattleMenuAfterUsedStart,
                                self.PieceAnimation.MoveBattleMenuUpdate],
            "frame" : [self.PieceAnimation.DeadFirstUsedStart,
                      self.PieceAnimation.DeadAfterUsedStart,
                      self.PieceAnimation.DeadUpdate]
            }# PieceAnimName : [FirstUsedStart, AfterUsedStart, Update]
        self.CmdAnimNameDic = {
            "jump" : ["jump"],
            "enemyStepAttack" : ["rightstep", "enemyHPmove", "stepAttackEffect"],
            "familyStepAttack" : ["leftstep", "enemyHPmove", "stepAttackEffect"],
            "showBattleMenu" : ["showBattleMenu"],
            "backBattleMenu" : ["backBattleMenu"],
            "dead" : ["frame"]
            } #CmdAnimName : [PieceAnimName, PieceAnimName, ...]


    def ProgramOtherParameter(self):
        self.NextObj = None

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
    def Update(self):
        self.Play()
        self.AutoChangePlaySingleList()
        self.AutoChangeContinuePalyList()

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
