import pygame
from pygame.locals import *
import sys

class Character:
    def __init__(self, MainClass, **kwargs):
        self.mainClass = MainClass
        self.options = {"name" : "名無し",
                        "picturepath" : "../../pictures/mon_016.bmp",
                        "position" : (0, 0)}
        self.options.update(kwargs)

        self.characterHelper = CharacterHelper()
        self.screen = self.mainClass.screen
        self.picture = self.characterHelper.PictureLoad(self.options["picturepath"], size=[self.mainClass.squareSize, self.mainClass.squareSize])
        self.position = self.options["position"]

    def Update(self):
        self.screen.blit(self.picture, self.position)

class CharacterHelper:
    def __init__(self):
        pass

    def PictureLoad(self, picturepath, size=[10, 10]):
        picture = pygame.transform.scale(pygame.image.load(picturepath).convert_alpha(), (size[0], size[1]))
        return picture