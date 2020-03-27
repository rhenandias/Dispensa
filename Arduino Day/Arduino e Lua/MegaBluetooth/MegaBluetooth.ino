
HardwareSerial & vrep 	    = Serial;
HardwareSerial & bluetooth 	= Serial3;

char command = 'P';

void setup() 
{
	bluetooth.begin(9600);
	vrep.begin(9600);
	
}

void loop() 
{
	if(bluetooth.available())
	{
		command = bluetooth.read();
	}

	switch(command)
	{
		//Para o carrinho
		case 'P':	vrep.println('P');
					break;

		//Movimentação para a Frente
		case 'F':	vrep.println('F');
					break;

		//Movimentação para a Trás
		case 'B':	vrep.println('T');
					break;
					
		//Movimentação para a Direita
		case 'R':	vrep.println('D');
					break;

		//Movimentação para a Esquerda
		case 'L':	vrep.println('E');
					break;
		
		default:	break;
	}	
}