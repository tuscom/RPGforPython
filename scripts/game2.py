# -*-coding:utf-8-*-
import pygame
from pygame.locals import *
import sys
import os

class map_draw:
    def __init__(self):
        self.line = 10   # 行の幅
    def generate(self):
        for i in range(0,9):
            pygame.draw.line(main().screen, (0,95,0), (self.line * i, 0), (self.line * i, 240))     #直線

class main:
    def __init__(self):
        (w,h) = (680,480)
        self.screen = pygame.display.set_mode((w,h))

        pygame.display.set_caption("test")
        #font = pygame.font.Font(None, 15)

    def main(self):
        while True:
            self.screen = pygame.display.set_mode((680,480))
            self.screen.fill((0,0,0))
            pygame.display.update

            # 終了処理
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            map_draw().generate()
            pygame.display.flip()

if __name__ == "__main__":    # コマンドラインから実行されるので
#    map_draw().generate()
    main().main()
