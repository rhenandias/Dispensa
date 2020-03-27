// =================================================================================================
// Programa básico para comunicação entre o Arduino e o V-Rep
// =================================================================================================

// Definições Fixas - Limites das juntas do robô
#define elo1_min -45	//Ângulo mínimo para a Junta 1 (ang°)
#define elo1_max 225	//Ângulo máximo para a Junta 1 (ang°)
#define elo2_min -135	//Ângulo mínimo para a Junta 2 (ang°)
#define elo2_max 135	//Ângulo máximo para a Junta 2 (ang°)
#define zmin 0.132f			//Posição de repouso do eixo Z
#define zmax 0.030f

#define pot_j1 A2		//Potenciometro para Junta 1
#define pot_j2 A5		//Potenciometro para Junta 2
#define pot_j3 A1		//Potenciometro para Eixo z

// Variaveis Globais
float 	setpoint_t1;	//Setpoint para a Junta 1		
float 	setpoint_t2;	//Setpoint para a Junta 2
float 	setpointz;	    //Setpoint para o eixo z
float 	sensor_t1;		//Sensor para a Junta 1
float 	sensor_t2;		//Sensor para a Junta 2
float   sensorz;		//Sensor para o eixo z

// =================================================================================================
// Funções de Funcionalidade do Sistema
// =================================================================================================

//Função para arredondar valores floats em n casas decimais
float roundx(float value, byte n)
{
	return round(value * int(pow(10, n))) / pow(10, n);
}

//Ciclo de Comunicação
void com_cycle() 
{
	// Trata dados a enviar
	int send_setpoint1 = roundx(setpoint_t1, 1) * 10;
	int send_setpoint2 = roundx(setpoint_t2, 1) * 10;

	// Envia angulos de setpoint
	Serial.write((const char *) & send_setpoint2, sizeof(int));
	Serial.write((const char *) & send_setpoint1, sizeof(int));

	// Cria variaveis responsáveis pela leitura
	int incoming_value1, incoming_value2, incoming_value3;
	unsigned char buffer[2];

	// Executa leitura do sensor 1
	Serial.readBytes(buffer, sizeof(int));
	memcpy(& incoming_value1, buffer, sizeof(int));

	// Executa leitura do sensor 2
	Serial.readBytes(buffer, sizeof(int));
	memcpy(& incoming_value2, buffer, sizeof(int));

	// Executa adaptação dos valores lidos
	sensor_t1 = roundx(incoming_value1 / 10.0f, 1);
	sensor_t2 = roundx(incoming_value2 / 10.0f, 1);
}


void com_cycle1() //Comunicação para movimentação em Z
{
	//Trata dados a enviar
	int send_setpoint = roundx(setpointz, 3) * 1000;

	//Envia valor de setpoint z
	Serial.write((const char *) & send_setpoint, sizeof(int));

	//Cria variaveis responsáveis pela leitura
	int incoming_value;
	unsigned char buffer[2];

	//Executa leitura do sensor de eixo z
	Serial.readBytes(buffer, sizeof(int));
	memcpy(& incoming_value, buffer, sizeof(int));

	//executa adaptação dos valores lidos
	sensorz = roundx(incoming_value / 1000.0f, 3);
}

void start_setup() //Procimento de inicialização
{
	// Cria variaveis responsáveis pela leitura
	int incoming_value1, incoming_value2, incoming_value3, incoming_value4;
	unsigned char buffer[2];

	// Executa leitura do sensor 1
	Serial.readBytes(buffer, sizeof(int));
	memcpy(& incoming_value1, buffer, sizeof(int));

	// Executa leitura do sensor 2
	Serial.readBytes(buffer, sizeof(int));
	memcpy(& incoming_value2, buffer, sizeof(int));

	// Executa leitura do sensor Z
	Serial.readBytes(buffer, sizeof(int));
	memcpy(& incoming_value3, buffer, sizeof(int));

	// Executa adaptação dos valores lidos
	sensor_t1 = roundx(incoming_value1 / 10.0f, 1);
	sensor_t2 = roundx(incoming_value2 / 10.0f, 1);
	sensorz   = roundx(incoming_value3 / 1000.0f, 3);

	// Define setpoint inicial para posição atual
	setpoint_t1 = sensor_t1;
	setpoint_t2 = sensor_t2;
}

// =================================================================================================
// Funções do Arduino
// =================================================================================================

void setup()
{
	//Inicia porta de comunicação serial
	Serial.begin(230400);

	//Adquire ângulos iniciais do robô
	start_setup();

	pinMode(A2, INPUT);
	pinMode(A5, INPUT);
	pinMode(A1, INPUT);

	pinMode(A3, OUTPUT);
	digitalWrite(A3, LOW);

	pinMode(A4, OUTPUT);
	digitalWrite(A4, LOW);

	pinMode(6, OUTPUT);
	analogWrite(6, 255);
}

void loop()
{
	//Ciclo de Comunicação
	
	//Realiza leitura dos potenciometros
	int read_pot_j1 = analogRead(pot_j1);
	int read_pot_j2 = analogRead(pot_j2);
	int read_pot_j3 = analogRead(pot_j3);

	//Adapta valores aos limites das juntas
	read_pot_j1 = map(read_pot_j1, 0, 1024, elo1_min, elo1_max);
	read_pot_j2 = map(read_pot_j2, 0, 1024, elo2_min, elo2_max);
	read_pot_j3 = map(read_pot_j3, 0, 1024, zmax	, zmin	  );

	//Define setpoint de juntas
	setpoint_t1 = read_pot_j1;
	setpoint_t2 = read_pot_j2;
	setpointz   = read_pot_j3;

	//Realiza comunicação com o V-Rep
	com_cycle();
	com_cycle1();
}