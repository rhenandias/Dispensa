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

#Finaliza simulação que esteja ocorrendo
#stopSim(clientID)

#Inicia nova simulação
startSim(clientID)

#Define objeto para Junta1
ret, joint1_handler = vrep.simxGetObjectHandle(clientID, "Junta1", vrep.simx_opmode_oneshot_wait)

#Define objeto para Junta2
ret, joint2_handler = vrep.simxGetObjectHandle(clientID, "Junta2", vrep.simx_opmode_oneshot_wait)

#=========================================================================

#Start Setup - Arduino está requisitando angulos para inicialização

#Executa leitura de valores de sensor do vrep
sensor = read_sensor(clientID, joint1_handler, joint2_handler)

#Transmite valores de sensor para o arduino
send_sensor(sensor, comport)

#=========================================================================

while True:

	#Executa leitura de comando do arduino
	scara_command = read_command(comport)

	#Caso o comando seja de abaixar ou levantar a caneta, passar ao Vrep
	if scara_command >= 1 and scara_command <= 3:
		#Executa escrita de comando no Vrep
		vrep.simxSetIntegerSignal(clientID, "scara_command", scara_command, vrep.simx_opmode_oneshot)

		#Executa leitura de setpoint do arduino
		setpoint = read_setpoint(comport)

		#Executa escrita de angulos no vrep
		write_angle(clientID, joint1_handler, setpoint[0])
		write_angle(clientID, joint2_handler, setpoint[1])

		#Executa leitura de valores de sensor do vrep
		sensor = read_sensor(clientID, joint1_handler, joint2_handler)

		#Transmite valores de sensor para o arduino
		send_sensor(sensor, comport)

		print "Setpoint: " + str(setpoint)
		print "Sensor  : " + str(sensor)
		print ""

	#Caso o comando seja outro, executar tratamento do comando
	elif scara_command == 4:
		print "Rotina Finalizada."
		stopSim(clientID)
		quit()

	elif scara_command == 5:
		debug_text, debug_number = read_debug(comport)
		print debug_text
		print debug_number
		print ""
		
