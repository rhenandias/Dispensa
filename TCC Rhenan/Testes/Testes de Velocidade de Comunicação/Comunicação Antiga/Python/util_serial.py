import sys, serial, time, copy, struct

#Executa conexao com porta COM
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

#Executa sincronizacao entre client e arduino
def sync_serial(comport):

	#Configura caracter de sincronizcao
	param_ascii = str(chr(116))

	print "Iniciando sincronizacao com Arduino."

	#Define flag de sincronizacao
	sync = False

	#Inicia sincronizacao
	while not sync:
			#Tenta enviar caractere de sincronizacao
			comport.write(param_ascii)

			#Recebe caractere de resposta
			syncserial = float(comport.readline().rstrip())

			#Verifica conferencia de caractere
			if syncserial == 116:
				print "Sincronizado."
				sync = True

#Executa leitura de setpoint recebido do arduino
def read_setpoint(comport):

	#Recebe valores de setpoint do arduino
	value_serial1 = float(comport.readline().rstrip()) 
	value_serial2 = float(comport.readline().rstrip())

	#Arredonda valores recebidos
	value_serial1 = round(value_serial1, 1)
	value_serial2 = round(value_serial2, 2)

	#Constroi e retorna vetor com angulos de setpoint
	setpoint = [value_serial1, value_serial2]

	return setpoint

#Executa envio de angulos de sensor para o arduino
def send_sensor(ang, comport):
	
	send_angle = copy.deepcopy(ang)

	#Adapta angulos de sensor
	send_angle[0] = (round(send_angle[0] * 10))
	send_angle[1] = (round(send_angle[1] * 10)) + 900

	#Envia angulos de sensor para o arduino
	comport.write(str(send_angle[0]))
	comport.write(str(send_angle[1]))