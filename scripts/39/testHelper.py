import pygame
from pygame.locals import *
import sys

class Character:
    def __init__(self, MainClass, **kwargs):
        self.mainClass = MainClass
        self.options = {"name" : "名無し",
                        "picturepath" : "../../pictures/mon_016.bmp",
                        "position" : (0, 0),
                        "mode" : "object"}
        self.options.update(kwargs)
        
        self.Modes = {"object" : None,
                     "player" : PlayerMode(MainClass)}

        self.characterHelper = CharacterHelper()
        self.screen = self.mainClass.screen
        self.picture = self.characterHelper.PictureLoad(self.options["picturepath"], size=[self.mainClass.squareSize, self.mainClass.squareSize])
        self.mode = self.Modes[self.options["mode"]]
        self.position = self.options["position"]

        self.nextPos = self.position

    def Update(self):
        self.nextPos = self.position
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
        self.keyPressed = pygame.key.get_pressed()

    def Move(self):
        pass

    def Update(self):
        self.keyPressed = pygame.key.get_pressed()
        if self.keyPressed[K_RIGHT]-self.keyPressed[K_LEFT]:
            print(self.keyPressed[K_RIGHT]-self.keyPressed[K_LEFT])

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
        pass
    def ShowKeyName(self):
        keyPressed = pygame.key.get_pressed()
        if any(keyPressed):
            print(pygame.key.name(keyPressed.index(1)))
