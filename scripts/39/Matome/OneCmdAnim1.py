
class OneCmdAnim:
    def __init__(self, name, ObjectClass, kwargs):
        self.GetSource(ObjectClass)
        self.SetOptions(kwargs)
        self.ProgramParameter()
        self.SetContinueFunc()

        self.SetAnimationList(name)

    def GetSource(self, ObjectClass):
        self.ObjectClass = ObjectClass
        self.MainClass = ObjectClass.MainClass
        self.PieceAnimDic = self.MainClass.AllAnimationController.PieceAnimDic
        self.CmdAnimNameDic = self.MainClass.AllAnimationController.CmdAnimNameDic
        self.PieceAnimation = self.MainClass.PieceAnimation

    def SetAnimationList(self, name):
        PieceAnimNameList = self.CmdAnimNameDic[name]
        self.PieceAnimList = [PieceAnimation(name, self.ObjectClass) for name in PieceAnimNameList]

    def SetOptions(self, kwargs):
        self.options = {
            "StartMoveCondition" : lambda : True,
            "StartFunc" : None,
            "EndFunc" : None,
            "ContinueName" : None,
            "SkipCondition" : lambda : False
            }
        if kwargs != None:
            self.options.update(kwargs)

    def ProgramParameter(self):
        self.StartMoveCondition = self.options["StartMoveCondition"]
        self.Action = None
        self.UpdateWithPlayStart = self.PlayWithFirstUsed
        self.StartFuncList = []
        self.StartFuncList.append(self.options["StartFunc"])
        self.EndFuncList = []
        self.EndFuncList.append(self.options["EndFunc"])
        self.SkipCondition = self.options["SkipCondition"]

    def SetContinueFunc(self):
        self.ContinueStartFuncDic = {
            "battle" : [lambda : self.ObjectClass.AdjustSelectAttackTarget()]
            }

        self.ContinueEndFuncDic = {}

        try:
            self.StartFuncList += self.ContinueStartFuncDic[self.options["ContinueName"]]
        except KeyError:
            pass

        try:
            self.EndFuncList += self.ContinueEndFuncDic[self.options["ContinueName"]]
        except KeyError:
            pass


    def SetAnimationList(self, name):
        PieceAnimNameList = self.CmdAnimNameDic[name]
        self.PieceAnimList = [self.PieceAnimation(name, self.ObjectClass, self) for name in PieceAnimNameList]
        CmdAnimKwargs = self.MainClass.AllAnimationController.CmdAnimKwargs
        try:
            kwargs = CmdAnimKwargs[name]
            if kwargs != None:
                self.options.update(kwargs)
        except KeyError:
            pass

    #Main
    def Main(self):
        if self.Action != None:
            self.Action()
    #Start
    def Start(self):
        if self.StartMoveCondition():
            self.Action = self.UpdateWithPlayStart

    #Update
    def Update(self):
        self.PlayPieceAnim()
        if self.EndCondition():
            self.Action = self.End

    def PlayPieceAnim(self):
        list(map(lambda pieceAnim : pieceAnim.Main(), self.PieceAnimList))

    def PlayWithFirstUsed(self):
        list(map(lambda func : func() if func != None else None, self.StartFuncList))
        self.PlayPieceAnim()
        self.UpdateWithPlayStart = self.PlayWithAfterUsed
        self.Action = self.Update
    def PlayWithAfterUsed(self):
        list(map(lambda func : func() if func != None else None, self.StartFuncList))
        self.PlayPieceAnim()
        self.Action = self.Update


    #End
    def End(self):
        list(map(lambda func : func() if func != None else None, self.EndFuncList))
        self.Action = None

    #Others
    def IsEndOfAnimation(self):
        return self.Action == None

    def EndCondition(self):
        boolList = list(map(lambda pieceAnim : pieceAnim.IsEndOfAnimation(), self.PieceAnimList))
        return all(boolList)

    def PlayON(self):
        if self.IsEndOfAnimation():
            self.Action = self.Start
            list(map(lambda pieceAnim : pieceAnim.PlayON(), self.PieceAnimList))
