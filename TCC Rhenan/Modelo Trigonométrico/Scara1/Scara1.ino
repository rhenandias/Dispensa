//Scara1.ino
#include<vector.h>

void setup()
{
	Serial.begin(9600);

	vector_position direct = direct_transform(180, -90, 10, 8);
	Serial.println("Direta (x, y)");
	Serial.println(direct.x);
	Serial.println(direct.y);

	vector4_angle inverse = inverse_transform(direct.x, direct.y, 10, 8);
	Serial.println("Inversa 1 (t1, t2)");
	Serial.println(inverse.t1);
	Serial.println(inverse.t2);
	Serial.println("Inversa 1 (t3, t4)");
	Serial.println(inverse.t3);
	Serial.println(inverse.t4);

	vector_position direct1 = direct_transform(inverse.t1, inverse.t2, 10, 8);
	Serial.println("Direta 1 (x, y)");
	Serial.println(direct1.x);
	Serial.println(direct1.y);

	vector_position direct2 = direct_transform(inverse.t3, inverse.t4, 10, 8);
	Serial.println("Direta 2 (x, y)");
	Serial.println(direct2.x);
	Serial.println(direct2.y);
}

void loop()
{

}

vector_position direct_transform(float t1, float t2, float l1, float l2)
{
	//Define vetores de posição
	vector_position r1, r2, r3;

	//Calcula vetores individuais para Elo 1
	r1.x = l1 * cos(radians(t1));
	r1.y = l1 * sin(radians(t1));

	//Calcula vetores individuais para Elo 2
	r2.x = l2 * cos(radians(t1 + t2));
	r2.y = l2 * sin(radians(t1 + t2));

	//Realiza soma vetorial para posição final
	r3.x = r1.x + r2.x;
	r3.y = r1.y + r2.y;

	return r3;
}

vector4_angle inverse_transform(float x, float y, float l1, float l2)
{

	vector4_angle res;
	float t1, t2, num, den;


	//Calculo para t2 positivo
	t2 = acos((pow(x, 2) + pow(y, 2) - pow(l1, 2) - pow(l2, 2))/(2 * l1 * l2));

	num = y * (l1 + l2 * cos(t2)) - x * l2 * sin(t2);
	den = x * (l1 + l2 * cos(t2)) + y * l2 * sin(t2);
	t1 = atan2(num, den);

	t1 = degrees(t1);
	t2 = degrees(t2);

	res.t1 = t1;
	res.t2 = t2;

	//Calculo para t2 negativo
	t2 = -acos((pow(x, 2) + pow(y, 2) - pow(l1, 2) - pow(l2, 2))/(2 * l1 * l2));

	num = y * (l1 + l2 * cos(t2)) - x * l2 * sin(t2);
	den = x * (l1 + l2 * cos(t2)) + y * l2 * sin(t2);
	t1 = atan2(num, den);

	t1 = degrees(t1);
	t2 = degrees(t2);

	res.t3 = t1;
	res.t4 = t2;

	return res;
}

