import pygame
from pygame.locals import *
import sys

class Object:
    def __init__(self, MainClass, **kwargs):
        self.mainClass = MainClass
        self.options = {"name" : "名無し",
                        "picturepath" : "../../pictures/mon_016.bmp",
                        "position" : (0, 0),
                        "scale" : (),
                        "mode" : "object"}
        self.options.update(kwargs)
