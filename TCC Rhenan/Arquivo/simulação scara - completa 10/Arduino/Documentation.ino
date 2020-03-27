//Documentação

//=================================================================================================
// Funções de Movimento
//=================================================================================================

void moveJ(float t1, float t2, bool interpolation)
{
	//Recebe posição de juntas em t1, t2 em graus
	//Move para um ponto no espaço das juntas

	//Com a interpolação ativa, ambas as juntas chegarão juntas ao angulo alvo
	//Com a interpolação desativada, as juntas respeitarão suas velocidades de movimento
}

void moveP(float x, float y, bool interpolation)
{
	//Recebe posição de espaço em X, Y em coordenadas cartesianas
	//Move para um ponto no espaço cartesiano

	//Com a interpolação ativa, ambas as juntas chegarão juntas ao angulo alvo
	//Com a interpolação desativada, as juntas respeitarão suas velocidades de movimento
}

void moveL(float x, float y, byte points)
{
	//Recebe posição de espaço em X, Y em coordenadas cartesianas
	//Move linearmente para um ponto no espaço cartesiano, a partir do ponto atual

	//O parâmetro points expressa a quantidade de pontos a serem feitos durante a reta
	//Quanto maior o número de pontos, mais precisa a reta
}

//=================================================================================================
// Comandos
//=================================================================================================

halt()
{
	//Executa função de congelamento no sistema do arduino
	//Executa geralmente ao fim de uma rotina de movimento
}

cmd_reset()
{
	//Executa reset do gráfico no V-Rep
	//Função executada no setup do arduino
	//Caso exista algum gráfico plotado no V-Rep, ele é apagado
	//Valor passado ao V-Rep como comando
}

cmd_up()
{
	//Comando para levantar a "caneta" no V-Rep
	//Quanto dado o cmd_up, a escrita no gráfico não é registrada
	//Valor passado ao V-Rep como comando
}

cmd_down()
{
	//Comando para abaixar a "caneta" no V-Rep
	//Quando dado o cmd_down, a escrita no grafico é registrada
	//Valor passado ao V-Rep como comando
}

cmd_end()
{
	//Finaliza simulação no V-Rep
	//Valor tratado apenas no arquivo client.py, não é passado ao V-Rep como comando
}

cmd_debug()
{
	//Informa o client que os valores a seguir serão tratados como debug
	//Valor tratado apenas no arquivo client.py, não é passado ao V-Rep como comando
}

//=================================================================================================
// Funções Auxiliares
//=================================================================================================

void debug(String text, float value)
{
	//Realiza escrita de valor de Debug no client.py
	//A cada função de debug é passado um texto, e um valor de debug
}

vector_angle closest_group(vector4_angle group)
{
	//Define conjunto de posições mais proxima dos angulos atuais
	//Recebe com conjunto de 4 angulos:
	//(t1, t2) e (t2, t3)
	//Define qual conjunto está mais próximo dos sensores atuais
}

//=================================================================================================
// Funções de Funcionalidades do Sistema
//=================================================================================================

void com_cycle()
{
	//Realiza um ciclo de comunicação
	//1 - Realiza escrita do comando atual
	//2 - Realiza escrita do setpoint atual
	//3 - Realiza leitura do sensor atual
}

void start_graph()
{
	//Inicia gráfico no V-Rep
	//Realiza a seguinte ordem:

	//1 - Levanta Caneta
	//2 - Com Cycle
	//3 - Abaixa Caneta
	//4 - Com Cycle

	//Isso garante que seja escrito um ponto no grafico
	//O V-Rep inprime um "CURVE" ao lado do primeiro ponto
	//Função apenas de cunho estético, uma vez que o "CURVE" pode atrapalhar 
	//a visualização do trajeto final
}

