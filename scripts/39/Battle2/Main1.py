"""
まだ短くてもセーブポイントで余計な更新がされないようファイルを区切る
Startは初めにFirstUsedStartを入れるようにする。あとはAfterStartを代入する

機能
基本レイアウト描画

要求version
ObjectClass    : 1
FieldCharacter : 1
FieldEnemy     : 1
FieldFamily    : 1
IconCharacter  : 1
"""

import pygame
from pygame.locals import *
import sys

from Source import *

class MainClass:
    def __init__(self):
        self.WindowParameter()
        self.FieldParameter()
        self.ControllerPanelParameter()
        self.ProgramParameter()
        self.GetSource()

        self.SetWindow()

    def GetSource(self):
        self.Helper = BattleHelper(self)
        self.BattleHelper = BattleHelper
        self.HelperModule = Helper
        self.ObjectClass = ObjectClass
        self.OneCmdAnim = OneCmdAnim
        self.FieldEnemy = FieldEnemy
        self.FieldFamily = FieldFamily

    def WindowParameter(self):
        self.windowSize = [1500, 800]
        self.squareSize = 32
        self.windowName = "Battle"
        self.screen = pygame.display.set_mode(self.windowSize)
    def FieldParameter(self):
        self.bgPicturePath = "../../../pictures/keimusyo_niwa001.jpg"
        self.charaSize = [250, 250]
        self.familyPos = pygame.math.Vector2(900, 100)
        self.enemyPos = pygame.math.Vector2(350, self.familyPos.y)
    def ControllerPanelParameter(self):
        self.charaControllerLayout = [0, 0.8, 1, 0.2]
        self.attackBtnLayout = pygame.math.Vector2(0.8, 0.7)
        self.attackBtnScale = pygame.math.Vector2(200, 200)
        self.attackBtnPicturePath = "../../../pictures/attackButton.png"
        self.charaControllerPanelPicturePath = "../../../pictures/normalPanel.png"
    def ProgramParameter(self):
        self.Action = None
        self.AllObjects = []
    def SetWindow(self):
        pygame.init()
        pygame.display.set_caption(self.windowName)

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

            self.Helper.LateUpdate()

            pygame.display.update()

    def Start(self):
        self.LoadMaterial()
        self.SetFieldCharacter()
        self.SetPanel()
        self.Action = self.Update
    def LoadMaterial(self):
        self.backGroundPicture = BattleHelper.ScaledPicture(self.bgPicturePath, size=self.windowSize)
    def SetPanel(self):
        charaControllerRect = self.Helper.NormToWorldRect(self.charaControllerLayout)
        kwargs = {
            "position" : pygame.math.Vector2(charaControllerRect[0], charaControllerRect[1]),
            "scale" : pygame.math.Vector2(charaControllerRect[2], charaControllerRect[3]),
            "picturepath" : self.charaControllerPanelPicturePath
            }
        self.charaControllerPanel = ObjectClass(self, kwargs)

        self.familyIcons = []
        for i in range(len(self.family)):
            self.familyIcons.append(IconCharacter(self, self.family[i], None))
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
        self.attackBtn = ObjectClass(self, kwargs)

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
                FieldFamily(self, kwargs)
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
                FieldEnemy(self, kwargs)
                )
            self.enemies[-1].position = self.enemyPos + i * pygame.math.Vector2(-140, 120)
    def Update(self):
        self.DrawBackGround()
        self.MainAllObjects()

    def MainAllObjects(self):
        list(map(lambda ObjectClass : ObjectClass.Main(), self.AllObjects))

    def DrawBackGround(self):
        self.screen.blit(self.backGroundPicture, (0, 0))

if __name__ == "__main__":
    MainClass().Main()
