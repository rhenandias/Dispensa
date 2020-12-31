
empty_identifier = None
exit_conditions = []
evaluate_hash = []
single_combination = False
valid_hashes = []

hash_log = []

# Função para criar uma lista de indíces vazios, que serão alteráveis na execução
def create_emptys(initial_hash):
  # Essa função pega cada posição vazia na hash inicial, ou seja, cada posição alteravel
  # E salva o seu indíce em um construtor (utilizar emptys = list(create_emptys(initial_hash)))
  for idx, position in enumerate(initial_hash):
    if position == empty_identifier:
      yield idx

# Define a profundidade da árvore, quantos valores alteráveis existem
def get_depth(emptys):
  return len(emptys)

def run_node(node_idx, value_range, depth, last_hash, emptys, single_combination = False):
  # Na execução de cada node percorremos os valores possíveis que uma célula vazia pode assumir
  for node_value in value_range:
    # Agora vamos executar uma cópia do hash imediatamente anterior
    current_hash = last_hash.copy()

    # Podemos entar alterar o hash e gerar um hash para a execução atual
    # Alteramos a posição referente a profundidade executada de acordo com um valor possível
    # Para um node_idx de 0 -> hash = [0, 0, 0] -> [1, 0, 0]
    current_hash[emptys[node_idx]] = node_value

    params = [node_value, last_hash, current_hash]

    # Condições de Saída
    # Aqui vão todas as condições de saída possíveis, quantas forem necessárias
    # As condições de saída devem retornar True caso deva sair, False quando deva continuar
    # Se pergunte o seguinte "Devo sair da execução? Estou em uma condição de saída?"
    # if should_exit:
    # 	continue 
    for idx, condition in enumerate(exit_conditions):
      if condition(params):
        continue

    # Recursividade
    # Caso não estejamos no final da profundidade da árvore, chamamos o próximo node
    # Caso chegamos ao final, não há nada a se fazer senão validar a combinação gerada
    if node_idx == depth - 1:
      # print("Board completo, validar")
      if evaluate_hash[0]:
        # Temos uma função de validaçao inserida
        combination_is_valid = evaluate_hash[0](params)
        if combination_is_valid:
          valid_hashes.append(current_hash)
          if single_combination:
            return "END"
    # Não chegamos ao final, executar a recursividade
    else:
      # print("Chamando proximo node a partir do idx", node_idx)
      # Executar próximo node, com parametro de last hash como a hash atual, e indíce como o atual + 1
      next_node = run_node(node_idx + 1, value_range, depth, current_hash, emptys, single_combination)
      # Condição de saída da recursividade caso queiramos apenas uma solução
      # Caso se deseje apenas uma solução e ela foi encontrada, passar o código "END" para a chamada raíz
      # Caso se deseje todas as soluções possíveis, continuar de onde foi a chadamada do último node
      if single_combination and next_node == "END":
        return "END"


