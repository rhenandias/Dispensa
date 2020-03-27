# Rhenan Dias, 2019
# diasrhenan@gmail.com
# https://github.com/rhenandias
# Realiza controle PID da planta com pêndulo e hélice

import vrep, time, math
import matplotlib.pyplot as plt
from simple_pid import PID

#Função para adquirir tempo atual em millisegundos
millis = lambda: int(round(time.time() * 1000))

def add_force_and_torque(shape_handler, force):

	#Função de extensão da API em Python
	#Uma vez que a API em Python nao possui a função "addForceAndTorque", 
	#Se faz necessário construir uma extensão da API
	#Para documentação: 
	#http://www.coppeliarobotics.com/helpFiles/en/remoteApiExtension.htm

	#Realiza chamado de função genérica
	vrep.simxCallScriptFunction(clientID, "Corpo", 1, "addForceAndTorque", [shape_handler], force, [], bytearray(), vrep.simx_opmode_blocking)

#Configura conexão com o Vrep, seleciona modo síncrono e inicia simulação
clientID = vrep.simxStart('127.0.0.1', 19997 , True, True, 5000, 5)
vrep.simxSynchronous(clientID, True)
vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot_wait)

#Handlers para os objetos no Vrep
ret, handler_junta  = vrep.simxGetObjectHandle(clientID, "Junta", vrep.simx_opmode_oneshot_wait)
ret, handler_helice = vrep.simxGetObjectHandle(clientID, "Helice", vrep.simx_opmode_oneshot_wait)

#Variaveis para plotagem do gráfico
list_setpoint = []
list_angle    = []
list_time     = []

#Configura objeto para o controle PID
pid = PID(Kp = 0.8, Ki = 1.5, Kd = 1, setpoint = 90)
pid.sample_time = 0.05
pid.output_limits = (0, 10)

#Loop de Controle
pid.setpoint = 90
start = millis()	
while(millis() - start < 25000):
	#Realiza coleta do tempo atual (ms)
	cur_time = millis()

	#Realiza leitura do ângulo da junta e converte para graus, com precisão decimal de 2 casas
	ret, ang = vrep.simxGetJointPosition(clientID, handler_junta, vrep.simx_opmode_oneshot_wait)
	ang = round(math.degrees(ang), 2)

	#Atualiza PID com ângulo atual como entrada
	output =  pid(ang)
	output = round(output, 2)
	print("Output", output)

	#adiciona força à planta
	add_force_and_torque(handler_helice, [0, 0, output])
	
	#Adiciona valores para plotagem do gráfico
	list_time.append(cur_time)
	list_angle.append(ang)
	list_setpoint.append(pid.setpoint)
	
	#Aguarda pelo trigger de modo síncrono da simulação
	vrep.simxSynchronousTrigger(clientID)

#Para simulação no Vrep
vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot_wait)

#Plotagem do Gráfico
plt.figure()
plt.title("Setpoint " + str(pid.setpoint) + "°")
plt.plot(list_time, list_setpoint, label = "Setpoint")
plt.plot(list_time, list_angle,    label = "Resposta")
plt.xticks([])
plt.xlabel("Tempo")
plt.ylabel("Ângulo")
plt.legend(loc=4)
plt.show()

