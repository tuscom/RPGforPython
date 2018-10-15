import pygame
from pygame.locals import *
import sys
import random
import math

import PieceAnimation3 as OldPieceAnimation

class PieceAnimation(OldPieceAnimation.PieceAnimation):
    def __init__(self, name, ObjectClass, ParentOneCmdAnim): #Animationの最小単位
        self.GetSource(ObjectClass, ParentOneCmdAnim)
        self.ProgramParameter()

        self.SetFunction(name)

    def GetSource(self, ObjectClass, ParentOneCmdAnim):
        super().GetSource(ObjectClass)
        self.OneCmdAnim = ParentOneCmdAnim

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
            [abs(int(self.scale.x)), abs(int(self.scale.y))])
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
        damage = self.TargetObject.CalcDamage(self.OneCmdAnim.options["attackRatio"])
        self.HPbarPicture = self.TargetObject.HPbarPicture
        self.pictureScale = self.HPbarPicture.get_size()
        pictureScaleRatio = self.pictureScale[0] / self.TargetObject.hp
        self.speed = damage * pictureScaleRatio / self.endTime
        self.TargetObject.hp -= damage

    #フェードイン1
    def FadeIn1FirstUsedStart(self):
        self.startPosition = pygame.math.Vector2(-400, 0)
        windowSize = self.MainClass.windowSize
        goalPosition = pygame.math.Vector2(windowSize[0], 0)
        self.endTime = 1
        self.speed = (goalPosition - self.startPosition) / self.endTime

    def FadeIn1AfterUsedStart(self):
        self.ObjectClass.position = pygame.math.Vector2(self.startPosition)

    def FadeIn1Update(self):
        self.ObjectClass.position += self.speed * self.Helper.pygamedeltatime

    #フェードアウト1
    def FadeOut1FirstUsedStart(self):
        windowSize = self.MainClass.windowSize
        self.startPosition = pygame.math.Vector2(windowSize[0], 0)
        goalPosition = pygame.math.Vector2(-400, 0)
        self.endTime = 1
        self.speed = (goalPosition - self.startPosition) / self.endTime

    def FadeOut1AfterUsedStart(self):
        self.ObjectClass.position = pygame.math.Vector2(self.startPosition)

    def FadeOut1Update(self):
        self.ObjectClass.position += self.speed * self.Helper.pygamedeltatime

    #ブラックボルト
    def BlackboltFirstUsedStart(self):
        self.endTime = 2
        self.rotateSpeed = 120
        self.sourcePicture = self.AnimController.blackboltPicture
        
        size = self.sourcePicture.get_size()
        self.scaleSpeed = 1 / self.endTime
        self.scaleSpeedV2 = pygame.math.Vector2(size[0], size[1]) / self.endTime
        self.scale = pygame.math.Vector2(size[0], size[1])

        self.screen = self.MainClass.screen

    def BlackboltAfterUsedStart(self):
        self.position = self.ObjectClass.AttackTarget.position + self.ObjectClass.AttackTarget.scale / 2
    def BlackboltUpdate(self):
        scale = (1 - self.clock * self.scaleSpeed)
        angle = self.rotateSpeed * self.clock
        picture = pygame.transform.rotozoom(self.sourcePicture, angle, scale)
        rect = picture.get_rect()
        rect.center = pygame.math.Vector2(self.position)

        #rad = math.radians(angle+45)
        #cos = math.cos(rad)
        #sin = math.sin(rad)
        #halfDiagonal = self.scale.length() / 2
        #yAdjuster = halfDiagonal * sin - self.scale.y/2
        #angleAdjuster = pygame.math.Vector2(0, -yAdjuster)
        #position += angleAdjuster

        self.screen.blit(picture, rect)
