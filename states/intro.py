import pygame as pg
from fsm import *
from config import *

class SplashScreen(BaseState):
    def __init__(self):
        super(SplashScreen, self).__init__()
        #pg.sprite.Sprite.__init__(self)

        self.all_images = ["recursos/loading/jorge/{}.png".format(i) for i in range(0,8)]
        self.contador = 0
        self.next_state = "GAMEPLAY"
        self.image = pg.image.load(self.all_images[self.contador])
        self.image = pg.transform.scale(self.image, (72,112))
        # pg.draw.line(self.image, (255, 255, 0), (0, 0), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH /2, HEIGHT /2)
        self.frame_c = FPS
        
        #font
        self.fontObj = pg.font.Font('recursos/fonts/pixelmix.ttf', 26)
        self.textSurfaceObj = self.fontObj.render('The ashes of Jorge', True, (0,0,0))
        self.fontObj = pg.font.Font('recursos/fonts/pixelmix.ttf', 14)
        self.loadingObj = self.fontObj.render('carregando', True, (0,0,0))
        self.textRectObj = self.textSurfaceObj.get_rect()
        self.loadingRectObj = self.loadingObj.get_rect()
        self.textRectObj.center  = ((WIDTH /2), (HEIGHT /2) - 89)
        self.loadingRectObj.center  = ((WIDTH /2), (HEIGHT /2) + 99)
        #
        self.doto = 1
        self.timo = 0

    def update(self, dt):
        self.timo += dt
        if self.timo > 1500: #por tempo, por agora
            self.timo = 0
            self.done = True

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
            self.done = True
    
    def draw(self, surface):
        if self.frame_c <= 0:
            self.contador = (self.contador + 1) % len(self.all_images)
            self.image = pg.image.load(self.all_images[self.contador])
            self.image = pg.transform.scale(self.image, (72,112))
            self.image = pg.transform.flip(self.image, True, False)
            self.loadingObj = self.fontObj.render('carregando{}'.format('.'*self.doto), True, (0,0,0))
            self.doto += 1 if self.doto < 3 else -1
            self.frame_c = FPS
        self.frame_c -= 4

        surface.fill(pg.Color("white"))
        surface.blit(self.textSurfaceObj, self.textRectObj)
        surface.blit(self.loadingObj, self.loadingRectObj)
        surface.blit(self.image, self.rect)   