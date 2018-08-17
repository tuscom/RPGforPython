import pygame
from pygame.locals import *
import sys

#=================ver0.0.2==================
class BaseMainClass:
    def __init__(self):
        self.windowSize = [1500, 800]
        self.pageColor = (255,255,255)
        self.squareSize = 32
        self.windowName = "ver0.0.2"

        pygame.init()
        self.screen = pygame.display.set_mode(self.windowSize)
        pygame.display.set_caption(self.windowName)

        #外部実装(test 用)
        self.Helper = None
        self.Window = None

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
                        "scale" : pygame.math.Vector2(1, 1),
                        "func" : None}
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

    def ResetPosition(self):
        self.position = self.options["position"]

class BaseTouchEventClass(BaseObjectClass):
    def __init__(self, MainClass, kwargs):
        super().__init__(MainClass, kwargs)
        self.touchFunc = self.options["func"]
        self.previousPlayerPos = None

    def Update(self):
        self.Draw()
        self.TouchFunction()

    def TouchFunction(self):
        if self.IsOnTouchWithPlayer():
            self.touchFunc()

    def IsOnTouchWithPlayer(self):
        result = False
        player = self.MainClass.Window.player
        if player.position != self.previousPlayerPos:
            if player.position == self.position:
                result = True

        self.previousPlayerPos = pygame.math.Vector2(player.position)
        return result

class BasePlayerClass(BaseObjectClass):
    def __init__(self, MainClass, kwargs):
        super().__init__(MainClass, kwargs)
        self.speedFactor = 1

        #Move
        self.nextPos = pygame.math.Vector2(self.position)
        self.goalDirection = self.nextPos - self.position
        self.movingDirection = self.nextPos - self.position
        if (self.movingDirection.x**2 + self.movingDirection.y**2)**(1/2) != 0:
            self.deltaPos = self.movingDirection.normalize() * self.speedFactor
        else:
            self.deltaPos = pygame.math.Vector2(0, 0)
        self.DeltaPositionVectorDot = self.movingDirection.dot(self.goalDirection)
        self.HorizontalDirection = self.Helper.intHorizontalKey
        self.VerticalDirection = self.Helper.intVerticalKey

    def Update(self):
        self.Draw()
        self.Move()

    def Move(self):
        self.InputPos()
        if self.ConditionPos():
            self.ReflectPos()

    def InputPos(self):
        self.HorizontalDirection = self.Helper.intHorizontalKey
        self.VerticalDirection = self.Helper.intVerticalKey

    def ConditionPos(self):
        result = False
        #変数更新
        self.movingDirection = self.nextPos - self.position
        if (self.movingDirection.x**2 + self.movingDirection.y**2)**(1/2) != 0:
            self.deltaPos = self.movingDirection.normalize() * self.speedFactor
        else:
            self.deltaPos = pygame.math.Vector2(0, 0)
        self.DeltaPositionVectorDot = self.movingDirection.dot(self.goalDirection)

        #移動条件
        if self.DeltaPositionVectorDot > 0:
            result = True

        #移動目的地の設定 : 入力はあるけど到着している→出発の瞬間
        if self.DeltaPositionVectorDot <= 0:
                
            self.position = pygame.math.Vector2(self.nextPos)
                    
            if self.ConditionArea():
                self.nextPos += (self.HorizontalDirection * pygame.math.Vector2(1, 0) + self.VerticalDirection * pygame.math.Vector2(0, -1)) * self.MainClass.squareSize

            self.goalDirection = self.nextPos - self.position

        return result

    def ReflectPos(self):
        self.position += self.deltaPos

    def ConditionArea(self):
        deltaNewPos = (self.HorizontalDirection * pygame.math.Vector2(1, 0) + self.VerticalDirection * pygame.math.Vector2(0, -1)) * self.MainClass.squareSize
        result = all(list(map(lambda point : self.MainClass.Window.IsInArea(point), self.Area(deltaNewPos+self.nextPos))))
        return result

    def ResetPosition(self):
        pass

class BaseStageClass:
    def __init__(self, MainClass, kwargs):
        self.MainClass = MainClass
        self.options={"name" : "名無しステージ",
                      "picture" : None,
                      "objects" : [],
                      "enemies" : [],
                      "player" : None}
        if kwargs != None:
            self.options.update(kwargs)

        self.screen = MainClass.screen
        self.Helper = MainClass.Helper
        self.picture = self.options["picture"]

        #配置するもの。
        self.player = self.options["player"]
        self.objects = self.options["objects"]
        self.enemies = self.options["enemies"]

        #配置条件
        self.availableArea = {}
        self.gridWindowSize = self.Helper.WorldToGridPos(pygame.math.Vector2(MainClass.windowSize[0], MainClass.windowSize[1]))
        self.AddArea(pygame.math.Vector2(), self.gridWindowSize)
        list(map(lambda obj : self.RemoveArea(obj.position, obj.position+pygame.math.Vector2(1,1).elementwise()*obj.scale*MainClass.squareSize), self.objects))

    def Update(self):
        self.Draw()

    def Draw(self):
        self.DrawBackground()

        list(map(lambda object:object.Update(), self.objects))
        list(map(lambda enemies:enemies.Update(), self.enemies))
        self.player.Update()

    def DrawBackground(self):
        self.screen.blit(self.picture, pygame.math.Vector2())

    def AddArea(self, fromVector2, toVector2):
        gridCountV2 = (toVector2 - fromVector2) // self.MainClass.squareSize
        noOfArea = int(gridCountV2.x * gridCountV2.y)

        for i in range(noOfArea):
            x = i%gridCountV2.x * self.MainClass.squareSize
            y = i//gridCountV2.x * self.MainClass.squareSize
            pointV2 = pygame.math.Vector2(x, y)
            self.availableArea[(int(pointV2.x), int(pointV2.y))] = True

    def RemoveArea(self, fromVector2, toVector2):
        gridCountV2 = (toVector2 - fromVector2) // self.MainClass.squareSize
        noOfArea = int(gridCountV2.x * gridCountV2.y)

        for i in range(noOfArea):
            x = i%gridCountV2.x * self.MainClass.squareSize
            y = i//gridCountV2.x * self.MainClass.squareSize
            pointV2 = pygame.math.Vector2(x, y)
            pointV2 += fromVector2
            self.availableArea[(int(pointV2.x), int(pointV2.y))] = False

    def IsInArea(self, targetV2):
        result = False
        try:
            result = self.availableArea[(int(targetV2.x), int(targetV2.y))]
        except KeyError:
            result = False

        return result

    def Reset(self):
        self.player.ResetPosition()
        list(map(lambda object:object.ResetPosition(), self.objects))
        list(map(lambda enemy:enemy.ResetPosition(), self.enemies))

    def ChangeStage(self, StageClass):
        self.Reset()
        self.MainClass.Window = StageClass

class BaseHelperClass:
    def __init__(self, MainClass):
        self.MainClass = MainClass

        #key
        self.nowPressed = pygame.key.get_pressed()
        self.previousPressed = self.nowPressed

        #left, right, up and down
        self.intHorizontalKey = self.nowPressed[K_RIGHT] - self.nowPressed[K_LEFT]
        self.intVerticalKey = self.nowPressed[K_UP] - self.nowPressed[K_DOWN]

        #grid lines
        self.screen = MainClass.screen
        self.gridColor = pygame.Color("BLACK")
        self.noOfLine = pygame.math.Vector2(MainClass.windowSize[0]/MainClass.squareSize, MainClass.windowSize[1]/MainClass.squareSize)

    def WorldToGridPos(self, worldPos):
        remainder = pygame.math.Vector2(worldPos.x%self.MainClass.squareSize, worldPos.y%self.MainClass.squareSize)
        return worldPos - remainder

    def DrawGridLine(self):
        for i in range(int(self.noOfLine.x)):
            pygame.draw.line(self.screen, self.gridColor, ((i+1)*self.MainClass.squareSize, 0), ((i+1)*self.MainClass.squareSize, self.MainClass.windowSize[1]))

        for i in range(int(self.noOfLine.y)):
            pygame.draw.line(self.screen, self.gridColor, (0, (i+1)*self.MainClass.squareSize), (self.MainClass.windowSize[0], (i+1)*self.MainClass.squareSize))

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
        #key
        self.nowPressed = pygame.key.get_pressed()

        #left, right, up, down
        self.intHorizontalKey = self.nowPressed[K_RIGHT] - self.nowPressed[K_LEFT]
        self.intVerticalKey = self.nowPressed[K_UP] - self.nowPressed[K_DOWN]

    def LateUpdate(self):
        self.previousPressed = self.nowPressed

    def ScaledPicture(picturepath, size=(100, 100)):
        picture = pygame.transform.scale(pygame.image.load(picturepath).convert_alpha(), size)
        return picture