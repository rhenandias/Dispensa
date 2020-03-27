#define pino_escrita	6
#define pino_leitura	A1

#define periodo					15		//Intervalo entre as coletas (ms)
#define	tempo_total_de_amostra 	2500	//Tempo total da coleta (ms)
#define inicio_da_subida		500		//Tempo de inicio de subida do setpoint (ms)
#define porcentagem_setpoint	35		//Porcentagem do setpoint 0 - 100 (%)

unsigned long ultimo_tempo, start;
unsigned int setpoint = 0;

byte* vetor_setpoint;	
float*	 vetor_leitura;	
unsigned int* vetor_tempo;

unsigned int indice;
unsigned int n;
boolean iniciou_subida = false;

void setup()
{
	//Inicializa porta serial e controle de tempo
	Serial.begin(9600);

	pinMode(pino_escrita, OUTPUT);
	analogWrite(pino_escrita, 0);

	//Define tamanho das arrays de setpoint e leitura
	n = tempo_total_de_amostra / periodo;
	Serial.print("Tamanho dos vetores: ");
	Serial.println(n);

	unsigned int estimativa_de_memoria = (2 * (n * 2)) + n;
	Serial.print("Estimativa de memória: ");
	Serial.print(estimativa_de_memoria);
	Serial.println(" bytes");

	//Aloca memória necessária para as arrays
	delete [] vetor_setpoint;		
	delete [] vetor_leitura;
	delete [] vetor_tempo;
	vetor_setpoint = new byte[n];
	vetor_leitura  = new float[n];
	vetor_tempo    = new unsigned int[n];

	Serial.println("Envie 's' para começar a coleta");

	while(!Serial.available()){};
	while(true)
	{
		char comando = char(Serial.read());
		if(comando == 's') break;
	}

	Serial.println("Iniciando Coleta");
	start = millis();
}

void loop()
{
	if(indice < n)
	{
		unsigned long tempo_atual = millis();

		if(tempo_atual - start > ultimo_tempo + periodo)
		{
			ultimo_tempo = tempo_atual - start;

			vetor_setpoint[indice] = setpoint;
			vetor_leitura[indice]  = analogRead(pino_leitura);
			vetor_tempo[indice]    = ultimo_tempo;

			indice++;
		}

		if((tempo_atual - start > inicio_da_subida) && !iniciou_subida)
		{
			iniciou_subida = true;
			setpoint = porcentagem_setpoint;
			analogWrite(pino_escrita, map(setpoint, 0, 100, 0, 255));
		}
	}
	else
	{
		analogWrite(pino_escrita, 0);

		Serial.println("Leitura Finalizada\n");

	
		//Adapta vetor de leitura para valores de tensão
		for (unsigned int i = 0; i < n ; i++)
		{
			vetor_leitura[i] = (5 * vetor_leitura[i])/1023;
		}

		Serial.println("T (ms)\tSet (%)\tMotor (V)");
		for(unsigned int i = 0; i < n; i++)
		{
			String line = String(vetor_tempo[i]) + "\t" + String(vetor_setpoint[i]) + "\t" + String(vetor_leitura[i]);
			Serial.println(line);
		}

		while(true) {};
	}
	
}