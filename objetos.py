'''
Objetos
'''

class Nave: 
  
  def __init__(self):
    # vértices que formam a nave
    self.vertices = np.array([[-2.5, 0.0, 2.5, -2.5], 
                              [0.0, 7.0, 0.0, 0.0], 
                              [1.0, 1.0, 1.0, 1.0]])
    # centro da nave
    self.centro = np.array([[0.0], 
                            [3.5], 
                            [1.0]])
    # vetor que orienta a movimentação da nave
    # seu módulo determina a velocidade da nave
    self.orientacao = np.array([[0.0],
                                [1.0],
                                [1.0]])
      
  def rotacao(self, angulo):
    rotacao = matrizRotacao(angulo)
    rotacao_centro = matrizRotacaoPontoArbitrario(angulo, self.centro)
    self.vertices = rotacao_centro@self.vertices
    self.orientacao = rotacao@self.orientacao
    return
  
  def move(self, vetor):
    translacao = matrizTranslacao(vetor)
    self.vertices = translacao@self.vertices
    self.centro = translacao@self.centro
    return