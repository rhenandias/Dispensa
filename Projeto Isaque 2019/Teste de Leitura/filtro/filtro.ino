#define pino_escrita 9
#define pino_leitura A1
#define pot A0

void setup()
{
	Serial.begin(9600);
	pinMode(pino_escrita, OUTPUT);
	analogWrite(pino_escrita, 0);
}

void loop()
{
	uint16_t valor_pot = analogRead(pot);
	analogWrite(pino_escrita, map(valor_pot, 0, 1023, 0, 255));
	uint16_t valor_lido = analogRead(pino_leitura);
	Serial.println(valor_lido);

	delay(100);
}