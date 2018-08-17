# -*-coding:utf-8-*-
import pygame
from pygame.locals import *
import sys
import os

path = os.getcwd()
print(path)

class Main:
    def __init__(self):
        self.w = 680
        self.h = 480
        self.screen = pygame.display.set_mode((self.w,self.h))
        self.frame = 1   # 現在のフレーム数
        self.x = 0   # アニメ画像の初期位置x
        self.clock = pygame.time.Clock()

        self.x_gyoza = self.w / 2
        self.y_gyoza = self.h / 2

        pygame.display.set_caption("test")
        #font = pygame.font.Font(None, 15)
        self.picture = pygame.image.load("../../pictures/mon_016.bmp").convert_alpha()
        self.chara_1 = pygame.image.load("../../pictures/suraimu.png").convert_alpha()
        self.chara_2 = pygame.image.load("../../pictures/chara_1.png").convert_alpha()
        self.chara_3 = pygame.image.load("../../pictures/airship.gif").convert_alpha()
        self.blockn_w = self.w // 32 # 20も別に変数を用意？
        self.blockn_h = self.h // 32
        self.lines = Draw_lines()
        self.chara = Chara().split(self.chara_2)    # 配列の関数を読み込み
        self.allgroup = pygame.sprite.Group()   # Group作成
        self.allgroup.add(Spclass("../../pictures/mon_016.bmp"))     # スプライトの作成、登録

    def main(self): # main
        while (1):
            self.screen.fill((0,0,0))
            pygame.display.update
            self.anime_index = int(self.frame / 3) % 5
#            self.screen.blit(self.chara_2, self.chara_2.get_rect())

            # 枠線描画
            Draw_lines().generate(self.blockn_w,self.blockn_h,self.w,self.h,self.screen)

            # 画像描画(アニメーションなので、保留)
#            self.screen.blit(self.chara_2[0], (0,0), (0, 0, 32, 32))

            for i in range(0,5):
                self.screen.blit(self.chara_1, (i * 20, 0), (32 * i, 0, 32, 32))

            # 餃子のキャラ表示
            self.screen.blit(self.picture, (self.x_gyoza, self.y_gyoza)) # 結局getrectなんなのか忘れた

            # Sprite更新
            self.allgroup.update()
            self.allgroup.draw(self.screen)

            # 終了処理
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.x += 1
            self.screen.blit(self.chara_1, (self.x, 164), (32 * self.anime_index, 0, 32, 32))

            pygame.display.flip()
            self.clock.tick(60)

            # フレーム更新
            self.frame += 1

# sprite class ClassName(object):
class Spclass(pygame.sprite.Sprite):
    def __init__(self,filename):
        self.w = 680
        self.h = 480
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = self.w / 2
        self.rect.centery = self.h / 2
        self.pressed_key = pygame.key.get_pressed()

    def update(self):
        if self.pressed_key[K_LEFT]:
            self.rect.move_ip(-8,0)
        if self.pressed_key[K_RIGHT]:
            self.rect.move_ip(8,0)
        if self.pressed_key[K_UP]:
            self.rect.move_ip(0,-8)
        if self.pressed_key[K_DOWN]:
            self.rect.move_ip(0,8)


class Draw:
    def __init__(self):
        pass

class Draw_lines:
    def __init__(self):
        pass
    def generate(self,w,h,maxw,maxh,screen):
        for i in range(0,32):
            pygame.draw.line(screen, (0,95,0), (w * i, 0), (w * i, maxh))     #直線
        for i in range(0,32):
            pygame.draw.line(screen, (0,95,0), (0, h * i,), (maxw, h * i))     #直線

class Chara:    # まずはchara_1.png専用のクラス  一旦保留
    def __init__(self):
        animcycle = 12
        frame = 0
    def split(self, image):
        #キャラの配列を取り出す。左上から順に名付け(したい)
        imagelist = []
        # imagelist = [
        #       下, 下, 下, 下,
        #       左, 左, 左, 左,
        #       右, 右, 右, 右,
        #       上, 上, 上, 上,
        #]  みたいな並び方
        for i in range(0,96,32):
        # 一列目
            self.surface = pygame.Surface((96, 144))
            self.surface.blit(image, (0,0), (i,0,32,32))
            self.surface.set_colorkey(self.surface.get_at((0,0)),RLEACCEL)
            self.surface.convert()
            imagelist.append(self.surface)
        for i in range(0,96,32):
        # 二列目
            self.surface = pygame.Surface((96, 144))
            self.surface.blit(image, (0,32), (i,32,32,32))
            self.surface.set_colorkey(self.surface.get_at((0,0)),RLEACCEL)
            self.surface.convert()
            imagelist.append(self.surface)
        for i in range(0,96,32):
        # 三列目
            self.surface = pygame.Surface((96, 144))
            self.surface.blit(image, (0,64), (i,64,32,32))
            self.surface.set_colorkey(self.surface.get_at((0,0)),RLEACCEL)
            self.surface.convert()
            imagelist.append(self.surface)
        for i in range(0,96,32):
        # 四列目
            self.surface = pygame.Surface((96, 144))
            self.surface.blit(image, (0,96), (i,96,32,32))
            self.surface.set_colorkey(self.surface.get_at((0,0)),RLEACCEL)
            self.surface.convert()
            imagelist.append(self.surface)

        return imagelist

    def update(self,image):
        # 配列に入れた画像をアニメーションする
        self.frame += 1
        self.image = self.images[self.frame/self.animcycle%3]

class Move:
    def __init__(self):
        self.pressed_key = pygame.key.get_pressed()
    def direction(self):
        if self.pressed_key[K_LEFT]:
            self.rect.move_ip(-8,0)
        if self.pressed_key[K_RIGHT]:
            self.rect.move_ip(8,0)
        if self.pressed_key[K_UP]:
            self.rect.move_ip(0,-8)
        if self.pressed_key[K_DOWN]:
            self.rect.move_ip(0,8)

class Facility:
    def __init__(self):
        pass

if __name__ == "__main__":    # コマンドラインから実行されるので
    Main().main()
