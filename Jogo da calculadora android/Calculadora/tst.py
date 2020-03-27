# -*- coding: utf-8 -*-
#Código
import itertools as it

compute1 = {
	#acc = compute[operation](acc)

	#Soma
	'+1' : lambda a : a + 1,
    '+2' : lambda a : a + 2,
    '+3' : lambda a : a + 3,
	'+4' : lambda a : a + 4,

	#Subtração
	'-2' : lambda a : a - 2,

	#Multiplicação
	'x4' : lambda a : a * 4,

	#Divisão
	'/4' : lambda a : a / 4,
	'/3' : lambda a : a / 3
}

def compute(expression, acc):
	#Adiciona um numero n ao final do total
	if   len(expression) == 1:
		#Computa linha
		hold = str(str(acc) + expression)
		#Verifica se o total começa com zero
		if hold[0] == '0': 
			#Remove 0 do inicio do total
			hold = hold.replace('0', '', 1)
		#Computa valor final
		return eval(hold)
	
	#Shift de 1 casa no total
	elif expression == "<<":
		return int(acc / 10)	

	#Expressão matemática	
	else:
		return eval(str(acc) + expression)

def evaluate():
	#Gera lista com todas as combinações possíveis
	possible_operations = it.product(available_operations, repeat = moves)

	#Percorre cada combinação gerada
	for combination in possible_operations:
		acc = start
		#Percorre cada movimento na combinação gerada
		for operation in combination:
			#Computa movimento
			acc = compute(operation, acc)
		#Verifica se encontrou o valor desejado
		if acc == target:
			return combination

problem = 23
target  = 10
moves 	= 4
start 	= 15
foo     = ['0', '+2', '/5']

available_operations = foo
resultado = evaluate()

print(resultado)

with open('solutions.txt', 'r') as file:
	data = file.readlines()
	lines = len(data)
	if lines == 0:
		data.append("Respostas dos Problemas\n")

line = str(problem) + " = " + str(resultado) + '\n'

if problem >= lines:
	#Sulução não gerada ainda, adicionar linha
	data.append(line)
else:
	#Solução já gerada, modificar existente
	data[problem] = line

with open('solutions.txt', 'w') as file:
	file.writelines(data)