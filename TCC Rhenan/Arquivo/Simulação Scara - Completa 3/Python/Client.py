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

#Manda juntas para posição inicial
write_angle(clientID, joint1_handler, 0)
write_angle(clientID, joint2_handler, 0)

#=========================================================================

#Realiza sincronizacao com arduino
sync_serial(comport)


while True:

	#Executa leitura de setpoint do arduino
	setpoint = read_setpoint(comport)

	print "Setpoint: " + str(setpoint)

	#Executa escrita de angulos no vrep
	write_angle(clientID, joint1_handler, setpoint[0])
	write_angle(clientID, joint2_handler, setpoint[1])

	#Executa leitura de valores de sensor do vrep
	sensor = read_sensor(clientID, joint1_handler, joint2_handler)

	print "Sensor: " + str(sensor)

	#Transmite valores de sensor para o arduino
	send_sensor(sensor, comport)