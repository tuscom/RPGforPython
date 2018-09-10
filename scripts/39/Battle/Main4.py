"""
Sub = Sub3
SubX = SubX4
SubXX = SubXX1

コードの書き方
１．同じ系列のファイルであれば、飛んで継承することもOK 
２．Start、Update、__init__は必ずOverrideする。
３．Subシリーズには最低限要求するSub下位シリーズ番号を記述する
４．下位シリーズのimportはバージョン管理のため、Source.pyからとする。

メモ
要らない継承を防ぐにはOverride
基本全てのファイルは下位versionを継承しているので最下層のimportをSourceで管理するのは意味がある。
ただし、SubシリーズとMain系で必要とする下位シリーズが異なる可能性があるので上手くSourceで調整する
"""

from Helper import BattleHelper

from Source import Sub
from Source import SubX
from Source import SubXX
import Main3 as MainModule

class MainClass(MainModule.MainClass):
    def __init__(self):
        super().__init__()

        if __name__ == "__main__":
            self.BattleHelper = BattleHelper
            self.IconCharacterClass = SubX.IconCharacterClass
            self.FieldCharacterClass = SubXX.FieldFamilyClass
            self.FieldEnemyClass = SubXX.FieldEnemyClass
            self.ObjectClass = Sub.ObjectClass

            self.AllAnimationController = Sub.AllAnimationController
            self.ContinueAnimation = Sub.ContinueAnimation
            self.OneCommandAnimation = Sub.OneCommandAnimation
            self.PieceAnimation = Sub.PieceAnimation

            self.Helper = self.BattleHelper(self)

    def Start(self):
        super().Start()
        self.SetAttackBtn()

    def Update(self):
        self.DrawBackGround()
        self.MainOfAllObjects()
        self.AnimationUpdate()

if __name__ == "__main__":
    MainClass().Main()
