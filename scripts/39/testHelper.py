import pygame
from pygame.locals import *
import sys

class Character:
    def __init__(self, MainClass, **kwargs):
        self.ArgumentSetting(MainClass, kwargs)

        self.nextPos = self.position

    def Parameters(self):
        pass

    def ArgumentSetting(self, MainClass, options):
        self.mainClass = MainClass
        self.options = {"name" : "名無し",
                        "picturepath" : "../../pictures/mon_016.bmp",
                        "position" : [0, 0],
                        "scale" : (),
                        "mode" : "object"}
        self.options.update(options)
        
        self.Modes = {"object" : None,
                     "player" : PlayerMode(self)}

        self.characterHelper = CharacterHelper()
        self.screen = self.mainClass.screen
        self.picture = self.characterHelper.PictureLoad(self.options["picturepath"], size=[self.mainClass.squareSize, self.mainClass.squareSize])
        self.mode = self.Modes[self.options["mode"]]
        self.position = self.options["position"]

    def Update(self):
        self.screen.blit(self.picture, self.position)
        self.mode.Update()

class CharacterHelper:
    def __init__(self):
        pass

    def PictureLoad(self, picturepath, size=[10, 10]):
        picture = pygame.transform.scale(pygame.image.load(picturepath).convert_alpha(), (size[0], size[1]))
        return picture

class PlayerMode:
    def __init__(self, CharaClass):
        self.CharaClass = CharaClass
        self.mainClass = self.CharaClass.mainClass
        self.KeyBoard = self.mainClass.KeyBoard
        self.Time = self.mainClass.Time
        self.deltaTime = 0
        self.moveDirection = [0, 0]

        self.speed = 0.

    def Move(self):
        self.moveDirection = [self.CharaClass.nextPos[0] - self.CharaClass.position[0], self.CharaClass.nextPos[1] - self.CharaClass.position[1]]
        magni = (self.moveDirection[0]**2+self.moveDirection[1]**2)**(1/2)
        if magni != 0:
            self.moveDirection = [self.moveDirection[0]/magni, self.moveDirection[1]/magni]

        #self.CharaClass.position = self.CharaClass.nextPos
        if self.CharaClass.position != self.CharaClass.nextPos:
            #self.CharaClass.position = [self.moveDirection[0] * self.deltaTime, self.moveDirection[1] * self.deltaTime]
            self.CharaClass.position[0] += self.moveDirection[0] * self.deltaTime * self.speed
            self.CharaClass.position[1] += self.moveDirection[1] * self.deltaTime * self.speed

    def Update(self):
        self.Move()
        self.deltaTime = self.Time.deltaTime
        if self.KeyBoard.IsHorizontalDown():
            self.CharaClass.nextPos[0] += self.KeyBoard.intHorizontalKey * self.mainClass.squareSize
        if self.KeyBoard.IsVerticalDown():
            self.CharaClass.nextPos[1] -= self.KeyBoard.intVerticalKey * self.mainClass.squareSize

class Grid:
    def __init__(self, MainClass):
        self.MainClass = MainClass
        self.windowSize = self.MainClass.windowSize
        self.squareSize = self.MainClass.squareSize
        self.screen = self.MainClass.screen
        self.color = pygame.Color("BLACK")
        self.noOfLine = [int(self.windowSize[0]/self.squareSize), int(self.windowSize[1]/self.squareSize)]

    def Update(self):
        for i in range(self.noOfLine[0]):
            pygame.draw.line(self.screen, self.color, ((i+1)*self.squareSize, 0), ((i+1)*self.squareSize, self.windowSize[1]))

        for i in range(self.noOfLine[1]):
            pygame.draw.line(self.screen, self.color, (0, (i+1)*self.squareSize), (self.windowSize[0], (i+1)*self.squareSize))

class KeyBoard:
    def __init__(self):
        self.nowPressed = pygame.key.get_pressed()
        self.previousPressed = self.nowPressed
        self.intHorizontalKey = self.nowPressed[K_RIGHT] - self.nowPressed[K_LEFT]
        self.previousIntHorizontalKey = self.intHorizontalKey
        self.intVerticalKey = self.nowPressed[K_UP] - self.nowPressed[K_DOWN]
        self.previousIntVerticalKey = self.intVerticalKey

    def ShowKeyName(self):
        keyPressed = pygame.key.get_pressed()
        if any(keyPressed):
            print(pygame.key.name(keyPressed.index(1)))

    def EarlyUpdate(self):
        self.nowPressed = pygame.key.get_pressed()
        #順序注意
        self.intHorizontalKey = self.nowPressed[K_RIGHT] - self.nowPressed[K_LEFT]
        self.intVerticalKey = self.nowPressed[K_UP] - self.nowPressed[K_DOWN]

    def LaterUpdate(self):
        self.previousPressed = self.nowPressed
        self.previousIntHorizontalKey = self.intHorizontalKey
        self.previousIntVerticalKey = self.intVerticalKey

    def IsKeyDown(self, KEYNAME):
        result = False

        if self.nowPressed[KEYNAME] and not self.previousPressed[KEYNAME]:
            result = True

        return result

    def IsHorizontalDown(self):
        return self.intHorizontalKey and not self.previousIntHorizontalKey

    def IsVerticalDown(self):
        return self.intVerticalKey and not self.previousIntVerticalKey

class Time:
    def __init__(self):
        self.nowTime = pygame.time.get_ticks() * 1e-3
        self.previousTime = 0
        self.deltaTime = self.nowTime - self.previousTime

    def EarlyUpdate(self):
        self.nowTime = pygame.time.get_ticks() * 1e-3
        self.deltaTime = self.nowTime - self.previousTime
        self.previousTime = self.nowTime