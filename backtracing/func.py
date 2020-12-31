funcs = []

def func1():
	return True

def func2():
	return False


funcs.append(func1)
funcs.append(func2)
funcs.append(None)
funcs.append(func1)

for func in funcs:
	if func:
		if func():
			print("Executou")
	else:
		print("Vazio")