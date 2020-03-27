import libvrep, random, time

#Arquivo de testes para o carrinho GERSE

vrep = libvrep.libvrep()	#Objeto de manipulação do Vrep
vrep.connect_vrep()			#Realiza conexão com o Vrep
vrep.start_sim()			#Inicia simulação no Vrep

#Adquire objeto de manipulação para as Juntas
motor_d = vrep.new_handler('Roda_D', 'Motor' ) 
motor_e = vrep.new_handler('Roda_E', 'Motor' )

#print('ID = Handler', vrep.handlers)
#print('ID = Type', vrep.types)


def rodad(vd, raio):
	lado = 12.5
	ve = ( (2 * raio * vd) - (lado * vd) )/(lado + (2 * raio))
	
	vrep.set_joint(motor_d, -vd)
	vrep.set_joint(motor_e, -ve)

def rodae(ve, raio):
	lado = 12.5	
	vd = ( (2 * raio * ve) - (lado * ve) )/(lado + (2 * raio))
		
	vrep.set_joint(motor_d, -vd)
	vrep.set_joint(motor_e, -ve)


def frente(vel):
	vrep.set_joint(motor_d, vel)
	vrep.set_joint(motor_e, vel)

while True:
	frente(-10)

