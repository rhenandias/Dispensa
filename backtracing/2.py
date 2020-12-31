# -*- coding: utf-8 -*- 

def evaluate_board(board):
	if board[0] + board[1] + board[2] != target: return False
	if board[3] + board[4] + board[5] != target: return False
	if board[6] + board[7] + board[8] != target: return False

	if board[0] + board[3] + board[6] != target: return False
	if board[1] + board[4] + board[7] != target: return False
	if board[2] + board[5] + board[8] != target: return False

	return True

def evaluate_row(board):
	if board[0] != 0 and board[1] != 0 and board[2] != 0:
		if board[0] + board[1] + board[2] != target: return False
	if board[3] != 0 and board[4] != 0 and board[5] != 0:
		if board[3] + board[4] + board[5] != target: return False
	if board[6] != 0 and board[7] != 0 and board[8] != 0:
		if board[6] + board[7] + board[8] != target: return False
		
	if board[0] != 0 and board[3] != 0 and board[6] != 0:
		if board[0] + board[3] + board[6] != target: return False
	if board[1] != 0 and board[4] != 0 and board[7] != 0:
		if board[1] + board[4] + board[7] != target: return False
	if board[2] != 0 and board[5] != 0 and board[8] != 0:
		if board[2] + board[5] + board[8] != target: return False

	return True

center = 5
target = center * 3
range_max = center + 5
single = False

board = [0, 0, 0, 0, center, 0, 0, 0, 0]

valids = []

emptys = []
for idx, position in enumerate(board):
	if position == 0:
		emptys.append(idx)

depth = len(emptys)
value_range = range(1, range_max)

print("Indices modificaveis:", emptys)
print("Depth:", depth)

def run_node(node_idx, last_board, single_combination):
	print("Iniciando com idx", node_idx)
	for node_value in value_range:
		current_board = last_board.copy()
		current_board[emptys[node_idx]] = node_value

		if node_value in last_board:
			continue

		if not evaluate_row(current_board):
			continue

		if node_idx == depth - 1:
			if evaluate_board(current_board):
				print("Valid Board", current_board)
				valids.append(current_board)
				if single_combination:
					return "END"
		else:
			next_node = run_node(node_idx + 1, current_board, single)
			if single_combination:
				if next_node == "END":
					return "END"

run_node(0, board, single)

print("Valid solutions", len(valids))
for valid in valids:
	print(valid)