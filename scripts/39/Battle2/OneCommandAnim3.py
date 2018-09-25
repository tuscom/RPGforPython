import OneCommandAnim2

class OneCommandAnim(OneCommandAnim2.OneCommandAnim): 
    def __init__(self, name, ObjectClass, kwargs):
        self.ObjectClass = ObjectClass
        self.PieceAnimation = ObjectClass.MainClass.PieceAnimation

        self.SetOptions(kwargs)

        self.PieceAnimationList = None

        self.Action = None

        self.SelectAnimation(name)

    def Start(self):
        if self.StartFunc != None:
            self.StartFunc()

        self.Action = self.Update

    def Update(self):
        if self.UpdateFunc != None:
            self.UpdateFunc()
        list(map(lambda pieceAnime : pieceAnime.Main(), self.PieceAnimationList))
        if self.EndCondition():
            self.Action = self.End

    def SelectAnimation(self, name):
        self.indexDict = {
            "leftAttackStep" : self.LeftAttackStep,
            "rightAttackStep" : self.RightAttackStep,
            "jump" : self.Jump,
            "mudaniHustle" : self.MudaniHustle,
            "ShowBattleMenu" : self.ShowBattleMenu,
            "BackBattleMenu" : self.BackBattleMenu,
            "explosion" : self.Explosion}

        self.indexDict[name]()

    #バトルメニュー戻し
    def BackBattleMenu(self):
        self.PieceAnimationList = [
            self.PieceAnimation("BackBattleMenu", self.ObjectClass, None)
            ]

    #爆破
    def Explosion(self):
        self.PieceAnimationList = [
            self.PieceAnimation("explosion", self.ObjectClass, None)
            ]

