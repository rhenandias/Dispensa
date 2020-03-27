#include "util.h"

//=================================================================================================
// Definições
//=================================================================================================

#define elo1				0.467f
#define elo2				0.4005f

#define elo1_min			-45
#define elo1_max			225
#define elo2_min			-135
#define elo2_max			135

#define velocity_joint1		0.3f
#define velocity_joint2		0.3f
#define threshold			0.1f

//=================================================================================================
// Comandos
//=================================================================================================

byte scara_command = 1;

#define halt();				while(true){}
#define cmd_up();			scara_command = 1;
#define cmd_down();			scara_command = 2;
#define cmd_reset();		scara_command = 3;
#define cmd_end();			{scara_command = 4; com_cycle();}
#define cmd_debug();		scara_command = 5;

//=================================================================================================
// Variaveis
//=================================================================================================

vector_angle setpoint, sensor, last_setpoint;

vector4_angle 	inv;
vector_position dir;

//=================================================================================================
// Funções de Cinemática Trigonométrica
//=================================================================================================

vector_position dir_transform(float t1, float t2, float l1, float l2)
{
	//Define vetores de posição
	vector_position r1, r2, r3;

	//Calcula vetores individuais para Elo 1
	r1.x = l1 * cos(radians(t1));
	r1.y = l1 * sin(radians(t1));

	//Calcula vetores individuais para Elo 2
	r2.x = l2 * cos(radians(t1 + t2));
	r2.y = l2 * sin(radians(t1 + t2));

	//Realiza soma vetorial para posição final
	r3.x = r1.x + r2.x;
	r3.y = r1.y + r2.y;

	return r3;
}

vector4_angle inv_transform(float x, float y, float l1, float l2)
{
	vector4_angle res;
	float t1, t2, num, den;

	//Calculo para t2 positivo
	t2 = acos((pow(x, 2) + pow(y, 2) - pow(l1, 2) - pow(l2, 2))/(2 * l1 * l2));

	//Verifica exceção na função acos
	if(isnan(t2)) t2 = 0;

	num = y * (l1 + l2 * cos(t2)) - x * l2 * sin(t2);
	den = x * (l1 + l2 * cos(t2)) + y * l2 * sin(t2);
	t1 = atan2(num, den);

	//t1 = abs(degrees(t1));
	t1 = degrees(t1);
	t2 = degrees(t2);

	res.t1 = t1;
	res.t2 = t2;

	//Calculo para t2 negativo
	t2 = -acos((pow(x, 2) + pow(y, 2) - pow(l1, 2) - pow(l2, 2))/(2 * l1 * l2));

	//Verifica exceção na funçao acos
	if(isnan(t2)) t2 = 0;

	num = y * (l1 + l2 * cos(t2)) - x * l2 * sin(t2);
	den = x * (l1 + l2 * cos(t2)) + y * l2 * sin(t2);
	t1 = atan2(num, den);

	//t1 = abs(degrees(t1));
	t1 = degrees(t1);
	t2 = degrees(t2);

	res.t3 = t1;
	res.t4 = t2;

	return res;
}

//=================================================================================================
// Funções de Movimento
//=================================================================================================

void moveP(float x, float y, bool interpolation)
{
	//Recebe posição de espaço em X, Y
	//Move para um ponto no espaço cartesiano
	
	//Calcula cinemática inversa
	vector4_angle envelope = inv_transform(x, y, elo1, elo2);

	//Computa diferenças para conjunto 1
	float dif1_elo1 = abs_dif(sensor.t1, envelope.t1);	//Diferença do t1 atual para t1 do conjunto 1
	float dif1_elo2 = abs_dif(sensor.t2, envelope.t2);	//Diferença do t2 atual para t2 do conjunto 1
	float dif_mean1 = (dif1_elo1 + dif1_elo2) / 2.0f;		

	//Computa diferenças para conjunto 2
	float dif2_elo1 = abs_dif(sensor.t1, envelope.t3);	//Diferença do t1 atual para t1 do conjunto 2
	float dif2_elo2 = abs_dif(sensor.t2, envelope.t4);	//Diferença do t2 atual para t2 do conjunto 2
	float dif_mean2 = (dif2_elo1 + dif2_elo2) / 2.0f;

	//Realiza escolha de conjuntos
	vector_angle output;
	output.t1 = (dif_mean1 <= dif_mean2)? envelope.t1 : envelope.t3;
	output.t2 = (dif_mean1 <= dif_mean2)? envelope.t2 : envelope.t4;

	//Realiza movimento
	moveJ(output.t1, output.t2, interpolation);
}

void moveJ(float t1, float t2, bool interpolation)
{
	//Recebe posição de juntas em t1, t2
	//Move para um ponto no espaço das juntas

	//Computa diferenças de angulos
	float dif_elo1 = abs_dif(sensor.t1, t1);	//Diferença do t1 atual para t1 do alvo
	float dif_elo2 = abs_dif(sensor.t2, t2);	//Diferença do t2 atual para t2 do alvo

	//Computa sentido de movimento (crescente ou decrescente)
	char sign_t1 = (sensor.t1 > t1)? -1 : 1;
	char sign_t2 = (sensor.t2 > t2)? -1 : 1;

	//Flags
	float step_t1 = 0,     step_t2   = 0;		//Angulo de incremento a cada ciclo de movimento
	int amount_t1 = 0,     amount_t2 = 0;		//Quantidade de ciclo de movimento
	int count_t1  = 0,     count_t2  = 0;		//Contador de ciclos já realizados
	bool moveP_j1 = 0, 	   moveP_j2  = 0;		//Movimento finalizado

	if(interpolation)
	{	
		//Movimento com interpolação de juntas

		if(dif_elo1 > dif_elo2)
		{
			//Diferença no elo 1 é maior, serve de unidade para o movimento
			step_t1   = velocity_joint1;
			amount_t1 = round(dif_elo1 / step_t1);

			step_t2 = dif_elo2 / amount_t1;
			amount_t2 = round(dif_elo2 / step_t2);
		} else
		{
			//Diferença no elo 2 é maior, serve de unidade para o movimento
			step_t2   = velocity_joint2;
			amount_t2 = round(dif_elo2 / step_t2);

			step_t1 = dif_elo1 / amount_t2;
			amount_t1 = round(dif_elo1 / step_t1);
		}

	} else
	{
		//Movimento sem interpolação de Juntas

		//Define quantidade de pontos de movimento nas juntas
		amount_t1 = round(dif_elo1 / velocity_joint1);
		amount_t2 = round(dif_elo2 / velocity_joint2);

		//Define steps como sendo a resoluçaõ da junta
		step_t1 = velocity_joint1;
		step_t2 = velocity_joint2;
	}

	//Realiza movimento
	while(!moveP_j1 || !moveP_j2)
	{
		//Movimento para junta 1
		if(count_t1++ < amount_t1) setpoint.t1 += (step_t1 * sign_t1);
		else moveP_j1 = true;

		//Movimento para junta 2
		if(count_t2++ < amount_t2) setpoint.t2 += (step_t2 * sign_t2);
		else moveP_j2 = true;

		com_cycle();
	}
}

void moveL(float x, float y, byte points)
{
	//Recebe posição de espaço em X, Y
	//Move linearmente para um ponto no espaço cartesiano

	vector_position cur_position = dir_transform(sensor.t1, sensor.t2, elo1, elo2);

	float dif_x = abs_dif(x, cur_position.x);
	float dif_y = abs_dif(y, cur_position.y);

	char sign_x = (cur_position.x > x)? -1 : 1;
	char sign_y = (cur_position.y > y)? -1 : 1;

	byte interpolation_type = 0;

	if(dif_y <= threshold && dif_x > threshold) 		interpolation_type = 0;	//Interpolação em x
	else if(dif_x <= threshold && dif_y > threshold)	interpolation_type = 1;	//Interpolação em y
	else if(dif_x > threshold && dif_y > threshold) 	interpolation_type = 2; //Interpolação normal

	//Flags
	int count = 0;
	float next_x = 0;
	float next_y = 0;
	float step_x = 0;
	float step_y = 0;

	switch(interpolation_type)
	{
		case 0:	step_x = dif_x / points;
				while(count++ < points)
				{
					//Computa próima posição de x
					next_x = cur_position.x + (sign_x * step_x * count);

					//Computada cinématica inversa para próximos ponto
					vector4_angle group = inv_transform(next_x, cur_position.y, elo1, elo2);

					//Realiza escolah do conjunto mais próximo
					vector_angle output = closest_group(group);

					//Atualiza setpoint
					setpoint.t1 = output.t1;
					setpoint.t2 = output.t2;

					com_cycle();
				}
			break;

		case 1:	step_y = dif_y / points;
				while(count++ < points)
				{
					//Computa próima posição de y
					next_y = cur_position.y + (sign_y * step_y * count);

					//Computada cinématica inversa para próximos ponto
					vector4_angle group = inv_transform(cur_position.x, next_y, elo1, elo2);

					//Realiza escolah do conjunto mais próximo
					vector_angle output = closest_group(group);

					//Atualiza setpoint
					setpoint.t1 = output.t1;
					setpoint.t2 = output.t2;

					com_cycle();
				}
			break;

		default: 
			break;
	}
}

//=================================================================================================
// Funções Auxiliares
//=================================================================================================

void debug(String text, float value)
{
	//Seleciona comando de modo debug
	cmd_debug();

	//Envia byte de comando
	Serial.write(scara_command);

	//Envia texto de debug
	Serial.println(text);

	//Trata valor de debug a ser enviado
	int send_value = round1(value) * 10;

	//Envia valor de debug
	Serial.write((const char *)&send_value, sizeof(int));
}

vector_angle closest_group(vector4_angle group)
{
	//Realiza escolha de angulos mais próximos dos atuais

	vector_angle response;

	//Computa diferenças para conjunto 1
	float dif1_elo1 = abs_dif(sensor.t1, group.t1);	//Diferença do t1 atual para t1 do conjunto 1
	float dif1_elo2 = abs_dif(sensor.t2, group.t2);	//Diferença do t2 atual para t2 do conjunto 1
	float dif_mean1 = (dif1_elo1 + dif1_elo2) / 2.0f;		

	//Computa diferenças para conjunto 2
	float dif2_elo1 = abs_dif(sensor.t1, group.t3);	//Diferença do t1 atual para t1 do conjunto 2
	float dif2_elo2 = abs_dif(sensor.t2, group.t4);	//Diferença do t2 atual para t2 do conjunto 2
	float dif_mean2 = (dif2_elo1 + dif2_elo2) / 2.0f;

	//Realiza escolha de conjuntos
	response.t1 = (dif_mean1 <= dif_mean2)? group.t1 : group.t3;
	response.t2 = (dif_mean1 <= dif_mean2)? group.t2 : group.t4;

	return response;
}

//=================================================================================================
// Funções de Funcionalidade do Sistema
//=================================================================================================

void com_cycle()
{
	//Envia byte de comando
	Serial.write(scara_command);

	//Trata dados a enviar
	int send_setpoint1 = round1(setpoint.t1) * 10;
	int send_setpoint2 = round1(setpoint.t2) * 10;

	//Envia angulos de sepoint1
	Serial.write((const char *)&send_setpoint2, sizeof(int));
	Serial.write((const char *)&send_setpoint1, sizeof(int));

	//Cria variaveis responsáveis pela leitura
	int incoming_value1, incoming_value2;
	unsigned char buffer[2];

	//Aguarda bytes disponiveis no buffer de leitura Serial
	while(Serial.available() < sizeof(int)){}

	//Executa leitura do sensor 1	
	Serial.readBytes(buffer, sizeof(int));			
	memcpy(&incoming_value1, buffer, sizeof(int));	

	//Executa leitura do sensor 2
	Serial.readBytes(buffer, sizeof(int));
	memcpy(&incoming_value2, buffer, sizeof(int));

	//Executa adaptação dos valores lidos
	sensor.t1 = round1(incoming_value1 / 10.0f);
	sensor.t2 = round1(incoming_value2 / 10.0f);
}

void start_setup()
{
	//Cria variaveis responsáveis pela leitura
	int incoming_value1, incoming_value2;
	unsigned char buffer[2];

	//Aguarda bytes disponiveis no buffer de leitura Serial
	while(Serial.available() < sizeof(int)){}

	//Executa leitura do sensor 1	
	Serial.readBytes(buffer, sizeof(int));			
	memcpy(&incoming_value1, buffer, sizeof(int));	

	//Aguarda bytes disponiveis no buffer de leitura Serial
	while(Serial.available() < sizeof(int)){}

	//Executa leitura do sensor 2
	Serial.readBytes(buffer, sizeof(int));
	memcpy(&incoming_value2, buffer, sizeof(int));

	//Executa adaptação dos valores lidos
	sensor.t1 = round1(incoming_value1 / 10.0f);
	sensor.t2 = round1(incoming_value2 / 10.0f);

	//Define setpoint inicial para posição atual
	setpoint.t1 = sensor.t1;
	setpoint.t2 = sensor.t2;
}

//=================================================================================================
// Funções de Desenho
//=================================================================================================

void quadrado()
{
	//Quadrado com Interpolação Linear
	cmd_up();					//Levanta caneta
	moveP(0.3f, 0.6f, true);	//Movimenta para o ponto inicial
	delay(1000);

	cmd_down();					//Abaixa caneta
	moveL(0.6f, 0.6f, 10);
	delay(1000);
	moveL(0.6f, 0.3f, 10);
	delay(1000);
	moveL(0.3f, 0.3f, 10);
	delay(1000);
	moveL(0.3f, 0.6f, 10);
	delay(1000);

	cmd_up();					//Levanta caneta
	moveJ(0.0f, 0.0f, true);	//Movimenta para ponto de repouso
	halt();
}

void ifsp()
{
	//"I"
	cmd_up();
	moveP(-0.35f, 0.70f, true);	
	delay(500);
	cmd_down();
	moveL(-0.25f, 0.70f, 60);		
	cmd_up();
	moveP(-0.3f, 0.70f, true);	
	cmd_down();
	moveL(-0.3f, 0.50f, 120);		
	cmd_up();
	moveP(-0.35f, 0.50, true);	
	cmd_down();
	moveL(-0.25f, 0.50f, 60);
	cmd_up();

	//"F"
	moveP(-0.15f, 0.50f, true);
	delay(500);
	cmd_down();
	moveL(-0.15f, 0.70f, 120);
	moveL(-0.05f, 0.70f, 60);
	cmd_up();
	moveP(-0.15f, 0.60f, true);
	cmd_down();
	moveL(-0.05f, 0.60f, 60);
	cmd_up();

	//"S"
	moveP(0.05f, 0.50f, true);
	delay(500);
	cmd_down();
	moveL(0.15f, 0.50f, 60);
	moveL(0.15f, 0.60f, 60);
	moveL(0.05f, 0.60f, 60);
	moveL(0.05f, 0.70f, 60);
	moveL(0.15f, 0.70f, 60);
	cmd_up();

	//"P"
	moveP(0.25f, 0.60f, true);
	delay(500);
	cmd_down();
	moveL(0.35f, 0.60f, 120);
	moveL(0.35f, 0.70f, 60);
	moveL(0.25f, 0.70f, 60);
	moveL(0.25f, 0.50f, 60);
	cmd_up();

	moveJ(0, 0, true);

	cmd_end();
	com_cycle();
}

void i()
{
	//"I"
	cmd_up();
	moveP(-0.35f, 0.70f, true);	
	delay(500);
	cmd_down();
	moveL(-0.25f, 0.70f, 60);		
	cmd_up();
	moveP(-0.3f, 0.70f, true);	
	cmd_down();
	moveL(-0.3f, 0.50f, 120);		
	cmd_up();
	moveP(-0.35f, 0.50, true);	
	cmd_down();
	moveL(-0.25f, 0.50f, 60);
	cmd_up();

	moveJ(0, 0, true);
}

//=================================================================================================
// Funções do Arduino
//=================================================================================================

void setup()
{
	//Inicia porta de comunicação serial
	Serial.begin(230400);

	//Envia comando para resetar gráfico
	cmd_reset();

	//Adquire angulos de inicio do robô
	start_setup();

	//Realiza primeiro ciclo de comunicação
	com_cycle();
}

void loop()
{

	i();

	cmd_end();

	halt();
}





