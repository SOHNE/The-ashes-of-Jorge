from __future__ import print_function
import os
import pygame as pg
from fsm import *
from config import *
import random
#import pixelperfect

#pid = os.getpid()
#py = psutil.Process(pid)

class Inimigo(pg.sprite.Sprite):
    def __init__(self, player, stage=None):
        pg.sprite.Sprite.__init__(self)
        self.frame_c, self.contador = FPS, 0 

        stage = stage if stage else 1

        self.all_images = ["data/image/inimigo/{}.png".format(i) for i in range(0,2)]

        self.image = pg.image.load(self.all_images[self.contador])
        self.image.set_colorkey((255,255,255))
        self.image = self.image.convert_alpha()

        self.mask = pg.mask.from_surface(self.image)
        self.player = player
        self.rect = self.image.get_rect()

        self.x_ = random.randint(2, 6)
        if self.x_ == 6:
            if random.choice([0,5]) < 4:
                self.x_ = 5
        self.y_ = 10
        escolha = random.choice(['direita', 'esquerda'])
        self.facing = escolha
        if escolha  == 'esquerda':
            self.rect.center = ((1024 + 380), HEIGHT - self.rect.height)
        elif escolha == 'direita':
            self.rect.center = ( - 380, HEIGHT - self.rect.height)
        self.isjump = False
        self.isnear = False

        self.fliped = pg.transform.flip(self.image, True, False)

        self.attributes = {
            'MAXHP': 45 * (stage // 3),
            'HP': 10 * (stage // 2),
            'ATT': 5 * (stage // 3),
            'DEF': 1 * (stage // 2),
            'SCORE': 35 * (stage // 4)
            }
        if self.attributes['HP'] > self.attributes['MAXHP']: self.attributes['HP'] = self.attributes['MAXHP']

    def startup(self, persistent):
        escolha = random.choice(['direita', 'esquerda'])
        self.facing = escolha
        if escolha  == 'esquerda':
            self.rect.center = ((1024 + 380), HEIGHT - self.rect.height)
        elif escolha == 'direita':
            self.rect.center = ( - 380, HEIGHT - self.rect.height)
        self.isjump = False
        self.isnear = False

        self.fliped = pg.transform.flip(self.image, True, False)

        self.attributes = {
            'MAXHP': 35 * (stage // 2),
            'HP': 10 * stage,
            'ATT': 5 * stage,
            'DEF': 1 * stage,
            'SCORE': 25 * stage
            }
        if self.attributes['HP'] > self.attributes['MAXHP']: self.attributes['HP'] = self.attributes['MAXHP']

    def jump(self):
        self.isjump = True
        if self.rect.bottom >= HEIGHT:
            self.y_ = -10

    def calc_grav(self):
        """ Calcula o efeito da gravidade. """

        if self.y_ == 0:
            self.y_ = 1
        else:
            self.y_ += .45

        if self.rect.y >= HEIGHT - self.rect.height and self.y_ >= 0:
            self.y_ = 0
            self.isjump = False
            self.rect.y = HEIGHT - self.rect.height

    def update(self):
        self.calc_grav()
        self.rect.y += self.y_
        print(self.attributes)
        #Movimentação do inimigo
        if self.rect.center[0] > self.player.rect.center[0] + 15:
            self.rect.x -= self.x_
            self.facing = 'esquerda'
        elif self.rect.center[0] < self.player.rect.center[0] + 15:
            self.rect.x += self.x_
            self.facing = 'direita'
        elif self.rect.center[0] != self.player.rect.center[0] + 15:
            self.rect.x += self.x_
            self.facing = 'direita'

        #if self.player.rect.center[0] - 15 < self.rect.center[0] >= self.player.rect.center[0] + 15 and not self.isjump:
        #    self.jump()

        if self.frame_c <= 0:
            self.contador = (self.contador + 1) % len(self.all_images)
            self.image.set_alpha(255)
            self.image.fill(0)
            self.image = pg.transform.flip(pg.image.load(self.all_images[self.contador]), True, False) if self.facing == 'direita' else pg.image.load(self.all_images[self.contador])
            self.frame_c = FPS
        else:
            self.frame_c -= 3.652

    def morre(self, all_sprites, sprites_group, player=False):
        if player:
            a = random.randint(0,21)
            valido = ['HP', 'ATQ', 'DEF']
            if a <= 6:
                escolha = Objects(random.choice(valido), self.rect.center, self.player)
                all_sprites.add(escolha)
                sprites_group.add(escolha)
        self.kill()


class Objects(pg.sprite.Sprite):
    def __init__(self, types, location, player):
        pg.sprite.Sprite.__init__(self)
        self.player = player
        self.types = types
        if types == 'HP':
            self.image = pg.image.load('data/image/objects/life.png')
            self.image = pg.transform.scale(self.image, (25, 25))
        elif types == 'ATQ':
            self.image = pg.image.load('data/image/objects/atq.png')
            self.image = pg.transform.scale(self.image, (25, 25))
        else:
            self.image = pg.image.load('data/image/objects/shield.jpg')
            self.image = pg.transform.scale(self.image, (25, 25))


        self.image.set_colorkey((255,255,255))
        self.image = self.image.convert_alpha()
        self.mask = pg.mask.from_surface(self.image)
        self._imagem = self.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = location

        self.y_ = -4
        self.life = 0

    def pega(self):
        rand = random.randint(1, random.randint(2, 20))
        if self.types == 'HP':
            if self.player.attributes['HP'] + rand < self.player.attributes['MAXHP']:
                self.player.attributes['HP'] += rand
        elif self.types == 'ATQ':
            self.player.attributes['ATT'] += rand
        else:
            self.player.attributes['DEF'] += rand
        self.kill()

    def calc_grav(self):
        """ Calcula o efeito da gravidade. """
        if self.y_ == 0:
            self.y_ = 1
        else:
            self.y_ += .45

        if self.rect.y >= HEIGHT - self.rect.height and self.y_ >= 0:
            self.y_ = 0
            self.rect.y = HEIGHT - self.rect.height

    def update(self):
        self.calc_grav()
        self.rect.y += self.y_
        if self.life >= 300:
            self.kill()
            self.life = 0
        else:
            self.life += 1


class Bala(pg.sprite.Sprite):
    def __init__(self, position, velo, fromface, Flip=None):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('data/QtiroFOIesse.png')
        self.image.set_colorkey((255,255,255))
        self.image = self.image.convert_alpha()
        self.mask = pg.mask.from_surface(self.image)
        self._imagem = self.image
        self.fromface = fromface
        if Flip:
            self.image = pg.transform.flip(self.image, Flip[0], Flip[1])
        else:
            self.image = pg.transform.flip(self.image, False, False)

        self.image = pg.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position
        (self.x_, self. y_) = velo
        self.life = 0

    def update(self):
        self.rect.x += self.x_
        self.rect.y += self.y_
        if self.rect.left > WIDTH and self.fromface == 'direita':
            self.kill()
        elif self.rect.left < -75 and self.fromface == 'esquerda':
            self.kill()
        elif self.rect.left < -75 and self.fromface == 'cima':
            self.kill()
        elif self.life > 123:
            self.kill()
        else:
            self.life += 1


class Player(pg.sprite.Sprite):

    def __init__(self, screen):
        pg.sprite.Sprite.__init__(self)
        self.sp = pg.image.load("data/image/persons.png")
        self.sp.set_colorkey((255,255,255))
        self.sp = self.sp.convert_alpha()

        self.all_images = {
            0: (111, 323, 27, 89)
            }

        #self.walking_images = {
            #0: (257, 135, 28, 91), # ( self.all_images[self.contador])
            #1: (291, 135, 19, 89),
            #2: (326, 135, 28, 91),
            #3: (359, 135, 28, 91)
            #}



        self.walking_images = {
            0: (45, 323, 19, 89), # ( self.all_images[self.contador])
            1: (71, 323, 28, 91)
            }
        self.contador = 0
        self.image = pg.Surface((28, 91), pg.SRCALPHA, 32).convert_alpha()
        self.o_image = pg.Surface((28, 91), pg.SRCALPHA, 32).convert_alpha()
        self.left_image = pg.transform.flip(self.image, True, False)
        self.image.blit(self.sp, (0, 0), self.all_images[self.contador])
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (164, 476)
        self.frame_c = FPS

        self.invencibilidade = False
        self.contador_inv = 300

        self.facing = 'direita'

        self.x_ = 0
        self.y_ = 0

        self.isjump = False
        self.afk = 0

        self.attributes = {
            "HP": 25,
            "MAXHP":25,
            "ATT": 6,
            "DEF": 1,
            "SCORE": 0,
            "CANULT": False,
            "ULT": 0
            }

    def atira(self, all_sprites, sprites_group):
        if len(sprites_group) == 1: return
        if self.facing == 'direita':
            bala = Bala((self.rect.center[0], self.rect.center[1] - 25), (20, 0), self.facing)
        elif self.facing == 'esquerda':
            bala = Bala((self.rect.center[0], self.rect.center[1] - 25), (-20, 0),
                        self.facing)

        all_sprites.add(bala)
        sprites_group.add(bala)
        self.afk = 0

    def calc_grav(self):
        """ Calcula o efeito da gravidade. """
        if self.y_ == 0:
            self.y_ = 1
        else:
            self.y_ += .45

        # para não dar uma de lince negra
        if self.rect.y >= HEIGHT - self.rect.height and self.y_ >= 0:
            self.y_ = 0
            self.isjump = False
            self.rect.y = HEIGHT - self.rect.height

    def jump(self):
        self.isjump = True
        if self.rect.bottom >= HEIGHT:
            self.y_ = -12.45
        self.afk = 0

    def go_left(self):
        if self.facing == 'direita':
            self.image = self.left_image

        self.facing = 'esquerda'
        self.x_ = -4
        self.afk = 0

    def go_right(self):
        if self.facing == 'esquerda':
            self.image = self.o_image
        self.facing = 'direita'

        self.x_ = 4
        self.afk = 0

    def stop(self, continua):
        self.x_ = continua

    def chargeUlt(self, n):
        if self.attributes['ULT'] < 100:
            self.attributes['ULT'] += int(n)
        elif self.attributes['ULT'] > 100:
            self.attributes['ULT'] = 100

    def ulta(self):
        if self.attributes['ULT'] < 100: return False
        else:
            pass

    def update(self):
        self.calc_grav()
        self.rect.x += self.x_
        self.rect.y += self.y_
        if self.afk < 242:
            self.afk += 1

        if self.x_ in [2, -2] and self.isjump == False:
            self.x_ = 0

        if self.x_ not in [2, 0, -2]:
            if self.frame_c <= 0:
                self.contador = (self.contador + 1) % len(self.walking_images)
                self.image.set_alpha(255)
                self.image.fill(0)
                self.image.blit(self.sp, (0, 0), self.walking_images[self.contador])
                self.image = pg.transform.flip(self.image, True, False) if self.facing == 'direita' else self.image
                self.frame_c = FPS
            else:
                self.frame_c -= 2.5

        elif self.x_ == 0:
            if self.afk < 242:
                self.image.fill(0)
                self.image.blit(self.sp, (0, 0), self.walking_images[0])
                self.image = pg.transform.flip(self.image, True, False) if self.facing == 'direita' else self.image
            else:
                self.image.fill(0)
                self.image.blit(self.sp, (0, 0), self.all_images[0])

        self.frame_c -= 1

        if self.invencibilidade:
            self.contador_inv -= 1

            if self.contador_inv <= 0:
                self.invencibilidade = False
                self.contador_inv = 150

        if self.invencibilidade:
            self.contador_inv -= 1

            if self.contador_inv <= 0:
                self.contador_inv = 150
                self.invencibilidade = False

            for _ in range(20):
                if self.contador_inv <= _ * 30 and self.contador_inv > (_ - 1) * 30 and _ % 2 != 0:
                    self.image.fill(0)
