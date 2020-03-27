#define pino_pwm	 6
#define pino_pot 	A2
#define pino_motor 	A1

void setup()
{
	Serial.begin(9600);
	pinMode(pino_pwm, OUTPUT);
}

void loop()
{
	int valor_pot   = analogRead(pino_pot);
	int valor_motor = analogRead(pino_motor);

	Serial.print("Pot:  ");
	Serial.println(valor_pot);

	Serial.print("Motor: ");
	Serial.println(valor_motor);

	analogWrite(pino_pwm, map(valor_pot, 0, 1024, 0, 255));
	delay(100);
}