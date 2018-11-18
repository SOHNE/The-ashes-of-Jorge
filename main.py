#This code is licensed under GPLv3.

import sys
import pygame as pg
import fsm #finite state machine
from states.intro import *
from states.gameplay import *
from states.gameover import *
from states.win import *
from config import *
    
#conexão com o servidor aqui

__authors__ = ["Leandro de Gonzaga Peres",
                "Dyego Marques Souza Costa",
                "Victoria Costa Oliveira"]

if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    states = {"SPLASH": SplashScreen(),
              "GAMEPLAY": Gameplay(),
              "OVER": Over(),
              "WIN": Win()
              }
    game = fsm.Game(screen, states, "SPLASH")
    game.run()
    pg.quit()
    sys.exit(0)