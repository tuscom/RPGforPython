import pygame
from pygame.locals import *
import sys

#=============ver0.0.1================
class BaseMainClass:
    def __init__(self):
        self.windowSize = [1500, 800]
        self.pageColor = (255,255,255)
        self.squareSize = 32
        self.windowName = "test"

        pygame.init()
        self.screen = pygame.display.set_mode(self.windowSize)
        pygame.display.set_caption(self.windowName)

        self.Helper = BaseHelperClass(self)
        self.Window = BaseStageClass(self, None)

    def Main(self):
        while True:
            self.screen.fill(self.pageColor)
            self.Helper.EarlyUpdate()

            self.Window.Update()
            self.Helper.DrawGridLine()

            self.Helper.LateUpdate()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

class BaseObjectClass:
    def __init__(self, MainClass, kwargs):
        self.MainClass = MainClass
        self.options = {"name" : "名無し",
                        "picturepath" : "../../pictures/mon_016.bmp",
                        "position" : pygame.math.Vector2(0, 0),
                        "scale" : pygame.math.Vector2(1, 1)}
        if kwargs != None:
            self.options.update(kwargs)

        self.screen = MainClass.screen
        self.position = self.options["position"]
        self.scale = self.options["scale"]
        self.picture = BaseHelperClass.ScaledPicture(self.options["picturepath"], size=(MainClass.squareSize*int(self.scale.x), MainClass.squareSize*int(self.scale.y)))
        self.Helper = MainClass.Helper

        self.positionArea = self.Helper.MakeArea(pygame.math.Vector2(), pygame.math.Vector2(1,1).elementwise()*self.scale)

    def Update(self):
        self.Draw()

    def Draw(self):
        self.screen.blit(self.picture, self.position)

    def Area(self, originV2):
        result = list(map(lambda pos:pos+originV2, self.positionArea))
        return result

class BasePlayerClass(BaseObjectClass):
    def __init__(self, MainClass, kwargs):
        super().__init__(MainClass, kwargs)

        self.nextPos = pygame.math.Vector2(self.position)

    def Update(self):
        self.Draw()
        self.Move()

    #動かす
    def Move(self):
        self.InputPos()
        if self.ConditionPos():
            self.ReflectPos()
    def ConditionPos(self):
        return True
    def InputPos(self):
        pass
    def ReflectPos(self):
        pass

class BaseStageClass:
    def __init__(self, MainClass, kwargs):
        self.MainClass = MainClass
        self.options={"name" : "名無しステージ",
                      "picturepath" : "../../pictures/stage.png"}
        if kwargs != None:
            self.options.update(kwargs)

        self.screen = MainClass.screen
        self.Helper = MainClass.Helper
        self.position = (0, 0)

        self.picture = BaseHelperClass.ScaledPicture(self.options["picturepath"], size=MainClass.windowSize)

        self.objects = []
        self.player = BasePlayerClass(MainClass, None)
        self.enemies = []
        self.availablePos = {}

    def Update(self):
        self.Draw()

    def Draw(self):
        self.DrawBackground()

        list(map(lambda object:object.Update(), self.objects))
        list(map(lambda enemies:enemies.Update(), self.enemies))
        self.player.Update()

    def DrawBackground(self):
        self.screen.blit(self.picture, self.position)

    def AddArea(self, fromVector2, toVector2):
        pass

    def RemoveArea(self, fromVector2, toVector2):
        pass

class BaseHelperClass:
    def __init__(self, MainClass):
        self.MainClass = MainClass

        #delta time
        self.nowTime = pygame.time.get_ticks() * 1e-3
        self.previousTime = self.nowTime
        self.deltaTime = self.nowTime - self.previousTime

        self.nowPressed = pygame.key.get_pressed()
        self.previousPressed = self.nowPressed

        #key is down
        self.intHorizontalKey = self.nowPressed[K_RIGHT] - self.nowPressed[K_LEFT]
        self.previousIntHorizontalKey = self.intHorizontalKey
        self.intVerticalKey = self.nowPressed[K_UP] - self.nowPressed[K_DOWN]
        self.previousIntVerticalKey = self.intVerticalKey

        #grid lines
        self.screen = MainClass.screen
        self.gridColor = pygame.Color("BLACK")
        self.noOfLine = pygame.math.Vector2(MainClass.windowSize[0]/MainClass.squareSize, MainClass.windowSize[1]/MainClass.squareSize)

    def NormToWorldPos(self, normalPos):
        return list(map(lambda axis:axis * self.MainClass.squareSize, normalPos))

    def WorldToGridPos(self, worldPos):
        remainder = pygame.math.Vector2(worldPos.x%self.MainClass.squareSize, worldPos.y%self.MainClass.squareSize)
        return worldPos - remainder

    def DrawGridLine(self):
        for i in range(int(self.noOfLine.x)):
            pygame.draw.line(self.screen, self.gridColor, ((i+1)*self.MainClass.squareSize, 0), ((i+1)*self.MainClass.squareSize, self.MainClass.windowSize[1]))

        for i in range(int(self.noOfLine.y)):
            pygame.draw.line(self.screen, self.gridColor, (0, (i+1)*self.MainClass.squareSize), (self.MainClass.windowSize[0], (i+1)*self.MainClass.squareSize))

    def IsKeyDown(self, KEYNAME):
        result = False

        if self.nowPressed[KEYNAME] and not self.previousPressed[KEYNAME]:
            result = True

        return result

    def MakeArea(self, fromV2, toV2):
        result = []
        posV2 = toV2 - fromV2
        noOfArea = int(posV2.x * posV2.y)

        for i in range(noOfArea):
            x = i%posV2.x * self.MainClass.squareSize
            y = i//posV2.x * self.MainClass.squareSize
            pointV2 = pygame.math.Vector2(x, y)
            
            result.append(pointV2)

        return result
    def EarlyUpdate(self):
        self.nowTime = pygame.time.get_ticks() * 1e-3
        self.deltaTime = self.nowTime - self.previousTime
        self.previousTime = self.nowTime

        self.nowPressed = pygame.key.get_pressed()

        self.intHorizontalKey = self.nowPressed[K_RIGHT] - self.nowPressed[K_LEFT]
        self.intVerticalKey = self.nowPressed[K_UP] - self.nowPressed[K_DOWN]

    def LateUpdate(self):
        self.previousPressed = self.nowPressed

        self.previousIntHorizontalKey = self.intHorizontalKey
        self.previousIntVerticalKey = self.intVerticalKey

    def ScaledPicture(picturepath, size=(100, 100)):
        picture = pygame.transform.scale(pygame.image.load(picturepath).convert_alpha(), size)
        return picture

