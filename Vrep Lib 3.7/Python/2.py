import libvrep, random, time

#Arquivo de testes para o carrinho GERSE

vrep = libvrep.libvrep()	#Objeto de manipulação do Vrep
vrep.connect_vrep()			#Realiza conexão com o Vrep
vrep.start_sim()			#Inicia simulação no Vrep

#Adquire objeto de manipulação para as Juntas
motor_d = vrep.new_handler('Roda_D', 'Motor' ) 
motor_e = vrep.new_handler('Roda_E', 'Motor' )

print('ID = Handler', vrep.handlers)
print('ID = Type', vrep.types)

while True:

	#Curva para um lado
	vrep.set_joint(motor_d, -30)
	vrep.set_joint(motor_e,  30)
	time.sleep(3)

	#Curva para outro lado
	vrep.set_joint(motor_d,   30)
	vrep.set_joint(motor_e,  -30)
	time.sleep(3)

	#Frente
	vrep.set_joint(motor_d, -35)
	vrep.set_joint(motor_e, -35)
	time.sleep(3)

	#Trás
	vrep.set_joint(motor_d, 35)
	vrep.set_joint(motor_e, 35)
	time.sleep(3)

	time.sleep(1)
	