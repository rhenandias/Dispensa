# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np

def print_radius(axes, l1, l2):
    
    raio_l1 = plt.Circle((0, 0), l1, fill=0)
    raio_l2 = plt.Circle((0, 0), l1 + l2, fill=0)
    
    ax.add_artist(raio_l1)
    ax.add_artist(raio_l2)
    
    
def gen_l1_line(l1, t1):

    r1 = np.array([])
    r1 = [l1 * np.cos(np.radians(t1)), l1 * np.sin(np.radians(t1))]

    return r1
    
def gen_dots(dots_lists):
    res_x = [0]
    res_y = [0]
    
    for i in dots_lists:
        res_x.append(i[0])
        res_y.append(i[1])
        
    return (res_x, res_y)

#Configuracao inicial do grafico
fig = plt.figure()
plt.axis('equal')
ax = plt.gca()
ax.set_xlim(-20, 20)
ax.set_ylim(-20, 20)


angle = 0
linha_l1 = gen_l1_line(8, 0)

dots_lists = []
dots_lists.append(linha_l1)
dots = gen_dots(dots_lists)

line = plt.plot(dots[0], dots[1])


#Printa raios dos elos
print_radius(ax, 8, 5)
#Exibe grafico final
fig.show()

