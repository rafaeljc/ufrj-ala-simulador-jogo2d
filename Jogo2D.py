'''

ALA Simulador Jogo2D
https://github.com/rafaeljc/ala-simulador-jogo2d

'''

# instalação:   python3 -m pip install --user numpy
import numpy as np

# instalação:   python3 -m pip install -U pygame --user
import pygame, sys
from pygame.locals import *



'''
CONSTANTES
'''
# cores (em RGB)
VERMELHO = (255, 0, 0)
PRETO = (0, 0, 0)

# configurações
TELA_TITULO = 'ALA 2019.2 - Simulador Jogo2D'
TELA_LARGURA = 800
TELA_ALTURA = 600
FPS = 15
COR_FUNDO = PRETO



'''
NAVE
'''
class Nave:

    def __init__(self):
        # vértices que formam a nave
        self.vertices = np.array([[385., 400., 415., 400., 385.],
                                  [310., 280., 310., 300., 310.],
                                  [1.,   1.,   1.,   1.,   1.  ]])
        # centro da nave
        self.centro = np.array([[400.], 
                                [300.],
                                [1.  ]])
        # vetor que orienta a movimentação da nave
        # módulo vetor: velociade da nave
        self.orientacao = np.array([[0.],
                                    [1.],
                                    [1.]])
        # largura traço da nave
        self.traco_largura = 3
        # cor traço da nave
        self.traco_cor = VERMELHO
        # desenha a nave na tela ligando os vértices

    def desenha(self):
        quantidade_colunas = self.vertices.shape[1]
        for i in range(quantidade_colunas - 1):
            ponto_inicial = (self.vertices[0,i], self.vertices[1,i])
            ponto_final = (self.vertices[0,i+1], self.vertices[1,i+1])
            pygame.draw.line(DISPLAYSURF, self.traco_cor, ponto_inicial, ponto_final, self.traco_largura)
        return



def main():

    iniciar()

    while True:
        jogar()



def iniciar():

    global FPSCLOCK, DISPLAYSURF, nave

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pygame.display.set_caption(TELA_TITULO)
    nave = Nave()   # instancia a nave



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

        # atualiza tela
        DISPLAYSURF.fill(COR_FUNDO)
        nave.desenha()
        pygame.display.update()
        FPSCLOCK.tick(FPS)



def sair():
    pygame.quit()
    sys.exit()



if __name__ == '__main__':
    main()