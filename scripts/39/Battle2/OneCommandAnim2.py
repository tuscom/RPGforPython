import OneCommandAnim1

class OneCommandAnim(OneCommandAnim1.OneCommandAnim): 
    def __init__(self, name, ObjectClass, kwargs):
        self.ObjectClass = ObjectClass
        self.PieceAnimation = ObjectClass.MainClass.PieceAnimation

        self.SetOptions(kwargs)

        self.PieceAnimationList = None

        self.Action = None

        self.SelectAnimation(name)

    def SetOptions(self, kwargs):
        self.options = {
            "StartFunc" : None,
            "UpdateFunc" : None,
            "EndFunc" : None}
        if kwargs != None:
            self.options.update(kwargs)
        self.StartFunc = self.options["StartFunc"]
        self.UpdateFunc = self.options["UpdateFunc"]
        self.EndFunc = self.options["EndFunc"]

    def SelectAnimation(self, name):
        self.indexDict = {
            "leftAttackStep" : self.LeftAttackStep,
            "rightAttackStep" : self.RightAttackStep,
            "jump" : self.Jump,
            "mudaniHustle" : self.MudaniHustle,
            "ShowBattleMenu" : self.ShowBattleMenu}

        self.indexDict[name]()

    #バトルメニュー表示
    def ShowBattleMenu(self):
        self.PieceAnimationList = [
            self.PieceAnimation("ShowBattleMenu", self.ObjectClass, None)
            ]

    #左ステップアタック
    def LeftAttackStep(self):
        self.PieceAnimationList = [
            self.PieceAnimation("leftStep", self.ObjectClass, None),
            self.PieceAnimation("HPmoveForAttack", self.ObjectClass, None),
            self.PieceAnimation("NormalAttackEffect", self.ObjectClass, None)
            ]

    #右ステップアタック
    def RightAttackStep(self):
        self.PieceAnimationList = [
            self.PieceAnimation("rightStep", self.ObjectClass, None),
            self.PieceAnimation("HPmoveForAttack", self.ObjectClass, None),
            self.PieceAnimation("NormalAttackEffect", self.ObjectClass, None)
            ]

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

    def End(self):
        super().End()
        if self.EndFunc != None:
            self.EndFunc()

