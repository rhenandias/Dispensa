#define analog_in A0

int value1, value2;

float position_1, position_2;
float angle1, angle2;

byte sync = 0;

void setup()
{
	Serial.begin(9600);

	//Sincronização
	while(!sync)
	{
		while(Serial.available() == 0) {}
		if(Serial.read() == 116)
		{
			Serial.println(116);
			sync = 1;
		}

	}
}

void loop()
{
	// 1 - Envia angulos para serem escritos no client
	Serial.println(angle1);
	Serial.println(angle2 + 90);

	// 2 - Aguarda receber algum dado do client
	while(Serial.available() == 0) {}

	// 3 - Armazena angulos de sensor recebidos do client
	position_1 = Serial.parseInt();
	position_2 = Serial.parseInt() - 900;

	//Recebe número inteiro e transforma em float
	position_1 = position_1 / 10;
	position_2 = position_2 / 10;

	// 4 - Trata os dados recebidos
	angle1 = (position_1 < 180)? position_1 += 1 : 0;
	angle2 = angle1 - 90;

	angle1 += 0.5;

}

