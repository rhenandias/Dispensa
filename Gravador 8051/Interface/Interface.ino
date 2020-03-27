#define MISO    12
#define MOSI    11
#define CLK     13
#define RST     10

uint8_t program[] = {0x2, 0x0, 0x6, 0x2, 0x0, 0x62, 0x75, 0x81, 0x7, 0x12, 0x0, 0x98, 0xe5, 0x82, 0x60, 0x3, 0x2, 0x0, 0x3, 0x79, 0x0, 0xe9, 0x44, 0x0, 0x60, 0x1b, 0x7a, 0x0, 0x90, 0x0, 0x9c, 0x78, 0x1, 0x75, 0xa0, 0x0, 0xe4, 0x93, 0xf2, 0xa3, 0x8, 0xb8, 0x0, 0x2, 0x5, 0xa0, 0xd9, 0xf4, 0xda, 0xf2, 0x75, 0xa0, 0xff, 0xe4, 0x78, 0xff, 0xf6, 0xd8, 0xfd, 0x78, 0x0, 0xe8, 0x44, 0x0, 0x60, 0xa, 0x79, 0x1, 0x75, 0xa0, 0x0, 0xe4, 0xf3, 0x9, 0xd8, 0xfc, 0x78, 0x0, 0xe8, 0x44, 0x0, 0x60, 0xc, 0x79, 0x0, 0x90, 0x0, 0x1, 0xe4, 0xf0, 0xa3, 0xd8, 0xfc, 0xd9, 0xfa, 0x2, 0x0, 0x3, 0x7f, 0x0, 0x8f, 0xa0, 0xf, 0x90, 0x0, 0x32, 0xc0, 0x7, 0x12, 0x0, 0x73, 0xd0, 0x7, 0x80, 0xf1, 0xae, 0x82, 0xaf, 0x83, 0x75, 0x89, 0x10, 0x75, 0x88, 0x0, 0xee, 0x4f, 0x60, 0x14, 0x75, 0x8d, 0xfc, 0x75, 0x8b, 0x18, 0xd2, 0x8e, 0x10, 0x8f, 0x2, 0x80, 0xfb, 0x1e, 0xbe, 0xff, 0x1, 0x1f, 0x80, 0xe8, 0xc2, 0x8e, 0x22, 0x75, 0x82, 0x0, 0x22};


void setup()
{
    Serial.begin(9600);
    
    pinMode(MISO, INPUT);
    pinMode(MOSI, OUTPUT);
    pinMode(CLK, OUTPUT);
    pinMode(RST, OUTPUT);

    //Apaga
    digitalWrite(RST, 1);
    programming_enable();
    erase_memory();

    //Escreve
    programming_enable();
    uint8_t addr = 0;
    for(uint8_t i = 0; i < 156; i++)
    {
        transfer_spi(0x40);
        transfer_spi(0x00);
        transfer_spi(addr++);
        transfer_spi(program[i]);
    }
    delay(500);
    digitalWrite(RST, 0);

    /*
    //Lê
    programming_enable();
    addr = 0;
    for(uint8_t i = 0; i < 41; i++)
    {
        transfer_spi(0x20);
        transfer_spi(0x00);
        transfer_spi(addr++);
        uint8_t blido = transfer_spi(0x00);
        Serial.println(blido, HEX);
    }
    */
}

void loop()
{
    
}

uint8_t transfer_spi(uint8_t data)
{
    /*
    A função atua tanto para leitura, quanto para escrita na memória do uc
    O modo de operação da função de transferência é definido pelos bytes de instrução enviados

    Quando definido o modo de escrita:
    O byte "data" é escrito bit a bit no uc
    - Byte 1 : Write Program Memory (byte mode)
    - Byte 2 : Addr High Byte
    - Byte 3 : ADDR Low Byte
    - Byte 4 : Data byte

    Quando definido o modo de leitura:
    O byte é lido bit bit na variavel "read_ bit", e então é formado um byte na variavel "read_byte"
    - Byte 1 : Read Program Memory (byte mode)
    - Byte 2 : Addr High Byte
    - Byte 3 : ADDR Low Byte
    - Byte 4 : Dummy Data

    */
    uint8_t read_byte = 0;     //Byte que será construído com os bits lidos
    uint8_t read_bit;          //Bit lido

    for(uint8_t i = 0; i < 8; i++)
    {
        if(data & 0x80) digitalWrite(MOSI, 1);
        else digitalWrite(MOSI, 0);

        digitalWrite(CLK, 1);
        delayMicroseconds(2);

        read_bit = digitalRead(MISO);
        
        digitalWrite(CLK, 0);
        delayMicroseconds(2);

        if(read_bit) read_byte |= 1;
        else read_byte &= 0xFE;

        if(i != 7)
        {
            read_byte <<= 1;
            data <<= 1;
        }
    }
    return read_byte;
}

void programming_enable()
{    
    transfer_spi(0xAC);
    transfer_spi(0x53);
    transfer_spi(0x00);
    transfer_spi(0x00);
    delay(500);
}

void erase_memory()
{
    transfer_spi(0xAC);
    transfer_spi(0x80);
    transfer_spi(0x00);
    transfer_spi(0x00);
    delay(500);
}