#include "util.h"

#define debug 				false
#define elo1				0.467f
#define elo2				0.4005f

#define elo1_min			-45
#define elo1_max			225
#define elo2_min			-135
#define elo2_max			135

#define command_print		0
#define command_up 			1
#define command_down 		2
#define command_reset_graph 3

#define velocity_joint1		0.3f
#define velocity_joint2		0.3f

#define halt();				while(true){}

vector_angle setpoint, sensor;

byte scara_command = command_up;

vector4_angle 	inv;
vector_position dir;

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

vector4_angle check_envelope(vector4_angle inv_response)
{
	//Verifica se os valores obtidos com a cinematica inversa
	//estão dentro dos limites permitidos (aka work envelope)

	vector4_angle response;

	//Executa verificação para resposta 1
	response.t1 = (inv_response.t1 >= elo1_min && inv_response.t1 <= elo1_max)? inv_response.t1 : 9999;
	response.t2 = (inv_response.t2 >= elo2_min && inv_response.t2 <= elo2_max)? inv_response.t2 : 9999;

	//Executa verificação para resposta 2
	response.t3 = (inv_response.t3 >= elo1_min && inv_response.t3 <= elo1_max)? inv_response.t3 : 9999;
	response.t4 = (inv_response.t4 >= elo2_min && inv_response.t4 <= elo2_max)? inv_response.t4 : 9999;

	return response;
}

void moveP(float x, float y, bool interpolation)
{
	//Recebe posição de alvo em X, Y
	//Move para um ponto no espaço cartesiano
	
	//Calcula cinemática inversa
	vector4_angle inverse = inv_transform(x, y, elo1, elo2);

	//Executa verificação de envelope
	vector4_angle envelope = check_envelope(inverse);

	//Escolhe angulo mais próximo
	vector_angle output;

	//Computa diferenças para conjunto 1
	float dif1_elo1 = abs_dif(sensor.t1, envelope.t1);	//Diferença do t1 atual para t1 do conjunto 1
	float dif1_elo2 = abs_dif(sensor.t2, envelope.t2);	//Diferença do t2 atual para t2 do conjunto 1
	float dif_mean1 = (dif1_elo1 + dif1_elo2) / 2.0f;		

	//Computa diferenças para conjunto 2
	float dif2_elo1 = abs_dif(sensor.t1, envelope.t3);	//Diferença do t1 atual para t1 do conjunto 2
	float dif2_elo2 = abs_dif(sensor.t2, envelope.t4);	//Diferença do t2 atual para t2 do conjunto 2
	float dif_mean2 = (dif2_elo1 + dif2_elo2) / 2.0f;

	//Realiza escolha de conjuntos
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

void moveL(vector_position tgt_position)
{
	//Recebeu posição de alvo em X, Y
	//Move linearmente para um ponto no espaço cartesiano
}

void check()
{
	scara_command = command_print;
	com_cycle();
	scara_command = command_up;
}

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

void setup()
{
	//Inicia porta de comunicação serial
	Serial.begin(115200);

	//Atualiza comando para resetar gráfico
	scara_command = command_reset_graph;

	//Adquire angulos de inicio do robô
	start_setup();

	//Realiza primeiro ciclo de comunicação
	com_cycle();

	scara_command = command_up; 
}

void loop()
{
	scara_command = command_down;

	
	moveJ(-36.0f, 20.0f, true);
	delay(1000);

	moveJ(46.8f, -14.6f, true);
	delay(1000);

	moveJ(-21.9f, 56.1f, true);
	delay(1000);

	moveJ(0.0f, 0.0f, true);
	delay(1000);

	moveJ(176.9f, -14.6f, true);
	delay(1000);

	moveJ(90.0f, -45.1f, true);
	delay(1000);
	

	halt();

	/*
	scara_command = command_up;
	moveP(0.2f, 0.8f, true);
	delay(1000);

	scara_command = command_down;
	moveP(0.2f, 0.3f, true);
	delay(1000);

	scara_command = command_up;
	moveP(0.8f, 0.2f, true);
	delay(1000);

	scara_command = command_down;
	moveP(0.3f, 0.2f, true);
	delay(1000);
	

	scara_command = command_up;
	moveP(-0.6f, 0.4f, true);
	while(true) {}
	*/
	

	/*
	setpoint.t1 = 0.0f;
	setpoint.t2 = -90.0f;
	com_cycle();


	while(sensor.t1 <= 180)
	{
		setpoint.t1 = sensor.t1 + 0.1f;
		setpoint.t2 = sensor.t2 + 0.1f;
		com_cycle();

		if (sensor.t1 == 1)   scara_command = command_down;
		if (sensor.t1 == 45)  scara_command = command_up;
		if (sensor.t1 == 90)  scara_command = command_down;
		if (sensor.t1 == 135) scara_command = command_up;
	}
	*/

	/*
	vector4_angle inv1;

	dir = dir_transform(175.3, 67.4f, elo1, elo2);
	inv1 = inv_transform(dir.x, dir.y, elo1, elo2);

	Serial.println(dir.x);
	Serial.println(dir.y);
	Serial.println(inv1.t1);
	Serial.println(inv1.t2);
	Serial.println(inv1.t3);
	Serial.println(inv1.t4);
	*/

	
	//while(true) {}
}




