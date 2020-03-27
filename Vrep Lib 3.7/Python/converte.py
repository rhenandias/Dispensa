import numpy as np 
import matplotlib.pyplot as plt

with open('grafico.csv','r') as input_file:
    content = input_file.read()

with open ('grafico.txt','w') as out_file:
	out_file.write(content)

#dados = np.loadtxt('grafico.csv', delimiter = ',')