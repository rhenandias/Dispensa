#include <8051.h>

void delay(unsigned int delay_ms);


void main()
{
    unsigned char i = 0x00;

    while(1)
    {
        P2 = i++;
        //delay(1);
    }
}

void delay(unsigned int delay_ms)
{
	/*
	Considerando um cristal de 12Mhz:
	Clock = fosc/12 -> 12MHz/12 -> 1MHz
	1 ciclo = 1/Clock -> 1/1MHz -> 1us
	1ms = 1000us, logo para 1ms são necessários 1000 ciclos de 1us
	(65536 - 1000) = 64536 -> 0xFC18
	Portando 0xFC18 realiza um delay de 1ms
	*/
	
    TMOD = 0x10;
    TCON = 0x00;

    for(delay_ms; delay_ms > 0; delay_ms--)
    {
        TH1 = 0xFC;     //(65536 - 1000) High Byte
        TL1 = 0x18;     //(65536 - 1000) Low Byte
        TR1 = 1;        //Habilita o timer
        while(!TF1){};  //Aguarda flag de interrupção
        TF1 = 0;        //Reseta flag de interrupção
    }
    TR1 = 0;            //Desabilita o timer
}