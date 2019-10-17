
# instalação:   python3 -m pip install --user numpy
import numpy as np

# instalação:   python3 -m pip install -U pygame --user
import pygame, sys
from pygame.locals import *

from constantes import *
from objetos import *



def main():

    global FPSCLOCK, DISPLAYSURF

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pygame.display.set_caption(TELA_TITULO)

    while True:
        jogar()



def jogar():

    # loop principal
    while True:
        # lidando com os eventos
        for event in pygame.event.get():
            if event.type == QUIT:
                sair()
            elif event.type == KEYDOWN:
                if event.key == K_x:
                    sair()

        v = np.array([[10.0, 50.0], 
                      [10.0, 50.0]])

        DISPLAYSURF.fill(COR_FUNDO)
        pygame.draw.line(DISPLAYSURF, VERMELHO, v[:,0], v[:,1], 5)
        pygame.display.update()
        FPSCLOCK.tick(FPS)



def sair():
    pygame.quit()
    sys.exit()



if __name__ == '__main__':
    main()