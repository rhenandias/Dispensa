import generic_backtracing as backtracing

# Função para verificar se uma combinação representa um quadrado mágico
# Valida a combinação final gerada, se ela passou por todas as condições de saída
def evaluate_board(params):
	board = params[2]
	# Verifica Linhas
	if board[0] + board[1] + board[2] != target: return False
	if board[3] + board[4] + board[5] != target: return False
	if board[6] + board[7] + board[8] != target: return False
	# Verifica Colunas
	if board[0] + board[3] + board[6] != target: return False
	if board[1] + board[4] + board[7] != target: return False
	if board[2] + board[5] + board[8] != target: return False
	return True

# Função para validar colunas e linhas
# Essa função diz com antescedencia se uma linha ou coluna que esteja completa é valida ou não
# Se temos uma coluna inválida, não precisamos verificar o quadrado todo
# Por isso, essa função é uma condição de saída
def evaluate_row_and_column(params):
	board = params[2]
	# Verifica linhas
	if board[0] != 0 and board[1] != 0 and board[2] != 0:
		if board[0] + board[1] + board[2] != target: return True
	if board[3] != 0 and board[4] != 0 and board[5] != 0:
		if board[3] + board[4] + board[5] != target: return True
	if board[6] != 0 and board[7] != 0 and board[8] != 0:
		if board[6] + board[7] + board[8] != target: return True
	# Verifica colunas
	if board[0] != 0 and board[3] != 0 and board[6] != 0:
		if board[0] + board[3] + board[6] != target: return True
	if board[1] != 0 and board[4] != 0 and board[7] != 0:
		if board[1] + board[4] + board[7] != target: return True
	if board[2] != 0 and board[5] != 0 and board[8] != 0:
		if board[2] + board[5] + board[8] != target: return True
	return False

def number_repeat(params):
	node_value = params[0]
	last_board = params[1]
	if node_value in last_board:
		return True
	return False

last = []
# Configurações do Backtracing
backtracing.empty_identifier = 0
backtracing.evaluate_hash.append(evaluate_board)
backtracing.exit_conditions.append(number_repeat)
backtracing.exit_conditions.append(evaluate_row_and_column)

# Configuração das Regras
center = 5
target = center * 3
range_max = center + 5
single = True
board = [0, 0, 0, 0, center, 0, 0, 0, 0]


emptys = list(backtracing.create_emptys(board))
print("Emptys", emptys)

depth = backtracing.get_depth(emptys)
print("Depth", depth)

valid_squares = backtracing.run_node(0, range(1, range_max), depth, board, emptys, single)

for valid in backtracing.valid_hashes:
	print(valid)
