"""
AfterUsedとFirstUsedは一緒に実行されない。
"""

import OneCmdAnim2 as OldOneCmdAnim

class OneCmdAnim(OldOneCmdAnim.OneCmdAnim):
    def __init__(self, name, ObjectClass, kwargs):
        self.GetSource(ObjectClass)
        self.SetOptions(kwargs)
        self.ProgramParameter()
        self.SetContinueFunc()

        self.SetAnimationList(name)

    def ProgramParameter(self):
        self.StartMoveCondition = self.options["StartMoveCondition"]
        self.Action = None
        self.UpdateWithPlayStart = self.PlayWithFirstUsed
        self.StartFuncList = []
        self.StartFuncList.append(self.options["StartFunc"])
        self.EndFuncList = []
        self.EndFuncList.append(self.options["EndFunc"])
        self.SkipCondition = self.options["SkipCondition"]

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

    def Start(self):
        if self.StartMoveCondition():
            self.Action = self.UpdateWithPlayStart

    def Update(self):
        self.PlayPieceAnim()
        if self.EndCondition():
            self.Action = self.End

    def PlayWithFirstUsed(self):
        list(map(lambda func : func() if func != None else None, self.StartFuncList))
        self.PlayPieceAnim()
        self.UpdateWithPlayStart = self.PlayWithAfterUsed
        self.Action = self.Update
    def PlayWithAfterUsed(self):
        list(map(lambda func : func() if func != None else None, self.StartFuncList))
        self.PlayPieceAnim()
        self.Action = self.Update

    def End(self):
        list(map(lambda func : func() if func != None else None, self.EndFuncList))
        self.Action = None
