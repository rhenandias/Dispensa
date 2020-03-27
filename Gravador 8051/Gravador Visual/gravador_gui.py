from screen import *
from intelhex import IntelHex
import sys, serial, time


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		self.setupUi(self)

		#Inicializa programa
		print('Iniciando gravador')
		self.text_log.append('Iniciando gravador.')

		#Inicializa portas COM
		self.get_serial_ports()	

		#Parâmetros e variáveis
		self.com_port = None			#Objeto para manipulação da conexão serial
		self.program_size = None		#Tamanho do programa após o segundo parse (bytes)
		self.addresses = []				#Lista para os endereços do programa (addr)
		self.bytes = []					#Lista para os bytes do programa (data)

		#Adiciona funcionalidade aos botões
		self.input_update_com_ports.clicked.connect(self.get_serial_ports)	#Atualizar portas COM
		self.input_open_com.clicked.connect(self.open_serial)				#Conectar Serial
		self.input_close_com.clicked.connect(self.close_serial)				#Desconectar Serial
		self.input_select_file.clicked.connect(self.selectFile)				#Carregar Arquivo
		self.input_parse.clicked.connect(self.parse)						#Botão de Parse
		

	#Executa parse de uma linha (utilizado em parse())
	def parse_hex_line(self, line):
		if len(line) == 0 : return
		bytecount   = int(line[0:2], 16)
		address     = int(line[2:6], 16)
		rec_type    = int(line[6:8], 16)

		rec_output = str(hex(address)) + '\t' + str(bytecount) + '\t'
		if rec_type == 0:
			rec_output += 'data'
			rec_output += '\t\t' + line[8:(8+2*(bytecount))]
		elif rec_type == 1:
			rec_output += 'end of file'
		elif rec_type == 2:
			rec_output += 'ext segment addr'
		elif rec_type == 3:
			rec_output += 'start segment address'
		elif rec_type == 4:
			rec_output += 'ext linear addr'
		elif rec_type == 5:
			rec_output += 'start linear address'
		print(rec_output)
		self.text_log.append(rec_output)

	#Executa Parse do arquivo
	def parse(self):
		#======================================================================
		#Executa primeiro parse do código, para exibir no terminal
		#======================================================================
		file_path = self.label_file_name.text()
		print('\nParsing: ' + file_path)
		self.text_log.append('Parsing: ' + str(file_path))
		hex_file = open(file_path, "rb")

		current_line = ''
		try:
			byte = '1' # initial placeholder
			print('Address\tLength\tType\t\tData')
			self.text_log.append('Address\tLength\tType\t\tData')
			while byte != "":
				byte = hex_file.read(1).decode('utf-8') 
				if byte == ":":
					#   (1) Parse the current line!
					self.parse_hex_line(current_line)
					#   (2) Reset the current line to build the next one!
					current_line = ""
				else:
					current_line += byte
			self.parse_hex_line(current_line)
		finally:
			hex_file.close()

		#======================================================================
		#Executa segundo parse do código, para gerar os bytes
		#======================================================================
		#Carrega código como .hex
		ih = IntelHex()										
		ih.fromfile(file_path, format='hex')	

		#Cria dicionário com o programa
		program_dict = ih.todict()		

		#Adquire tamanho do programa (em bytes)
		self.program_size = len(program_dict)	

		#Calcula tamanho do programa (em %)
		memory_per_cent = round((self.program_size * 100)/8192, 1)

		print("O programa usa " + str(self.program_size) + str(' bytes (') + str(memory_per_cent) + "%) de armazenamento. Máximo de 8192 bytes")
		self.text_log.append("O programa usa " + str(self.program_size) + str(' bytes (') + str(memory_per_cent) + "%) de armazenamento. Máximo de 8192 bytes")

		if self.input_addr_plus_code.isChecked():	parse_mode = 0
		if self.input_only_code.isChecked():		parse_mode = 1

		if parse_mode:
			#Transforma dicionário em lista de tuples
			#Organiza ordem crescente pelos endereços
			program_dict = sorted(program_dict.items(), key=lambda kv: kv[0])
		else:
			#Transforma dicionário em lista de tuples
			#Não organiza ordem crescente pelos endereços
			program_dict = [(k, v) for k, v in program_dict.items()]

		#Gera lista de endereços e bytes de programa
		for instruction in program_dict:
			self.addresses.append(instruction[0])
			self.bytes.append(hex(instruction[1]))
				
	#Seleciona arquivo para ser carregado
	def selectFile(self):
		options = QtWidgets.QFileDialog.Options()
		file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "", "", "Hex Files (*.hex *.ihx)", options=options)

		if file_path == '': return

		self.label_file_name.setText(file_path)
		print('Carregar arquivo: ' + str(file_path))
		self.text_log.append('Carregar arquivo: ' + str(file_path))
			
	#Verifica portas COM disponíveis
	def get_serial_ports(self):
		print('Atualizando portas COM')
		self.text_log.append('Atualizando portas COM')

		#Limpa ComboBox com conexões serial disponíveis
		self.input_com_port.clear()

		#Gera lista com nome das portas COM disponíveis
		if sys.platform.startswith('win'):
			ports = ['COM%s' % (i + 1) for i in range(256)]

		#Para realiza o port para linux:
		#elif sys.platform.startswith('linux'):
		#	ports = glob.glob('/dev/tty[A-Za-z]*')

		#Tenta se conectar a cada uma das portas na lista
		result = []
		for port in ports:
			try:
				s = serial.Serial(port)
				s.close()
				result.append(port)
			except (OSError, serial.SerialException):
				pass

		#Retorna lista com portas COM disponíveis
		if len(result) > 0:
			self.input_com_port.addItems(result)

	#Inicia conexão serial
	def open_serial(self):
		#Verifica se existe uma conexão serial em andamento
		if self.com_port != None and self.com_port.isOpen(): return
			
		#Adquire parâmetros de conexão
		port = self.input_com_port.currentText()
		baud_rate = self.input_baud_rate.currentText()
		
		#Tenta realiza conexão serial
		try:
			serial_port = serial.Serial(port, baud_rate)
		except:	
			print('Falha ao estabelecer conexão serial.') 
			self.text_log.append('Falha ao estabelecer conexão serial.')
			return

		#Conexão realizada
		print('Conexão serial estabelecida')
		self.text_log.append('Conexão serial estabelecida')
		self.com_port = serial_port

		#Atualiza exibição do status de conexão
		self.label_serial_status.setText('Conectado')
		self.label_serial_status.setStyleSheet('color: rgb(85, 170, 0)')

	#Finaliza conexão serial
	def close_serial(self):
		#Verifica se existe uma conexão serial em andamento
		if self.com_port != None and not self.com_port.isOpen(): return

		#Fecha conexão serial
		self.com_port.close()
		print('Desconectado da porta serial.')
		self.text_log.append('Desconectado da porta serial.')

		#Atualiza exibição do status de conexão
		self.label_serial_status.setText('Desconectado')
		self.label_serial_status.setStyleSheet('color: rgb(255, 0, 0)')


Application = QtWidgets.QApplication([])
Window = MainWindow()
Window.show()
Application.exec_()