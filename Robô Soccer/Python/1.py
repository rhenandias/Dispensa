import vrep, time, math
import matplotlib.pyplot as plt

def adapt(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

#Configura conexão com o Vrep, seleciona modo síncrono e inicia simulação
clientID = vrep.simxStart('127.0.0.1', 19997 , True, True, 5000, 5)
vrep.simxSynchronous(clientID, True)
vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot_wait)

#Handlers para os objetos no Vrep
ret, ponto  = vrep.simxGetObjectHandle(clientID, "Ponto", vrep.simx_opmode_oneshot_wait)
ret, soccer = vrep.simxGetObjectHandle(clientID, "Soccer", vrep.simx_opmode_oneshot_wait)
ret, roda_d = vrep.simxGetObjectHandle(clientID, "roda_d_joint", vrep.simx_opmode_oneshot_wait)
ret, roda_e = vrep.simxGetObjectHandle(clientID, "roda_e_joint", vrep.simx_opmode_oneshot_wait)

encoder_steps 	= 270
encoder_d 		= 0
ret, last_ang_d	= vrep.simxGetJointPosition(clientID, roda_d, vrep.simx_opmode_oneshot_wait)
total_ang_d 	= last_ang_d

lado = 80
pulso = 0
circ = 0

def get_encoder_d():
	res,retInts,retFloats,retStrings,retBuffer = vrep.simxCallScriptFunction(clientID, "Soccer", 1, "get_encoder_d", [soccer], [], [], bytearray(), vrep.simx_opmode_blocking)
	return retInts[0]

def get_encoder_e():
	res,retInts,retFloats,retStrings,retBuffer = vrep.simxCallScriptFunction(clientID, "Soccer", 1, "get_encoder_e", [soccer], [], [], bytearray(), vrep.simx_opmode_blocking)
	return retInts[0]

def frente(vel):
	vrep.simxSetJointTargetVelocity(clientID, roda_d, math.radians(vel), vrep.simx_opmode_oneshot)
	vrep.simxSetJointTargetVelocity(clientID, roda_e, math.radians(vel), vrep.simx_opmode_oneshot)

def para():
	vrep.simxSetJointTargetVelocity(clientID, roda_d, 0, vrep.simx_opmode_oneshot)
	vrep.simxSetJointTargetVelocity(clientID, roda_e, 0, vrep.simx_opmode_oneshot)

def angulo_d(ang, vd, raio):
	global lado, pulso, circ

	ve = ((2 * raio * vd) - (lado * vd) )/(lado + (2 * raio))
	vrep.simxSetJointTargetVelocity(clientID, roda_d, math.radians(vd), vrep.simx_opmode_oneshot)
	vrep.simxSetJointTargetVelocity(clientID, roda_e, math.radians(ve), vrep.simx_opmode_oneshot)

	circ = (ang * math.pi * (raio + 40)) / 180

	pulso = (circ * 270) / 100

def angulo_e(ang, ve, raio):
	global lado, pulso, circ

	vd = ((2 * raio * ve) - (lado * ve) )/(lado + (2 * raio))
	vrep.simxSetJointTargetVelocity(clientID, roda_d, math.radians(vd), vrep.simx_opmode_oneshot)
	vrep.simxSetJointTargetVelocity(clientID, roda_e, math.radians(ve), vrep.simx_opmode_oneshot)

	circ = (ang * math.pi * (raio + 40)) / 180

	pulso = (circ * 270) / 100

tgt_angle = 45
tgt_raio = 200
angulo_d(tgt_angle, -200, tgt_raio)

list_x = []
list_y = []

while(True):
	encoder_d = get_encoder_d()

	if encoder_d >= pulso:
		para()
		break
		
	ret, position = vrep.simxGetObjectPosition(clientID, ponto, -1, vrep.simx_opmode_oneshot_wait)
	list_x.append(position[0])
	list_y.append(position[1])
	vrep.simxSynchronousTrigger(clientID)

vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot_wait)

list_x = list([i * 100 for i in list_x])
list_y = list([i * 100 for i in list_y])

raio_medido = round(max(list_x) - min(list_x), 2)
print("raio medido", raio_medido)
print("circ", circ)

plt.figure()
plt.title('Curva de ' + str(tgt_angle) + "°")
plt.plot(list_x, list_y)
plt.axis('equal')
plt.xlabel("X (mm)")
plt.ylabel("Y (mm)")
#plt.text(0, 6, "Circ. Calculada " + str(round(circ, 2)) + " mm")
plt.annotate("Circ. Calculada " + str(round(circ, 2)) + " mm", xy=(0.6, 0.95), xycoords='axes fraction')
plt.annotate("Raio  " + str(tgt_raio) + " mm", xy=(0.6, 0.90), xycoords='axes fraction')
plt.show()
