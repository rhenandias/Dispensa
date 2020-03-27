import sys, serial, time

def connect_com(com_port, baud_rate):
	try:
		comport = serial.Serial(com_port, baud_rate)
	except:
		print "Falha ao conectar porta COM."
		sys.exit(0)

	print "Conexao estabelecida."

	time.sleep(2)

	return comport	
