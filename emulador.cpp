#include <stdio.h>
#include <stdlib.h>
#include <iostream>

typedef unsigned int word;
typedef unsigned char byte;
typedef unsigned long int microInstrucao;

byte Z , N;
word mar, mdr, pc, sp = 0, lv, cpp, tos, opc, h = 0, mpc, instruction;
word bA, bB, bC, bD;
byte mbr;

byte barramento_read, op_ula;
word barramento_write, next;
int jam;

microInstrucao microPrograma[512];
byte ram[16*1024];
byte wr, rd, fetch;

char bin[36];

void decode(word instruction){
	barramento_read = (instruction << 60) >> 60;
	op_ula = (instruction << 40) >> 56;
	barramento_write = (instruction << 48) >> 55;
	next = (instruction >> 27);
	jam = (instruction << 37) >> 61;
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

void gravar_registrador(word ender){
	if(ender & 1) mar = bC;		//0 0000 0001
	if(ender & 2) mdr = bC;		//0 0000 0010
	if(ender & 4) pc = bC; 		//0 0000 0100
	if(ender & 8) sp = bC;		//0 0000 1000
	if(ender & 16) lv = bC;		//0 0001 0000
	if(ender & 32) cpp = bC; 	//0 0010 0000 
	if(ender & 64) tos = bC;	//0 0100 0000
	if(ender & 128) opc = bC;	//0 1000 0000
	if(ender & 256) h = bC;		//1 0000 0000
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

void next_function(word next, int jam){

	if (jam == 0){
		mpc = next;
	}
	// if (jam == 1)	next = next | (Z<<8);
	// if (jam == 2)	next = next | (N<<8);
	// if (jam == 4)	next = next | mbr;
}

void dec2bin(int decimal){
    int aux;
    for (aux = 35; aux >= 0; aux--) {
    	if(aux % 9 == 0){
    		bin[aux] = ' ';
    	}
        else if (decimal % 2 == 0) {
            bin[aux] = '0';
            decimal = decimal / 2;
        }
        else {
            bin[aux] = '1';
            decimal = decimal / 2;
        }
    }
	printf("%s", bin);
}


void debug(){
	system("clear");

	// Registrador MAR
	dec2bin(mar);
	printf(" | %u | MAR\n", mar);

	// Registrador MDR
	dec2bin(mdr);
	printf(" | %u | MDR\n", mdr);

	// Registrador PC
	dec2bin(pc);
	printf(" | %u | PC\n", pc);

	// Registrador SP
	dec2bin(sp);
	printf(" | %u | SP\n", sp);

	// Registrador LV
	dec2bin(lv);
	printf(" | %u | LV\n", lv);

	// Registrador CPP
	dec2bin(cpp);
	printf(" | %u | CPP\n", cpp);

	// Registrador TOS
	dec2bin(tos);
	printf(" | %u | TOS\n", tos);

	// Registrador OPC
	dec2bin(opc);
	printf(" | %u | OPC\n", opc);

	// Registrador H
	dec2bin(h);
	printf(" | %u | H\n", h);
}

int main()
{
    while(1){

    	debug();

    	// Valores do micro programa
    	// next_address - 9 | Jam - 3 | Deslocador - 2 | F0 | F1 | En A | En B | Inv A | Inc | H | OPC | TOS | CPP | LV | SP | PC | MDR | MAR | WRITE | READ | FETCH | Barramento B - 4
		// Barramento B
		// MDR - 0 | PC - 1 | MBR - 2 | MBRU - 3 | SP - 4 | LV - 5 | CPP - 6 | TOS - 7 | OPC - 8 
		 
		// microPrograma[teste] = 0b000000010 000 00000000 000000000 000 0000;

		microPrograma[0] = 0b000000010000000000000000000000000000; // Next address = 2

		microPrograma[2] = 0b000000011000001101010000010000000100; // Next 2; bB+1; Write SP; Read SP
		microPrograma[3] = 0b000000100000001101010000010000000100; // Next 2; bB+1; Write SP; Read SP
		microPrograma[4] = 0b000000101000001101010000010000000100; // Next 2; bB+1; Write SP; Read SP
		microPrograma[5] = 0b000000010000001101010000010000000100; // Next 2; bB+1; Write SP; Read SP

		instruction = microPrograma[mpc];
		decode(instruction);
	
		ler_registrador(barramento_read);
		ula(op_ula);
		gravar_registrador(barramento_write);
		next_function(next, jam);

		getchar();
	}



return 0;
}
