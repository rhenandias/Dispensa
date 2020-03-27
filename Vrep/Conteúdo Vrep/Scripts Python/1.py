import vrep, math, time

#Configura conexão com o Vrep, seleciona modo síncrono e inicia simulação
clientID = vrep.simxStart('127.0.0.1', 19997 , True, True, 5000, 5)
vrep.simxSynchronous(clientID, False)
vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot_wait)

#Handlers para os objetos no Vrep
ret, roda_d = vrep.simxGetObjectHandle(clientID, "roda_d_joint", vrep.simx_opmode_oneshot_wait)
ret, roda_e = vrep.simxGetObjectHandle(clientID, "roda_e_joint", vrep.simx_opmode_oneshot_wait)

lado = 8.2

def mover(vel):
	vrep.simxSetJointTargetVelocity(clientID, roda_d, math.radians(vel), vrep.simx_opmode_oneshot_wait)
	vrep.simxSetJointTargetVelocity(clientID, roda_e, math.radians(vel), vrep.simx_opmode_oneshot_wait)

def parar():
	vrep.simxSetJointTargetVelocity(clientID, roda_d, 0, vrep.simx_opmode_oneshot_wait)
	vrep.simxSetJointTargetVelocity(clientID, roda_e, 0, vrep.simx_opmode_oneshot_wait)

def arco_d(vd, raio):
	ve = ((2 * raio * vd) - (lado * vd) )/(lado + (2 * raio))
	vrep.simxSetJointTargetVelocity(clientID, roda_d, math.radians(vd), vrep.simx_opmode_oneshot_wait)
	vrep.simxSetJointTargetVelocity(clientID, roda_e, math.radians(ve), vrep.simx_opmode_oneshot_wait)

def arco_e(ve, raio):
	vd = ((2 * raio * ve) - (lado * ve) )/(lado + (2 * raio))
	vrep.simxSetJointTargetVelocity(clientID, roda_d, math.radians(vd), vrep.simx_opmode_oneshot_wait)
	vrep.simxSetJointTargetVelocity(clientID, roda_e, math.radians(ve), vrep.simx_opmode_oneshot_wait)

#Rotina
mover(-150)
time.sleep(3)
parar()
time.sleep(1)

mover(150)
time.sleep(3)
parar()
time.sleep(1)

arco_e(-150, 10)