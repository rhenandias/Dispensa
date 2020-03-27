#include "vector.h"

float sensor1, sensor2;
float setpoint1, setpoint2, setpoint3, setpoint4;

vector4_angle inv;
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

	t1 = abs(degrees(t1));
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

	t1 = abs(degrees(t1));
	t2 = degrees(t2);

	res.t3 = t1;
	res.t4 = t2;

	return res;
}

float round1(float value)
{
	return round(value * 10) / 10.0f;
}

void test_cycle()
{
	//Trata dados a enviar
	float send_setpoint1 = round1(setpoint1);
	float send_setpoint2 = round1(setpoint2) + 90.0f;
	float send_setpoint3 = round1(setpoint3);
	float send_setpoint4 = round1(setpoint4) + 90.0f;

	//Envia angulos de setpoint
	Serial.println(send_setpoint1);
	Serial.println(send_setpoint2);
	Serial.println(send_setpoint3);
	Serial.println(send_setpoint4);
}

void com_cycle2()
{
	//Trata dados a enviar
	int send_setpoint1 = round1(setpoint1) * 10;
	int send_setpoint2 = round1(setpoint2) * 10;

	//Envia angulos de sepoint1
	Serial.write((const char *)&send_setpoint2, sizeof(int));
	Serial.write((const char *)&send_setpoint1, sizeof(int));

	//Cria variaveis responsáveis pela leitura
	int incoming_value1, incoming_value2;
	unsigned char buffer[2];

	//Executa leitura do sensor 1
	while(Serial.available() < sizeof(int)){}		
	Serial.readBytes(buffer, sizeof(int));			
	memcpy(&incoming_value1, buffer, sizeof(int));	

	//Executa leitura do sensor 2
	while(Serial.available() < sizeof(int)){}
	Serial.readBytes(buffer, sizeof(int));
	memcpy(&incoming_value2, buffer, sizeof(int));

	//Executa adaptação dos valores lidos
	sensor1 = round1(incoming_value1 / 10.0f);
	sensor2 = round1(incoming_value2 / 10.0f);
}

void com_cycle3() //Backup
{
	//Trata dados a enviar
	int send_setpoint1 = round1(setpoint1) * 10;
	int send_setpoint2 = round1(setpoint2) * 10;

	//Envia angulos de sepoint1
	Serial.write((const char *)&send_setpoint2, sizeof(int));
	Serial.write((const char *)&send_setpoint1, sizeof(int));

	int incoming_value1, incoming_value2;
	unsigned char buffer[2];

	if (Serial.readBytes(buffer, sizeof(int)) == sizeof(int))
		memcpy(&incoming_value1, buffer, sizeof(int));
	if (Serial.readBytes(buffer, sizeof(int)) == sizeof(int))
		memcpy(&incoming_value2, buffer, sizeof(int));

	sensor1 = round1(incoming_value1 / 10.0f);
	sensor2 = round1(incoming_value2 / 10.0f);
}


void com_cycle()
{
	//Trata dados a enviar
	float send_setpoint1 = round1(setpoint1);
	float send_setpoint2 = round1(setpoint2);

	//Envia angulos de setpoint
	Serial.println(send_setpoint1);
	Serial.println(send_setpoint2);

	//Aguarda receber algum sinal do client
	while(Serial.available() == 0) {}

	//Armazena valores recebidos
	int received_sensor1 = Serial.parseInt();
	int received_sensor2 = Serial.parseInt() - 900;

	//Trata os valores recebidos
	sensor1 = round1(received_sensor1 / 10.0f);
	sensor2 = round1(received_sensor2 / 10.0f);
}

void setup()
{
	//Inicia porta de comunicação serial
	Serial.begin(230400);
}

void loop()
{
	/*
	for(int i = 0; i <= 180; i += 90)
	{
		for(int j = -90; j <= 90; j += 90)
		{
			Serial.println("============================");
			Serial.print(i);
			Serial.print(",");
			Serial.println(j);

			dir = dir_transform(i, j, 0.4, 0.4);
			inv = inv_transform(dir.x, dir.y, 0.4, 0.4);
			setpoint1 = inv.t1;
			setpoint2 = inv.t2;
			setpoint3 = inv.t3;
			setpoint4 = inv.t4;
			test_cycle();
		}
	}
	*/

	/*
	dir = dir_transform(90, 90, 0.4, 0.4);
	inv = inv_transform(dir.x, dir.y, 0.4, 0.4);
	setpoint1 = inv.t1;
	setpoint2 = inv.t2;
	setpoint3 = inv.t3;
	setpoint4 = inv.t4;
	test_cycle();
	*/

	//com_cycle();
	

	//delay(1000);
	setpoint1 = 0.0f;
	setpoint2 = -90.0f;
	com_cycle2();


	while(sensor1 <= 180)
	{
		setpoint1 = sensor1 + 0.1f;
		setpoint2 = sensor2 + 0.1f;
		com_cycle2();
	}
	
	
	/*
	setpoint1 = 174.3;
	setpoint2 = -45.7;

	com_cycle();

	setpoint1 = sensor1 + 0.2f;
	setpoint2 = sensor2 + 0.2f;

	com_cycle();

	setpoint1 = sensor1 + 0.2f;
	setpoint2 = sensor2 + 0.2f;

	com_cycle();
	*/

	while(true) {}

}




