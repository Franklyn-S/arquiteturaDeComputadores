#include <stdio.h>
#include <stdlib.h>
#include <iostream>

typedef unsigned int word;                 //32 bits.
typedef unsigned char byte;				   //8 bits.
typedef unsigned long int microInstrucao;  //64 bits.

byte mbr;           //Registrador mbr (especial).
byte Z , N;
byte ram[16*1024];  //Memória RAM de 16 Bytes.
byte wr, rd, fetch;

word bA, bB, bC, bD;   							  //Barramentos da ULA.
word mar, mdr, pc, sp, lv, cpp, tos, opc, h, mpc; //Registradores da ULA.

microInstrucao microPrograma[512];				  //Vetor onde se pode guardar 512 instruções de 64 bits.

//Função que recebe a instrução (32 bits) e detecta qual o registrador no qual será armazenado a informação.
void gravar_registrador(word ender){
	if(ender & 1)   mar = bC;	//... 0 0000 0001
	if(ender & 2)   mdr = bC;	//... 0 0000 0010
	if(ender & 4)   pc  = bC; 	//... 0 0000 0100
	if(ender & 8)   sp  = bC;	//... 0 0000 1000
	if(ender & 16)  lv  = bC;	//... 0 0001 0000
	if(ender & 32)  cpp = bC; 	//... 0 0010 0000
	if(ender & 64)  tos = bC;	//... 0 0100 0000
	if(ender & 128) opc = bC;	//... 0 1000 0000
	if(ender & 256) h   = bC;	//... 1 0000 0000
}

    
void ler_registrador(byte ender){//endereço
        switch(ender){
            case 0: bB = mdr; 	break;
            case 1: bB = pc; 	break;
            case 2: bB = mbr; 	break;
            case 3: //mbru = mbr com extensão de sinal
            {
                word sinal = mbr >> 7;
                bB = (sinal) ? 0xFFFFFF0 : 0;
                bB = bB | mbr;
            }
            					break;
            case 4: bB = sp;	break;
            case 5: bB = lv;	break;
            case 6: bB = cpp; 	break;
            case 7: bB = tos; 	break;
            case 8: bB = opc; 	break;
       }
}

    void ula(byte operacao){
		
		bA = h;

		byte opUla = (operacao << 2) >> 2;
		byte desloc = operacao >> 6;

		switch(opUla){
			case 12: bC = bA & bB;		break;
			case 16: bC = 0;			break;
			case 20: bC = bB;			break;
			case 24: bC = bA;			break;
			case 26: bC = ~bA;			break;
			case 28: bC = bA | bB;		break;
			case 44: bC = ~bB;			break;
			case 49: bC = 1;			break;
			case 50: bC = -1;			break;
			case 53: bC = bB + 1;		break;
			case 54: bC = bB - 1;		break;
			case 57: bC = bA + 1;		break;
			case 59: bC = -bA;			break;
			case 60: bC = bA + bB;		break;
			case 61: bC = bA + bB + 1;	break;
			case 63: bC = bB - bA;		break;
			default: break;
		}

		if (bC == 0){
			N = 0;
			Z = 1;
		}
		else{
			N = 1;
			Z = 0;
		}


		switch(desloc){
			case 0:					break;
			case 1: bC = bC >> 1; 	break;
			case 2: bC = bC << 8; 	break;
			default: bC = (bC << 8) >> 1;
		}
	}

	word next_function(word next , int jam){

		if (jam == 0){
			//return next; nao precisa pois não ha caso onde 000
		}
		if (jam == 1)	next = next | (Z<<8);
		if (jam == 2)	next = next | (N<<8);
		if (jam == 4)	next = next | mbr;
		return next;
	}

int main()
{
    while(1){
    	// Valores do micro programa
    	// next_address - 9 | Jam - 3 | Deslocador - 2 | F0 | F1 | En A | En B | Inv A | Inc | H | OPC | TOS | CPP | LV | SP | PC | MDR | MAR | WRITE | READ | FETCH | Barramento B - 4
		// Barramento B
		// MDR - 0 | PC - 1 | MBR - 2 | MBRU - 3 | SP - 4 | LV - 5 | CPP - 6 | TOS - 7 | OPC - 8 
		 
		// microPrograma[teste] = 000000110 000 00000000 000000000 000 0010;

		microPrograma[0] = 0b000000010000000000000000000000000000;

		microPrograma[2] = 0b000000011000001110010000010000000100;
		microPrograma[3] = 0b000000100000001110010000010000000100;
		microPrograma[4] = 0b000000101000001110010000010000000100;
		microPrograma[5] = 0b000000110000001110010000010000000100;

		microPrograma[6] = 0b000000111000000000000000100000000100;
		microPrograma[7] = 0b000000110000000000000000000000000010;


		byte ender_read = (microPrograma[0] << 32) >> 32;
		byte oper = (microPrograma[0] << 12) >> 28;
		word ender_write = (microPrograma[0] << 20) >> 27;
		word next = (microPrograma[0] >> 27);
		int jam = (microPrograma[0] << 9) >> 33;

		ler_registrador(ender_read);
		ula(oper);
		gravar_registrador(ender_write);
		next_function(next, jam);

		// getchar();
	}



return 0;
}
