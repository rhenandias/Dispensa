# -*- coding: utf-8 -*-
import vrep, sys, math, serial, time, struct

class libvrep(object):

	#Construtor da classe
	def __init__(self):
		#Objeto de manipulação com o Vrep
		self.clientID = None

		#Precisão decimal padrão de escrita e leitura
		self.decimal_place = 2

		#Objeto de manipulação da porta COM
		self.com_port = None

		#Handlers e Tipos das juntas
		self.handlers = {}
		self.types    = {}
		self.joint_type = {
			'Revolute'	: 1,
			'Prismatic'	: 2,
			'Spherical'	: 3,
			'Motor'		: 4
		}
		
		#ID das funções para integração com Arduino
		self.functions = {
			1 : self.function1
		}

	#============================================================================
	# 	Funções de Configuração
	#============================================================================

	#Realiza conexão com o Vrep
	def connect_vrep(self):
		#Fecha conexões existentes
		vrep.simxFinish(-1)		

		#Define objeto de conexão ao Vrep												
		clientID = vrep.simxStart('127.0.0.1', 19997 , True, True, 5000, 5) 

		#Verifica status da conexão
		if clientID != -1:
			print("\nConectado ao Vrep.")

			#Retorna objeto de conexão
			self.clientID = clientID

			return True
		else:
			print("\nErro ao conectar ao Vrep.")
			return False

	#Desconecta do Vrep
	def disconnect_vrep(self):
		#Finaliza conexão com o Vrep
		vrep.simxFinish(self.clientID)
		print("\nConexão com o V-Rep finalizada")

		return True

	#Inicia a simulação no Vrep
	def start_sim(self):
		print("\nIniciando simulação no Vrep")
		vrep.simxStartSimulation(self.clientID, vrep.simx_opmode_oneshot_wait)
		
	#Para a simulação no Vrep
	def stop_sim(self):
		print("\nFinalizando simulação no Vrep")
		vrep.simxStopSimulation(self.clientID, vrep.simx_opmode_oneshot_wait)

	#Configura execução de sincronicidade do client
	def set_sync(self, value):
		#Modo de operação padrão: assíncrono
		vrep.simxSynchronous(self.clientID, value)	

	#Verifica return code da Vrep API
	def check_return_code(self, return_code):
		#Verifica o código de retorno gerado pela Vrep API

		#Sucesso na execução da função desejada
		if return_code == vrep.simx_return_ok: 
			return True

		#Houve algum problema na execução da função desejada
		print("\nErro encontrado na execução do pedido.")
		print("Verificar a documentação da Vrep API: \n")

		errors = {
			vrep.simx_return_novalue_flag			: 'There is no command reply in the input buffer.',
			vrep.simx_return_timeout_flag			: 'The function timed out (probably the network is down or too slow).',
			vrep.simx_return_illegal_opmode_flag 	: 'The specified operation mode is not supported for the given function.',
			vrep.simx_return_remote_error_flag		: 'The function caused an error on the server side (e.g. an invalid handle was specified).',
			vrep.simx_return_split_progress_flag	: 'The communication thread is still processing previous split command of the same type.',
			vrep.simx_return_local_error_flag		: 'The function caused an error on the client side.',
			vrep.simx_return_initialize_error_flag	: 'simxStart was not yet called.'
		}

		print(errors[return_code])

		return False

	#Altera precisão decimal do sistema
	def set_decimal_place(self, new_decimal_place):
		print("Alterando precisão decimal para: " + str(new_decimal_place) + "\n")
		self.decimal_place = new_decimal_place

	#============================================================================
	#	Funções de Juntas
	#============================================================================
	
	#Adquire handler para um objeto especificado
	def new_handler(self, joint_name, joint_type, joint_id = None):
		#Executa pedido de geração de handler
		return_code, handler = vrep.simxGetObjectHandle(self.clientID, joint_name, vrep.simx_opmode_oneshot_wait)
		
		#Verifica se o pedido foi executado com sucesso
		if self.check_return_code(return_code):
			#Pedido executado com sucesso, prosseguir

			#Verifica se foi especificado uma ID para o handler
			if joint_id != None:
				#Foi especificado uma ID, atribuir ao handler
				self.handlers[joint_id] = handler
			else:
				#Não foi especificado uma ID, atribuir ID sequencial
				self.handlers[len(self.handlers)] = handler

			#Adiciona tipo da junta selecionado
			if joint_type in ['Revolute', 'Prismatic', 'Spherical', 'Motor']:
				self.types[handler] = self.joint_type.get(joint_type)
			else:
				#Tipo inválido de junta informado
				print('\nTipo de junta informado inválido.')

			return handler

	#Escrita em junta de tipo genérico
	def set_joint(self, handler, value, cur_decimal_place = None):
		#Identificar o tipo de junta
		joint_type = self.types.get(handler)

		#Erro ao acessar handler ou tipo
		if joint_type == None:
			print('Erro ao acessar handler/type.')
			print('O handler foi criado? O tipo de junta foi assimilado corretamente?')
			return

		#Verifica precisão decimal desejada
		if cur_decimal_place == None:
			cur_decimal_place = self.decimal_place

		#Executa movimento desejado

		#Escrita em Junta de Revolução (deg)
		if joint_type == self.joint_type['Revolute']:
			#Realiza conversão necessária e escrita na junta
			value = math.radians(round(value, cur_decimal_place))
			vrep.simxSetJointPosition(self.clientID, handler, value, vrep.simx_opmode_oneshot)

		#Escrita em Junta Prismática (m)
		elif joint_type == self.joint_type['Prismatic']:
			#Realiza conversão necessária e escrita na junta
			value = round(value, cur_decimal_place)
			vrep.simxSetJointPosition(self.clientID, handler, value, vrep.simx_opmode_oneshot)  

		#Escrita em Junta de Motor (deg/s)
		elif joint_type == self.joint_type['Motor']:
			#Realize conversão necessária e escrita na junta
			value = math.radians(round(value, cur_decimal_place))
			vrep.simxSetJointTargetVelocity(self.clientID, handler, value, vrep.simx_opmode_oneshot)

	#Leitura em junta de tipo genérico
	def get_joint(self, handler, cur_decimal_place = None):
		
		#Identificar o tipo de junta
		joint_type = self.types.get(handler)

		#Erro ao acessar handler ou tipo
		if joint_type == None:
			print('Erro ao acessar handler/type.')
			print('O handler foi criado? O tipo de junta foi assimilado corretamente?')
			return

		#Verifica precisão decimal desejada
		if cur_decimal_place == None:
			cur_decimal_place = self.decimal_place

		#Executa leitura desejado

		#Leitura em Junta de Revolução (deg)
		if joint_type == self.joint_type['Revolute']:
			#Realiza leitura e conversão necessária
			return_code, value = vrep.simxGetJointPosition(self.clientID, handler, vrep.simx_opmode_oneshot_wait)
			return round(math.degrees(value), cur_decimal_place)

		#Leiura em Junta Prismática (m)
		elif joint_type == self.joint_type['Prismatic']:
			#Realiza leitura e conversão necessária
			return_code, value = vrep.simxGetJointPosition(self.clientID, handler, vrep.simx_opmode_oneshot_wait)
			return round(value, cur_decimal_place)

		#Leitura em Junta de Motor (deg/s)
		elif joint_type == self.joint_type['Motor']:
			#Realiza leitura e conversão necessária
			return_code, value = vrep.simxGetObjectFloatParameter (self.clientID, handler, vrep.sim_jointfloatparam_velocity, vrep.simx_opmode_oneshot_wait)
			return round(math.degrees(value), cur_decimal_place)

	#Escreve um valor de ângulo (graus) em uma junta de Reveolução
	def set_joint_angle(self, handler, ang, cur_decimal_place = None):
		#Juntas de Revolu��o
		#Escreve um valor de �ngulo (em graus)

		#Verifica precis�o decimal desejada
		if cur_decimal_place == None:
			#Precis�o decimal n�o especificada
			#Assumir precis�o decimal padr�o
			cur_decimal_place = self.decimal_place

		#Realiza adapta��o do valor de �ngulo a ser escrito
		tgt_angle = math.radians(round(ang, cur_decimal_place))

		#Realiza escrita do valor de �ngulo desejado
		vrep.simxSetJointPosition(self.clientID, handler, tgt_angle, vrep.simx_opmode_oneshot)  

	#Escreve um valor de posi��o (metros) em uma junta Prism�tica
	def set_joint_position(self, handler, m, cur_decimal_place = None):
		#Juntas Prism�ticas
		#Escreve um valor de posi��o (em metros)

		#Verifica precis�o decimal desejada
		if cur_decimal_place == None:
			#Precis�o decimal n�o especificada
			#Assumir precis�o decimal padr�o
			cur_decimal_place = self.decimal_place

		#Realiza adapta��o do valor de �ngulo a ser escrito
		tgt_pos = round(m, cur_decimal_place)

		#Realiza escrita do valor de posi��o desejado
		vrep.simxSetJointPosition(self.clientID, handler, tgt_pos, vrep.simx_opmode_oneshot)  

	#Escreve um valor de velocidade (graus/s) em um motor (junta de Revolu��o)
	def set_joint_velocity(self, handler, vel, cur_decimal_place = None):
		#Juntas de Revolu��o
		#Escreve um valor de velocidade em motores (graus/s)

		#Verifica precis�o decimal desejada
		if cur_decimal_place == None:
			#Precis�o decimal n�o especificada
			#Assumir precis�o decimal padr�o
			cur_decimal_place = self.decimal_place

		#Realiza adapta��o do valor de �ngulo a ser escrito
		tgt_velocity = math.radians(round(vel, cur_decimal_place))

		#Realiza escrita do valor de velocidade desejado
		vrep.simxSetJointTargetVelocity(self.clientID, handler, tgt_velocity, vrep.simx_opmode_oneshot)

	#Executa leitura do ângulo (graus) de uma junta de Revolução
	def get_joint_angle(self, handler, cur_decimal_place = None):
		#Juntas de Revolução
		#Leitura de posição de uma junta (graus)
		return_code, angle = vrep.simxGetJointPosition(self.clientID, handler, vrep.simx_opmode_oneshot_wait)

		#Verifica precisão decimal desejada
		if cur_decimal_place == None:
			#Precisão decimal não especificada
			#Assumir precisão decimal padrão
			cur_decimal_place = self.decimal_place

		#Realiza adaptação decimal e retorna valor de leitura
		return round(math.degrees(angle), cur_decimal_place)

	#Executa leitura da posição (metros) de uma junta Prismática
	def get_joint_position(self, handler, cur_decimal_place = None):
		#Juntas Prismáticas
		#Leitura de posição de uma junta (m)
		return_code, position = vrep.simxGetJointPosition(self.clientID, handler, vrep.simx_opmode_oneshot_wait)

		#Verifica precisão decimal desejada
		if cur_decimal_place == None:
			#Precisão decimal não especificada
			#Assumir precisão decimal padrão
			cur_decimal_place = self.decimal_place

		#Realiza adaptação decimal e retorna valor de leitura
		return round(position, cur_decimal_place)

	#Executa leitura da velocidade (graus/s) de um motor (junta de Revolução)
	def get_joint_velocity(self, handler, cur_decimal_place = None):
		#Juntas de Revolução
		#Leitura de velocidade de um motor (graus/s)
		return_code, velocity = vrep.simxGetObjectFloatParameter (self.clientID, handler, vrep.sim_jointfloatparam_velocity, vrep.simx_opmode_oneshot_wait)

		#Verifica precisão decimal desejada
		if cur_decimal_place == None:
			#Precisão decimal não especificada
			#Assumir precisão decimal padrão
			cur_decimal_place = self.decimal_place

		#Realiza adaptação decimal e retorna valor de leitura
		return round(math.degrees(velocity), cur_decimal_place)

	#============================================================================
	#	Funções de Configuração Serial
	#============================================================================

	#Realiza conexão com a porta serial especificada
	def open_serial(self, com_port, baud_rate):
		#Tenta realizar conexão serial
		try:
			serial_port = serial.Serial(com_port, baud_rate)
		except:
			print('Falha ao estabelecer conexão serial.\n')
			return False

		#Conexão realizada com sucesso
		print('Conexão serial estabelecida.\n')

		#Atualiza objeto de manipulação da porta COM
		self.com_port = serial_port

		time.sleep(2)

		return True

	def close_serial(self):
		#Desconecta porta serial
		self.com_port.close()

		#Porta COM fechada com sucesso
		print('Desconectado da porta serial.\n')

		return True

	#============================================================================
	#	Funções de Leitura Serial
	#============================================================================
	
	#Realiza leitura de 1 byte via porta serial
	def read_serial_byte(self):
		#Realiza leitura de 1 byte via porta serial
		value = ord(self.com_port.read(1))

		#Retorna valor lido
		return value

	#Realiza leitura de 2 bytes via porta serial
	def read_serial_int(self):
		#Realiza leitura de 2 bytes via porta serial
		value = self.com_port.read(2)

		#Realiza unpack do valor em inteiro de 2 bytes
		value = struct.unpack('<h', value)[0]

		#Retorna valor lido
		return value

	#Realiza leitura de 4 bytes via porta serial
	def read_serial_float(self, cur_decimal_place = None):
		#Realiza leitura de 4 bytes via porta serial
		value = self.com_port.read(4)

		#Realiza unpack do valor em float de 4 bytes
		value = struct.unpack('<f', value)[0]

		#Verifica precisão decimal desejada
		if cur_decimal_place == None:
			#Precisão decimal não especificada
			#Assumir precisão decimal padrão
			cur_decimal_place = self.decimal_place

		#Retorna valor lido
		return round(value, cur_decimal_place)

	#============================================================================
	#	Funções de Escrita Serial
	#============================================================================

	def write_serial_byte(self, value):
		pass

	def write_serial_int(self, value):
		pass 

	def write_serial_flaot(self, value):
		pass 
		

	def function1(self):
		value1 = self.read_serial_byte()
		value2 = self.read_serial_float()

		print('id = '+ str(value1))
		print('valor = '+ str(value2))

	def loop(self):
		while True:
			#Executa leitura do comando
			command = self.read_serial_byte()

			#Verifica comando e executa função especifica
			self.functions[command]()
