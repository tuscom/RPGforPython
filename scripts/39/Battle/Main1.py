"""
SubX1を要求
"""

import pygame
from pygame.locals import *
import sys

import Helper
from Helper import BattleHelper

import SubX1 as Sub

class MainClass:
    def __init__(self):
        self.windowSize = [1500, 800]
        self.squareSize = 32
        self.windowName = "Battle"

        pygame.init()
        self.screen = pygame.display.set_mode(self.windowSize)
        pygame.display.set_caption(self.windowName)

        self.Action = None

        #フィールド
        self.bgPicturePath = "../../../pictures/keimusyo_niwa001.jpg"
        self.charaSize = [250, 250]
        self.familyPos = pygame.math.Vector2(900, 100)
        self.enemyPos = pygame.math.Vector2(350, self.familyPos.y)

        #キャラコントローラーパネル
        self.charaControllerLayout = [0, 0.8, 1, 0.2]
        self.attackBtnLayout = pygame.math.Vector2(0.8, 0.7)
        self.attackBtnScale = pygame.math.Vector2(200, 200)
        self.attackBtnPicturePath = "../../../pictures/attackButton.png"
        self.charaControllerPanelPicturePath = "../../../pictures/normalPanel.png"

        #派生実装
        if __name__ == "__main__":
            self.BattleHelper = BattleHelper
            self.IconCharacterClass = Sub.IconCharacterClass
            self.FieldCharacterClass = Sub.FieldCharacterClass
            self.FieldEnemyClass = Sub.FieldEnemyClass
            self.ObjectClass = Sub.Sub.ObjectClass

            self.Helper = self.BattleHelper(self)
        self.Sub = Sub

    def Main(self):
        #変数セット
        self.Action = self.Start

        while True:
            self.Helper.EarlyUpdate()

            if self.Action != None:
                self.Action()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

    def Start(self):
        self.LoadMaterial()
        self.SetFieldCharacter()
        self.SetPanel()
        self.Action = self.Update
    def LoadMaterial(self):
        self.backGroundPicture = self.BattleHelper.ScaledPicture(self.bgPicturePath, size=self.windowSize)
    def SetPanel(self):
        charaControllerRect = self.Helper.NormToWorldRect(self.charaControllerLayout)
        kwargs = {
            "position" : pygame.math.Vector2(charaControllerRect[0], charaControllerRect[1]),
            "scale" : pygame.math.Vector2(charaControllerRect[2], charaControllerRect[3]),
            "picturepath" : self.charaControllerPanelPicturePath
            }
        self.charaControllerPanel = self.ObjectClass(self, kwargs)

        self.familyIcons = []
        for i in range(len(self.family)):
            self.familyIcons.append(self.IconCharacterClass(self, self.family[i], None))
            self.familyIcons[-1].position = pygame.math.Vector2(
                i * charaControllerRect[3],
                charaControllerRect[1]
                )

        #攻撃ボタン
        attackBtnPos = self.Helper.NormToWorldPos(self.attackBtnLayout)
        kwargs = {
            "picturepath" : self.attackBtnPicturePath,
            "position" : attackBtnPos,
            "scale" : self.attackBtnScale
            }
        self.attackBtn = self.ObjectClass(self, kwargs)

    def SetFieldCharacter(self):
        familyPictures = [
            "../../../pictures/9c338508771fd401ada29fba07b34ebf.png",
            "../../../pictures/ahobakaizer.png",
            "../../../pictures/9c338508771fd401ada29fba07b34ebf.png"
            ]
        enemyPictures = [
            "../../../pictures/igyo-yousei01.png",
            "../../../pictures/igyo-yousei01.png",
            "../../../pictures/igyo-boushi01.png"
            ]
        self.family = []
        for i in range(len(familyPictures)):
            kwargs = {
                "name" : str(i),
                "picturepath" : familyPictures[i],
                "scale" : self.charaSize,
                "speed" : i+5
                }
            self.family.append(
                self.FieldCharacterClass(self, kwargs)
                )
            self.family[-1].position = self.familyPos + i*pygame.math.Vector2(120, 120)

        self.enemies = []
        for i in range(len(enemyPictures)):
            kwargs = {
                "name" : str(i),
                "picturepath" : enemyPictures[i],
                "scale" : self.charaSize,
                "speed" : i+5
                }
            self.enemies.append(
                self.FieldEnemyClass(self, kwargs)
                )
            self.enemies[-1].position = self.enemyPos + i * pygame.math.Vector2(-140, 120)
    def Update(self):
        self.DrawBackGround()
        self.DrawFieldCharacter()
        self.DrawPanel()
    def DrawBackGround(self):
        #背景描画
        self.screen.blit(self.backGroundPicture, (0, 0))
    def DrawPanel(self):
        self.charaControllerPanel.Main()
        list(map(lambda icon:icon.Main(), self.familyIcons))
        self.attackBtn.Main()
    def DrawFieldCharacter(self):
        list(map(lambda family : family.Main(), self.family))
        list(map(lambda enemy : enemy.Main(), self.enemies))

if __name__ == "__main__":
    MainClass().Main()
