# -*- coding: utf-8 -*-
import numpy as np
from numpy import cos, sin, radians, array
 
#Transformacao Direta
#Realiza passagem do Espaco das Juntas, para o Espaco Cartesiano
def direct_transform(t1, t2, l1, l2):
     
    #Computa vetores individuais para elos L1 e L2
    r1 = array([l1 * cos(radians(t1)), l1 * sin(radians(t1))])
    r2 = array([l2 * cos(radians(t1 + t2)), l2 * sin(radians(t1 + t2))])
 
    #Realiza soma dos vetores individuais para obter coordenadas do ponto Pw(x)
    r3 = array(r1 + r2)
     
    return r3
     
     
print(direct_transform(30, 30, 10, 5))