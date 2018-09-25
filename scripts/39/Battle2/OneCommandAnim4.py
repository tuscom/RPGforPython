import OneCommandAnim3

class OneCommandAnim(OneCommandAnim3.OneCommandAnim): 
    def __init__(self, name, ObjectClass, kwargs):
        self.ObjectClass = ObjectClass
        self.PieceAnimation = ObjectClass.MainClass.PieceAnimation
        
        self.SetOptions(kwargs)
        self.SelectAnimation(name)
        self.PieceAnimationList = None
        self.Action = None


    def SetOptions(self, kwargs):
        self.options = {
            "PlayCondition" : None,
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


    def Start(self):
        if self.StartFunc != None:
            self.StartFunc()

        self.SendLogMessage()
        self.Action = self.Update

    def SendLogMessage(self):
        pass

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

    #================= Play Condition ================
    def NowPlayCondition(self):
        return True

