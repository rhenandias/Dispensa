# -*- coding: utf-8 -*-
import vrep, sys, time, serial, os
from util_vrep import *
from util_serial import *
from numpy import radians, degrees

#=========================================================================
print u"\nIniciando conexão com a porta COM."

#Adquire objeto para client de conexão com porta COM
comport = connect_com('COM3', 230400)

console = True
#=========================================================================
print u"Iniciando conexão ao Vrep."

#Adquire objeto para client de conexão com o Vrep
clientID = connectVREP()

#Inicia nova simulação
startSim(clientID)

#Define objeto para Junta1 - Rotação do Elo 1
ret, joint1_handler = vrep.simxGetObjectHandle(clientID, "Junta1", vrep.simx_opmode_oneshot_wait)

#Define objeto para Junta2 - Rotação do Elo 2
ret, joint2_handler = vrep.simxGetObjectHandle(clientID, "Junta2", vrep.simx_opmode_oneshot_wait)

#Define objeto para Junta2 - Rotação do Elo 2
ret, joint3_handler = vrep.simxGetObjectHandle(clientID, "Junta3", vrep.simx_opmode_oneshot_wait)

#=========================================================================

#Start Setup - Arduino está requisitando angulos para inicialização

#Executa leitura de valores de sensor XY do vrep
sensor = read_sensor_xy(clientID, joint1_handler, joint2_handler)

#Transmite valores de sensor XY para o arduino
send_sensor_xy(sensor, comport)

#executa leitura de valores de sensor Z do vrep
sensor = read_sensor_z(clientID, joint3_handler)

#Transmite valores de sensor Z para o arduino
send_sensor_z(sensor, comport)

#=========================================================================

while True:

	#Ciclo de comunicação para movimento

	#Executa leitura de setpoint do arduino
	setpoint = read_setpoint_xy(comport)

	#Executa escrita de angulos no vrep
	write_angle(clientID, joint1_handler, setpoint[0])
	write_angle(clientID, joint2_handler, setpoint[1])

	#Executa leitura de valores de sensor do vrep
	sensor = read_sensor_xy(clientID, joint1_handler, joint2_handler)

	#Transmite valores de sensor para o arduino
	send_sensor_xy(sensor, comport)

	if console:
		print "Setp  (C): " + str(setpoint)
		print "Sens  (C): " + str(sensor)
		print ""

	#Executa leitura de setpoint do arduino
	setpoint = read_setpoint_z(comport)

	#Executa escrita de angulos no vrep
	write_pos(clientID, joint3_handler, setpoint[0])

	#Executa leitura de valores de sensor do vrep
	sensor = read_sensor_z(clientID, joint3_handler)

	#Transmite valores de sensor para o arduino
	send_sensor_z(sensor, comport)

	sensor = [float("{0:.4f}".format(sensor[0]))]

	if console:
		print "Setp  (Z): " + str(setpoint)
		print "Sens  (Z): " + str(sensor)
		print ""