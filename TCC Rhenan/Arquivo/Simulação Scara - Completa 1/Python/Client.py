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

#Inicia client Vrep
startSim(clientID)

#=========================================================================
#Manda juntas para posição inicial
write_angle(clientID, joint1_handler, 0)
write_angle(clientID, joint2_handler, 0)

time.sleep(1.8)

#=========================================================================
cont = 0

while True:

	print "\nCiclo de Escrita"

	value_serial1 = float(comport.readline().rstrip())
	value_serial2 = float(comport.readline().rstrip())

	setpoint = [value_serial1, value_serial2]

	print "Setpoint: " + str(setpoint)

	write_angle(clientID, joint1_handler, float(setpoint[0]))
	write_angle(clientID, joint2_handler, float(setpoint[1]))

	sens1 = read_angle(clientID, joint1_handler)
	sens2 = read_angle(clientID, joint2_handler)
	
	sensor = [sens1, sens2]

	print "Sensor  : " + str(sensor)
	
	cont += 1
	print cont
				
time.sleep(2)
stopSim(clientID)
time.sleep(1)
disconnectVREP(clientID)       