# -*- coding: utf-8 -*-
import vrep, sys, time, serial, os
from util_vrep import *
from util_serial import *
from numpy import radians, degrees

#=========================================================================
print u"Iniciando conexão com a porta COM."

#Adquire objeto para client de conexão com porta COM
comport = connect_com('COM4', 230400)

#=========================================================================
print u"Iniciando conexão ao Vrep."

#Adquire objeto para client de conexão com o Vrep
clientID = connectVREP()

#Define objeto para Junta1
ret, joint1_handler = vrep.simxGetObjectHandle(clientID, "Junta1", vrep.simx_opmode_oneshot_wait)

#Define objeto para Junta2
ret, joint2_handler = vrep.simxGetObjectHandle(clientID, "Junta2", vrep.simx_opmode_oneshot_wait)

#=========================================================================

#=========================================================================
som = []
#setpoint = [0, -90]
#=========================================================================
#Start Setup - Arduino está requisitando angulos para inicialização

#Executa leitura de valores de sensor do vrep
sensor = read_sensor(clientID, joint1_handler, joint2_handler)

#Transmite valores de sensor para o arduino
send_sensor2(sensor, comport)

#=========================================================================

while True:
	
	#'''
	#=====================================================================
	#Com Cycle no client Python
	#start = time.time()

	#Executa leitura de comando do arduino
	scara_command = read_command(comport)

	if scara_command == 0:
		print "Print."

	#Executa escrita de comando no Vrep
	vrep.simxSetIntegerSignal(clientID, "scara_command", scara_command, vrep.simx_opmode_oneshot)

	#Executa leitura de setpoint do arduino
	setpoint = read_setpoint2(comport)

	#Executa escrita de angulos no vrep
	write_angle(clientID, joint1_handler, setpoint[0])
	write_angle(clientID, joint2_handler, setpoint[1])

	#Executa leitura de valores de sensor do vrep
	sensor = read_sensor(clientID, joint1_handler, joint2_handler)

	#Transmite valores de sensor para o arduino
	send_sensor2(sensor, comport)

	print "Setpoint: " + str(setpoint)
	print "Sensor  : " + str(sensor)
	print "\n"
	#end = time.time()
	#som.append(end - start)
	#media = sum(som)/len(som)

	if sensor[0] == 180:
		#print "Time    : " + str(media)

		while True:
			pass
	#print "Time    : " + str(media)
	#=====================================================================



	#'''
	'''
	#=====================================================================

	start = time.time()

	write_angle(clientID, joint1_handler, setpoint[0])
	write_angle(clientID, joint2_handler, setpoint[1])
	sensor = read_sensor(clientID, joint1_handler, joint2_handler)

	print "Setpoint: " + str(setpoint)
	print "Sensor  : " + str(sensor)

	if sensor[0] < 180:
		setpoint[0] = round(sensor[0] + 1, 1)
		setpoint[1] = round(sensor[1] + 1, 1)
	else:
		setpoint = [0, - 90]

	end = time.time()
	som.append(end - start)
	media = round(sum(som)/len(som), 4)
	print "Time    : " + str(media)

	#=====================================================================
	'''


