
def change_element(combination, element):
	if element == 'C':
		combination[combination.index(element)] = 'W'
		element = 'W'

	return combination, element

combination = ['A', 'B', 'C', 'D']

for element in combination:
	
	if element == 'C':
		combination[combination.index(element)] = 'W'
		
	print('=====')
	print('combination: ' + str(combination))

