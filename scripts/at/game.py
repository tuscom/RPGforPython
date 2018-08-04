# -*-coding:utf-8-*-
import pygame
from pygame.locals import *
import sys
import os

# path = os.getcwd()
# print(path)

class main:
    def __init__(self):
        (w,h) = (680,480)
        self.screen = pygame.display.set_mode((w,h))
        self.frame = 1   # 現在のフレーム数
        self.x = 0   # アニメ画像の初期位置x
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("test")
        #font = pygame.font.Font(None, 15)
        self.picture = pygame.image.load("./pictures/mon_016.bmp").convert_alpha()
        self.anime = pygame.image.load("./pictures/suraimu.png").convert_alpha()
        self.blockn_w = 680 // 20
        self.blockn_h = 480 // 20

    def main(self): # main
        while (1):
            self.screen.fill((0,0,0))

#            self.screen.blit(self.anime, self.anime.get_rect())
            self.anime_index = int(self.frame / 3) % 5

            # 枠線描画
            map_draw().generate()

            for i in range(0,5):
                self.screen.blit(self.anime, (0 + i * 20, 104), (32 * i, 0, 32, 32))

            # 終了処理
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.x += 1
            self.screen.blit(self.anime, (self.x, 164), (32 * self.anime_index, 0, 32, 32))
            pygame.display.update
            pygame.display.flip()
            self.clock.tick(60)

            # フレーム更新
            self.frame += 1

class map_draw:
    line = 0
    def __init__(self):
        self.line = 10   # 行の幅
    def generate(self):
        for i in range(0,9):
            pygame.draw.line(main().screen, (0,95,0), (self.line * i, 0), (self.line * i, 240))     #直線

if __name__ == "__main__":    # コマンドラインから実行されるので
#    map_draw().generate()
    main().main()
