#include <iostream>
#include <cstdlib>
#include <cstring>
#include <cstdio>

typedef unsigned int word;                 // 32 bits.
typedef unsigned char byte;                // 8 bits.
typedef unsigned long int microInstrucao;  // 64 bits.

byte mbr;                                         // Registrador MBR (especial).								
byte Z , N;
byte barramento_read, op_ula;

word bA, bB, bC;                              // Barramentos da ULA.
word barramento_write, next;
word mar = 0, mdr = 0, pc = 0, sp = 0, lv = 0, cpp = 0, tos = 0, opc = 0, h = 0, mpc = 0;

int jam, op_memory;
char bin[36];                                     // Vetor auxiliar para mostrar na tela o valor binário

byte RAM[16*1024];                                // Memória RAM de 16 Mega Bytes.
microInstrucao microPrograma[512];                // Vetor com as micro-instruções
microInstrucao mir;


void decode(microInstrucao instruction){
	barramento_read = 0b1111 & (instruction); //Esse 0b1111 é uma máscara e ao se fazer o & lógico obteremos o valor dos 4 primeiros bis de instruction.
	op_ula = 0b11111111 & (instruction >> 16); //0b11111111 é uma máscara para podermos pegar os bits que são operações da ula.
	barramento_write = 0b111111111 & (instruction >> 7);//0b111111111 é uma máscara, e ao se fazer o & lógico com instruction deslocado 7 bits obteremos os 9 bits que habilitarão a escrita nos registradores.
	next = (instruction >> 27);
	jam = 0b111 & (instruction >> 24);// 0b111 é uma máscara e ao se fazer o & lógico com instruction deslocado 24 bits obteremos os bits da jam.

	op_memory = 0b111 & (instruction >> 4); //Operação de Memória. 3 bits (write, read, fetch)
}

void ler_registrador(byte ender){
    switch(ender){
        case 0: bB = mdr; 	break;
        case 1: bB = pc; 	break;
        case 2: bB = mbr; 	break;
        case 3: // mbru = mbr com extensão de sinal
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
	if(ender & 1) mar = bC;		//... 0 0000 0001
	if(ender & 2) mdr = bC;		//... 0 0000 0010
	if(ender & 4) pc = bC; 		//... 0 0000 0100
	if(ender & 8) sp = bC;		//... 0 0000 1000
	if(ender & 16) lv = bC;		//... 0 0001 0000
	if(ender & 32) cpp = bC; 	//... 0 0010 0000 
	if(ender & 64) tos = bC;	//... 0 0100 0000
	if(ender & 128) opc = bC;	//... 0 1000 0000
	if(ender & 256) h = bC;		//... 1 0000 0000
}


void ula(byte operacao){
	
	bA = h;

	byte opUla  = (operacao << 2) >> 2;  // Operação da ULA que trabalha com 6 bits
	byte desloc = operacao >> 6;         // Operação do deslocador que trabalha com 2 bits

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


	// Verifica se a operação da ULA retorna 0. Retorno usado no JAM
	if (bC == 0){
		N = 0;
		Z = 1;

	}else{
		N = 1;
		Z = 0;
	}

	// Operação de deslocamento
	switch(desloc){
		case 0:					break;
		case 1: bC = bC >> 1; 	break;
		case 2: bC = bC << 8; 	break;
		default: bC = (bC << 8) >> 1;
	}
}

void next_function(word next, int jam){

	if (jam == 0)	mpc = next;				// Próxima instrução
	if (jam == 1)	mpc = next | (Z<<8);	// Pula quando bC = 0
	if (jam == 2)	mpc = next | (N<<8);	// Pula quando bC != 0
	if (jam == 4)	mpc = next | mbr;		// Pulo da memória
}

void memory(int op_memory){
	switch(op_memory){
		case 1:	mbr = RAM[pc];                break;	// Fetch;
		case 2: memcpy(&mdr, &RAM[mar*4], 4); break;	// Read
		case 4: memcpy(&RAM[mar*4], &mdr, 4); break;	// Write
		default: ;
	}
}

void dec2bin(int decimal){
    
    int aux;
    for (aux = 35; aux >= 0; aux--) {

    	if(aux % 9 == 0){
    		bin[aux] = ' ';

    	}else if (decimal % 2 == 0) {
            bin[aux] = '0';
            decimal /= 2;

        }else {
            bin[aux] = '1';
            decimal /= 2;
        }
    }
	printf("%s", bin);
}


void debug(){
	system("clear");

	// MPC
	dec2bin(mpc);
	printf(" | %u | MPC\n\n", mpc);

	// Registrador MBR
	dec2bin(mbr);
	printf(" | %u | MBR\n", mbr);

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

	printf("\n\n");
	
	printf("Barramentos\n");
	printf("%u | Barramento A\n", bA);
	printf("%u | Barramento B\n", bB);
	printf("%u | Barramento C\n", bC);

	printf("\n\n");
	
	printf("Variáveis\n");
	printf("Dividendo: %u\n", RAM[25*4]);
	printf("Divisor: %u\n", RAM[26*4]);
	printf("Quociente: %u\n", RAM[27*4]);
	printf("Auxiliar: %u\n", RAM[28*4]);
	


}

void programa(){
	// Auxiliar <- Dividendo
	RAM[1] = 2;		RAM[2] = 25;	// ADD OPC,	[25]
	RAM[3] = 6;		RAM[4] = 28;	// MOV OPC,	[28]
	RAM[5] = 13;	RAM[6] = 25;	// SUB OPC,	[25]

	// LOOP
	RAM[7] = 2;		RAM[8] = 28;	// ADD OPC,	[28] 
	RAM[9] = 11;	RAM[10] = 27;	// JZ OPC,	[27]

	// Dividendo <- Dividendo - Divisor
	RAM[11] = 13;	RAM[12] = 26;	// SUB OPC,	[26]
	RAM[13] = 6;	RAM[14] = 28;	// MOV OPC,	[28]
	RAM[15] = 13;	RAM[16] = 28;	// SUB OPC,	[28]

	// Quociente ++
	RAM[17] = 2;	RAM[18] = 27;	// ADD OPC,	[27]
	RAM[19] = 2;	RAM[20] = 29;	// ADD OPC,	[29]
	RAM[21] = 6;	RAM[22] = 27;	// MOV OPC,	[27]
	RAM[23] = 13;	RAM[24] = 27;	// SUB OPC,	[27]

	// GOTO
	RAM[25] = 9;	RAM[26] = 7;	// GOTO OPC, [7]
	RAM[27] = 9;	RAM[28] = 27;	// GOTO OPC, [27]

	// Variáveis

	RAM[25*4] = 24;	// Dividendo
	RAM[26*4] = 6;	// Divisor
	RAM[27*4] = 0;	// Quociente
	RAM[28*4] = 0;	// Auxiliar
	RAM[29*4] = 1;	// Mais um
}

void firmware(){
	microPrograma[0] = 0b000000000100001101010000001000010001; //PC <- PC + 1; FETCH; GOTO MBR;

	//OPC = OPC + memory[word]; (Sintaxe assembly: ADD OPC, [END])
	microPrograma[2] = 0b000000011000001101010000001000010001; //PC <- PC + 1; FETCH;
	microPrograma[3] = 0b000000100000000101000000000010100010; //MAR <- MBR; READ;
	microPrograma[4] = 0b000000101000000101001000000000000000; //H <- MDR;
	microPrograma[5] = 0b000000000000001111000100000000001000; //OPC <- OPC + H; GOTO MAIN;

	//memory[word] = OPC; (Sintaxe assembly: MOV OPC, [END])
	microPrograma[6] = 0b000000111000001101010000001000010001; //PC <- PC + 1; FETCH;
	microPrograma[7] = 0b000001000000000101000000000010000010; //MAR <- MBR;
	microPrograma[8] = 0b000000000000000101000000000101001000; //MDR <- OPC; write; GOTO MAIN;

	//goto endereco_comando_programa;(Sintaxe assembly: GOTO byte)
	microPrograma[9]  = 0b000001010000001101010000001000010001; //PC <- PC + 1; FETCH;
	microPrograma[10] = 0b000000000100000101000000001000010010; //PC <- MBR; FETCH; GOTO MBR;

	//if OPC = 0 goto endereco_comando_programa else goto proxima_linha;(Sintaxe assembly: JZ OPC, byte)
	microPrograma[11]  = 0b000001100001000101000100000000001000; //OPC <- OPC; IF ALU = 0 GOTO 268 (100001100) ELSE GOTO 12 (000001100);
	microPrograma[12]  = 0b000000000000001101010000001000000001; //PC <- PC + 1; GOTO MAIN;
	microPrograma[268] = 0b100001101000001101010000001000010001; //PC <- PC + 1; FETCH;
	microPrograma[269] = 0b000000000100000101000000001000010010; //PC <- MBR; FETCH; GOTO MBR;

	//OPC = OPC - memory[word]; (Sintaxe assembly: SUB OPC, [END])
	microPrograma[13] = 0b000001110000001101010000001000010001; //PC <- PC + 1; FETCH;
	microPrograma[14] = 0b000001111000000101000000000010100010; //MAR <- MBR; READ;
	microPrograma[15] = 0b000010000000000101001000000000000000; //H <- MDR;
	microPrograma[16] = 0b000000000000001111110100000000001000; //OPC <- OPC - H; GOTO MAIN;
}

int main(){

	// PROGRAMA
	programa();

	// FIRMWARE
	firmware();
	
    while(1){

    	debug();

		mir = microPrograma[mpc];

		decode(mir);

		ler_registrador(barramento_read);

		ula(op_ula);

		gravar_registrador(barramento_write);

		memory(op_memory);

		next_function(next, jam);

		getchar();
}

return 0;
}
