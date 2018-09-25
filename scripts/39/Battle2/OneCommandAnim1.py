class OneCommandAnim: #まとめて一つとするアニメーション
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

        self.Action = None

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
        if self.EndCondition():
            self.Action = self.End

    def End(self):
        self.Action = None

    def IsEndOfAnimation(self):
        return self.Action == None

    def EndCondition(self):
        boolList = list(map(lambda pieceAnim : pieceAnim.IsEndOfAnimation(), self.PieceAnimationList))
        return all(boolList)

    def PlayON(self):
        if self.IsEndOfAnimation():
            self.Action = self.Start
            list(map(lambda pieceAnim : pieceAnim.PlayON(), self.PieceAnimationList))

