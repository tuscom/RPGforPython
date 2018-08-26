import pygame
from pygame.locals import *
import sys

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
        self.SetPanel()
        self.Action = self.Update

    def LoadScene(self):
        pass
    def SetFieldCharacter(self):
        pass
    def SetPanel(self):
        pass

    #================ Update =================
    def Update(self):
        self.DrawBackGround()
        self.DrawCharacter()
        self.DrawPanel()

        if self.AnimationController != None:
            self.AnimationController()

    def DrawPanel(self):
        pass
    def DrawBackGround(self):
        pass
    def DrawCharacter(self):
        pass

    #================ Button ===============
    def AttackOnClick(self):
        pass

class Helper:
    def __init__(self, MainClass):
        self.MainClass = MainClass
        self.windowSize = MainClass.windowSize
        self.screen = MainClass.screen

        self.pygameclock = pygame.time.get_ticks() * 1e-3
        self.pygamedeltatime = 0

    def NormToWorldPos(self, normV2):
        windowSize = self.MainClass.windowSize
        windowSizeV2 = pygame.math.Vector2(windowSize[0], windowSize[1])
        return normV2.elementwise() * windowSizeV2

    def NormToWorldRect(self, rect):
        windowSize = self.MainClass.windowSize
        result = [rect[0]*windowSize[0], rect[1]*windowSize[1], rect[2]*windowSize[0], rect[3]*windowSize[1]]
        result = [int(i) for i in result]
        return result

    def EarlyUpdate(self):
        previousclock = self.pygameclock
        self.pygameclock = pygame.time.get_ticks() * 1e-3
        self.pygamedeltatime = self.pygameclock - previousclock

    def ScaledPicture(picturepath, size=(100, 100)):
        picture = pygame.transform.scale(pygame.image.load(picturepath).convert_alpha(), size)
        return picture

    def Vector2ToIntlist(v2):
        return [int(v2.x), int(v2.y)]

    def FadeIn001(self):
        pass

class ObjectClass:
    def __init__(self, MainClass, kwargs):
        self.MainClass = MainClass
        self.options = {"name" : "名無し",
                        "picturepath" : "../../pictures/mon_016.bmp"}
        if kwargs != None:
            self.options.update(kwargs)

class FieldCharacterClass:
    def __init__(self, MainClass, kwargs):
        self.MainClass = MainClass
        self.Helper = MainClass.Helper
        self.screen = MainClass.screen
        self.options = {"name" : "名無し",
                        "picturepath" : "../../pictures/mon_016.bmp",
                        "position" : pygame.math.Vector2(),
                        "scale" : pygame.math.Vector2(100, 100),
                        "type" : "IsOnDown",
                        "func" : lambda:print("Btn pushed!"),
                        "hp" : 100,
                        "attack" : 10,
                        "block" : 10,
                        "speed" : 10}
        if kwargs != None:
            self.options.update(kwargs)

        self.name = self.options["name"]
        self.position = pygame.math.Vector2(self.options["position"])
        self.scale = pygame.math.Vector2(self.options["scale"])
        self.picture = None
        self.BtnAction = ButtonAction(self)
        self.actiondict = {"IsOnDown" : self.BtnAction.IsOnDown}
        self.BoolAction = self.actiondict[self.options["type"]]
        self.Func = self.options["func"]

        self.enemies = None
        self.family = None
        self.AttackTarget = None
        self.nextDamage = 0

        self.Action = self.Start

        #外部実装
        self.Animation = None

    def Main(self):
        if self.Action != None:
            self.Action()

    def AttackTargetAutoSelected(self):
        self.AttackTarget = self.family[-1]
    def LoadMaterial(self):
        #画像ロード
        self.picture = pygame.transform.scale(pygame.image.load(self.options["picturepath"]).convert_alpha(), Helper.Vector2ToIntlist(self.scale))
    def Start(self):
        self.enemies = self.MainClass.enemies
        self.family = self.MainClass.family

        self.LoadMaterial()
        self.AttackTargetAutoSelected()
        self.Action = self.Update

    def Draw(self):
        #描画
        self.screen.blit(self.picture, self.position)
    def Update(self):
        self.BtnAction.mousePos = pygame.mouse.get_pos()
        self.BtnAction.mousePressed = pygame.mouse.get_pressed()

        self.Draw()
        self.AnimationUpdate()

        if self.BoolAction():
            self.Func()

        self.BtnAction.previousPressed = self.BtnAction.mousePressed

    def AnimationUpdate(self):
        pass

    def Attack(self):
        pass

class FieldEnemyClass(FieldCharacterClass):
    def __init__(self, MainClass, kwargs):
        super().__init__(MainClass, kwargs)
        self.options.update(
            {"HPbarPicturePath" : "../../pictures/HPbar.png",
             "HPbarbackPicturePath" : "../../pictures/HPbar_back.png",
             "HPscale" : pygame.math.Vector2(80, 10)}
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
        self.HPbarPicture = Helper.ScaledPicture(
            self.options["HPbarPicturePath"],
            Helper.Vector2ToIntlist(self.options["HPscale"])
            )
        self.HPbarbackPicture = Helper.ScaledPicture(
            self.options["HPbarbackPicturePath"],
            Helper.Vector2ToIntlist(self.options["HPscale"])
            )

    def Draw(self):
        super().Draw()
        self.DrawHPbar()

    def DrawHPbar(self):
        self.screen.blit(self.HPbarbackPicture, self.HPbarPos)
        self.screen.blit(self.HPbarPicture, self.HPbarPos)


class ButtonAction:
    def __init__(self, ParentClass):
        self.ParentClass = ParentClass
        self.mousePos = (0, 0)
        self.mousePressed = (0, 0, 0)
        self.previousPressed = (1, 1, 1)

    def IsOnDown(self):
        result = False
        rect = self.Rect()
        if self.mousePressed[0] and not self.previousPressed[0]:
            if rect[0] <= self.mousePos[0] <= rect[0]+rect[2] and rect[1] <= self.mousePos[1] <= rect[1]+rect[3]:
                result = True

        return result

    def Rect(self):
        #rect 計算
        return (self.ParentClass.position.x, self.ParentClass.position.y, self.ParentClass.scale.x, self.ParentClass.scale.y)

class Animations:
    def __init__(self, Character):
        self.Character = Character
        self.Helper = Character.MainClass.Helper

        self.Action = None
        self.IsEndOfAnimation = False
        self.goalPos = pygame.math.Vector2()


    def Reset(self):
        self.IsEndOfAnimation = False

    def Main(self):
        self.Reset()

        if self.Action != None:
            self.Action()

        if self.IsEndOfAnimation:
            self.Action = None

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

