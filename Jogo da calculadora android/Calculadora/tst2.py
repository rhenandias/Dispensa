import itertools as it 

def compute(expression, acc):
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

def l_shift(acc):
	acc = str(acc)
	part1 = acc[1:]
	part2 = acc[0]
	return eval(part1 + part2)	

def r_shift(acc):
	acc = str(acc)
	part1 = acc[-1]
	part2 = acc[0:-1]
	return eval(part1 + part2)	

value = compute('1>0', -15)
print(value)

print(l_shift(1123))
print(r_shift(5432))