#define analog_in A0

int value1, value2;

float sensor1, sensor2;
float angle1, angle2;

byte sync = 0;

void com_cycle()
{
	//Envia angulos de setpoint
	Serial.println(angle1);
	Serial.println(angle2 + 90);

	//Aguarda receber algum sinal do client
	while(Serial.available() == 0) {}

	//Armazena valores recebidos
	sensor1 = Serial.parseInt();
	sensor2 = Serial.parseInt() - 900;

	//Recebe os angulos em número inteiro e transforma em float
	sensor1 = sensor1 / 10;
	sensor2 = sensor2 / 10;
}

void sync_serial()
{
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

void setup()
{
	//Inicia porta de comunicação serial
	Serial.begin(9600);

	//Sincroniza client python com arduino
	sync_serial();
}

void loop()
{
	//Executa ciclo de comunicação com o vrep
	com_cycle();

	//Executa tratamento de cinemática
	angle1 = (sensor1 < 180)? sensor1 += 0.1 : 0;
	angle2 = angle1 - 90;

}



