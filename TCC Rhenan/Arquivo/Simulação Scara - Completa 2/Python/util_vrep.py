import vrep
from numpy import radians, degrees

def connectVREP():
	#Fecha conexoes existentes
	vrep.simxFinish(-1)		

	#Define objeto de conexao ao Vrep												
	clientID = vrep.simxStart('127.0.0.1', 19997 , True, True, 5000, 5) 

	#Verifica status da Conexao
	if clientID != -1:
		print 'Conectado ao Vrep.'

		#Inicia conexao com a simulacao do Vrep
		vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot)

		#Define modo de conexao como sincrono
		vrep.simxSynchronous(clientID, False)

		#Retorna objeto de conexao
		return clientID
	else:
		print "Erro ao conectar ao Vrep!"
		sys.exit(0)


#Inicia conexao com client Vrep
def startSim(clientID):
	vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot)

#Para conexao com client Vrep
def stopSim(clientID):
	vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot)

#Disconeca do client Vrep
def disconnectVREP(clientID):
	vrep.simxFinish(clientID)
	print "Conexao finalizada"

def write_angle(clientID, handler, ang):
	#Escreve angulo de posicao da Junta
	vrep.simxSetJointPosition(clientID,handler,radians(ang),vrep.simx_opmode_oneshot)  

def read_angle(clientID, handler):
	#Executa leitura de posicao da Junta
	ret, joint = vrep.simxGetJointPosition(clientID,handler,vrep.simx_opmode_oneshot)
	joint = round(degrees(joint), 1)
	return joint