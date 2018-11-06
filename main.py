#This code is licensed under GPLv3.

import sys
import pygame as pg
import fsm #finite state machine
from states.intro import *
from states.gameplay import *
from config import *
    
#conexão com o servidor aqui
    
if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    states = {"SPLASH": SplashScreen(),
              "GAMEPLAY": Gameplay()
              }
    game = fsm.Game(screen, states, "SPLASH")
    game.run()
    pg.quit()
    sys.exit()