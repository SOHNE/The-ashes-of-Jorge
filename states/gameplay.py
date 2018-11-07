from __future__ import print_function
import os
import pygame as pg
from fsm import *
from config import *

#pid = os.getpid()
#py = psutil.Process(pid)

class Inimigo(pg.sprite.Sprite):
    def __init__(self, position, player):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('recursos/zumbi.jpg').convert_alpha()
        self.rect = self.image.get_rect()

    def update(self):
        pass
        '''
        if rect.x > rectRocket.x:
            rectUFO.x -= velocidade
        else:
            rectUFO.x += velocidade

        if rectUFO.y > rectRocket.y:
            rectUFO.y -= velocidade
        else:
            rectUFO.y += velocidade
            '''
    def move(self):
        pass

class Bala(pg.sprite.Sprite):
    def __init__(self, position, velo, fromface, Flip=None):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('recursos/QtiroFOIesse.png').convert_alpha()
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
        self.sp = pg.image.load("recursos/image/jude and jorge.png").convert_alpha()
        self.all_images = {
            0: (219, 135, 28, 91)
            #0: (257, 135, 28, 91),
            #1: (291, 135, 28, 91),
            #2: (326, 135, 28, 91),
            #3: (359, 135, 28, 91)
            }
        self.walking_images = {
            0: (257, 135, 28, 91),
            1: (291, 135, 28, 91),
            2: (326, 135, 28, 91),
            3: (359, 135, 28, 91)
            }
        self.contador = 0
        self.image = pg.Surface((28, 91))
        self.image.blit(self.sp, (0, 0), self.all_images[self.contador])
        self.rect = self.image.get_rect()
        self.rect.center = (164, 476)
        self.frame_c = FPS

        self.facing = 'direita'

        self.x_ = 0
        self.y_ = 0

        self.isjump = False
        self.afk = 0

        self.attributes = {
            "HP": 0,
            "MAXHP":5,
            "ATQ": 0,
            "DEF": 0
            }
    def atira(self, all_sprites, sprites_group):
        if self.facing == 'direita':
            bala = Bala(self.rect.center, (20, 0), self.facing)
        elif self.facing == 'esquerda':
            bala = Bala(self.rect.center, (-20, 0),
                        self.facing, Flip=(True, True))
        elif self.facing == 'cima':
            bala = Bala(self.rect.center, (0, -20),
                        self.facing, Flip=(False, False))
        all_sprites.add(bala)

        sprites_group.add(bala)

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
            self.y_ = -10
        self.afk = 0

    def go_left(self):
        self.image = pg.transform.flip(self.image, True, False) if self.facing in [
            'direita', 'cima'] else self.image
        self.facing = 'esquerda'
        self.x_ = -4
        self.afk = 0

    def go_right(self):
        self.image = pg.transform.flip(self.image, True, False) if self.facing in [
            'esquerda', 'cima'] else self.image
        self.facing = 'direita'
        self.x_ = 4
        self.afk = 0

    def stop(self, continua):
        self.x_ = continua
        if not self.isjump:
            self.image.blit(self.sp, (0, 0), self.all_images[0])

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
                self.image.blit(self.sp, (0, 0), self.walking_images[self.contador])
                self.frame_c = FPS
            else:
                self.frame_c -= 3.652

        elif self.x_ == 0:
            if self.afk < 242:
                self.image.blit(self.sp, (0, 0), self.walking_images[0])
            else:
                self.image.blit(self.sp, (0, 0), self.all_images[0])

        self.frame_c -= 1


class Gameplay(BaseState):
    def __init__(self):
        super(Gameplay, self).__init__()
        self.rect = pg.Rect((0, 0), (128, 128))
        self.x_velocity = 1
        self.fundo = pg.image.load('recursos/image/CENARIO.png').convert_alpha()
        self.fundoX, self.fundoY = self.fundo.get_rect().size


        self.stage = {
            "X": 0, #coordenada x
            "W": self.fundoX, # tamanho
            "I": (HEIGHT / 2) + 156 # inicio do scroll
            }

    def startup(self, persistent):
        self.all_sprites = pg.sprite.Group()
        self.balas = pg.sprite.Group()
        self.player = Player((2,1))
        #self.inimigos = Inimigo
        #self.all_sprites.add(self.inimigos)
        self.all_sprites.add(self.player)

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.done = True

            if event.key == pg.K_k:
                self.player.atira(self.all_sprites, self.balas)

            # if event.key == pg.K_w:
            #    self.player.facing = 'cima'
            if event.key == pg.K_a:
                self.player.go_left()
            if event.key == pg.K_d:
                self.player.go_right()
            if event.key == pg.K_SPACE:
                self.player.jump()

        if event.type == pg.KEYUP:
            if event.key == pg.K_a and self.player.x_ < 0:
                self.player.stop(-2)
            if event.key == pg.K_d and self.player.x_ > 0:
                self.player.stop(2)

    def update(self, dt):
        pass

    def draw(self, surface):

        if self.player.rect.x <= 0:
            self.player.rect.x = 0
        elif self.player.rect.x >= WIDTH - self.player.rect.size[0]:
            self.player.rect.x = WIDTH - self.player.rect.size[0]

        elif self.player.rect.x > self.stage['I'] and (self.player.rect.x < self.stage['W'] - self.stage['I']):
            self.stage['X'] += - self.player.x_ / 2

        surface.blit(self.fundo, (self.stage['X'], -250))


        self.all_sprites.update()
        self.all_sprites.draw(surface)
