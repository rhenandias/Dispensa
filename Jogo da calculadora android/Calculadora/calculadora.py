import itertools as it
from tkinter import *
import time

class Application:
	def __init__(self, master):
		#Parâmetros do problema
		self.problem = 22
		self.target  = 9
		self.moves 	= 4
		self.start 	= 0
		self.av_oper = []

		self.debug_state = 1

		master.title('Calculator: The Game Solver')
		master.geometry('400x400')

		#Cria conteineres para as linhas
		self.line_problem 				= Frame(master)
		self.line_target 				= Frame(master)
		self.line_moves					= Frame(master)
		self.line_start 				= Frame(master)
		self.line_evaluate				= Frame(master)
		self.line_result				= Frame(master)
		self.line_add_operation			= Frame(master)
		self.line_operations			= Frame(master)
		self.line_add_operations_title 	= Frame(master)
		self.line_availabe_operations 	= Frame(master)
		self.line_debug_button			= Frame(master)
		self.line_debug_man_operation	= Frame(master)

		self.line_invisible_1			= Frame(master)
		self.line_invisible_2			= Frame(master)
		self.line_invisible_3			= Frame(master)
		self.line_invisible_4			= Frame(master)
		
		self.line_problem.pack()
		self.line_target.pack()
		self.line_moves.pack()
		self.line_start.pack()
		self.line_invisible_1.pack(pady=10)
		self.line_add_operations_title.pack()
		self.line_add_operation.pack()
		self.line_availabe_operations.pack()
		self.line_operations.pack()
		self.line_invisible_2.pack(pady=10)
		self.line_evaluate.pack()
		self.line_result.pack()
		self.line_invisible_3.pack(pady=10)
		self.line_debug_button.pack()
		self.line_invisible_4.pack(pady=5)
		self.line_debug_man_operation.pack()

		#==================================================================================================
		# Seleção do Problema
		#==================================================================================================
		self.label_problem = Label(self.line_problem, text="Problema           ")
		self.label_problem.pack(side=LEFT)

		#vcmd_problem = (master.register(self.validate_entry_problem), '%d', '%P', '%S')
		self.entry_problem = Entry(self.line_problem)#, validate = 'key', validatecommand = vcmd_problem)
		self.entry_problem["width"] = 30
		self.entry_problem.pack(side=RIGHT)

		#==================================================================================================
		# Configuração do Objetivo
		#==================================================================================================
		self.label_target = Label(self.line_target, text="Objetivo             ")
		self.label_target.pack(side=LEFT)

		#vcmd_target = (master.register(self.validate_entry_target), '%d', '%P', '%S')
		self.entry_target = Entry(self.line_target)#, validate = 'key', validatecommand = vcmd_target)
		self.entry_target["width"] = 30
		self.entry_target.pack(side=RIGHT)

		#==================================================================================================
		# Configuração da Quantidade de Movimentos
		#==================================================================================================
		self.label_moves = Label(self.line_moves, text="Movimentos      ")
		self.label_moves.pack(side=LEFT)

		self.entry_moves = Entry(self.line_moves)
		self.entry_moves["width"] = 30
		self.entry_moves.pack(side=RIGHT)

		#==================================================================================================
		# Configuração do Valor Inicial
		#==================================================================================================
		self.label_start = Label(self.line_start, text="Inicio                  ")
		self.label_start.pack(side=LEFT)

		self.entry_start = Entry(self.line_start)
		self.entry_start["width"] = 30
		self.entry_start.pack(side=RIGHT)

		#==================================================================================================
		# Adicionar Operações Disponíveis
		#==================================================================================================
		#Titulo
		self.label_title_add_operations = Label(self.line_add_operations_title, text = 'Adicionar Operações')
		self.label_title_add_operations.pack()
		
		#Entrada 
		self.entry_add_operation = Entry(self.line_add_operation)
		self.entry_add_operation['width'] = 10
		self.entry_add_operation.pack(side=LEFT)
		self.entry_add_operation.bind('<Control_R>', self.call_run)

		#Botão
		self.button_add_operation = Button(self.line_add_operation)
		self.button_add_operation['text'] = 'Add'
		self.button_add_operation['command'] = self.add_operation
		self.button_add_operation.pack(side=RIGHT)
		self.entry_add_operation.bind('<Return>', self.add_operation)
		
		#Titulo
		self.label_available_operations_title = Label(self.line_availabe_operations, text = 'Operações Disponíveis')
		self.label_available_operations_title.pack()

		#Operações
		self.label_available_operations = Label(self.line_operations, text = '[   ]')
		self.label_available_operations.pack()

		#==================================================================================================
		# Botão de Evaluate / Clear
		#==================================================================================================
		self.button_evaluate = Button(self.line_evaluate)
		self.button_evaluate['text'] = 'Validar'
		self.button_evaluate['command'] = self.run
		self.button_evaluate.pack(side=LEFT)
		self.button_evaluate.bind('<FocusIn>', self.set_focus_to_operation_entry)

		self.button_clear = Button(self.line_evaluate)
		self.button_clear['text'] = 'Limpar'
		self.button_clear['command'] = self.clear
		self.button_clear.pack(side=LEFT)
		master.bind('<Delete>', self.clear)
		master.bind('<Escape>', self.clear)

		#==================================================================================================
		# Exibição do Resultado
		#==================================================================================================
		self.label_result = Label(self.line_result)
		self.label_result.pack()

		#==================================================================================================
		# Debug
		#==================================================================================================
	
		self.button_debug_show = Button(self.line_debug_button, text = 'Exibir Debug')
		self.button_debug_show['command'] = self.toggle_debug
		self.button_debug_show.pack()


		self.label_acumulado = Label(self.line_debug_man_operation, text = 'Total   ')
		self.label_acumulado.pack(side=LEFT)

		self.entry_acumulado = Entry(self.line_debug_man_operation)
		self.entry_acumulado['width'] = 10
		self.entry_acumulado.pack(side=LEFT)

		self.label_manual_operation = Label(self.line_debug_man_operation, text = '   Operação  ')
		self.label_manual_operation.pack(side=LEFT)

		self.entry_manual_operation = Entry(self.line_debug_man_operation)
		self.entry_manual_operation['width'] = 10
		self.entry_manual_operation.pack(side=LEFT)
		self.entry_manual_operation.bind('<Return>', self.compute_debug)

		self.button_debug_compute = Button(self.line_debug_man_operation, text = 'Validar')
		self.button_debug_compute['command'] = self.compute_debug
		self.button_debug_compute.pack(side=LEFT, padx = 10)
		
	def compute_debug(self, foo= None):
		total 		= eval(self.entry_acumulado.get())
		expression 	= self.entry_manual_operation.get()
		result = self.compute(expression, total)
		self.entry_acumulado.delete(0, END)
		self.entry_acumulado.insert(0, result)
		self.entry_manual_operation.delete(0, END)

	def toggle_debug(self):
		if self.debug_state:
			#Desativar Debug
			self.debug_state = 0
			self.line_debug_man_operation.pack_forget()
		else:
			#Ativar debug
			self.debug_state = 1
			self.line_debug_man_operation.pack()

	def set_focus_to_operation_entry(self, foo=None):
		self.entry_add_operation.focus()

	def call_run(self, foo=None):
		self.run(self)

	#Função de execução do botão Run
	def run(self, foo=None):
		self.problem = eval(self.entry_problem.get())
		self.target  = eval(self.entry_target.get())
		self.moves 	= eval(self.entry_moves.get())
		self.start 	= eval(self.entry_start.get())

		resultado = self.evaluate(self.av_oper, self.target, self.moves, self.start)
		print(resultado)

		if self.problem != None:
			self.write_answer(self.problem, resultado)

		if resultado != None:
			resultado = '[' + ',   '.join(resultado) + ']'
		else:
			resultado = "Resultado não encontrado"

		self.label_result['text'] = resultado

	def clear(self, foo = None):
		self.entry_problem.delete(0, END)
		self.entry_target.delete(0, END)
		self.entry_moves.delete(0, END)
		self.entry_start.delete(0, END)
		self.label_available_operations['text'] = '[   ]'
		self.label_result['text'] = ''
		self.av_oper = []

		self.entry_problem.focus()

	def add_operation(self, foo=None):
		self.av_oper.append(self.entry_add_operation.get())
		self.entry_add_operation.delete(0, END)
		formated_av_oper = '[' +  ',   '.join(self.av_oper) + ']'
		self.label_available_operations['text'] = formated_av_oper

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

	#Computa uma unica expressão
	def compute(self, expression, acc, foo = None):

		if 'mirro' in expression:
			pass
			
		if 'shift' in expression:
			#Verifica se o valor acumulado é negativo
			#Armazena essa informação em um multiplicador
			mult = 1 if acc >= 0 else -1
			#Retira sinal "-" da string, só de segurança
			acc = str(acc).replace('-', '')
			
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
			while part1[0] == '0':
				part1 = part1.replace('0', '', 1)
				if len(part1) == 0: 
					part1 = '0'
					break

			while part2[0] == '0':
				part2 = part2.replace('0', '', 1)
				if len(part1) == 0: 
					part2 = '0'
					break

			#Unifica as partes
			total = part1 + part2

			#Retira os zeros inicias do total
			while total[0] == '0':
				total = total.replace('0', '', 1)
				if len(total) == 0: 
					total = '0'
					break

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
			while acc[0] == '0':
				acc = acc.replace('0', '', 1)
				if len(acc) == 0: 
					acc = '0'
					break
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
			while acc[0] == '0':
				acc = acc.replace('0', '', 1)
				if len(acc) == 0: 
					acc = '0'
					break
			#Valida resultado final
			return eval(acc) * mult			

		#Shift de 1 casa 
		if '<<' in expression:
			return int(acc / 10)

		#Expressão matemática
		if any([i in expression for i in ['+', '-', '/', '*']]):
			#Executa expressão matematica
			hold = eval(str(acc) + expression)
			#Verifica se valor gerou um float com casa decimal zero
			#Ex: 15/3 irá gerar 5.0, retornar 5
			if int(hold) == hold : hold = int(hold)
			return hold

		#Número Solto
		else:
			#Computa linha
			hold = str(str(acc) + expression)
			#Verifica se o total começa com zero
			if hold[0] == '0': 
				#Remove 0 do inicio do total
				hold = hold.replace('0', '', 1)
			#Computa valor final
			return eval(hold)

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
				acc = self.compute(operation, acc)
			#Verifica se encontrou o valor desejado
			if acc == target:
				return combination

root = Tk()
Application(root)
root.mainloop()