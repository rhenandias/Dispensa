# -*- coding: utf-8 -*-
import sys, serial, time, copy, struct

#Executa conezão com porta COM
def connect_com(com_port, baud_rate):

	#Executa conexão com porta COM
	try:
		comport = serial.Serial(com_port, baud_rate)
	except:
		print "Falha ao conectar porta COM."
		sys.exit(0)

	print u"Conexão estabelecida."

	time.sleep(2)

	return comport	

#Executa sinzeonização entre client e arduino
def sync_serial(comport):

	#Configura caracter de sincronização
	param_ascii = str(chr(116))

	print "Iniciando sincronizacao com Arduino."

	#Define flag de sincronização
	sync = False

	#Inicia sincronização
	while not sync:
			#Tenta enviar caractere de sincronização
			comport.write(param_ascii)

			#Recebe caractere de resposta
			syncserial = float(comport.readline().rstrip())

			#Verifica conferencia de caractere
			if syncserial == 116:
				print "Sincronizado."
				sync = True

def read_debug(comport):

	#Leitura do texto de debug
	text = comport.readline().rstrip()

	#Leitura de valores via serial
	incoming_value = comport.read(2)

	#Realiza unpack de valores em inteiros de 2 bytes
	value_serial = struct.unpack('<h', incoming_value)[0]

	#Atualiza valores para números floats
	value_serial /= 10.0

	return text, value_serial

def read_setpoint(comport):

	#Leitura de valores via serial
	incoming_value1 = comport.read(2)
	incoming_value2 = comport.read(2)

	#Realiza unpack de valores em inteiros de 2 bytes
	value_serial2 = struct.unpack('<h', incoming_value1)[0]
	value_serial1 = struct.unpack('<h', incoming_value2)[0]
	
	#Atualiza valores para números floats
	value_serial1 /= 10.0
	value_serial2 /= 10.0

	#Define vector de setpoint1 [t1, t2]
	setpoint = [value_serial1, value_serial2]

	return setpoint

def send_sensor(ang, comport):

	#Realiza copia do vetor de angulos
	send_angle = copy.deepcopy(ang)

	#Ajusta valores para envio via serial
	send_angle[0] = (round(send_angle[0] * 10))
	send_angle[1] = (round(send_angle[1] * 10))

	#Realiza pack de valores em inteiros de 2 bytes
	send_sensor1 = struct.pack('<h', send_angle[0])
	send_sensor2 = struct.pack('<h', send_angle[1])

	#Executa escrita dos bytes via serial
	comport.write(bytes(send_sensor1))
	comport.write(bytes(send_sensor2))

def read_command(comport):

	#Leitura do valor de comando via serial
	incoming_command = comport.read(1)

	#Realiza unpack do valor de comando em número inteiro
	unpacked_command = ord(incoming_command)

	return unpacked_command