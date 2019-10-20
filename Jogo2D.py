'''

ALA 2019.2 - Simulador Jogo2D
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
PRETO = (0, 0, 0)
CINZA = (166, 166, 166)
VERDE = (45, 253, 4)

# configurações
TELA_TITULO = 'ALA 2019.2 - Simulador Jogo2D'
TELA_LARGURA = 800
TELA_ALTURA = 600
TELA_COR_FUNDO = PRETO
TELA_FPS = 15

# configurações padrões da nave
NAVE_TRACO_LARGURA = 3
NAVE_TRACO_COR = CINZA
NAVE_ROTACAO_ANGULO = np.pi / 64      # na tela, o sentido positivo do eixo 'y' é para baixo, logo o sentido positivo de rotação é o horário

# configurações padrões do projétil
PROJETIL_TRACO_LARGURA = 2
PROJETIL_TRACO_COR = VERDE
PROJETIL_VELOCIDADE = 20
PROJETIL_DURACAO = 50



'''
NAVE
'''
class Nave:

    def __init__(self):
        # vértices que formam a nave
        self.vertices = np.array([[5., 2.,  0.,  0.,   2.,   5.,   28.,  28.,  40.,  43.,  48.,  52.,  72.,  76.,  81.,  84.,  96.,  96.,  119., 122., 124., 124., 122., 119., 96., 96., 84., 81., 75., 70., 62., 54., 49., 43., 40., 28., 28., 5.], 
                                  [0., 92., 96., 105., 109., 147., 127., 107., 109., 113., 118., 126., 126., 118., 113., 109., 107., 127., 147., 109., 105., 96.,  92.,  0.,   87., 94., 92., 87., 81., 78., 77., 78., 81., 87., 92., 94., 87., 0.], 
                                  [1., 1.,  1.,  1.,   1.,   1.,   1.,   1.,   1.,   1.,   1.,   1.,   1.,   1.,   1.,   1.,   1.,   1.,   1.,   1.,   1.,   1.,   1.,   1.,   1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.]])
        # centro da nave
        self.centro = np.array([[62.], 
                                [100.],
                                [1.  ]])
        # vetor que orienta a movimentação da nave
        # módulo vetor: velociade da nave
        self.orientacao = np.array([[0.],
                                    [-4.],
                                    [1.]])
        # largura traço da nave
        self.traco_largura = NAVE_TRACO_LARGURA
        # cor traço da nave
        self.traco_cor = NAVE_TRACO_COR
        # ajusta tamanho da nave
        self.escala(0.5)
        # ajusta posição da nave pro centro da tela
        pra_origem = np.array([[-self.centro[0,0]],
                               [-self.centro[1,0]],
                               [1.]])
        self.move(pra_origem)
        pro_centro_tela = np.array([[TELA_LARGURA / 2],
                                    [TELA_ALTURA / 2],
                                    [1.]])
        self.move(pro_centro_tela)
        
    # desenha a nave na tela ligando os vértices
    def desenha(self):
        quantidade_colunas = self.vertices.shape[1]
        for i in range(quantidade_colunas - 1):
            ponto_inicial = (self.vertices[0,i], self.vertices[1,i])
            ponto_final = (self.vertices[0,i+1], self.vertices[1,i+1])
            pygame.draw.line(DISPLAYSURF, self.traco_cor, ponto_inicial, ponto_final, self.traco_largura)
        return

    # altera o tamanho da nave
    def escala(self, valor):
        escala_centro = matrizEscalaPontoArbitrario(valor, self.centro)
        self.vertices = escala_centro @ self.vertices
        return

    # gira a nave um determinado ângulo
    def rotacao(self, angulo):
        rotacao = matrizRotacao(angulo)
        rotacao_centro = matrizRotacaoPontoArbitrario(angulo, self.centro)
        self.vertices = rotacao_centro @ self.vertices
        self.orientacao = rotacao @ self.orientacao
        return
  
    # move a nave no sentido do vetor orientação
    def move(self, vetor):
        translacao = matrizTranslacao(vetor)
        self.vertices = translacao @ self.vertices
        self.centro = translacao @ self.centro
        return

    # efetua disparos
    def dispara(self):
        # coordenadas do canhão 1
        canhao1 = np.array([[self.vertices[0,29]],
                            [self.vertices[1,29]],
                            [1.]])
        # coordenadas do canhão 2
        canhao2 = np.array([[self.vertices[0,31]],
                            [self.vertices[1,31]],
                            [1.]])
        projetil1 = Projetil(canhao1, self.orientacao)
        projetil2 = Projetil(canhao2, self.orientacao)
        projeteis.append(projetil1)
        projeteis.append(projetil2)
        return



'''
PROJÉTIL
'''
class Projetil:

    def __init__(self, ponto, vetor):

        # define vértices
        self.vertices = np.array([[ponto[0,0], ponto[0,0] + vetor[0,0]],
                                  [ponto[1,0], ponto[1,0] + vetor[1,0]],
                                  [1.,         1.]])
        # vetor que orienta a movimentação do projétil
        self.orientacao = np.array([[PROJETIL_VELOCIDADE * vetor[0,0]], 
                                    [PROJETIL_VELOCIDADE * vetor[1,0]],
                                    [1.]])
        # largura traço do projétil
        self.traco_largura = PROJETIL_TRACO_LARGURA
        # cor traço do projétil
        self.traco_cor = PROJETIL_TRACO_COR
        # duração do projétil
        self.duracao = 0

    # desenha o disparo na tela ligando os vértices
    def desenha(self):
        quantidade_colunas = self.vertices.shape[1]
        for i in range(quantidade_colunas - 1):
            ponto_inicial = (self.vertices[0,i], self.vertices[1,i])
            ponto_final = (self.vertices[0,i+1], self.vertices[1,i+1])
            pygame.draw.line(DISPLAYSURF, self.traco_cor, ponto_inicial, ponto_final, self.traco_largura)
        return

    # move o projétil no sentido da nave no momento do disparo
    def move(self):
        translacao = matrizTranslacao(self.orientacao)
        self.vertices = translacao @ self.vertices
        self.duracao += 1
        return



'''
SIMULADOR
'''
def main():

    iniciar()

    while True:
        jogar()



def iniciar():

    global FPSCLOCK, DISPLAYSURF, nave, projeteis

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pygame.display.set_caption(TELA_TITULO)

    nave = Nave()   # instancia a nave
    projeteis = []    # inicia array no qual serão colocados os projeteis



def jogar():

    # loop principal
    while True:
        # lidando com os eventos
        for event in pygame.event.get():

            if event.type == QUIT:      # encerra o programa se fechar a janela
                sair()

            elif event.type == KEYDOWN:

                if event.key == K_x:    # tecla 'x':    encerra o programa
                    sair()

                elif event.key == K_SPACE:  # tecla 'espaço':   efetua disparo
                    nave.dispara()              

        tecla_pressionada = pygame.key.get_pressed()
        if tecla_pressionada[K_w]:      # tecla 'w':    movimenta nave para frente
            nave.move(nave.orientacao)

        if tecla_pressionada[K_a]:      # tecla 'a':    gira nave no sentido anti-horário
            nave.rotacao(-NAVE_ROTACAO_ANGULO)

        if tecla_pressionada[K_s]:      # tecla 's':    movimenta nave para trás
            vetor = np.array([[-nave.orientacao[0,0]], 
                              [-nave.orientacao[1,0]], 
                              [1.0]])
            nave.move(vetor)

        if tecla_pressionada[K_d]:      # tecla 'd':    gira nave no sentido horário
            nave.rotacao(NAVE_ROTACAO_ANGULO)

        # atualiza tela
        DISPLAYSURF.fill(TELA_COR_FUNDO)        
        for p in projeteis:
            if p.duracao > PROJETIL_DURACAO:
                projeteis.remove(p)
                continue            
            p.desenha()
            p.move()        
        nave.desenha()
        pygame.display.update()
        FPSCLOCK.tick(TELA_FPS)



# instruções para encerrar o programa
def sair():
    pygame.quit()
    sys.exit()



'''
MATRIZES DE TRANSFORMAÇÃO
'''
def matrizTranslacao(vetor):  
    v1 = vetor[0,0]
    v2 = vetor[1,0]  
    return np.array([[1.0, 0.0, v1], 
                     [0.0, 1.0, v2], 
                     [0.0, 0.0, 1.0]])



def matrizRotacao(angulo):
    sin = np.sin(angulo)
    cos = np.cos(angulo)
    return np.array([[cos, -sin, 0.0], 
                     [sin, cos,  0.0], 
                     [0.0, 0.0,  1.0]])



def matrizRotacaoPontoArbitrario(angulo, ponto):
    sin = np.sin(angulo)
    cos = np.cos(angulo)
    p1 = ponto[0,0]
    p2 = ponto[1,0]
    return np.array([[cos, -sin, p1 + (p2 * sin) - (p1 * cos)], 
                     [sin, cos,  p2 - (p2 * cos) - (p1 * sin)], 
                     [0.0, 0.0,  1.0]])



def matrizEscalaPontoArbitrario(valor, ponto):
    x = valor
    p1 = ponto[0,0]
    p2 = ponto[1,0]
    return np.array([[x,  0., p1 - (p1 * x)],
                     [0., x,  p2 - (p2 * x)],
                     [0., 0., 1.]])



# inicia função 'main'
if __name__ == '__main__':
    main()
