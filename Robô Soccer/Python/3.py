import vrep, time, math
import matplotlib.pyplot as plt

def adapt(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

#Configura conexão com o Vrep, seleciona modo síncrono e inicia simulação
clientID = vrep.simxStart('127.0.0.1', 19997 , True, True, 5000, 0)
vrep.simxSynchronous(clientID, True)
vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot)

#Handlers para os objetos no Vrep
ret, ponto  = vrep.simxGetObjectHandle(clientID, "Ponto", vrep.simx_opmode_oneshot_wait)
ret, soccer = vrep.simxGetObjectHandle(clientID, "Soccer", vrep.simx_opmode_oneshot_wait)
ret, roda_d = vrep.simxGetObjectHandle(clientID, "roda_d_joint", vrep.simx_opmode_oneshot_wait)
ret, roda_e = vrep.simxGetObjectHandle(clientID, "roda_e_joint", vrep.simx_opmode_oneshot_wait)

encoder_d 		= 0
encoder_e 		= 0 
ret, last_ang_d	= vrep.simxGetJointPosition(clientID, roda_d, vrep.simx_opmode_oneshot_wait)
ret, last_ang_e	= vrep.simxGetJointPosition(clientID, roda_e, vrep.simx_opmode_oneshot_wait)
total_ang_d 	= last_ang_d
total_ang_e 	= last_ang_e
last_clear_encoder_d = 0
last_clear_encoder_e = 0

encoder_steps = 360

lado = 75.9 #0.0759

pulso = 0
circ = 0

def get_encoder_d():
	res,retInts,retFloats,retStrings,retBuffer = vrep.simxCallScriptFunction(clientID, "Soccer", 1, "get_encoder_d", [soccer], [], [], bytearray(), vrep.simx_opmode_oneshot_wait)
	return retInts[0]

def get_encoder_e():
	res,retInts,retFloats,retStrings,retBuffer = vrep.simxCallScriptFunction(clientID, "Soccer", 1, "get_encoder_e", [soccer], [], [], bytearray(), vrep.simx_opmode_oneshot_wait)
	return retInts[0]

def clear_encoders():
	global last_clear_encoder_d, last_clear_encoder_e
	last_clear_encoder_d = get_encoder_d()
	last_clear_encoder_e = get_encoder_e()
	
def frente(vel):
	vrep.simxSetJointTargetVelocity(clientID, roda_d, math.radians(vel), vrep.simx_opmode_oneshot)
	vrep.simxSetJointTargetVelocity(clientID, roda_e, math.radians(vel), vrep.simx_opmode_oneshot)

def para():
	vrep.simxSetJointTargetVelocity(clientID, roda_d, 0, vrep.simx_opmode_oneshot)
	vrep.simxSetJointTargetVelocity(clientID, roda_e, 0, vrep.simx_opmode_oneshot)

def angulo_d(ang, vd, raio):
	global lado, last_clear_encoder_d, encoder_steps

	ve = ((2 * raio * vd) - (lado * vd) )/(lado + (2 * raio))
	circ = (ang * math.pi * (raio + 40)) / 180
	pulso = (circ * encoder_steps) / 100

	vrep.simxSetJointTargetVelocity(clientID, roda_d, math.radians(vd), vrep.simx_opmode_oneshot)
	vrep.simxSetJointTargetVelocity(clientID, roda_e, math.radians(ve), vrep.simx_opmode_oneshot)
	vrep.simxSynchronousTrigger(clientID)

	while get_encoder_d() - last_clear_encoder_d < pulso:	
		vrep.simxSynchronousTrigger(clientID)
	para()

	clear_encoders()

def angulo_e(ang, ve, raio):
	global lado, last_clear_encoder_e

	vd = ((2 * raio * ve) - (lado * ve) )/(lado + (2 * raio))
	vrep.simxSetJointTargetVelocity(clientID, roda_d, math.radians(vd), vrep.simx_opmode_oneshot)
	vrep.simxSetJointTargetVelocity(clientID, roda_e, math.radians(ve), vrep.simx_opmode_oneshot)

	circ = (ang * math.pi * (raio + 40)) / 180

	pulso = (circ * 270) / 100

	while get_encoder_e() - last_clear_encoder_e <= pulso:	
		vrep.simxSynchronousTrigger(clientID)

	clear_encoders()
	para()

def giro_e(ang, vel):
	global encoder_steps, last_clear_encoder_d, lado
	
	circ = (ang * math.pi * (lado/2)) / 180
	pulso = (circ * encoder_steps) / 100
	#error_percent = 5
	#error = (error_percent * pulso)/100
	#pulso = pulso - math.ceil(error)
	
	vrep.simxSetJointTargetVelocity(clientID, roda_d, math.radians( vel), vrep.simx_opmode_oneshot)
	vrep.simxSetJointTargetVelocity(clientID, roda_e, math.radians(-vel), vrep.simx_opmode_oneshot)
	vrep.simxSynchronousTrigger(clientID)

	while get_encoder_d() - last_clear_encoder_d < pulso:	
		vrep.simxSynchronousTrigger(clientID)
	
	vrep.simxSynchronousTrigger(clientID)
	para()
	
	clear_encoders()

giro_e(90, -250)
time.sleep(1)
giro_e(45, -250)
time.sleep(1)
giro_e(45, -250)
time.sleep(1)
giro_e(90, -250)
time.sleep(1)
giro_e(45, -250)
time.sleep(1)
giro_e(45, -250)

time.sleep(100)
