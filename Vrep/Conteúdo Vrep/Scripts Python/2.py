import vrep, math

#Configura conexão com o Vrep, seleciona modo síncrono e inicia simulação
clientID = vrep.simxStart('127.0.0.1', 19997 , True, True, 5000, 5)
vrep.simxSynchronous(clientID, False)
vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot_wait)

#Handlers para os objetos no Vrep
ret, junta1 = vrep.simxGetObjectHandle(clientID, "MTB_axis1", vrep.simx_opmode_oneshot_wait)
ret, junta2 = vrep.simxGetObjectHandle(clientID, "MTB_axis2", vrep.simx_opmode_oneshot_wait)

vrep.simxSetJointTargetPosition(clientID, junta1, math.radians(90), vrep.simx_opmode_oneshot_wait)
vrep.simxSetJointTargetPosition(clientID, junta2, math.radians(90), vrep.simx_opmode_oneshot_wait)

while True:
	pass