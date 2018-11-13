#MAIN CLASS FOR GAME

from __future__ import print_function
import os
import pygame as pg
from fsm import *
from config import *
from .classes import *
#import resource_manager

#pid = os.getpid()
#py = psutil.Process(pid)

__author__ = "Leandro Peres"

class Gameplay(BaseState):
    def __init__(self):
        super(Gameplay, self).__init__()
        self.rect = pg.Rect((0, 0), (128, 128))
        self.x_velocity = 1
        self.fundo = pg.image.load('data/image/CENARIO.png').convert_alpha()
        self.fundoX, self.fundoY = self.fundo.get_rect().size

        self.fontObj = pg.font.Font('data/fonts/Minecraft.ttf', 26)
        self.textObj = self.fontObj.render('0 POINTS', True, (0,0,0))
        self.lifeObj = self.fontObj.render('0/0', True, (0,0,0))
        self.lifeRect = self.lifeObj.get_rect()
        self.textRect = self.textObj.get_rect()
        self.textRect.center  = (150, 50)


        self.stage = {
            "X": 0, #cordenada x
            "W": self.fundoX, # tamanho
            "I": (HEIGHT / 2) + 156, # inicio do scroll
            "H": 1 # horda
            }

    def startup(self, persistent):
        self.all_sprites = pg.sprite.Group()
        self.balas = pg.sprite.Group()
        self.player = Player((2,1))
        self.inimigos = pg.sprite.Group()
        self.objects = pg.sprite.Group()
        self.all_sprites.add(self.inimigos)
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.objects)
        #
        for i in range(0, self.stage['H']):
            bala = Inimigo(self.player)

            self.all_sprites.add(bala)
            self.inimigos.add(bala)
        #

        self.lifeRect.center  = (120, 100)

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()

            if event.key == pg.K_k:
                self.player.atira(self.all_sprites, self.balas)

            # if event.key == pg.K_w:
            #    self.player.facing = 'cima'
            if event.key == pg.K_a:
                self.player.go_left()
            if event.key == pg.K_d:
                self.player.go_right()
            if event.key == pg.K_w:
                self.player.go_up()
            if event.key == pg.K_SPACE:
                self.player.jump()

        if event.type == pg.KEYUP:
            if event.key == pg.K_a and self.player.x_ < 0:
                self.player.stop(-2)
            if event.key == pg.K_d and self.player.x_ > 0:
                self.player.stop(2)

    def update(self, dt):
        self.textObj = self.fontObj.render('{} POINTS'.format(self.player.attributes['SCORE']), True, (0,0,0))
        self.lifeObj = self.fontObj.render('{}'.format(self.player.attributes['ULT']), True, (0,0,0))
        tiroteio = pg.sprite.groupcollide(self.inimigos, self.balas, False, pg.sprite.collide_mask)
        #es = pg.sprite.spritecollideany(umb, all_sprites)
        #esfaqueamento = pg.sprite.groupcollide(self.player, self.inimigos, False, pg.sprite.collide_mask)
        if tiroteio:
            for inimigo, bala in tiroteio.items():
                dano = self.player.attributes['ATT'] - inimigo.attributes['DEF']
                if (dano >= inimigo.attributes['HP']) or (inimigo.attributes['HP'] < 0):
                    bala[0].kill()
                    inimigo.morre(self.all_sprites, self.objects)
                    self.player.attributes['SCORE'] += inimigo.attributes['SCORE']
                    self.player.chargeUlt(inimigo.attributes['SCORE'] // 3)
                else:
                    print(dano)
                    inimigo.attributes['HP'] -= dano

        contato = pg.sprite.spritecollideany(self.player, self.inimigos)
        if contato:
            if self.player.x_ == 0 and not self.player.invencibilidade: #and contato.facing == self.player.facing 
                dano = contato.attributes['ATT'] - self.player.attributes['DEF']
                self.player.attributes['HP'] -= dano
                self.player.invencibilidade = True
            else:
                dano = self.player.attributes['ATT'] - contato.attributes['DEF']
                if (dano >= contato.attributes['HP']) or (contato.attributes['HP'] < 0):
                    contato.morre(self.all_sprites, self.objects)
                    self.player.attributes['SCORE'] += contato.attributes['SCORE']
                    self.player.chargeUlt(contato.attributes['SCORE'] // 3)
                else:
                    contato.attributes['HP'] -= dano
                #self.player.rect.x += -75 if self.player.facing == 'esquerda' else 75

        if len(self.inimigos) == 0:
            self.stage['H'] += 3
            for i in range(0, self.stage['H'] + 1):
                bala = Inimigo(self.player)

                self.all_sprites.add(bala)
                self.inimigos.add(bala)

    def draw(self, surface):
        if self.player.rect.x <= 0:
            self.player.rect.x = 0
        elif self.player.rect.x >= WIDTH - self.player.rect.size[0]:
            self.player.rect.x = WIDTH - self.player.rect.size[0]

        elif self.player.rect.x > self.stage['I'] and (self.player.rect.x < self.stage['W'] - self.stage['I'] + 250):
            self.stage['X'] -= self.player.x_ / 2.2
            for o, i in zip(self.objects, self.inimigos):
                o.rect.x -= self.player.x_ / 1.6
                i.rect.x -= self.player.x_ / 1.6

        else: self.stage['X'] = 0

        surface.blit(self.fundo, (self.stage['X'], -250))
        self.all_sprites.update()
        self.all_sprites.draw(surface)
        surface.blit(self.textObj, self.textRect)
        surface.blit(self.lifeObj, self.lifeRect)
        pg.draw.rect(surface, (245,0,0), (120, 50, 200 - (2 * (50 - self.player.attributes['MAXHP'])), 10) )
        pg.draw.rect(surface, (00,255,0), (120, 50, 200 - (2 * (50 - self.player.attributes['HP'])), 10) ) 