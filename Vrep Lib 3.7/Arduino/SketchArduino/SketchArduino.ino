#include <vrep_lua.h>

#define halt(); while(true){};

#define lado 8.2

vrep_lua vrep;

int motor_d, motor_e;

//Variaveis de Encoder
float encoder_d;
double last_ang_d, total_ang_d;
int encoder_steps = 270;

void setup()
{
	Serial.begin(74880);

	vrep.start();

	motor_d = vrep.getObjectHandle("roda_d_joint");
	motor_e = vrep.getObjectHandle("roda_e_joint");

	last_ang_d = vrep.getJointPosition(motor_d);
	total_ang_d = last_ang_d;
	
	delay(1000);

}

void loop()
{

	vrep.setJointTargetVelocity(motor_d, radians(-30), false);
	vrep.setJointTargetVelocity(motor_e, radians(-30), false);

	float ang = vrep.do_encoder_d();
	vrep.debug(String(ang));

	//halt();
}

void arco_d(float vd, float raio)
{
    float ve = ((2 * raio * vd) - (lado * vd) )/(lado + (2 * raio));
    vrep.setJointTargetVelocity(motor_d, radians(vd), false);
    vrep.setJointTargetVelocity(motor_e, radians(ve), false);
}

void arco_e(float ve, float raio)
{
    float vd = ((2 * raio * ve) - (lado * ve) )/(lado + (2 * raio));
    vrep.setJointTargetVelocity(motor_d, radians(vd), false);
    vrep.setJointTargetVelocity(motor_e, radians(ve), false);
} 

void do_encoder_d()
{
    double delta_d = vrep.getJointPosition(motor_d) - last_ang_d;

    if (delta_d >= 0) delta_d = fmod(delta_d + PI, 2 * PI) - PI;
    else delta_d = fmod(delta_d - PI, 2 * PI) + PI;

    delta_d = map(delta_d, 0, radians(360), 0, radians(encoder_steps));

    total_ang_d = total_ang_d + delta_d;

    last_ang_d = vrep.getJointPosition(motor_d);

    encoder_d = floor(degrees(abs(total_ang_d)));

 }