import sys, serial, time

def connect_com(com_port, baud_rate):

	#Executa conexao com porta COM
	try:
		comport = serial.Serial(com_port, baud_rate)
	except:
		print "Falha ao conectar porta COM."
		sys.exit(0)

	print "Conexao estabelecida."

	time.sleep(2)

	return comport	

def sync_serial(comport):

	#Configura caracter de sincronizcao
	param_caracter = 't'
	param_ascii = str(chr(116))

	print "Iniciando sincronizacao com Arduino."

	sync = False
	while not sync:
			comport.write(param_ascii)
			syncserial = float(comport.readline().rstrip())
			if syncserial == 116:
				print "Sincronizado."
				sync = True

def read_setpoint(comport):

	#Recebe valores de setpoint do arduino
	value_serial1 = float(comport.readline().rstrip())
	value_serial2 = float(comport.readline().rstrip()) - 90

	#Constroi e retorna vetor com angulos de setpoint
	setpoint = [value_serial1, value_serial2]

	return setpoint


def send_sensor(ang, comport):
	#Envia angulos de sensor para arduino
	ang[0] = round(ang[0] * 10)
	ang[1] = round(ang[1] * 10) + 900
	comport.write(str(ang[0]))
	comport.write(str(ang[1]))