
import OneCmdAnim1 as OldOneCmdAnim

class OneCmdAnim(OldOneCmdAnim.OneCmdAnim):
    def __init__(self, name, ObjectClass, kwargs):
        self.GetSource(ObjectClass)
        self.SetOptions(kwargs)
        self.ProgramParameter()

        self.SetAnimationList(name)

    def SetOptions(self, kwargs):
        self.options = {
            "StartMoveCondition" : lambda : True,
            "StartFunc" : None,
            "EndFunc" : None
            }
        if kwargs != None:
            self.options.update(kwargs)

    def ProgramParameter(self):
        self.StartMoveCondition = self.options["StartMoveCondition"]
        self.StartFunc = self.options["StartFunc"]
        self.EndFunc = self.options["EndFunc"]
        self.Action = None
        self.UpdateWithPlayStart = self.PlayWithFirstUsed

    def Start(self):
        if self.StartMoveCondition():
            self.Action = self.UpdateWithPlayStart
            #self.Action = self.Update

    def Update(self):
        self.PlayPieceAnim()
        if self.EndCondition():
            self.Action = self.End
    def PlayWithFirstUsed(self):
        self.PlayPieceAnim()
        self.UpdateWithPlayStart = self.PlayWithAfterUsed
        self.Action = self.Update
        if self.StartFunc != None:
            self.StartFunc()
    def PlayWithAfterUsed(self):
        self.PlayPieceAnim()
        self.Action = self.Update
        if self.StartFunc != None:
            self.StartFunc()

    def End(self):
        self.Action = None
        if self.EndFunc != None:
            self.EndFunc()