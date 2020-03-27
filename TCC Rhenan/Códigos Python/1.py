# -*- coding: utf-8 -*-
import numpy as np

#Transformacao Direta
#Realiza passagem do Espaco das Juntas, para o Espaco Cartesiano
#t1 e t2 = angulos theta1 e theta2
#l1 e l2 = comprimento dos elos L1 e L2
def direct_transform(t1, t2, l1, l2):
    #Cria vetores
    r1 = np.array([])
    r2 = np.array([])
    r3 = np.array([])
    
    #Computa vetores individuais para elos L1 e L2
    r1 = [l1 * np.cos(np.radians(t1)), l1 * np.sin(np.radians(t1))]
    r2 = [l2 * np.cos(np.radians(t1 + t2)), l2 * np.sin(np.radians(t1 + t2))]

    #Realiza soma dos vetores individuais para obter coordenadas do ponto Pw(x)
    r3 = r1 + r2    
    
    return r3
    
    
print direct_transform(30, 30, 10, 5)


