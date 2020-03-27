import libvrep, random, time

#Arquivo de testes para o carrinho GERSE

vrep = libvrep.libvrep()	#Objeto de manipulação do Vrep
vrep.connect_vrep()			#Realiza conexão com o Vrep
vrep.start_sim()			#Inicia simulação no Vrep

#Adquire objeto de manipulação para as Juntas
motor_d = vrep.new_handler('Roda_D', 'Motor' ) 
motor_e = vrep.new_handler('Roda_E', 'Motor' )


vrep.set_joint(motor_d, -80)
vrep.set_joint(motor_e, -80)

time.sleep(0.5)

vrep.set_joint(motor_d,  40)
vrep.set_joint(motor_e, -40)

time.sleep(1)

vrep.set_joint(motor_d, -80)
vrep.set_joint(motor_e, -80)

while True:
	pass

