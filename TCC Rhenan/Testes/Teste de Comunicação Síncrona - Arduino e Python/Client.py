# -*- coding: utf-8 -*-
import sys, time, serial
from util_serial import *
from numpy import radians, degrees

#=========================================================================
print "Iniciando conexao com a porta COM."

#Adquire objeto para client de conexao com porta COM
comport = connect_com('COM3', 9600)

#=========================================================================
param_caracter = 't'
param_ascii = str(chr(116))

time.sleep(1.8)

while True:
	comport.write(param_ascii)
	value_serial = comport.readline()

	print value_serial
     