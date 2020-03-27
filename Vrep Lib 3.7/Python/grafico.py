import numpy as np 
import matplotlib.pyplot as plt 

lista = np.loadtxt('grafico.txt', delimiter = ',')

menor = min(lista[:,1])
maior = max(lista[:,1])

tamanho = maior - menor

print('Tamanho = ', tamanho)

plt.figure()
plt.axis('equal')
plt.plot(lista[:,1], lista[:,2])
plt.show() 