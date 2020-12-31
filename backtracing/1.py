# -*- coding: utf-8 -*- 

def evaluate_board(board):
	if board[0] + board[1] + board[2] != 15: return False
	if board[3] + board[4] + board[5] != 15: return False
	if board[6] + board[7] + board[8] != 15: return False

	if board[0] + board[3] + board[6] != 15: return False
	if board[1] + board[4] + board[7] != 15: return False
	if board[2] + board[5] + board[8] != 15: return False

	return True

board = [8, 0, 0, 3, 5, 7, 4, 9, 0]

# Primeiramente vamos gerar uma lista com os indexes dos valores alteraveis no board
emptys = []
for idx, position in enumerate(board):
	if position == 0:
		emptys.append(idx)

print("Indexes modificaveis:", emptys)

# Node 0
for n0_value in range(1, 10):
	n0_board = board.copy()
	n0_board[emptys[0]] = n0_value

	if n0_value in board:
		continue
		
	# Node 1
	for n1_value in range(1, 10):
		n1_board = n0_board.copy()
		n1_board[emptys[1]] = n1_value

		if n1_value in n0_board:
			continue

		# Node 2
		for n2_value in range(1, 10):
			n2_board = n1_board.copy()
			n2_board[emptys[2]] = n2_value

			# Condição de escape para o node 2
			if n2_value in n1_board:
				continue
			
			if not evaluate_board(n2_board):
				continue

			print("Valid Board", n2_board)


def prof2():
	# Node 0
	for n1_value in range(1, 10):
		# O board para o node 1 vai ser igual ao board anterior
		n1_board = board.copy()
		# Gera novo board para esse node
		# O nome 0 é tem liberar para alterar o elemento 0 da lista de modificaveis
		n1_board[emptys[0]] = n1_value

		# Condição de escape para o node 1, verificar conflito em relação ao board anterior
		if n1_value in board:
			continue

		# Node 1
		for n2_value in range(1, 10):
			# Novamente o board para esse node vai ser igual ao board anterior
			n2_board = n1_board.copy()
			# O nome 1 é tem liberar para alterar o elemento 1 da lista de modificaveis
			n2_board[emptys[1]] = n2_value

			# Condição de escape para o node 2
			if n2_value in n1_board:
				continue

			# Passou por todas as condições de escape
			# Tentativa válida, chamar função de validação
			print("Evaluate board ", n2_board)