// Controle de Motor de Passo - Modo Passo Completo alto torque (Full step) 
// Blog Eletrogate - https://blog.eletrogate.com/guia-completo-do-motor-de-passo-28byj-48-driver-uln2003
// Baseado em  http://www.elecrow.com/wiki/index.php?title=ULN2003_Stepper_Motor_Driver
// Motor 28BYJ48/5V com Módulo ULN20023 - Arduino Nano / IDE 1.8.5
// Uma volta no eixo = 4075 pulsos / 512 x 8 = 4096 
// Gustavo Murta 23/jul/2018
 
byte HOR[4] = {0x09,0x03,0x06,0x0C};    // Matriz dos bytes das Fases do Motor - sentido Horário Full Step
byte AHO[4] = {0x0C,0x06,0x03,0x09};    // Matriz dos bytes das Fases do Motor - sentido Anti-Horário Full Step
int atraso_fase = 2 ;                   // Intervalo de tempo entre as fases em milisegundos - min 2 para Full Step 
int intervalo = 1000 ;                  // Intervalo de tempo entre os movimentos do motor em ms
 
void Motor_AHO()                    // Movimento no sentido anti-horário 
{
  for(int i = 0; i < 512; i++)      // incrementa o contador i de 0 a 511 - uma volta
  
    for(int j = 0; j < 4; j++)      // incrementa o contador j de 0 a 3 
    {
      PORTB = AHO[j];               // Carrega bytes da Matriz AHO na Porta B 
      delay (atraso_fase);          // Atraso de tempo entre as fases em milisegundos
    }    
}
 
void Motor_HOR()                    // Movimento no sentido horário 
{
  for(int i = 0; i < 512; i++)      // incrementa o contador i de 0 a 511 - uma volta
  
    for(int j = 0; j < 4; j++)      // incrementa o contador j de 0 a 3 
    {
      PORTB = HOR[j];               // Carrega bytes da Matriz HOR na Porta B 
      delay (atraso_fase);          // Atraso de tempo entre as fases em milisegundos
    }
}
 
void setup()
{
  DDRB = 0x0F;           // Configura Portas D08,D09,D10 e D11 como saída 
  PORTB = 0x00;          // Reset dos bits da Porta B (D08 a D15) 
}
 
void loop()
{
 Motor_HOR();           // Gira motor no sentido Horário 
 delay (intervalo);     // Atraso em milisegundos 
 Motor_AHO();           // Gira motor no sentido Anti-Horário 
 delay (intervalo);     // Atraso em milisegundos 
}
