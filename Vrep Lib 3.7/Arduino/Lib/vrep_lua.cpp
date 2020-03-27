#include <vrep_lua.h>

vrep_lua::vrep_lua(){
}

void vrep_lua::start(){
	Serial.println("start");
}

void vrep_lua::debug(String value){
	String protocol = String(lua_function_debug) + '#' + String(value);
	Serial.println(protocol);
}

int vrep_lua::getObjectHandle(String name){
	//ff#name

	String protocol = String(lua_function_getObjectHandle) + '#' + name;
	Serial.println(protocol);
	
	String joint_handler = Serial.readStringUntil('#');
	return joint_handler.toInt();
}

void vrep_lua::setJointPosition(int handler, float position, boolean sync = true){
	//ff#handler#position
	String protocol = String(lua_function_setJointPosition) + '#' + String(handler) + '#' + String(position);
	Serial.println(protocol);

	if(sync) while(Serial.read() != '#'){};
}

float vrep_lua::getJointPosition(int handler){
	//ff#handler
	String protocol = String(lua_function_getJointPosition) + '#' + String(handler);
	Serial.println(protocol);

	String joint_position = Serial.readStringUntil('#');
	return joint_position.toFloat();
}

void vrep_lua::setJointTargetPosition(int handler, float position, boolean sync = true)
{
	//ff#handler#position
	String protocol = String(lua_function_setJointTargetPosition) + '#' + String(handler) + '#' + String(position);
	Serial.println(protocol);

	if(sync) while(Serial.read() != '#') {};
}

void vrep_lua::setJointTargetVelocity(int handler, float velocity, boolean sync = true)
{
	//ff#handler#velocity
	String protocol = String(lua_function_setJointTargetVelocity) + '#' + String(handler) + '#' + String(velocity);
	Serial.println(protocol);

	if(sync) while(Serial.read() != '#'){};
}

int vrep_lua::do_encoder_d()
{
	//ff
	String protocol = String(6);
	Serial.println(protocol);

	String encoder = Serial.readStringUntil('#');
	return encoder.toInt();
}