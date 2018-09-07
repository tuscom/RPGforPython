import pygame
from pygame.locals import *
import sys

import BaseBattle
import Helper
from Helper import BattleHelper

class MainClass(BaseBattle.MainClass):
    def __init__(self):
        super().__init__()

        self.Helper = Helper.BattleHelper(self)

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
        self.targetIconPicturePath = "../../pictures/targetIcon.png"
        self.SelectedEnemy = None
        self.SelectedFamily = None

        #アニメーション
        self.SortedAttackCharacterList = []
        self.AnimationsUpdate = []
        self.Animations = []
        self.TargetAnimation = None
        self.animationIndex = 0

    #=================Start====================
    def LoadScene(self):
        #背景描画
        self.backGroundPicture = BattleHelper.ScaledPicture(self.bgPicturePath, size=self.windowSize)
        self.targetIconPicture = BattleHelper.ScaledPicture(self.targetIconPicturePath, self.charaSize)
    def SetFieldCharacter(self):
        #positionセット
        self.familyPictures = [
            "../../pictures/9c338508771fd401ada29fba07b34ebf.png",
            "../../pictures/ahobakaizer.png",
            "../../pictures/9c338508771fd401ada29fba07b34ebf.png"
            ]
        self.menus = [
            ["ぶつかる", "コケる"],
            ["きる", "からぶる"],
            ["ぶつかる", "コケる"]
            ]
        self.menuFuncs = [
            [lambda:print("ぶつかった"), lambda:print("こけた")],
            [lambda:print("きった"), lambda:print("からぶった")],
            [lambda:print("ぶつかった"), lambda:print("こけた")]
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
                    scale=self.charaSize,
                    menu=self.menus[i],
                    menufunc=self.menuFuncs[i]
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
    def SetAnimations(self):
        #animation取得
        allCharacter = self.family + self.enemies
        self.AnimationsUpdate = [Character.AnimationUpdate for Character in allCharacter]
        self.Animations = [Character.Animation for Character in allCharacter]
    def SetPanel(self):
        self.charaControllerRect = self.Helper.NormToWorldRect(self.charaControllerLayout)
        self.charaControllerPanelPicture = BattleHelper.ScaledPicture("../../pictures/normalPanel.png", size=(self.charaControllerRect[2], self.charaControllerRect[3]))
        self.familyIcons = []
        for i in range(len(self.family)):
            self.familyIcons.append(
                IconCharacter(self, self.family[i])
                )
            self.familyIcons[-1].position = pygame.math.Vector2(
                i * self.charaControllerRect[3],
                self.charaControllerRect[1]
                )
            self.familyIcons[-1].SetHPbarPos()
            
        attackBtnPos = self.Helper.NormToWorldPos(self.attackBtnLayout)
        self.attackBtn = Helper.Button(
            self.screen,
            rect=[attackBtnPos.x, attackBtnPos.y, 200, 200],
            picturename=self.attackPicturePath,
            text="",
            func=self.AttackOnClick)

    #================Update==================
    def DrawBackGround(self):
        #背景描画
        self.screen.blit(self.backGroundPicture, (0, 0))
    def DrawPanel(self):
        self.screen.blit(self.charaControllerPanelPicture, (self.charaControllerRect[0], self.charaControllerRect[1]))

        list(map(lambda familyIcon : familyIcon.Main(), self.familyIcons))

        self.attackBtn.Update()
    def DrawCharacter(self):
        list(map(lambda familyMember : familyMember.Main(), self.family))
        list(map(lambda enemy : enemy.Main(), self.enemies))
    def DrawAnimations(self):
        #anime実行
        list(map(lambda anime:anime(), self.AnimationsUpdate))
    def DrawTargetIcon(self):
        if self.SelectedEnemy != None:
            self.screen.blit(self.targetIconPicture, self.SelectedEnemy.position)

    #================Button==================
    def AllBattleMenuOff(self):
        #すべての戦闘メニュー非表示
        list(map(lambda familyIcon:familyIcon.BattleMenuSwitchOff(), self.familyIcons))
    def SetAttackAnimation(self):
        if self.AnimationController == None:
            self.AnimationController = self.AttackAnimation
            self.animationIndex = 0
            self.TargetAnimation = self.Animations[self.animationIndex]

    #=============== Animation ==============
    def AttackAnimation(self):
        self.TargetAnimation.Play()

        if self.TargetAnimation.IsEndOfAnimationFunc():
            self.animationIndex += 1
            if self.animationIndex >= len(self.Animations):
                self.AnimationController = None
            else:
                self.TargetAnimation = self.Animations[self.animationIndex]

class IconCharacter(BaseBattle.IconCharacterClass):
    def __init__(self, MainClass, CharacterClass, **kwargs):
        super().__init__(MainClass, CharacterClass, kwargs)

        self.MenuBtn = BattleCharacterMenu(
            MainClass,
            menu=self.menu,
            func=self.menuFunc
            )
        self.BattleMenuSwitch = False

    #Update
    def DrawBattleMenu(self):
        if self.BattleMenuSwitch:
            self.MenuBtn.Main()

    #Button
    def OnClick(self):
        #onclick
        self.Selected()
    def Selected(self):
        self.MainClass.AllBattleMenuOff()
        self.BattleMenuSwitch = True

        self.MainClass.SelectedEnemy = self.CharacterClass.AttackTarget
        self.MainClass.SelectedFamily = self.CharacterClass
    def BattleMenuSwitchOff(self):
        #メニュー非表示
        self.BattleMenuSwitch = False

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
        self.Animation = Animations(self)
        self.IsEndOfAnimation = False

    def AnimationUpdate(self):
        self.Animation.Main()
        self.IsEndOfAnimation = self.Animation.IsEndOfAnimation

    def OnClick(self):
        if self.MainClass.SelectedEnemy != None:
            self.MainClass.SelectedEnemy = self
        if self.MainClass.SelectedFamily != None:
            self.MainClass.SelectedFamily.AttackTarget = self

class Animations(BaseBattle.Animations):
    def __init__(self, Character):
        super().__init__(Character)
        #左右ステップアタック
        self.stepAttackTime = 1
        self.stepAttackWidth = 100
        self.stepAttackTimer = 0
        self.stepAttackSpeed = 0
        self.stepAttackHPMoveTime = self.stepAttackTime / 2
        self.stepAttackDirection = pygame.math.Vector2()

        #HP変動
        self.damage = 0
        self.hp = 0
        self.moveHpTime = 0.5
        self.hpBarSize = [0, 0]
        self.hpMoveSpeed = 0
        self.hpPicture = None

        #ノーマル攻撃エフェクト
        self.normalAttackPicturePath = "../../pictures/attack.png"
        self.normalAttackTime = self.stepAttackTime
        self.normalAttackPicture = None
        self.normalAttackPosition = pygame.math.Vector2()
        self.normalAttackNextPos = pygame.math.Vector2()
        self.normalAttackScaleSpeed = pygame.math.Vector2()
        self.normalAttackScale = pygame.math.Vector2(200, 200)
        self.normalAttackCenter = pygame.math.Vector2()

        self.TargetSurfaceAnimations = []
        self.FamilyStepAttack = [
            OneSurfaceAnimation( #左ステップ
                self.MainClass,
                Character,
                endTime=self.stepAttackTime,
                StartFunc=self.LeftAttackStepStartAnim,
                UpdateFunc=self.LeftAttackStepUpdateAnim
                ),
            OneSurfaceAnimation( #HP変動
                self.MainClass,
                Character,
                endTime=self.moveHpTime,
                delayTime=0.5,
                StartFunc=self.MoveHPStartAnim,
                UpdateFunc=self.MoveHPUpdateAnim,
                EndFunc=self.MoveHPEndAnim
                ),
            OneSurfaceAnimation( #ノーマルエフェクト
                self.MainClass,
                self,
                endTime=1,
                StartFunc=self.NormalAttackStartAnim,
                UpdateFunc=self.NormalAttackUpdateAnim
                )
            ]

    def Play(self):
        list(map(lambda OneAnim:OneAnim.Main(), self.TargetSurfaceAnimations))
    def IsEndOfAnimationFunc(self):
        boolList = list(map(lambda OneAnimation : OneAnimation.isEndOfAnimation, self.TargetSurfaceAnimations))
        return all(boolList)
    def SetTargetAnimation(self, SurfaceAnimations):
        self.TargetSurfaceAnimations = SurfaceAnimations
    def AutoSetSurfaceAnimation(self):
        self.TargetSurfaceAnimations = self.FamilyStepAttack

    #左アタック　ver2
    def LeftAttackStepStartAnim(self):
        self.leftAttackStepAnimTime = self.stepAttackTime
        self.leftAttackStepAnimTimer = 0
        self.leftAttackStepAnimDirection = pygame.math.Vector2(-1, 0)
        self.leftAttackStepAnimSpeed = self.stepAttackWidth / self.stepAttackTime * 2
    def LeftAttackStepUpdateAnim(self):
        deltatime = self.Helper.pygamedeltatime
        self.leftAttackStepAnimTimer += deltatime
        if self.leftAttackStepAnimTimer <= self.leftAttackStepAnimTime/2:
            self.Character.position += self.leftAttackStepAnimDirection * deltatime * self.leftAttackStepAnimSpeed
        if self.leftAttackStepAnimTimer >= self.leftAttackStepAnimTime/2:
            self.Character.position -= self.leftAttackStepAnimDirection * deltatime * self.leftAttackStepAnimSpeed

    #HP変動　ver2
    def MoveHPStartAnim(self):
        AttackTarget = self.Character.AttackTarget
        AttackTarget.Animation.damage = 10
        self.MoveHPSourcePicture = AttackTarget.HPbarPicture
        self.MoveHPSourceBackPicture = AttackTarget.HPbarbackPicture
        self.MoveHPpictureScaleRatio = AttackTarget.MaxHPSizeList()[0] / AttackTarget.MaxHP()
        self.MoveHPspeed = -AttackTarget.Animation.damage / self.moveHpTime * self.MoveHPpictureScaleRatio
        self.MoveHPbarScale = pygame.math.Vector2(AttackTarget.HPscale)

        AttackTarget.hp -= AttackTarget.Animation.damage
    def MoveHPUpdateAnim(self):
        deltatime = self.Helper.pygamedeltatime
        self.MoveHPbarScale.x += self.MoveHPspeed * deltatime
        self.Character.AttackTarget.HPbarPicture = pygame.transform.scale(
            self.MoveHPSourcePicture,
            [int(self.MoveHPbarScale.x), int(self.MoveHPbarScale.y)]
            )
    def MoveHPEndAnim(self):
        self.MoveHPbarScale = pygame.math.Vector2(
            self.Character.AttackTarget.hp * self.MoveHPpictureScaleRatio,
            self.MoveHPbarScale.y)
        self.Character.AttackTarget.HPscale = self.MoveHPbarScale

    #ノーマルエフェクト　ver2
    def NormalAttackStartAnim(self):
        self.NormalAttackAnimTime = 1
        self.NormalAttackAnimSourcePicture = self.NormalAttackPicture
        self.NormalAttackAnimScale = pygame.math.Vector2(self.normalAttackScale)
        self.NormalAttackAnimSpeed = -self.NormalAttackAnimScale / self.NormalAttackAnimTime
        self.NormalAttackAnimPos = pygame.math.Vector2(self.Character.AttackTarget.position)
        self.NormalAttackAnimStartCenter = self.NormalAttackAnimPos + self.NormalAttackAnimScale/2
        self.NormalAttackAnimStartPos=pygame.math.Vector2(self.NormalAttackAnimPos)
    def NormalAttackUpdateAnim(self):
        deltatime = self.Helper.pygamedeltatime

        picture = pygame.transform.scale(
            self.NormalAttackAnimSourcePicture, 
            [int(self.NormalAttackAnimScale.x), int(self.NormalAttackAnimScale.y)])
        newCenter = self.NormalAttackAnimStartPos + self.NormalAttackAnimScale/2
        newPos = self.NormalAttackAnimStartPos + (self.NormalAttackAnimStartCenter - newCenter)
        self.NormalAttackAnimScale += self.NormalAttackAnimSpeed * deltatime

        self.screen.blit(picture, newPos)

    #左アタック
    def LeftAttackStepSet(self):
        self.stepAttackTimer = 0
        self.stepAttackDirection = pygame.math.Vector2(-1, 0)

        self.stepAttackSpeed = self.stepAttackWidth / self.stepAttackTime * 2
        self.goalPos = pygame.math.Vector2(self.Character.position)

        self.normalAttackPosition = pygame.math.Vector2(self.Character.AttackTarget.position)
        self.normalAttackNextPos = pygame.math.Vector2(self.normalAttackPosition)
        self.normalAttackCenter = self.Character.AttackTarget.position + self.Character.AttackTarget.scale/2
        self.normalAttackScaleSpeed = pygame.math.Vector2(self.normalAttackScale.x, self.normalAttackScale.y) / self.normalAttackTime
    def LeftAttackStepUpdate(self):
        deltatime = self.Helper.pygamedeltatime
        previousTimer = self.stepAttackTimer
        self.stepAttackTimer += deltatime

        if self.stepAttackTimer <= self.stepAttackTime/2:
            self.Character.position += pygame.math.Vector2(-1, 0) * self.stepAttackSpeed * deltatime

        if self.stepAttackTimer >= self.stepAttackTime/2:
            self.Character.position += pygame.math.Vector2(1, 0) * self.stepAttackSpeed * deltatime

        if self.stepAttackTimer >= self.stepAttackTime:
            self.IsEndOfAnimation = True
            self.Character.position = pygame.math.Vector2(self.goalPos)

        if self.stepAttackTimer >= self.stepAttackHPMoveTime:
            if previousTimer < self.stepAttackHPMoveTime:
                self.Character.AttackTarget.Animation.MoveHP()

        
        if self.normalAttackTime > self.stepAttackTimer:
            normalAttackNextScale = self.normalAttackScale - self.stepAttackTimer * self.normalAttackScaleSpeed
            normalAttackPictureCenter = self.normalAttackNextPos + normalAttackNextScale/2
            self.normalAttackNextPos += self.normalAttackCenter - normalAttackPictureCenter
            normalAttackPicture = pygame.transform.scale(
                self.normalAttackPicture, 
                [int(normalAttackNextScale.x), int(normalAttackNextScale.y)])
            self.screen.blit(normalAttackPicture, self.normalAttackNextPos)

    #HP変動
    def CalcHP(self):
        self.damage = 10
        self.hpPicture = self.Character.HPbarPicture
        self.hp = self.Character.hp

        self.hp -= self.damage
        self.Character.hp = self.hp
        self.hpMoveSpeed = -self.damage / self.moveHpTime
        self.hpBarSize = list(self.hpPicture.get_size())
    def MoveHPAnime(self):
        deltatime = self.Helper.pygamedeltatime
        self.hpBarSize[0] += self.hpMoveSpeed * deltatime
        self.hpPicture = pygame.transform.scale(
            self.hpPicture, 
            [int(i) for i in self.hpBarSize])
        self.Character.HPbarPicture = self.hpPicture
    def MoveHPEnd(self):
        if self.hp >= self.hpBarSize[0]:
            self.damage = 0
            self.IsEndOfAnimation = True

    #ノーマル攻撃エフェクト
    def LoadMaterial(self):
        self.normalAttackPicture = BattleHelper.ScaledPicture(
            self.normalAttackPicturePath, 
            [int(self.normalAttackScale.x), int(self.normalAttackScale.y)])

        #ノーマルエフェクト　ver2
        self.NormalAttackPicture = BattleHelper.ScaledPicture(
            self.normalAttackPicturePath,
            [int(self.normalAttackScale.x), int(self.normalAttackScale.y)]
            )

class OneSurfaceAnimation(BaseBattle.OneSurfaceAnimation):
    def __init__(self, MainClass, surface, **kwargs):
        super().__init__(MainClass, surface, kwargs)

class BattleCharacterMenu(BaseBattle.BattleCharacterMenu):
    def __init__(self, MainClass, **kwargs):
        super().__init__(MainClass, kwargs)
#====================実行部分=================
MainClass().Main()