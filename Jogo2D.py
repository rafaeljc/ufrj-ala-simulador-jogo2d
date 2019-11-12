'''
Álgebra Linear Algorítmica 2019.2   -   Simulador Jogo2D

Descrição:  Simulador de jogo 2D no qual seus objetos são movimentados na tela utilizando apenas multiplicação de matrizes

Aluno:      Rafael Jordão Clemente
DRE:        118172210

Projeto:    Gráficos 2D e transformações
Colab:      https://colab.research.google.com/drive/1YWCrNh5y9L8RqA9gebt-a3MNNziOHw3K
GitHub:     https://github.com/rafaeljc/ala-simulador-jogo2d
'''

# importações necessárias para executar o programa
import numpy as np

import pygame, sys
from pygame.locals import *



'''
CONSTANTES
'''
# definição das cores (em RGB)
PRETO = (0, 0, 0)
CINZA = (166, 166, 166)
VERDE = (45, 253, 4)

# configurações do simulador
TELA_TITULO = 'ALA 2019.2 - Simulador Jogo2D'
TELA_LARGURA = 800
TELA_ALTURA = 600
TELA_COR_FUNDO = PRETO
TELA_FPS = 15   # taxa de atualização da tela (em quadros por segundo)

# configurações da nave
NAVE_TRACO_LARGURA = 2
NAVE_TRACO_COR = CINZA
NAVE_ROTACAO_ANGULO = np.pi / 64    # em radianos

# configurações do projétil
PROJETIL_TRACO_LARGURA = 1
PROJETIL_TRACO_COR = VERDE
PROJETIL_VELOCIDADE = 20
PROJETIL_DURACAO = 50   # por quantos 'ciclos' o projétil irá existir



'''
NAVE
'''
class Nave:

    # rotina de iniciação de uma nova nave
    def __init__(self):
        # define os vértices que formam a nave
        self.vertices = np.array([[5., 2.,  0.,  0.,   2.,   5.,   28.,  28.,  40.,  43.,  48.,  52.,  72.,  76.,  81.,  84.,  96.,  96.,  119., 122., 124., 124., 122., 119., 96., 96., 84., 81., 75., 70., 62., 54., 49., 43., 40., 28., 28., 5.], 
                                  [0., 92., 96., 105., 109., 147., 127., 107., 109., 113., 118., 126., 126., 118., 113., 109., 107., 127., 147., 109., 105., 96.,  92.,  0.,   87., 94., 92., 87., 81., 78., 77., 78., 81., 87., 92., 94., 87., 0.], 
                                  [1., 1.,  1.,  1.,   1.,   1.,   1.,   1.,   1.,   1.,   1.,   1.,   1.,   1.,   1.,   1.,   1.,   1.,   1.,   1.,   1.,   1.,   1.,   1.,   1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.]])
        # define o centro da nave
        self.centro = np.array([[62.], 
                                [100.],
                                [1.  ]])
        # define o vetor que orienta a movimentação da nave
        # módulo do vetor: velociade da nave
        self.orientacao = np.array([[0.],
                                    [-4.],
                                    [1.]])
        # define a largura do traço que a nave será desenhada
        self.traco_largura = NAVE_TRACO_LARGURA
        # define a cor do traço da nave
        self.traco_cor = NAVE_TRACO_COR
        # ajusta o tamanho da nave
        self.escala(0.5)    # reduz à metade
        # ajusta posição da nave para o centro da tela
        # calcula o vetor diferença entre o centro da tela e o centro da nave
        # e depois a move
        pro_centro_tela = np.array([[ (TELA_LARGURA / 2) - self.centro[0,0] ],
                                    [ (TELA_ALTURA / 2) - self.centro[1,0] ],
                                    [ 1. ]])
        self.move(pro_centro_tela)
        
    # desenha a nave na tela traçando retas entre os vértices que a formam
    def desenha(self):
        quantidade_colunas = self.vertices.shape[1]
        for i in range(quantidade_colunas - 1):
            ponto_inicial = (self.vertices[0,i], self.vertices[1,i])
            ponto_final = (self.vertices[0,i+1], self.vertices[1,i+1])
            pygame.draw.line(DISPLAYSURF, self.traco_cor, ponto_inicial, ponto_final, self.traco_largura)
        return

    # altera o tamanho da nave
    # gera a matriz de transformação com base no vetor centro e depois
    # a aplica na matriz dos vértices que compõem a nave
    def escala(self, valor):
        escala_centro = matrizEscalaPontoArbitrario(valor, self.centro)
        self.vertices = escala_centro @ self.vertices
        return

    # gira a nave um determinado ângulo
    # gera as matrizes de transformação, rotação e rotação em um ponto (centro da nave)
    # e as aplica, respectivamente, na matriz dos vértices que compõem a nave e no vetor
    # orientação da nave (nesse vetor, não foi aplicada a rotação em um ponto arbitrário
    # pois ele sempre estará na origem)
    def rotacao(self, angulo):
        rotacao = matrizRotacao(angulo)
        rotacao_centro = matrizRotacaoPontoArbitrario(angulo, self.centro)
        self.vertices = rotacao_centro @ self.vertices
        self.orientacao = rotacao @ self.orientacao
        return
  
    # move a nave no sentido do seu vetor orientação
    # gera a matriz de transformação com base no vetor passado como parâmetro
    # e a aplica na matriz dos vértices que compõem a nave e no vetor centro
    def move(self, vetor):
        translacao = matrizTranslacao(vetor)
        self.vertices = translacao @ self.vertices
        self.centro = translacao @ self.centro
        return

    # efetua disparos
    def dispara(self):
        # os canhões são dois dos vértices da nave
        # coordenadas do canhão 1
        canhao1 = np.array([[self.vertices[0,29]],
                            [self.vertices[1,29]],
                            [1.]])
        # coordenadas do canhão 2
        canhao2 = np.array([[self.vertices[0,31]],
                            [self.vertices[1,31]],
                            [1.]])
        # gera os projéteis com base na posição dos canhões e vetor orientação da nave
        projetil1 = Projetil(canhao1, self.orientacao)
        projetil2 = Projetil(canhao2, self.orientacao)
        # após gerar os projéteis, armazene-os na lista de projéteis ativos
        # para que possam ser desenhados na tela
        projeteis.append(projetil1)
        projeteis.append(projetil2)
        return



'''
PROJÉTIL
'''
class Projetil:

    # rotina de iniciação de um novo projétil
    def __init__(self, ponto, vetor):
        # define os vértices do projétil
        self.vertices = np.array([[ponto[0,0], ponto[0,0] + vetor[0,0]],
                                  [ponto[1,0], ponto[1,0] + vetor[1,0]],
                                  [1.,         1.]])
        # define o vetor que orienta a movimentação do projétil
        self.orientacao = np.array([[PROJETIL_VELOCIDADE * vetor[0,0]], 
                                    [PROJETIL_VELOCIDADE * vetor[1,0]],
                                    [1.]])
        # define a largura do traço que o projétil será desenhado
        self.traco_largura = PROJETIL_TRACO_LARGURA
        # define a cor traço do projétil
        self.traco_cor = PROJETIL_TRACO_COR
        # inicia o contador de duração do projétil
        self.duracao = 0

    # desenha o projétil na tela traçando uma reta entre os vértices que o formam
    def desenha(self):
        quantidade_colunas = self.vertices.shape[1]
        for i in range(quantidade_colunas - 1):
            ponto_inicial = (self.vertices[0,i], self.vertices[1,i])
            ponto_final = (self.vertices[0,i+1], self.vertices[1,i+1])
            pygame.draw.line(DISPLAYSURF, self.traco_cor, ponto_inicial, ponto_final, self.traco_largura)
        return

    # move o projétil no sentido do seu vetor orientação
    # gera a matriz de transformação com base no vetor orientação do projétil
    # e a aplica na matriz dos vértices que compõem o projétil e, após isso,
    # incrementa o contador de duração
    def move(self):
        translacao = matrizTranslacao(self.orientacao)
        self.vertices = translacao @ self.vertices
        self.duracao += 1
        return



'''
SIMULADOR
'''
# função 'main'
def main():
    iniciar()
    jogar()


# função que executa a rotina de iniciação do programa
def iniciar():

    global FPSCLOCK, DISPLAYSURF, nave, projeteis

    pygame.init()   # inicia o pygame
    FPSCLOCK = pygame.time.Clock() # inicia o relógio que será utilizado para controlar a taxa de atualização da tela
    DISPLAYSURF = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))  # cria a tela
    pygame.display.set_caption(TELA_TITULO) # define o título da tela

    nave = Nave()   # instancia a nave
    projeteis = []    # inicia array no qual serão colocados os projeteis


# função que executa o 'jogo'
def jogar():

    # loop principal
    while True:
        # lidando com os eventos
        for event in pygame.event.get():

            if event.type == QUIT:      # encerra o programa se fechar a janela
                sair()

            # se alguma tecla for pressionada...
            # nota: esse tipo de evento é ativado uma única vez, quando a tecla é pressionada,
            # mesmo que a tecla continue pressionada, não gerará um novo evento
            elif event.type == KEYDOWN:

                if event.key == K_x:    # tecla 'x':    encerra o programa
                    sair()

                elif event.key == K_SPACE:  # tecla 'espaço':   efetua disparo
                    nave.dispara()              

        # no caso das teclas direcionais, iremos checar diretamente o estado das teclas
        # para que possamos movimentar a nave com as teclas continuamente pressionadas
        # nota: na tela, o sentido positivo do eixo 'y' é para baixo, logo, ao chamar
        # os métodos de rotação, teremos que mudar o sinal do ângulo já que o sentido positivo
        # de rotação será o horário 
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

        # executa a movimentação dos objetos e depois atualiza a tela
        DISPLAYSURF.fill(TELA_COR_FUNDO)    # 'limpa' a tela
        # controla os projéteis  
        for p in projeteis:
            # remove os projéteis que ultrapassarem a duração máxima
            if p.duracao > PROJETIL_DURACAO:
                projeteis.remove(p)
                continue
            # desenha na tela
            # nota: foi escolhido desenhar o projétil antes de atualizar sua posição
            # para causar um efeito melhor no momento em que ele é disparado              
            p.desenha()
            # executa a movimentação
            p.move()        
        nave.desenha()
        pygame.display.update() # aplica as atualizações na tela
        FPSCLOCK.tick(TELA_FPS) # controla a taxa de atualização da tela



# função que executa a rotina de encerramento do programa
def sair():
    pygame.quit()   # encerra o pygame
    sys.exit()  # sai do programa



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
