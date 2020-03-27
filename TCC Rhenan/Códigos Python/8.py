# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from numpy import cos, sin, arccos, arctan2, radians, degrees, array, power

decimal_precision = 8

#Transformacao Direta
#Realiza passagem do Espaco das Juntas para o Espaco Cartesiano
def direct_transform(t1, t2, l1, l2):
    
    #Computa vetores individuais para elos L1 e L2
    r1 = array([l1 * cos(radians(t1)), l1 * sin(radians(t1))])
    r2 = array([l2 * cos(radians(t1 + t2)), l2 * sin(radians(t1 + t2))])
 
    #Realiza soma dos vetores individuais para obter coordenadas do ponto Pw(x)
    r3 = np.array(r1 + r2)

    return [r1, r2, r3]
    
#Transformacao Inversa
#Realiza passagem do Espaco Cartesiano para o Estaco das Juntas
def inverse_transform(x, y, l1, l2):
    
    res = []

    for i in (-1, 1):
        
	    #Computa valor de t2
	    t2 = arccos((power(x, 2) + power(y, 2) - power(l1, 2) - power(l2, 2))/(2*l1*l2)) 
	    
	    #Atualiza multiplicador de t2
	    t2 *= i

	    #Verifica se t2 retornou NaN
	    if np.isnan(t2): t2 = 0
	    
	    #Computa valor de t1
	    num = y * (l1 + l2 * cos(t2)) - x * l2 * sin(t2)
	    den = x * (l1 + l2 * cos(t2)) + y * l2 * sin(t2)
	    t1 = arctan2(num, den)
	    
	    #Converte em graus
	    t1 = degrees(t1)
	    t2 = degrees(t2)

	    res.append(t1)
	    res.append(t2)
    
    return res
     
def gen_dots(dots_lists):
    res_x = [0]
    res_y = [0]
    
    for i in dots_lists:
        res_x.append(i[0])
        res_y.append(i[1])
        
    return (res_x, res_y)

#============================================== 

t1 = 180
t2 = -90
l1 = 10
l2 = 8

#Gera transformada direta inicial
direct = direct_transform(t1, t2, l1, l2)

#Gera transformada inversa partindo das coordenadas obtidas
inverse = inverse_transform(direct[2][0], direct[2][1], l1, l2)

#Gera rova real para os angulos obtidos
direct1 = direct_transform(inverse[0], inverse[1], l1, l2)
direct2 = direct_transform(inverse[2], inverse[3], l1, l2)

#Arredondamento de valores
direct[2]  = [round(i, 2) for i in direct[2]]
direct1[2] = [round(i, 2) for i in direct1[2]]
direct2[2] = [round(i, 2) for i in direct2[2]]
inverse = [round(i, 2) for i in inverse]

#Escreve resultados obtidos
print "\nDados iniciais:"
print "t1 = " + str(t1)
print "t2 = " + str(t2)

print "\nTransformada direta inicial: (x, y)"
print direct[2]

print "\nAngulos obtidos com a transformada inversa: (t1, t2)"
print [inverse[0], inverse[1]]
print [inverse[2], inverse[3]]

print "\nProva real com os angulos obtidos: (x, y)"
print direct1[2]
print direct2[2]

#=============================================
'''
#Plot

#Configuracao inicial do grafico
plt.figure()
plt.axis('equal')
ax = plt.gca()
ax.set_xlim(-25, 25)
ax.set_ylim(-20, 20)

#Plota raios
raio_l1 = plt.Circle((0, 0), l1, fill=0)
raio_l2 = plt.Circle((0, 0), l1 + l2, fill=0)
ax.add_artist(raio_l1)
ax.add_artist(raio_l2)

#Gera linhas para plotagem

#Plota posicionamento 1
dots_lists = []
dots_lists.append([direct1[0][0], direct1[0][1]])
dots_lists.append([direct1[0][0] + direct1[1][0], direct1[0][1] + direct1[1][1]])
dots = gen_dots(dots_lists)

lines = plt.plot(dots[0], dots[1], marker=".")

#Plota posicionamento 2
dots_lists = []
dots_lists.append([direct2[0][0], direct2[0][1]])
dots_lists.append([direct2[0][0] + direct2[1][0], direct2[0][1] + direct2[1][1]])
dots = gen_dots(dots_lists)

lines = plt.plot(dots[0], dots[1], marker=".")

plt.show()
'''