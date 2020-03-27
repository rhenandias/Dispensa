#include <arduino.h>

//Vetor de posição
//Armazena coordenadas no espaço 
//[vector.x, vector.y]
typedef struct
{
	float x = 0, y = 0;
}vector_position;


//Vetor de ângulos - Dois ângulos
//Armazena angulos das juntas
//[vector.t1, vector.t2]
typedef struct
{
	float t1 = 0, t2 = 0;
}vector_angle;


//Vetor de ângulos - Quatro ângulos
//Armazena ângulos das juntas
//[vector.t1, vector.t2, vector.t3, vector.t4]
typedef struct
{
	float t1 = 0, t2 = 0, t3 = 0, t4 = 0; 
}vector4_angle;


//Função para arredondar valores em floats
//Arredonda com precisão de uma casa decimal
float round1(float value)
{
	return round(value * 10) / 10.0f;
}

float round2(float value)
{
	return round(value * 100) / 100.0f;
}

float round3(float value)
{
	return round(value * 1000) / 1000.0f;
}

//Função para calcular diferença absoluta entre dois valores
float abs_dif(float value1, float value2)
{
	return max(value1, value2) - min(value1, value2);
}

int sign(float a)
{
	if(a > 0) return 1;
	if(a < 0) return -1;
	if(a == 0) return 0;
}