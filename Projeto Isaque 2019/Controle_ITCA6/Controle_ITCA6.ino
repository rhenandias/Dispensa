#define pino_potenciometro	A2
#define pino_leitura_motor	A1
#define pino_pwm			6

float T, Kp, Ki, e, e_1, u, up, ui, ui_1;
int Pot, PV;

void setup()
{
   T    = 1 / 485;
   Kp   = 10;
   Ki   = 20;
   e_1  = 0;
   ui_1 = 0;

   pinMode(pino_potenciometro, INPUT);
   pinMode(pino_leitura_motor, INPUT);
   pinMode(pino_pwm, OUTPUT);

   Serial.begin(9600);
}

void loop()
{
   Pot = analogRead(pino_potenciometro); 
   //PV  = analogRead(pino_leitura_motor);

  int acc = 0;
  for(byte i = 0;  i < 20; i++)
  {
    acc += analogRead(pino_leitura_motor);
  }
  acc /= 20;
  PV = acc;

   
   e  = (float)(Pot-PV);
   up = Kp*e;
   ui = ui_1+(Ki/2)*T*(e+e_1);

   ui = constrain(ui, 0, 255);

   u = up + ui;

   u = constrain(u, 0, 255);

   analogWrite(pino_pwm,(int)u);

   ui_1 = ui;
   e_1  = e;

   Serial.print(Pot);
   Serial.print("  ");
   Serial.println(PV);
}
