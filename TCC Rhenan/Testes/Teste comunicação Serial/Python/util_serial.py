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
