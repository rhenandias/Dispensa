#include <arduino.h>

//Vetor de posição
//Armazena coordenadas no espaço 
//[vector.x, vector.y]
typedef struct
{
	float x, y;
}vector_position;


//Vetor de ângulos - Dois ângulos
//Armazena angulos das juntas
//[vector.t1, vector.t2]
typedef struct
{
	float t1, t2;
}vector_angle;


//Vetor de ângulos - Quatro ângulos
//Armazena ângulos das juntas
//[vector.t1, vector.t2, vector.t3, vector.t4]
typedef struct
{
	float t1, t2, t3, t4; 
}vector4_angle;


//Função para arredondar valores em floats
//Arredonda com precisão de uma casa decimal
float round1(float value)
{
	return round(value * 10) / 10.0f;
}

//Função para calcular diferença absoluta entre dois valores
float abs_dif(float value1, float value2)
{
	return max(value1, value2) - min(value1, value2);
}