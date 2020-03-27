void moveJ(float t1, float t2, bool interpolation)
{
	// Recebe posição de juntas em t1, t2
	// Move para um ponto no espaço das juntas
	// Computa diferenças de angulos
	float dif_elo1 = abs_dif(sensor.t1, t1); // Diferença do t1 atual para t1 do alvo
	float dif_elo2 = abs_dif(sensor.t2, t2); // Diferença do t2 atual para t2 do alvo
	// Computa sentido de movimento (crescente ou decrescente)
	char sign_t1 = (sensor.t1 > t1)? -1:1;
	char sign_t2 = (sensor.t2 > t2)? -1:1;
	// Flags
	float step_t1 = 0, step_t2 = 0; // Angulo de incremento a cada ciclo de movimento
	int amount_t1 = 0, amount_t2 = 0; // Quantidade de ciclo de movimento
	int count_t1 = 0, count_t2 = 0; // Contador de ciclos já realizados
	bool moveP_j1 = 0, moveP_j2 = 0; // Movimento finalizado

	if (interpolation)
	{
		// Movimento com interpolação de juntas
		if (dif_elo1 > dif_elo2)
		{
			// Diferença no elo 1 é maior, serve de unidade para o movimento
			step_t1 = velocity_joint1;
			amount_t1 = round(dif_elo1 / step_t1) + 1;
			step_t2 = dif_elo2 / amount_t1;
			amount_t2 = round(dif_elo2 / step_t2) + 1;
		}
		else
		{
			// Diferença no elo 2 é maior, serve de unidade para o movimento
			step_t2 = velocity_joint2;
			amount_t2 = round(dif_elo2 / step_t2) + 1;
			step_t1 = dif_elo1 / amount_t2;
			amount_t1 = round(dif_elo1 / step_t1) + 1;
		}
	}
	else
	{
		// Movimento sem interpolação de Juntas
		// Define quantidade de pontos de movimento nas juntas
		amount_t1 = round(dif_elo1 / velocity_joint1);
		amount_t2 = round(dif_elo2 / velocity_joint2);
		// Define steps como sendo a resoluçaõ da junta
		step_t1 = velocity_joint1;
		step_t2 = velocity_joint2;
	}


	//debug("step = ", step_t1);
	//debug("count = ", amount_t1);
	//delay(2000);
	float soma = 0;
	// Realiza movimento
	while (!moveP_j1 || !moveP_j2)
	{

		// Movimento para junta 1
		if (count_t1++ < amount_t1)
		{
			setpoint.t1 += (step_t1 * sign_t1);
		}else
			moveP_j1 = true;

		// Movimento para junta 2
		if (count_t2++ < amount_t2)
		{
			setpoint.t2 += (step_t2 * sign_t2);
		}else
			moveP_j2 = true;


		last_sensor = sensor;
		com_cycle();


		soma = 0;

		soma += abs_dif(last_sensor.t1, sensor.t1) * sign_t1;
		soma += abs_dif(last_sensor.t2, sensor.t2) * sign_t2;
		setpointr = sensorr - soma;

		com_cycle2();
	}
}


void moveJ(float t1, float t2, bool interpolation)
{
	// Recebe posição de juntas em t1, t2
	// Move para um ponto no espaço das juntas

	// Computa diferenças de angulos
	float dif_elo1 = abs_dif(sensor.t1, t1); // Diferença do t1 atual para t1 do alvo
	float dif_elo2 = abs_dif(sensor.t2, t2); // Diferença do t2 atual para t2 do alvo
	// Computa sentido de movimento (crescente ou decrescente)
	char sign_t1 = (sensor.t1 > t1)? -1:1;
	char sign_t2 = (sensor.t2 > t2)? -1:1;

	//Flags
	bool moved_j1 = 0, moved_j2 = 0; // Movimento finalizado
	float step_t1 = 0, step_t2 = 0; // Angulo de incremento a cada ciclo de movimento
	int amount_t1 = 0, amount_t2 = 0; // Quantidade de ciclo de movimento
	
	float soma = 0;

	if(interpolation)
	{
		// Movimento com interpolação de juntas
		if (dif_elo1 > dif_elo2)
		{
			// Diferença no elo 1 é maior, serve de unidade para o movimento
			step_t1 = velocity_joint1;
			amount_t1 = round(dif_elo1 / step_t1) + 1;
			step_t2 = dif_elo2 / amount_t1;
			amount_t2 = round(dif_elo2 / step_t2) + 1;
		}
		else
		{
			// Diferença no elo 2 é maior, serve de unidade para o movimento
			step_t2 = velocity_joint2;
			amount_t2 = round(dif_elo2 / step_t2) + 1;
			step_t1 = dif_elo1 / amount_t2;
			amount_t1 = round(dif_elo1 / step_t1) + 1;
		}
	}

	while(!moved_j1 || !moved_j2)
	{
		//Movimento para junta 1

		bool flag_t1 = 0;
		bool flag_t2 = 0;

		if(sign_t1 > 0)
		{
			//Movimento em T1 positivo
			while(!flag_t1)
			{
				//Verificar se movimentar o step irá passar o target
				if(sensor.t1 + (step_t1 * sign_t1) <= t1)
				{
					//Movimentar o step não irá passar o target
					setpoint.t1 = sensor.t1 + (step_t1 * sign_t1);
					flag_t1 = 1;
				} else 
				{
					//Movimentar o step irá passar o target
					step_t1 = fine_approach;
					if(sensor.t1 + (step_t1 * sign_t1) <= t1)
					{
						setpoint.t1 = sensor.t1 + (step_t1 * sign_t1);
						flag_t1 = 1;
					} else 
					{
						moved_j1 = 1;
						flag_t1 = 1;
					}
				}
			}
		} else
		{
			//Movimento em T1 Negativo
			while(!flag_t1)
			{
				if(sensor.t1 + (step_t1 * sign_t1) >= t1)
				{
					//Movimentar o step não irá passar o target
					setpoint.t1 = sensor.t1 + (step_t1 * sign_t1);
					flag_t1 = 1;
				} else 
				{
					//Movimentar o step irá passar o target
					step_t1 = fine_approach;
					if(sensor.t1 + (step_t1 * sign_t1) >= t1)
					{
						setpoint.t1 = sensor.t1 + (step_t1 * sign_t1);
						flag_t1 = 1;
					} else 
					{
						moved_j1 = 1;
						flag_t1 = 1;
					}
				}
			}
		}

		//Movimento para junta 2
		if(sign_t2 > 0)
		{
			//Movimento em T2 positivo
			while(!flag_t2)
			{
				if(sensor.t2 + (step_t2 * sign_t2) <= t2)
				{
					//Movimentar o step não irá passar o target
					setpoint.t2 = sensor.t2 + (step_t2 * sign_t2);
					flag_t2 = 1;
				} else 
				{
					//Movimentar o step irá passar o target
					step_t2 = fine_approach;
					if(sensor.t2 + (step_t2 * sign_t2) <= t2)
					{
						setpoint.t2 = sensor.t2 + (step_t2 * sign_t2);
						flag_t2 = 1;
					} else 
					{
						moved_j2 = 1;
						flag_t2 = 1;
					}
				}
			}
		} else
		{
			//Movimento em T2 Negativo
			while(!flag_t2)
			{
				if(sensor.t2 + (step_t2 * sign_t2) >= t2)
				{
					//Movimentar o step não irá passar o target
					setpoint.t2 = sensor.t2 + (step_t2 * sign_t2);
					flag_t2 = 1;
				} else 
				{

					//Movimentar o step irá passar o target
					step_t2 = fine_approach;
					if(sensor.t2 + (step_t2 * sign_t2) >= t2)
					{
						setpoint.t2 = sensor.t2 + (step_t2 * sign_t2);
						flag_t2 = 1;
					} else 
					{
						moved_j2 = 1;
						flag_t2 = 1;
					}
				}
			}
		}

		last_sensor = sensor;
		com_cycle();

		soma = 0;

		soma += abs_dif(last_sensor.t1, sensor.t1) * sign_t1;
		soma += abs_dif(last_sensor.t2, sensor.t2) * sign_t2;
		setpointr = sensorr - soma;

		com_cycle2();
	

	}





}





void moveZ(float z, float speed)
{

	int sign = 999;

	while(sign != 0)
	{
		if(sensorz > z)  sign = -1;
		if(sensorz < z)  sign = 1;
		if(sensorz == z) sign = 0;

		setpointz = sensorz + (sign * speed);
		com_cycle1();
	}
}



//Movimento da Junta 1
		if(!moved_j1)
		{
			//Verifica se pode mover o valor inteiro de step
			if(dif_elo1 >= min_distance + step_t1)
			{
				//Mover o valor de step não ultrapassará a menor distância
				setpoint.t1 = sensor.t1 + (step_t1 * sign_t1);
			} else 
			{
				//Mover o valor de step irá ultrapassar a menor distância
				if(!flag_min_t1)
				{
					//Se mover para a menor distância
					setpoint.t1 = t1 - (min_distance * sign_t1);
					flag_min_t1 = true;
					//debug("Menor em ", 1);
				} else 
				{	
					//Verifica se é permitido iniciar a aproximação suave
					if(dif_elo1 >= fine_approach)
					{
						//Iniciar aproximação suave
						setpoint.t1 = sensor.t1 + (fine_approach * sign_t1);
						//debug("Suave em ", 1);
					} else 
					{
						//Movimento em T1 encerrado
						moved_j1 = true;
						//debug("Moveu em ", 1);
					}
				}
			}
		}










		void moveZ(float z, float speed)
{
		float z_offset = 0.1320f;

	//Computa diferença no valor do eixo Z
	float dif_z = abs_dif(sensorz, z);
	// Computa sentido de movimento (crescente ou decrescente)
	char sign_z = (sensorz > z)? -1 : 1;

	//Flags
	bool moved_z = false;
	bool flag_min_z = false;

	float min_distance = 0.01f;
	float fine_approach = 0.001f;

	float tgt_z = z_offset - z;

	debug("tgt_z ", tgt_z * 10000);

	int sign = 999;

	int sign1 = 999;

	while(sign1 != 0)
	{
		if(round3(sensorz) > round3(tgt_z))  sign1 = -1;
		if(round3(sensorz) < round3(tgt_z))  sign1 = 1;
		if(round3(sensorz) == round3(tgt_z)) sign1 = 0;

		setpointz = sensorz + (sign1 * speed);
		com_cycle1();
	}