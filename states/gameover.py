# -*- coding: utf-8 -*-

import pygame as pg
from fsm import *
from config import *

class Over(BaseState):
    def __init__(self):
        super(Over, self).__init__()
        self.title = self.font.render(
            "Game Over", True, pg.Color("white"), 36)

        self.titleRect = self.title.get_rect()
        self.titleRect.center = (WIDTH / 2, HEIGHT / 2)
        self.next_state = "SPLASH"


    def startup(self, persist):
        self.score = self.font.render("{} pontos".format(persist['score']), True, pg.Color("red"))
        self.scoreRect = self.score.get_rect()
        self.scoreRect.center = (WIDTH / 2, (HEIGHT / 2) + 95)

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                self.done = True
            elif event.key == pg.K_ESCAPE:
                self.quit = True

    def draw(self, surface):
        surface.fill(pg.Color("black"))
        surface.blit(self.title, self.titleRect)
        surface.blit(self.score, self.scoreRect)