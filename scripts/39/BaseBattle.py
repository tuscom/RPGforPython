import pygame
from pygame.locals import *
import sys

from Helper import BattleHelper
import Helper

#戦闘シーン
class MainClass:
    def __init__(self):
        self.windowSize = [1500, 800]
        self.pageColor = (255,255,255)
        self.squareSize = 32
        self.windowName = "Battle"

        pygame.init()
        self.screen = pygame.display.set_mode(self.windowSize)
        pygame.display.set_caption(self.windowName)

        self.Action = None

        #フィールド
        self.SelectedEnemy = None
        self.SelectedFamily = None

        #派生実装
        self.Helper = None

        #アニメーション
        self.AnimationController = None

    def Main(self):
        #変数セット
        self.Action = self.Start

        while True:
            self.screen.fill(self.pageColor)
            self.Helper.EarlyUpdate()

            if self.Action != None:
                self.Action()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

    #================== Start ==================
    def Start(self):
        self.LoadScene()
        self.SetFieldCharacter()
        self.SetAnimations()
        self.SetPanel()
        self.Action = self.Update

    def LoadScene(self):
        pass
    def SetFieldCharacter(self):
        pass
    def SetAnimations(self):
        pass
    def SetPanel(self):
        pass

    #================ Update =================
    def Update(self):
        self.DrawBackGround()
        self.DrawCharacter()
        self.DrawAnimations()
        self.DrawPanel()
        self.DrawTargetIcon()

        if self.AnimationController != None:
            self.AnimationController()

    def DrawPanel(self):
        pass
    def DrawBackGround(self):
        pass
    def DrawCharacter(self):
        pass
    def DrawAnimations(self):
        pass
    def DrawTargetIcon(self):
        pass

    #================ Button ===============
    def AttackOnClick(self):
        self.SetAttackAnimation()
        self.AllBattleMenuOff()
        self.SelectedEnemy = None
        self.SelectedFamily = None
    def AllBattleMenuOff(self):
        pass
    def SetAttackAnimation(self):
        pass

    #=============== Animation ==============
    def AttackAnimation(self):
        pass

class ObjectClass:
    def __init__(self, MainClass, kwargs):
        self.MainClass = MainClass
        self.options = {"name" : "名無し",
                        "picturepath" : "../../pictures/mon_016.bmp",
                        "position" : pygame.math.Vector2(),
                        "scale" : pygame.math.Vector2(100, 100)}
        if kwargs != None:
            self.options.update(kwargs)

class IconCharacterClass:
    def __init__(self, MainClass, ChracterClass, kwargs):
        self.options = {
            "position" : pygame.math.Vector2(),
            "type" : "IsOnDown",
            "HPbarPicturePath" : "../../pictures/HPbar.png",
            "HPbarbackPicturePath" : "../../pictures/HPbar_back.png",
            "HPscale" : pygame.math.Vector2(100, 10)
            }
        if kwargs != None:
            self.options.update(kwargs)
        self.CharacterClass = ChracterClass
        self.MainClass = MainClass

        self.position = pygame.math.Vector2(self.options["position"])
        self.BtnAction = Helper.ButtonAction(self)
        self.actiondict = {"IsOnDown" : self.BtnAction.IsOnDown}
        self.BoolAction = self.actiondict[self.options["type"]]
        self.Func = self.OnClick
        self.charaControllerRect = self.MainClass.charaControllerRect
        self.scale = pygame.math.Vector2(self.charaControllerRect[3], self.charaControllerRect[3])

        self.picture = None
        self.screen = MainClass.screen

        self.Action = self.Start

        self.menu = self.CharacterClass.menu
        self.menuFunc = self.CharacterClass.menuFunc

        #HPbar
        self.HPbarScale = pygame.math.Vector2(self.scale.x, 10)
        self.HPbarPos = pygame.math.Vector2()
        self.HPbarPicture = BattleHelper.ScaledPicture(
            self.options["HPbarPicturePath"],
            (int(self.HPbarScale.x), int(self.HPbarScale.y))
            )
        self.HPbarbackPicture = BattleHelper.ScaledPicture(
            self.options["HPbarbackPicturePath"],
            (int(self.HPbarScale.x), int(self.HPbarScale.y))
            )

        #外部実装
        self.MenuBtn = None

    def Main(self):
        if self.Action != None:
            self.Action()

    def Start(self):
        self.SetPicture()
        self.Action = self.Update
    def SetPicture(self):
        #画像ロード
        self.picture = pygame.transform.scale(self.CharacterClass.picture, (self.charaControllerRect[3], self.charaControllerRect[3]))

    def Update(self):
        self.BtnAction.mousePos = pygame.mouse.get_pos()
        self.BtnAction.mousePressed = pygame.mouse.get_pressed()

        self.Draw()
        self.DrawBattleMenu()
        self.DrawHPbar()

        if self.BoolAction():
            self.Func()

        self.BtnAction.previousPressed = self.BtnAction.mousePressed
    def Draw(self):
        #描画
        self.screen.blit(self.picture, self.position)
    def DrawBattleMenu(self):
        pass
    def OnClick(self):
        print("btn pushed!")
    def Selected(self):
        pass

    #HPbar
    def DrawHPbar(self):
        self.screen.blit(self.HPbarbackPicture, self.HPbarPos)
        self.screen.blit(self.HPbarPicture, self.HPbarPos)
    def SetHPbarPos(self):
        self.HPbarPos = self.position + pygame.math.Vector2(0, 1) * (self.scale.y - self.HPbarScale.y)

class FieldCharacterClass:
    def __init__(self, MainClass, kwargs):
        #ソース
        self.MainClass = MainClass
        self.Helper = MainClass.Helper
        self.screen = MainClass.screen
        self.options = {"name" : "名無し",
                        "picturepath" : "../../pictures/mon_016.bmp",
                        "position" : pygame.math.Vector2(),
                        "scale" : pygame.math.Vector2(100, 100),
                        "type" : "IsOnDown",
                        "hp" : 100,
                        "attack" : 10,
                        "block" : 10,
                        "speed" : 10,
                        "menu" : ["戦う", "迷う"],
                        "menufunc" : [lambda:print("戦った"), lambda:print("迷った")]}
        if kwargs != None:
            self.options.update(kwargs)

        self.name = self.options["name"]
        self.hp = self.options["hp"]
        self.position = pygame.math.Vector2(self.options["position"])
        self.scale = pygame.math.Vector2(self.options["scale"])
        self.picture = None
        self.BtnAction = Helper.ButtonAction(self)
        self.actiondict = {"IsOnDown" : self.BtnAction.IsOnDown}
        self.BoolAction = self.actiondict[self.options["type"]]
        self.Func = self.OnClick
        self.menu = self.options["menu"]
        self.menuFunc = self.options["menufunc"]

        self.enemies = None
        self.family = None
        self.AttackTarget = None
        self.nextDamage = 0

        self.Action = self.Start

        #外部実装
        self.Animation = None


    #===================Main=================
    def Main(self):
        if self.Action != None:
            self.Action()

    #==================Start=================
    def Start(self):
        self.enemies = self.MainClass.enemies
        self.family = self.MainClass.family

        self.picture = pygame.transform.scale(pygame.image.load(self.options["picturepath"]).convert_alpha(), BattleHelper.Vector2ToIntlist(self.scale))

        self.AttackTargetAutoSelected()
        self.Action = self.Update
    def AttackTargetAutoSelected(self):
        #攻撃対象自動選択
        self.AttackTarget = self.enemies[-1]

    #==================Update===============
    def Update(self):
        self.BtnAction.mousePos = pygame.mouse.get_pos()
        self.BtnAction.mousePressed = pygame.mouse.get_pressed()

        self.Draw()

        if self.BoolAction():
            self.Func()

        self.BtnAction.previousPressed = self.BtnAction.mousePressed
    def Draw(self):
        #描画
        self.screen.blit(self.picture, self.position)
    def AnimationUpdate(self):
        pass

    #====================Button===================
    def Attack(self):
        pass
    def OnClick(self):
        print("btn pushed!")

    #====================Others=================
    def MaxHP(self):
        return self.options["hp"]

    def MaxHPSizeList(self):
        size = self.options["HPscale"]
        return [int(size.x), int(size.y)]

class FieldEnemyClass(FieldCharacterClass):
    def __init__(self, MainClass, kwargs):
        super().__init__(MainClass, kwargs)
        self.options.update(
            {"HPbarPicturePath" : "../../pictures/HPbar.png",
             "HPbarbackPicturePath" : "../../pictures/HPbar_back.png",
             "HPscale" : pygame.math.Vector2(100, 10)}
            )

        self.HPscale = self.options["HPscale"]
        self.HPbarPos = pygame.math.Vector2()
        self.HPbarbackPicture = None
        self.HPbarPicture = None


    def Start(self):
        super().Start()
        self.SetHPbar()

    def SetHPbar(self):
        self.HPbarPos = pygame.math.Vector2(self.position) + pygame.math.Vector2((self.scale.x - self.HPscale.x)/2, self.scale.y)
        self.HPbarPicture = BattleHelper.ScaledPicture(
            self.options["HPbarPicturePath"],
            BattleHelper.Vector2ToIntlist(self.options["HPscale"])
            )
        self.HPbarbackPicture = BattleHelper.ScaledPicture(
            self.options["HPbarbackPicturePath"],
            BattleHelper.Vector2ToIntlist(self.options["HPscale"])
            )

    def Draw(self):
        super().Draw()
        self.DrawHPbar()

    def DrawHPbar(self):
        self.screen.blit(self.HPbarbackPicture, self.HPbarPos)
        self.screen.blit(self.HPbarPicture, self.HPbarPos)

    def AttackTargetAutoSelected(self):
        self.AttackTarget = self.family[-1]
class BattleCharacterMenu:
    def __init__(self, MainClass, kwargs):
        self.MainClass = MainClass
        self.options = {
            "layout" : [0, None, 1, 0.1],
            "noOfMenu" : 4,
            "menu" : [],
            "func" : []
            }
        if kwargs != None:
            self.options.update(kwargs)

        self.Action = self.Start
        self.charaControllerLayout = []
        self.windowSize = []
        self.layout = self.options["layout"]
        self.Buttons = []
        self.screen = self.MainClass.screen

    def Start(self):
        self.SetLayout()
        self.SetButtons()
        self.Action = self.Update
    def SetLayout(self):
        self.charaControllerLayout = self.MainClass.charaControllerLayout
        self.windowSize = self.MainClass.windowSize
        self.layout[1] = (self.windowSize[1] - (self.charaControllerLayout[3] + self.layout[3])*self.windowSize[1]) / self.windowSize[1]
    def SetButtons(self):
        buttonScale = [
            self.layout[2] / self.options["noOfMenu"] * self.windowSize[0],
            self.layout[3] * self.windowSize[1]]
        for i in range(len(self.options["menu"])):
            buttonRect = [i*buttonScale[0], 
                          self.layout[1] * self.windowSize[1],
                          buttonScale[0],
                          buttonScale[1]]
            self.Buttons.append(
                Helper.Button(
                    self.screen,
                    rect=[int(i) for i in buttonRect],
                    func=self.options["func"][i],
                    text=self.options["menu"][i])
                )
    def Update(self):
        self.ShowButtons()
    def ShowButtons(self):
        list(map(lambda btn : btn.Update(), self.Buttons))

    def Main(self):
        if self.Action != None:
            self.Action()

class Animations:
    def __init__(self, Character):
        self.Character = Character
        self.Helper = Character.MainClass.Helper
        self.MainClass = Character.MainClass

        self.Action = None
        self.screen = None
        self.IsEndOfAnimation = False
        self.goalPos = pygame.math.Vector2()

        self.Main = self.Start

    def LoadMaterial(self):
        #画像のロード
        pass

    def AutoSetSurfaceAnimation(self):
        pass

    def Start(self):
        self.screen = self.Character.screen
        self.LoadMaterial()
        self.AutoSetSurfaceAnimation()
        self.Main = self.Update

    def Reset(self):
        self.IsEndOfAnimation = False

    def Update(self):
        self.Reset()

        if self.Action != None:
            self.Action()

        if self.IsEndOfAnimation:
            self.Action = None

    #左アタック
    def LeftAttackStep(self):
        if self.Action != self.LeftAttackStepUpdate:
            self.Action = self.LeftAttackStepStart
    def LeftAttackStepStart(self):
        self.LeftAttackStepSet()
        self.Action = self.LeftAttackStepUpdate
    def LeftAttackStepSet(self):
        pass
    def LeftAttackStepUpdate(self):
        pass

    #右アタック
    def RightAttackStep(self):
        if self.Action != None:
            self.Action = self.RightAttackStepStart
    def RightAttackStepStart(self):
        self.RightAttackStepSet()
        self.Action = self.RightAttackStepUpdate
    def RightAttackStepSet(self):
        pass
    def RightAttackStepUpdate(self):
        pass

    #HP変動
    def MoveHP(self):
        self.Action = self.MoveHPStart
    def MoveHPStart(self):
        self.CalcHP()
        self.Action = self.MoveHPUpdate
    def MoveHPUpdate(self):
        self.MoveHPAnime()
        self.MoveHPEnd()
    def CalcHP(self):
        pass
    def MoveHPEnd(self):
        pass
    def MoveHPAnime(self):
        pass

class OneSurfaceAnimation:
    def __init__(self, MainClass, CharaClass, kwargs):
        self.Helper = MainClass.Helper
        self.options = {
            "delayTime" : 0,
            "endTime" : 1,
            "StartFunc" : None,
            "UpdateFunc" : None,
            "EndFunc" : None
            }
        if kwargs != None:
            self.options.update(kwargs)
        self.StartFunc = self.options["StartFunc"]
        self.UpdateFunc = self.options["UpdateFunc"]
        self.EndFunc = self.options["EndFunc"]
        self.delayTime = self.options["delayTime"]
        self.endTime = self.options["endTime"]

        self.timer = 0
        self.isEndOfAnimation = False #すべてのOneSurfaceAnimationが終了したらON→次のOneSurfaceAnimationを代入する
        self.Action = self.Start

    def Start(self):
        if self.timer >= self.delayTime:
            self.isEndOfAnimation = False
            if self.StartFunc != None:
                self.StartFunc()
            self.Action = self.Update

    def Update(self):
        if self.UpdateFunc != None:
            self.UpdateFunc()

        if self.timer >= self.endTime+self.delayTime:
            self.Action = self.End

    def End(self):
        if self.EndFunc != None:
            self.EndFunc()
        self.isEndOfAnimation = True
        self.Action = self.Start
        self.timer = 0

    def Main(self):
        self.timer += self.Helper.pygamedeltatime

        if self.Action != None:
            self.Action()

    #def IsEndOfAnimation(SurfaceAnimations):
    #    boolList = list(map(lambda OneAnimation : OneAnimation.isEndOfAnimation, SurfaceAnimations))
    #    return all(boolList)