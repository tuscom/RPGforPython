
import pygame
from pygame.locals import *
import sys

from Source import PieceAnimation
import AllAnimationController1

class AllAnimationController(AllAnimationController1.AllAnimationController):
    def __init__(self, MainClass):
        self.GetSource(MainClass)
        self.ProgramParameter()

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
            "jump" : [self.PieceAnimation.JumpFirstUsedStart,
                      self.PieceAnimation.JumpAfterUsedStart,
                      self.PieceAnimation.JumpUpdate],
            "leftstep" : [self.PieceAnimation.LeftStepFirstUsedStart,
                          self.PieceAnimation.StepAfterUsedStart,
                          self.PieceAnimation.StepUpdate],
            "rightstep" : [self.PieceAnimation.RightStepFirstUsedStart,
                           self.PieceAnimation.StepAfterUsedStart,
                           self.PieceAnimation.StepUpdate],
            "familyHPmove" : [self.PieceAnimation.HPmoveOfFamilyFirstUsedStart,
                              self.PieceAnimation.HPmoveAfterUsedStart,
                              self.PieceAnimation.HPmoveUpdate],
            "enemyHPmove" : [self.PieceAnimation.HPmoveOfEnemyFirstUsedStart,
                             self.PieceAnimation.HPmoveAfterUsedStart,
                             self.PieceAnimation.HPmoveUpdate]
            }# PieceAnimName : [FirstUsedStart, AfterUsedStart, Update]
        self.CmdAnimNameDic = {
            "jump" : ["jump"],
            "enemyStepAttack" : ["rightstep", "enemyHPmove"],
            "familyStepAttack" : ["leftstep", "enemyHPmove"]
            } #CmdAnimName : [PieceAnimName, PieceAnimName, ...]

    def Start(self):
        self.Action = self.Update

    def Update(self):
        self.Play()
        self.AutoChangePlaySingleList()
        self.AutoChangeContinuePalyList()
