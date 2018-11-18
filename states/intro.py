import pygame as pg
from fsm import *
from config import *
#from resource_manager import *

class SplashScreen(BaseState):
    def __init__(self):
        super(SplashScreen, self).__init__()
        #pg.sprite.Sprite.__init__(self)

        self.all_images = ["data/loading/jorge/{}.png".format(i) for i in range(0,8)]
        self.contador = 0
        self.next_state = "GAMEPLAY"
        self.image = pg.image.load(self.all_images[self.contador])
        self.image = pg.transform.scale(self.image, (72,112))
        # pg.draw.line(self.image, (255, 255, 0), (0, 0), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH /2, HEIGHT /2)
        self.frame_c = FPS
        
        #font
        self.fontObj = pg.font.Font('data/fonts/pixelmix.ttf', 26)
        self.titleObj = self.fontObj.render('The ashes of Jorge', True, (0,0,0))
        self.fontObj = pg.font.Font('data/fonts/pixelmix.ttf', 14)
        self.enterObj = self.fontObj.render('Pressione ENTER/RETURN para jogar', True, (0,0,0))
        self.escObj = self.fontObj.render('Pressione ESC para sair', True, (0,0,0))
        self.anoObj = self.fontObj.render('2018 -- Leandro, Victoria, Dyego Marques', True, (0,0,0))

        self.titleRect = self.titleObj.get_rect()
        self.enterRect = self.enterObj.get_rect()
        self.escRect = self.enterObj.get_rect()
        self.anoRect = self.enterObj.get_rect()

        self.escRect.center  = ((WIDTH /2), (HEIGHT /2) + 120)
        self.enterRect.center  = ((WIDTH /2), (HEIGHT /2) + 99)
        self.titleRect.center  = ((WIDTH /2), (HEIGHT /2) - 89)
        #
        self.doto = 1

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
            self.done = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self.done = True
            if event.key == pg.K_ESCAPE:
                self.quit = True
    
    def draw(self, surface):
        if self.frame_c <= 0:
            self.contador = (self.contador + 1) % len(self.all_images)
            self.image = pg.image.load(self.all_images[self.contador])
            self.image = pg.transform.scale(self.image, (72,112))
            self.image = pg.transform.flip(self.image, True, False)
            self.doto += 1 if self.doto < 3 else -1
            self.frame_c = FPS
        self.frame_c -= 4

        surface.fill(pg.Color("white"))
        surface.blit(self.titleObj, self.titleRect)
        surface.blit(self.enterObj, self.enterRect)
        surface.blit(self.enterObj, self.enterRect)
        surface.blit(self.escObj, self.escRect)
        surface.blit(self.anoObj, self.anoRect)
        surface.blit(self.image, self.rect)   