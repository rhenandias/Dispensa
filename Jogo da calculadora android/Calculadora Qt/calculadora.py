from screen_ui import *
import itertools as it

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		self.setupUi(self)

		self.clear()

		#Parâmetros do problema
		self.problem 	= 0		#Índice do problema
		self.target 	= 0		#Objetivo do problema
		self.moves 		= 0		#Movimentos disponíveis
		self.start 		= 0		#Valor inicial
		self.av_oper 	= []	#Array para as operações disponíveis

		#Adiciona função ao botão 'Add' 
		self.button_add_operation.clicked.connect(self.add_operation)

		#Adiciona função ao botão 'Validar'
		self.button_evaluate.clicked.connect(self.run)

		#Adiciona função ao botão 'Limpar'
		self.button_clear.clicked.connect(self.clear)

		#Adiciona função do botão 'Validar' de Debug
		self.button_evaluate_manual_operation.clicked.connect(self.evaluate_debug)


	def clear(self):
		#Executa limpeza dos valores anteriores
		self.input_problem.clear()							#Limpa o valor do problema
		self.input_target.clear()							#Limpa o valor do objetivo
		self.input_moves.clear()							#Limpa a quantidade de movimentos
		self.input_start.clear()							#Limpa o valor inicial
		self.label_available_operations.setText('[   ]')	#Limpa as operações disponíveis
		self.label_result.setText('[   ]')					#Limpa o resultado anterior
		self.av_oper = []									#Reinicia a array de operações disponíveis
		self.input_manual_operation.clear()					#Limpa entrada de operação manual
		self.input_total.clear()							#Limpa valor total da operação manual
		self.input_problem.setFocus()						#Devolve o foco de volta ao problema

	def evaluate_debug(self):
		#Adquires valores de operação manual
		total 		= self.input_total.value()				#Adquire valor total acumulado
		expression 	= self.input_manual_operation.text()	#Adquiera operação a ser computada
		result 		= self.compute(expression, total)		#Resultado da operação

		#Atualiza exibição do resultado 			
		self.input_total.setValue(result)					#Exibe valor total acumulado
		self.input_manual_operation.clear()					#Limpa entrada de operação manual
		self.input_manual_operation.setFocus()				#Devolve foco a entrada de operação manua

	def add_operation(self):
		#Adiciona operação a array de operações disponíveis
		self.av_oper.append(self.input_operation.text())

		#Atualiza a exibição de operações disponíveis
		self.input_operation.clear()								#Limpa a exibição da lista
		formated_av_oper = '[' +  ',   '.join(self.av_oper) + ']'	#Formata nova lista
		self.label_available_operations.setText(formated_av_oper)	#Atualiza exibição

		#Devolve foco para entrada de operações
		self.input_operation.setFocus()

	def run(self):
		#Adquire entradas do problema
		self.problem = self.input_problem.value()	#Adquire número do problema
		self.target = self.input_target.value()		#Adquire objetivo do problema
		self.moves = self.input_moves.value()		#Adquire quantidade de movimentos
		self.start = self.input_start.value()		#Adquire valor inicial

		#Executa solução do problema
		resultado = self.evaluate(self.av_oper, self.target, self.moves, self.start)
		print('Resultado: ' + str(resultado))
		
		#Verifica se foi encontrado um resultado
		if resultado != None:
			#executa escrita do resultado no arquivo de soluções
			if self.problem != None:
				self.write_answer(self.problem, resultado)

			#Formata resultado para exibição na tela
			resultado = '[' + ',   '.join(resultado) + ']'
		else:
			resultado = "Resultado não encontrado"

		#Atualiza exibição do resultado
		self.label_result.setText(resultado)

	#Escreve uma solução encontrada no arquivo de soluções
	def write_answer(self, problem, resultado):
		with open('solutions.txt', 'r') as file:
			#Realiza leitura do arquivo de soluções
			data = file.readlines()
			#Contabiliza quantidade de problemas solucionados
			lines = len(data)
			#Cria cabeçalho caso nenhuma solução registrada
			if lines == 0: data.append("Respostas dos Problemas\n")

		#Cria linha com indice do problema e solução
		line = str(problem) + " = " + str(resultado) + '\n'

		#Verifica existencia da solução em questão
		if problem >= lines:
			#Sulução não gerada ainda, adicionar linha
			data.append(line)
		else:
			#Solução já gerada, modificar existente
			data[problem] = line

		#Realiza escrita no arquivo de soluções
		with open('solutions.txt', 'w') as file:
			file.writelines(data)

	#Gera e computa todas as combinações de expressões possíveis
	def evaluate(self, available_operations, target, moves, start):
		#Gera lista com todas as combinações possíveis
		possible_operations = it.product(available_operations, repeat = moves)

		#Percorre cada combinação gerada
		for combination in possible_operations:
			print("Iniciando tentativa para: " + str(combination))
			acc = start
			#Percorre cada movimento na combinação gerada
			for operation in combination:
				#Computa movimento
				if acc != None: acc = self.compute(operation, acc, combination)
				#Atualiza os parâmetros
				self.move -= 1
				self.start = acc 
			#Verifica se encontrou o valor desejado
			if acc == target:
				return combination
	
	#Computa uma unica expressão
	def compute(self, expression, acc, combination, foo = None):

		if '[+]1' in expression:
			pass


		if 'mirror' in expression:
			#Verifica se o valor acumulado é negativo
			#Armazena essa informação em um multiplicador
			mult = 1 if acc >= 0 else -1
			#Retira sinal "-" da string, só de segurança
			acc = str(acc).replace('-', '')
			#Tamanho maximo para operação mirror é de 3 casas
			#O limite de caracteres na tela é de 6 casas
			if len(acc) > 3: return None
			#Inverte o valor acumulado e adiciona ao fim		
			acc = acc + acc[::-1]
			#Remove zeros do inicio 
			acc = self.remove_zeros(acc)
			#Valida resultado
			return eval(acc) * mult
			
		if 'shift' in expression:
			#Verifica se o valor acumulado é negativo
			#Armazena essa informação em um multiplicador
			mult = 1 if acc >= 0 else -1
			#Retira sinal "-" da string, só de segurança
			acc = str(acc).replace('-', '')
			#Tamanho minimo para shift precisa ser maior ou igual a 2
			if len(acc) == 1: return eval(acc)
			#Holders para as partes 1 e 2 do shift
			part1 = None
			part2 = None
			#Shift para a Esquerda
			if '<' in expression:
				part1 = acc[1:]
				part2 = acc[0]
			#Shift para a Direita
			if '>' in expression:
				part1 = acc[-1]
				part2 = acc[0:-1]
			#Retira os zeros iniciais da parte 1 e 2
			part1 = self.remove_zeros(part1)
			part2 = self.remove_zeros(part2)
			#Unifica as partes
			total = part1 + part2
			#Retira os zeros inicias do total
			total = self.remove_zeros(total)
			#Valida o resultado
			return eval(total) * mult

		#Soma todos os valores do acumulador
		if 'sum' in expression:
			#Verifica se o valor acumulado é inteiro
			if type(acc) != int : return 0			
			#Verifica se o valor acumulado é negativo
			#Armazena essa informação em um multiplicador
			mult = 1 if acc >= 0 else -1
			#Retira sinal "-" da string, só de segurança
			acc = str(acc).replace('-', '')
			#Separa elementos do acumulador
			acc = [int(i) for i in str(acc)] 
			#Valida o resultado
			return sum(acc) * mult

		#Reverte o valor total
		if 'reverse' in expression:
			#Valor acumulado precisa ser diferente de 0
			if acc == 0: return acc
			#Verifica se o valor acumulado é negativo
			#Armazena essa informação em um multiplicador
			mult = 1 if acc >= 0 else -1
			#Retira sinal "-" da string, só de segurança
			acc = str(acc).replace('-', '')
			#Reverte valor total convertendo em string
			acc = str(acc)[::-1]
			#Verifica se o primeiro digito se tornou um zero
			acc = self.remove_zeros(acc)
			#Valida valor total (com multiplicador)
			return eval(acc) * mult

		#Troca de sinais
		if '+/-' in expression:
			return acc * -1

		#Potência matemática
		if 'x^' in expression:
			power = int(expression.split('x^')[1])
			return pow(acc, power)

		#Troca de dígitos
		if '>' in expression:
			#Separa expressão em duas partes
			digits = expression.split('>')
			#Verifica se o valor acumulado é negativo
			#Armazena essa informação em um multiplicador
			mult = 1 if acc >= 0 else -1
			#Retira sinal "-" da string, só de segurança
			acc = str(acc).replace('-', '')
			#Realiza troca de dígitos
			acc = str(acc).replace(digits[0], digits[1])
			#Verifica e remove zeros do inicio do número
			acc = self.remove_zeros(acc)
			#Valida resultado final
			return eval(acc) * mult			

		#Shift de 1 casa 
		if '<<' in expression:
			return int(acc / 10)

		#Expressão matemática
		if any([i in expression for i in ['+', '-', '/', '*']]):
			#Executa expressão matematica
			hold = eval(str(acc) + expression)
			#Verifica se valor gerou um float com casa decimal diferente de zero
			#Ex: 15/3 irá gerar 5.0, retornar 5, valor valido
			#Ex: 3/2 irá gerar 1.5, valor invalido, nao pode retornar apenas 1

			if int(hold) == hold : hold = int(hold)
			else: return None

			return int(hold)

		#Número Solto
		else:
			#Computa linha
			hold = str(str(acc) + expression)
			#Verifica se o total começa com zero
			if hold[0] == '0': hold = hold.replace('0', '', 1)
			#Computa valor final
			return eval(hold)


	def remove_zeros(self, acc):
		while acc[0] == '0':
				acc = acc.replace('0', '', 1)
				if len(acc) == 0: 
					acc = '0'
					break
		return acc

Application = QtWidgets.QApplication([])
Window = MainWindow()
Window.show()
Application.exec_()