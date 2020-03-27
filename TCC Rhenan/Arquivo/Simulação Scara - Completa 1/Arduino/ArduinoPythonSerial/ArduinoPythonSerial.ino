#define analog_in A0

int value1, value2;

void setup()
{
	Serial.begin(9600);
}

void loop()
{
		value1 = analogRead(A0);
		value1 = map(value1, 0, 1023, 0, 180);
	 	Serial.println(value1);

	 	value2 = value1 - 90;
	 	Serial.println(value2);

	 delay(200);
}