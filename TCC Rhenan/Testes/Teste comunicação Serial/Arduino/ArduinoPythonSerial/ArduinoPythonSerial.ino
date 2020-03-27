void setup()
{
	Serial.begin(230400);
}

void loop()
{
	/*
	float my_value;
	for(my_value = 0.0f; my_value < 180.0f; my_value+= 0.1f)
	{
	 	Serial.write((const char *)&my_value, sizeof(float));
	}
	*/
	

	/*
	int my_value;
	for(my_value = -900; my_value < 900; my_value += 1)
	{
	 	Serial.write((const char *)&my_value, sizeof(int));
	}
	*/
	
	/*
	float my_value;
	for(my_value = 0.0f; my_value < 180.0f; my_value+= 0.1f)
	{
	 	Serial.println(my_value);
	}
	*/
	
	
	//Leitura de Valores
	int incoming_value;
	unsigned char buffer[2];

	// If we read enough bytes, unpacked it
	if (Serial.readBytes(buffer, sizeof(int)) == sizeof(int))
		memcpy(&incoming_value, buffer, sizeof(int));

	int my_value = incoming_value;

	//Escritas de Valores
	Serial.write((const char *)&my_value, sizeof(int));	
	

	//while(true){}
}