import IconCharacter4

class IconCharacter(IconCharacter4.IconCharacter):
    def __init__(self, MainClass, CharaClass, kwargs):
        self.MainClass = MainClass
        self.BattleHelper = MainClass.BattleHelper
        self.Helper = MainClass.Helper
        self.screen = MainClass.screen
        self.CharaClass = CharaClass
        self.OneCommandAnimation = MainClass.OneCommandAnimation

        self.SetOptions(kwargs)
        self.SetParameter()
        self.SetButton()
        self.OnInstanceFunc()
        self.SetAction()

    def Start(self):
        self.LoadMaterial()
        self.Action = self.Update

        self.SetScale()
        self.SetHPbar()
        self.SetHPbarPosition()
        self.SetbgPicture()
        self.SetCharacterPicture()
        self.ReflectToCharaClass()
        self.SetBattleMenu()
        self.SetAnimationCommand()

    def Update(self):
        self.HelperUpdate()

        self.Draw()
        self.DrawBattleMenu()
        self.BtnUpdate()

    def OnClick(self):
        super().OnClick()
        self.MainClass.SelectedEnemy = self.CharaClass.AttackTarget
        self.MainClass.SelectedFamily = self.CharaClass
