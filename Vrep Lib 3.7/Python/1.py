import libvrep, random, time

#Arquivo de testes para o SCARA

vrep = libvrep.libvrep()	#Objeto de manipulação do Vrep
vrep.connect_vrep()			#Realiza conexão com o Vrep
vrep.start_sim()			#Inicia simulação no Vrep

#Adquire objeto de manipulação para as Juntas
junta1 = vrep.new_handler('Junta1', 'Revolute' ) 
junta2 = vrep.new_handler('Junta2', 'Revolute' )
junta3 = vrep.new_handler('Junta3', 'Prismatic')

print('ID = Handler', vrep.handlers)
print('ID = Type', vrep.types)

while True:

	val1 = random.randint(0, 180)
	val2 = random.randint(-90, 90)
	val3 = round(random.random() * 0.1, 2)

	print('tgt1', val1)
	print('tgt2', val2)
	print('tgt3', val3)

	vrep.set_joint(junta1, val1)
	vrep.set_joint(junta2, val2)
	vrep.set_joint(junta3, val3)

	print('get1', vrep.get_joint(junta1))
	print('get2', vrep.get_joint(junta2))
	print('get3', vrep.get_joint(junta3))

	print('\n')

	time.sleep(1)
	