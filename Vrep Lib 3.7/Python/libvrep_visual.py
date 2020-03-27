# -*- coding: utf-8 -*-
from screen import *
import libvrep
import sys, serial

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

	def __init__(self, vrep):
		QtWidgets.QMainWindow.__init__(self)
		self.setupUi(self)

		#Parâmetros do programa

		#Inicializa portas COM
		self.get_serial_ports()	

		#Adiciona funcionalidade aos botões
		self.input_update_com_ports.clicked.connect(self.get_serial_ports)	#Atualizar portas COM
		self.input_open_com.clicked.connect(self.open_serial)				#Conectar Serial
		self.input_close_com.clicked.connect(self.close_serial)				#Desconectar Serial
		self.input_connect_vrep.clicked.connect(self.connect_vrep)			#Conectar Vrep
		self.input_disconnect_vrep.clicked.connect(self.disconnect_vrep)	#Desconectar Vrep
		self.input_insert_joint.clicked.connect(self.insert_joint)			#Insere Junta
		self.input_remove_joint.clicked.connect(self.remove_joint)			#Remove Junta
		

	#Insere Junta no banco de dados de juntas
	def insert_joint(self):
		#Adquire parâmetros da junta a ser inserida
		joint_name  = self.input_joint_name.text()			#Nome da Junta
		joint_id 	= self.input_joint_id.value()			#ID da Junta
		joint_type  = self.input_joint_type.currentText()	#Tipo da Junta

		#limpa entrada do nome da junta
		self.input_joint_name.clear()					

		#Adquire quantidade de linhas e define a próxima a ser inserida
		row = self.list_joints.rowCount()
		row = 0 if row == None else row

		#Insere nova linha na tabela
		self.list_joints.insertRow(row)

		#Insere items
		self.list_joints.setItem(row, 0, QtWidgets.QTableWidgetItem(joint_name))		#Nome
		self.list_joints.setItem(row, 1, QtWidgets.QTableWidgetItem(str(joint_id)))		#ID
		self.list_joints.setItem(row, 2, QtWidgets.QTableWidgetItem(joint_type))		#Tipo

		#Formata alinhamento da columa de ID
		self.list_joints.item(row, 1).setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)

		#Realiza sorting por ordem crescente na coluna de IDs
		self.list_joints.sortByColumn(1, 0)

	#Remove Junta do banco de dados de juntas
	def remove_joint(self):
		#Remove item selecionado 
		self.list_joints.removeRow(self.list_joints.currentRow())

		#Realiza sorting por odem crescente na coluna de IDs
		self.list_joints.sortByColumn(1, 0)

	#Realiza conexão com o Vrep
	def connect_vrep(self):
		#Realiza conexão com o Vrep
		vrep_state = vrep.connect_vrep()

		#Atualiza exibição do status de conexão com o Vrep	
		if vrep_state: 
			self.label_vrep_status.setText('Conectado')
			self.label_vrep_status.setStyleSheet('color: rgb(85, 170, 0)')

	#Finaliza conexão com o Vrep
	def disconnect_vrep(self):
		#Finaliza conexão com o Vrep
		vrep_state = vrep.disconnect_vrep()

		#Atualiza exibição do status de conexão com o Vrep
		if vrep_state: 
			self.label_vrep_status.setText('Desconectado')
			self.label_vrep_status.setStyleSheet('color: rgb(255, 0, 0)')

	#Verifica portas COM disponíveis
	def get_serial_ports(self):

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
		#Adquire porta COM e Baud rate
		com_port  = self.input_com_port.currentText()
		baud_rate = self.input_baud_rate.currentText()
		
		#Estabelece conexão serial
		serial_state = vrep.open_serial(com_port, baud_rate)

		#Atualiza exibição do status de conexão
		if serial_state: 
			self.label_serial_status.setText('Conectado')
			self.label_serial_status.setStyleSheet('color: rgb(85, 170, 0)')

	#Finaliza conexão serial
	def close_serial(self):
		#Fecha conexão serial
		serial_state = vrep.close_serial()

		#Atualiza exibição do status de conexão
		if serial_state: 
			self.label_serial_status.setText('Desconectado')
			self.label_serial_status.setStyleSheet('color: rgb(255, 0, 0)')


#Objeto de manipulação da Libvrep
vrep = libvrep.libvrep()
vrep.__init__()

Application = QtWidgets.QApplication([])
Window = MainWindow(vrep)
Window.show()
Application.exec_()