# -*- coding: utf-8 -*-
import vrep, sys, time, serial, os
from util_vrep import *
from util_serial import *
from numpy import radians, degrees

#=========================================================================
print "Iniciando conexao com a porta COM."

#Adquire objeto para client de conexao com porta COM
comport = connect_com('COM3', 9600)

#=========================================================================

print "Iniciando conexao ao Vrep."

#Adquire objeto para client de conexao com o Vrep
clientID = connectVREP()

#Define objeto para Junta1
ret, joint1_handler = vrep.simxGetObjectHandle(clientID, "Junta1", vrep.simx_opmode_oneshot_wait)

#Define objeto para Junta2
ret, joint2_handler = vrep.simxGetObjectHandle(clientID, "Junta2", vrep.simx_opmode_oneshot_wait)


#=========================================================================
#Manda juntas para posição inicial
write_angle(clientID, joint1_handler, 0)
write_angle(clientID, joint2_handler, 0)

time.sleep(1.8)

#=========================================================================
#Configura caracter de sincronização
param_caracter = 't'
param_ascii = str(chr(116))

#=========================================================================

print "Iniciando sincronizacao com Arduino."

sync = False
while not sync:
		comport.write(param_ascii)
		syncserial = float(comport.readline().rstrip())
		if syncserial == 116:
			print "Sincronizado."
			sync = True

while True:

	# 1 -Recebe angulos do arduino
	value_serial1 = float(comport.readline().rstrip())
	value_serial2 = float(comport.readline().rstrip()) - 90
	setpoint = [value_serial1, value_serial2]
	print "Setpoint: " + str(setpoint)

	# 2 - Escreve angulos no vrep
	write_angle(clientID, joint1_handler, value_serial1)
	write_angle(clientID, joint2_handler, value_serial2)

	# 3 - Adquire valor dos sensores
	sens1 = read_angle(clientID, joint1_handler)
	sens2 = read_angle(clientID, joint2_handler)
	sensor = [value_serial1, value_serial2]
	print "Sensor: " + str(sensor)

	#Transforma floats em ints para serem transmitidos
	sens1 = round(sens1 * 10)
	sens2 = round(sens2 * 10) + 900

	# 4 - Envia posicao do sensor para o arduino
	comport.write(str(sens1))
	comport.write(str(sens2))