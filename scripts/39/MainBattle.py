import pygame
from pygame.locals import *
import sys

import BaseBattle
import Helper

class MainClass(BaseBattle.MainClass):
    def __init__(self):
        super().__init__()

        self.Helper = BattleHelper(self)

        #背景
        self.bgPicturePath = "../../pictures/keimusyo_niwa001.jpg"

        #パネル
        self.charaControllerLayout = [0, 0.8, 1, 0.2]
        self.attackBtnLayout = pygame.math.Vector2(0.8, 0.7)
        self.attackPicturePath = "../../pictures/attackButton.png"

        #フィールド
        self.charaSize = [250, 250]
        self.familyPos = pygame.math.Vector2(900, 100)
        self.enemyPos = pygame.math.Vector2(350, self.familyPos.y)

        #アニメーション
        self.SortedAttackCharacterList = []

    def LoadScene(self):
        #背景描画
        self.backGroundPicture = BattleHelper.ScaledPicture(self.bgPicturePath, size=self.windowSize)
    def SetFieldCharacter(self):
        #positionセット
        self.familyPictures = [
            "../../pictures/9c338508771fd401ada29fba07b34ebf.png",
            "../../pictures/ahobakaizer.png",
            "../../pictures/9c338508771fd401ada29fba07b34ebf.png"
            ]
        self.enemyPictures = [
            "../../pictures/igyo-yousei01.png",
            "../../pictures/igyo-yousei01.png",
            "../../pictures/igyo-boushi01.png"
            ]

        self.family = []
        for i in range(len(self.familyPictures)):
            self.family.append(
                FieldCharacter(
                    self,
                    name=str(i),
                    picturepath=self.familyPictures[i],
                    scale=self.charaSize
                    )
                )
            self.family[-1].position = self.familyPos + i*pygame.math.Vector2(120, 120)

        self.enemies = []
        for i in range(len(self.enemyPictures)):
            self.enemies.append(
                FieldEnemyClass(
                    self,
                    name=str(i),
                    picturepath=self.enemyPictures[i],
                    scale=self.charaSize,
                    )
                )
            self.enemies[-1].position = self.enemyPos + i * pygame.math.Vector2(-120, 120)

    def SetPanel(self):
        self.charaControllerRect = self.Helper.NormToWorldRect(self.charaControllerLayout)
        self.charaControllerPanelPicture = BattleHelper.ScaledPicture("../../pictures/normalPanel.png", size=(self.charaControllerRect[2], self.charaControllerRect[3]))
        self.familyIcons = list(map(lambda picturepath:BattleHelper.ScaledPicture(picturepath, (self.charaControllerRect[3], self.charaControllerRect[3])), self.familyPictures))

        attackBtnPos = self.Helper.NormToWorldPos(self.attackBtnLayout)
        self.attackBtn = Helper.Button(
            self.screen,
            rect=[attackBtnPos.x, attackBtnPos.y, 200, 200],
            picturename=self.attackPicturePath,
            text="",
            func=self.AttackOnClick)
    def DrawBackGround(self):
        #背景描画
        self.screen.blit(self.backGroundPicture, (0, 0))
    def DrawPanel(self):
        self.screen.blit(self.charaControllerPanelPicture, (self.charaControllerRect[0], self.charaControllerRect[1]))

        list(map(lambda i : self.screen.blit(self.familyIcons[i], (i*self.charaControllerRect[3], self.charaControllerRect[1])), range(len(self.familyIcons))))

        self.attackBtn.Update()
    def DrawCharacter(self):
        list(map(lambda familyMember : familyMember.Main(), self.family))
        list(map(lambda enemy : enemy.Main(), self.enemies))

    def AttackAnimationStart(self):
        targetIndex = 0
        self.family[targetIndex].Attack()
        self.SortedAttackCharacterList = self.family

        self.AnimationController = self.AttackAnimationUpdate
    def AttackAnimationUpdate(self):
        for i in range(len(self.SortedAttackCharacterList)):
            if self.SortedAttackCharacterList[i].IsEndOfAnimation:
                if i+1 < len(self.SortedAttackCharacterList):
                    self.SortedAttackCharacterList[i+1].Attack()

        if self.SortedAttackCharacterList[-1].IsEndOfAnimation:
            self.AnimationController = None

    def AttackOnClick(self):
        if self.AnimationController == None:
            self.AnimationController = self.AttackAnimationStart

class FieldCharacter(BaseBattle.FieldCharacterClass):
    def __init__(self, MainClass, **kwargs):
        super().__init__(MainClass, kwargs)
        self.Animation = Animations(self)
        self.IsEndOfAnimation = False

    def Attack(self):
        self.Animation.LeftAttackStep()

    def AnimationUpdate(self):
        self.Animation.Main()
        self.IsEndOfAnimation = self.Animation.IsEndOfAnimation

class FieldEnemyClass(BaseBattle.FieldEnemyClass):
    def __init__(self, MainClass, **kwargs):
        super().__init__(MainClass, kwargs)

class BattleHelper(BaseBattle.Helper):
    def __init__(self, MainClass):
        super().__init__(MainClass)

        #Fade In 001
        self.pictureSize001 = (self.windowSize[0]+350, self.windowSize[1])
        self.fadePicture001 = BattleHelper.ScaledPicture("../../pictures/myFade.png", size=self.pictureSize001)
        self.position001 = pygame.math.Vector2(-300, 0)

    def FadeIn001(self):
        if self.windowSize[0] - self.position001.x > 0:
            self.screen.blit(self.fadePicture001, self.position001)
            self.position001 += pygame.math.Vector2(10, 0)

class Animations(BaseBattle.Animations):
    def __init__(self, Character):
        super().__init__(Character)
        #左アタック
        self.leftAttackTime = 1
        self.leftAttackWidth = 100
        self.leftAttackTimer = 0
        self.leftAttackStepSpeed = 0

    def LeftAttackStepSet(self):
        self.leftAttackTimer = 0

        self.leftAttackStepSpeed = self.leftAttackWidth / self.leftAttackTime * 2
        self.goalPos = pygame.math.Vector2(self.Character.position)

    def LeftAttackStepUpdate(self):
        deltatime = self.Helper.pygamedeltatime
        self.leftAttackTimer += deltatime

        if self.leftAttackTimer <= self.leftAttackTime/2:
            self.Character.position += pygame.math.Vector2(-1, 0) * self.leftAttackStepSpeed * deltatime

        if self.leftAttackTimer >= self.leftAttackTime/2:
            self.Character.position += pygame.math.Vector2(1, 0) * self.leftAttackStepSpeed * deltatime

        if self.leftAttackTimer >= self.leftAttackTime:
            self.IsEndOfAnimation = True
            self.Character.position = pygame.math.Vector2(self.goalPos)


#====================実行部分=================
MainClass().Main()