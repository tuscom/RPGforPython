from Source import PieceAnimation

class OneCmdAnim:
    def __init__(self, name, ObjectClass, kwargs):
        self.GetSource(ObjectClass)
        self.SetOptions(kwargs)
        self.ProgramParameter()

        self.SetAnimationList(name)

    def GetSource(self, ObjectClass):
        self.ObjectClass = ObjectClass
        self.MainClass = ObjectClass.MainClass
        self.PieceAnimDic = self.MainClass.AllAnimationController.PieceAnimDic
        self.CmdAnimNameDic = self.MainClass.AllAnimationController.CmdAnimNameDic
    def SetOptions(self, kwargs):
        self.options = {
            "StartMoveCondition" : lambda : True
            }
        if kwargs != None:
            self.options.update(kwargs)
    def ProgramParameter(self):
        self.StartMoveCondition = self.options["StartMoveCondition"]
        self.Action = None

    def SetAnimationList(self, name):
        PieceAnimNameList = self.CmdAnimNameDic[name]
        self.PieceAnimList = [PieceAnimation(name, self.ObjectClass) for name in PieceAnimNameList]

    #Main
    def Main(self):
        if self.Action != None:
            self.Action()
    #Start
    def Start(self):
        if self.StartMoveCondition():
            self.Action = self.Update

    #Update
    def Update(self):
        self.PlayPieceAnim()
        if self.EndCondition():
            self.Action = self.End

    def PlayPieceAnim(self):
        list(map(lambda pieceAnim : pieceAnim.Main(), self.PieceAnimList))

    #End
    def End(self):
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
