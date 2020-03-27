import time, struct, sys, serial
from util_serial import *

#=========================================================================
print "Iniciando conexao com a porta COM."

#Adquire objeto para client de conexao com porta COM
comport = connect_com('COM3', 230400)

#=========================================================================

som = []
#i = 0

while True:
	
	#while not comport.inWaiting():
	#	pass

	'''
	#Float
	start = time.time()
	data1 = comport.read(4)
	data2 = struct.unpack('<f', data1)[0]
	data2 = round(data2, 1)
	end = time.time()
	som.append(end - start)
	print sum(som)/len(som)
	#print data2
	'''

	'''
	#Int
	start = time.time()
	data1 = comport.read(2)
	data2 = struct.unpack('<h', data1)[0]
	data2 = data2 / 10.0
	end = time.time()
	som.append(end - start)
	print sum(som)/len(som)
	#print data2
	'''

	'''
	#Metodo Antigo
	start = time.time()
	data1 = float(comport.readline().rstrip())
	end = time.time()
	som.append(end - start)
	print sum(som)/len(som)
	print data1
	'''

	
	for i in range(-100, 100):
		#Escreve VAlor
		data1 = i
		data1 = struct.pack('<h', data1)
		comport.write(bytes(data1))

		#Le e exibe Valor
		data1 = comport.read(2)
		data2 = struct.unpack('<h', data1)[0]
		data2 = data2 / 10.0
		print data2

	while True:
		pass
	

	'''
	#Escreve Valor
	data1 = i
	data1 = struct.pack('<h', data1)
	comport.write(bytes(data1))

	#Le e exibe Valor
	data1 = comport.read(2)
	data2 = struct.unpack('<h', data1)[0]
	data2 = data2 / 10.0
	print data2
	'''


	