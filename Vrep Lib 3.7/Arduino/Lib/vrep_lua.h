#ifndef vrep_lua_h
#define vrep_lua_h

#include <Arduino.h>

#define lua_function_debug						0
#define lua_function_getObjectHandle 			1
#define lua_function_setJointPosition			2
#define lua_function_getJointPosition			3
#define lua_function_setJointTargetPosition		4
#define lua_function_setJointTargetVelocity		5

//Classe para utilização com Lua
class vrep_lua
{
	public:
		vrep_lua();

		void start();

		void debug(String value);

		int getObjectHandle(String name);

		void setJointPosition(int handler, float position, boolean sync = true);
		float getJointPosition(int handler);
		void setJointTargetPosition(int handler, float position, boolean sync = true);
		void setJointTargetVelocity(int handler, float velocity, boolean sync = true);

		int do_encoder_d();

};

#endif