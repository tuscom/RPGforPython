import sys

import Helper
from Helper import BattleHelper

import Base2 as Base

class ObjectClass(Base.ObjectClass):
    def __init__(self, MainClass, kwargs):
        super().__init__(MainClass, kwargs)

        self.MainClass.AllObjectList.append(self)
        self.Action = self.Update

    def Update(self):
        self.HelperUpdate()

        self.Draw()
        self.BtnUpdate()

    def HelperUpdate(self):
        self.BtnAction.mousePos = self.Helper.mousePos
        self.BtnAction.mousePressed = self.Helper.mousePressed
        self.BtnAction.previousPressed = self.Helper.previousPressed

    def AnimationUpdate(self):
        if self.Animation != None:
            self.Animation()

