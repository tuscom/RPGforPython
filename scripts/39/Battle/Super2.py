"""
アニメーションの構造
Base2を要求
"""
import pygame
from pygame.locals import *
import sys

import Helper
from Helper import BattleHelper

import Super1 as Super

class MainClass(Super.MainClass):
    def __init__(self):
        super().__init__()

        if __name__ == "__main__":
            self.BattleHelper = BattleHelper
            self.IconCharacterClass = IconCharacterClass
            self.FieldCharacterClass = FieldCharacterClass
            self.FieldEnemyClass = FieldEnemyClass

            self.AllAnimationController = AllAnimationController
            self.ContinueAnimation = ContinueAnimation
            self.OneCommandAnimation = OneCommandAnimation
            self.PieceAnimation = PieceAnimation

            self.Helper = self.BattleHelper(self)

    def Main(self):
        #変数セット
        self.Action = self.Start

        while True:
            self.Helper.EarlyUpdate()

            if self.Action != None:
                self.Action()

            self.Helper.LateUpdate()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

    def Start(self):
        super().Start()
        self.SetAnimation()

    def SetAnimation(self):
        testAnimTarget = self.family + self.enemies
        testComAnimList = [target.CommandAnimationDic["mudaniHustle"] for target in testAnimTarget]
        kwargs = {
            "isRepeat" : True
            }
        testContiAnim = self.ContinueAnimation(testComAnimList, kwargs)
        testContiAnimList = [testContiAnim]

        self.AnimationController = self.AllAnimationController(testContiAnimList)

    def Update(self):
        super().Update()
        self.AnimationUpdate()

    def AnimationUpdate(self):
        self.AnimationController.Main()


class IconCharacterClass(Super.IconCharacterClass):
    def __init__(self, MainClass, Character, kwargs):
        super().__init__(MainClass, Character, kwargs)

    def SetHPbar(self):
        super().SetHPbar()
        self.CharaClass.IconClass = self
        self.CharaClass.HPbarPicture = self.HPbarPicture

class FieldCharacterClass(Super.FieldCharacterClass):
    def __init__(self, MainClass, kwargs):
        super().__init__(MainClass, kwargs)

        self.options.update({
            "hp" : 100
            })

        self.hp = self.options["hp"]
        self.HPbarPicture = None
        self.IconClass = None

        self.CommandAnimationDic = {
            "jump" : self.OneCommandAnimation("jump", self, None),
            "mudaniHustle" : self.OneCommandAnimation("mudaniHustle", self, None)
            }

    def Update(self):
        super().Update()
        self.ReflectHPbarPicture()

    def ReflectHPbarPicture(self):
        self.IconClass.HPbarPicture = self.HPbarPicture

class FieldEnemyClass(Super.FieldEnemyClass):
    def __init__(self, MainClass, kwargs):
        super().__init__(MainClass, kwargs)

        self.options.update({
            "hp" : 100
            })

        self.hp = self.options["hp"]

        self.CommandAnimationDic = {
            "jump" : self.OneCommandAnimation("jump", self, None),
            "mudaniHustle" : self.OneCommandAnimation("mudaniHustle", self, None)
            }

class AllAnimationController:
    def __init__(self, ContiAnimList):
        self.ContiAnimList = ContiAnimList
        self.Action = self.Start

    def Main(self):
        if self.Action != None:
            self.Action()

    def Start(self):
        self.Action = self.Update

    def Update(self):
        list(map(lambda contiAnim : contiAnim.Main(), self.ContiAnimList))

class ContinueAnimation: #時間的に連続するアニメーション
    def __init__(self, CommandAnimationList, kwargs):
        self.Action = self.Start
        self.options = {"isRepeat" : False}
        if kwargs != None:
            self.options.update(kwargs)
        self.UpdateFunc = self.RepeatUpdate if self.options["isRepeat"] else self.AutoEndUpdate

        self.CommandAnimationList = CommandAnimationList
        self.indexOfAnimation = 0

    def Main(self):
        if self.Action != None:
            self.Action()

    def Start(self):
        self.noOfComAnim = len(self.CommandAnimationList)
        self.Action = self.Update

    def Update(self):
        self.UpdateFunc()

    def RepeatUpdate(self):
        comAnim = self.CommandAnimationList[self.indexOfAnimation]

        comAnim.Main()
        if comAnim.IsEndOfAnimation():
            self.indexOfAnimation += 1
            self.indexOfAnimation %= self.noOfComAnim

            if self.indexOfAnimation == 0:
                self.PlayON()

    def AutoEndUpdate(self):
        comAnim = self.CommandAnimationList[self.indexOfAnimation]

        comAnim.Main()
        if comAnim.IsEndOfAnimation():
            self.indexOfAnimation += 1

            if self.indexOfAnimation % self.noOfComAnim == 0:
                self.Action = None

    def PlayON(self):
        list(map(lambda comAnim : comAnim.PlayON(), self.CommandAnimationList))

class OneCommandAnimation: #まとめて一つとするアニメーション
    def __init__(self, name, ObjectClass, kwargs):
        self.ObjectClass = ObjectClass
        self.PieceAnimation = ObjectClass.MainClass.PieceAnimation
        self.options = {
            "StartFunc" : None,
            "UpdateFunc" : None,
            "EndFunc" : None}
        if kwargs != None:
            self.options.update(kwargs)
        self.StartFunc = self.options["StartFunc"]
        self.UpdateFunc = self.options["UpdateFunc"]
        self.EndFunc = self.options["EndFunc"]

        self.PieceAnimationList = None

        self.Action = self.Start

        #============= 選べるアニメーション ==========
        self.indexDict = {
            "leftAttackStep" : self.LeftAttackStep,
            "jump" : self.Jump,
            "mudaniHustle" : self.MudaniHustle}

        self.indexDict[name]()

    #左ステップアタック
    def LeftAttackStep(self):
        self.PieceAnimationList = [
            self.PieceAnimation("leftStep", self.ObjectClass, None)
            ]

    #ジャンプ
    def Jump(self):
        self.PieceAnimationList = [
            self.PieceAnimation("jump", self.ObjectClass, None)
            ]

    #無駄にハッスル
    def MudaniHustle(self):
        self.PieceAnimationList = {
            self.PieceAnimation("jump", self.ObjectClass, None),
            self.PieceAnimation("HPmove", self.ObjectClass, None)
            }

    def Main(self):
        if self.Action != None:
            self.Action()

    def Start(self):
        if self.StartFunc != None:
            self.StartFunc()

        self.Action = self.Update

    def Update(self):
        if self.UpdateFunc != None:
            self.UpdateFunc()
        list(map(lambda pieceAnime : pieceAnime.Main(), self.PieceAnimationList))
        if self.IsEndOfAnimation():
            self.Action = self.End

    def End(self):
        self.Action = None

    def IsEndOfAnimation(self):
        boolList = list(map(lambda pieceAnime : pieceAnime.isEndOfAnimation, self.PieceAnimationList))
        return all(boolList)

    def PlayON(self):
        if self.Action == None:
            self.Action = self.Start
        list(map(lambda pieceAnim : pieceAnim.PlayON(), self.PieceAnimationList))

class PieceAnimation:
    def __init__(self, name, ObjectClass, kwargs): #Animationの最小単位
        self.ObjectClass = ObjectClass
        self.MainClass = ObjectClass.MainClass
        self.Helper = self.MainClass.Helper
        self.options = {}
        if kwargs != None:
            self.options.update(kwargs)

        self.isEndOfAnimation = False
        self.StartFunc = None
        self.UpdateFunc = None
        self.clock = 0

        self.delayTime = 0

        self.Action = self.Start

        #================= カスタマイズ可能なアニメーション =============
        self.indexDic = {
            "leftStep" : self.LeftStep,
            "jump" : self.Jump,
            "HPmove" : self.HPmove}

        self.indexDic[name]()

    #左ステップ
    def LeftStep(self):
        self.endTime = 1
        self.width = 100
        self.StartFunc = self.LeftStepStart
        self.UpdateFunc = self.LeftStepUpdate
    def LeftStepStart(self):
        pass
    def LeftStepUpdate(self):
        pass

    #ジャンプ
    def Jump(self):
        self.endTime = 1
        self.height = 100

        self.StartFunc = self.JumpStart
        self.UpdateFunc = self.JumpUpdate
    def JumpStart(self):
        self.firstPosition = self.ObjectClass.position
    def JumpUpdate(self):
        y = -(self.clock - self.endTime/2)**2 * (4*self.endTime*self.height) + self.height
        y = self.firstPosition.y - y #y軸が逆向き

        position = pygame.math.Vector2(self.firstPosition.x, y)
        self.ObjectClass.position = pygame.math.Vector2(position)

    #HP変動
    def HPmove(self):
        self.endTime = 0.5
        self.delayTime = 0.5
        self.StartFunc = self.HPmoveStart
        self.UpdateFunc = self.HPmoveUpdate
    def HPmoveStart(self):
        damage=10
        self.HPbarPicture = self.ObjectClass.HPbarPicture
        self.pictureScale = self.HPbarPicture.get_size()
        pictureScaleRatio = self.pictureScale[0] / self.ObjectClass.hp
        self.speed = damage * pictureScaleRatio / self.endTime
        self.ObjectClass.hp -= damage
    def HPmoveUpdate(self):
        clock = self.clock - self.delayTime
        pictureScale = (
            self.pictureScale[0]-self.speed*clock,
            self.pictureScale[1])
        self.ObjectClass.HPbarPicture = pygame.transform.scale(
            self.HPbarPicture,
            [int(pictureScale[0]), int(pictureScale[1])]
            )

    def Main(self):
        self.clock += self.Helper.pygamedeltatime
        if self.Action != None:
            self.Action()

    def Start(self):

        if self.clock >= self.delayTime:
            self.isEndOfAnimation = False

            if self.StartFunc != None:
                self.StartFunc()

            self.Action = self.Update

    def Update(self):
        if self.UpdateFunc != None:
            self.UpdateFunc()

        if self.clock >= self.endTime + self.delayTime:
            self.Action = self.End

    def End(self):
        self.clock = 0
        self.isEndOfAnimation = True
        self.Action = None

    def PlayON(self):
        if self.Action == None:
            self.Action = self.Start


if __name__ == "__main__":
    MainClass().Main()
