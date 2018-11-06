import pygame as pg
from fsm import *
from config import *


class Bala(pg.sprite.Sprite):
    def __init__(self, position, velo, fromface, Flip=None):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('recursos/QtiroFOIesse.png')
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


class Player(pg.sprite.Sprite):

    def __init__(self, screen):
        pg.sprite.Sprite.__init__(self)
        self.sp = pg.image.load("recursos/image/jude and jorge.png")
        self.all_images = {
            0: (219, 135, 28, 91),
            1: (257, 135, 28, 91),
            2: (291, 135, 28, 91),
            3: (326, 135, 28, 91)
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
            self.y_ += .4558949845132156748979756132

        # está no chao?
        if self.rect.y >= HEIGHT - self.rect.height and self.y_ >= 0:
            self.y_ = 0
            self.isjump = False
            self.rect.y = HEIGHT - self.rect.height

    def jump(self):
        self.isjump = True
        if self.rect.bottom >= HEIGHT:
            self.y_ = -10

    def go_left(self):
        self.image = pg.transform.flip(self.image, True, False) if self.facing in [
            'direita', 'cima'] else self.image
        self.facing = 'esquerda'
        self.x_ = -3

    def go_right(self):
        self.image = pg.transform.flip(self.image, True, False) if self.facing in [
            'esquerda', 'cima'] else self.image
        self.facing = 'direita'
        self.x_ = 3

    def stop(self):
        self.x_ = 0

    def update(self):
        self.calc_grav()
        self.rect.x += self.x_
        self.rect.y += self.y_

        if self.x_ in [2, -2] and self.isjump == False:
            self.x_ = 0

        if self.rect.left > WIDTH - 50:
            self.rect.right = -50

        if self.frame_c <= 0:
            self.contador = (self.contador + 1) % len(self.all_images)
            self.image.blit(self.sp, (0, 0), self.all_images[self.contador])
            self.frame_c = FPS
        else:
            self.frame_c -= 1.652

        self.frame_c -= 1

        # Motimentação
        r'''
        pressed = pg.key.get_pressed()
        if pressed[pg.K_d]:
            self.facing = 'direita'
            self.rect.x += 6
        elif pressed[pg.K_a]:
            self.facing = 'esquerda'
            self.rect.x -= 6
        elif pressed[pg.K_s]:
            self.facing = None
            self.rect.y += 7
        elif pressed[pg.K_w]:
            self.facing = 'cima'
            self.rect.y -= 10
            ##usado pra animar
            if self.frame_c <= 0:
                self.contador = (self.contador + 1) % len(self.all_images)
                self.image = pg.image.load(self.all_images[self.contador])
                self.image = pg.transform.scale(self.image, (72,112))
                self.image = pg.transform.flip(self.image, True, False)
                self.frame_c = FPS
            else:
                self.frame_c -= 10
        '''


class Gameplay(BaseState):
    def __init__(self):
        super(Gameplay, self).__init__()
        self.rect = pg.Rect((0, 0), (128, 128))
        self.x_velocity = 1
        self.fundo = pg.image.load('recursos/image/CENARIO.png')
        self.fundoX, self.fundoY = self.fundo.get_rect().size
        self.fundo = pg.transform.scale(self.fundo, (self.fundoX + 25, self.fundoY + 25))

        self.startScrollingPosX = WIDTH * .3
        self.stagePosX = 0
        self.stageWidth = self.fundoX + 123

    def startup(self, persistent):
        self.all_sprites = pg.sprite.Group()
        self.balas = pg.sprite.Group()
        self.player = Player(self.screen_rect)
        self.all_sprites.add(self.player)

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.quit()

            if event.key == pg.K_DOWN:
                self.player.atira(self.all_sprites, self.balas)

            # if event.key == pg.K_w:
            #    self.player.facing = 'cima'
            if event.key == pg.K_LEFT:
                self.player.go_left()
            if event.key == pg.K_RIGHT:
                self.player.go_right()
            if event.key == pg.K_UP:
                self.player.jump()

        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT and self.player.x_ < 0:
                self.player.x_ = -2
            if event.key == pg.K_RIGHT and self.player.x_ > 0:
                self.player.x_ = 2

    def update(self, dt):
        for i in self.balas:
            if i.rect.left > WIDTH and i.fromface == 'direita':
                i.kill()
            elif i.rect.left < -75 and i.fromface == 'esquerda':
                i.kill()
            elif i.rect.left < -75 and i.fromface == 'cima':
                i.kill()
            elif i.life > 123:
                i.kill()
            else:
                i.life += 1

    def draw(self, surface):

        if self.player.rect.left <= 0:
            self.player.rect.x = 0

        if self.player.rect.x < self.stageWidth - self.startScrollingPosX:
            self.stagePosX -= self.player.x_ // 2

        rel_x = self.stagePosX % self.fundoX
        surface.blit(self.fundo, (rel_x - self.fundoX, -240))
        if rel_x < WIDTH: # acontinuação do fundo
            surface.blit(self.fundo, (rel_x, -240))


        self.all_sprites.update()
        self.all_sprites.draw(surface)
