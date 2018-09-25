import pygame
from pygame.locals import *
import sys
import random

import PieceAnimation3 as OldPieceAnimation

class PieceAnimation(OldPieceAnimation.PieceAnimation):
    def __init__(self, name, ObjectClass): #Animationの最小単位
        self.GetSource(ObjectClass)
        self.ProgramParameter()

        self.SetFunction(name)

    def AfterUsedStart(self):
        self.clock += self.Helper.pygamedeltatime
        if self.clock >= self.delayTime:
            self.Action = self.Update
            if self.AfterUsedStartFunc != None:
                self.AfterUsedStartFunc(self)

    def Update(self):
        self.clock += self.Helper.pygamedeltatime
        if self.EndCondition():
            self.Action = self.End
            self.clock = self.endTime + self.delayTime
        if self.UpdateFunc != None:
            self.UpdateFunc(self)

    #↓静的空間にあるとして扱う
    #ステップ攻撃エフェクト
    def StepAttackEffectUpdate(self):
        deltatime = self.Helper.pygamedeltatime
        self.scale += self.speed * deltatime
        picture = pygame.transform.scale(
            self.sourcePicture,
            [int(self.scale.x), int(self.scale.y)])
        self.position -= self.speed/2 * deltatime
        self.screen.blit(picture, self.position)
    def SetParameterForStepAttackEffect(self):
        self.position = pygame.math.Vector2(self.ObjectClass.AttackTarget.position)
        self.scale = pygame.math.Vector2(self.ObjectClass.scale)
        self.speed = -self.scale / self.endTime
    def StepAttackEffectFirstUsedStart(self):
        self.endTime = 1
        self.sourcePicture = self.AnimController.stepAttackEffectPicture
        self.screen = self.MainClass.screen
        #self.SetParameterForStepAttackEffect()
    def StepAttackEffectAfterUsedStart(self):
        self.SetParameterForStepAttackEffect()

    #HP変動
    #敵HP変動
    def HPmoveOfEnemyAfterUsedStart(self):
        self.TargetObject = self.ObjectClass.AttackTarget
        self.HPmoveAfterUsedStart()

    #dead
    def DeadFirstUsedStart(self):
        self.endTime = 1
        self.noOfPicture = 10
        self.sourcePicture = self.AnimController.framePicture
        self.screen = self.MainClass.screen
    def DeadAfterUsedStart(self):
        position = pygame.math.Vector2(self.ObjectClass.position)
        self.positionList = [position+pygame.math.Vector2(random.randrange(0, 250), random.randrange(0, 250)) for i in range(self.noOfPicture)]
        self.pictureList = [self.sourcePicture for i in range(self.noOfPicture)]
    def DeadUpdate(self):
        self.positionList = list(map(lambda pos : pos + pygame.math.Vector2(random.randrange(-5, 5), random.randrange(-5, 5)), self.positionList))
        for i in range(self.noOfPicture):
            self.screen.blit(self.pictureList[i], self.positionList[i])

    #HP変動
    def HPmoveAfterUsedStart(self):
        damage = 50
        self.HPbarPicture = self.TargetObject.HPbarPicture
        self.pictureScale = self.HPbarPicture.get_size()
        pictureScaleRatio = self.pictureScale[0] / self.TargetObject.hp
        self.speed = damage * pictureScaleRatio / self.endTime
        self.TargetObject.hp -= damage
