#include <iostream>
#include <sstream>
#include <cstdlib>
#include <cstring>
#include <string>
#include <cstdio>

using namespace std;

namespace patch {
    template < typename T > std::string to_string( const T& n )
    {
        std::ostringstream stm ;
        stm << n ;
        return stm.str() ;
    }
}


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

byte RAM[16*1024*1024];                           // Memória RAM de 16 Mega Bytes.
microInstrucao microPrograma[512];                // Vetor com as micro-instruções
microInstrucao mir;

//Carrega todo o firmeware do arquivo microprog.rom.
void carregar_microprograma() {
	FILE *arquivo;
	arquivo = fopen("microprog.rom", "rb");

	if(arquivo == NULL) {
		printf("Não foi possível abrir o arquivo");
		exit(1);
	}
	fread(microPrograma, sizeof(microInstrucao), 512, arquivo);
	fclose(arquivo);
}

//Carrega na memória as operações correspondetes ao assembly.
void carregar_operacao(const char *arquivo) {
	FILE *programa;
	word tamanho;
	byte tam_arquivo[4];

	programa = fopen(arquivo, "rb");

	if (programa != NULL) {
		fread(tam_arquivo, sizeof(byte), 4, programa);
		memcpy(&tamanho, tam_arquivo, 4);

		fread(RAM, sizeof(byte), 20, programa);
		fread(&RAM[0x0401], sizeof(byte), tamanho - 20, programa);
	}
}

//Decodifica as instruções mandadas.
void decode(microInstrucao instruction) {
	barramento_read = (instruction << 60) >> 60;
	op_ula = (instruction << 40) >> 56;
	barramento_write = (instruction << 48) >> 55;
	next = (instruction >> 27);
	jam = (instruction << 37) >> 61;

	op_memory = (instruction << 57) >> 61; //Operação de Memória. 3 bits (write, read, fetch)
}


void ler_registrador(byte ender) {
    switch (ender) {
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


void gravar_registrador(word ender) {
	if (ender & 1) mar = bC;	//... 0 0000 0001
	if (ender & 2) mdr = bC;	//... 0 0000 0010
	if (ender & 4) pc = bC; 	//... 0 0000 0100
	if (ender & 8) sp = bC;		//... 0 0000 1000
	if (ender & 16) lv = bC;	//... 0 0001 0000
	if (ender & 32) cpp = bC; 	//... 0 0010 0000 
	if (ender & 64) tos = bC;	//... 0 0100 0000
	if (ender & 128) opc = bC;	//... 0 1000 0000
	if (ender & 256) h = bC;	//... 1 0000 0000
}


void ula(byte operacao) {
	
	bA = h;

	byte opUla  = (operacao << 2) >> 2;  // Operação da ULA que trabalha com 6 bits
	byte desloc = operacao >> 6;         // Operação do deslocador que trabalha com 2 bits

	switch (opUla) {
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
	if (bC == 0) {
		N = 0;
		Z = 1;

	} else {
		N = 1;
		Z = 0;
	}

	// Operação de deslocamento
	switch (desloc) {
		case 0:					break;
		case 1: bC = bC >> 1; 	break;
		case 2: bC = bC << 8; 	break;
		default: bC = (bC << 8) >> 1;
	}
}


void next_function(word next, int jam) {

	if (jam == 0)	mpc = next;				// Próxima instrução
	if (jam == 1)	mpc = next | (Z<<8);	// Pula quando bC = 0
	if (jam == 2)	mpc = next | (N<<8);	// Pula quando bC != 0
	if (jam == 4)	mpc = next | mbr;		// Pulo da memória
}

void memory(int op_memory) {
	switch (op_memory) {
		case 1:	mbr = RAM[pc];                break;	// Fetch;
		case 2: memcpy(&mdr, &RAM[mar*4], 4); break;	// Read
		case 4: memcpy(&RAM[mar*4], &mdr, 4); break;	// Write
		default: ;
	}
}

void dec2bin(int decimal) {
    
    int aux;
    for (aux = 35; aux >= 0; aux--) {

    	if(aux % 9 == 0) {
    		bin[aux] = ' ';

    	} else if (decimal % 2 == 0) {
            bin[aux] = '0';
            decimal /= 2;

        } else {
            bin[aux] = '1';
            decimal /= 2;
        }
    }

	printf("%s", bin);
}

void center(int num, int length) {
	string str = patch::to_string(num);
	int len = str.length() - 1;
	int left = (int)(length - len)/2;
	char fill[left+1];
	for (int i = 0; i < left; i++)
	fill[i] = ' ';
	fill[left] = '\0';
	cout << fill << ' ' << str << fill << (len % 2 ? "  " : " ");
}

void debug() {

	system("clear");
	int j = 0;
	//Esse for percorre a RAM a partir da posição que está no lv até a posição que está no sp

	if(lv && sp){
		cout << "╔════════════════════════════════════════════════════════════════╗" << endl;
		cout << "║                              PILHA                             ║	" << endl;
		cout << "╟────────────────────────────────────────────────────────────────╢	" << endl;

		for (word i = lv*4; i <= sp*4; i += 4) {
			byte aux = (RAM[i] & 0x000000FF) | ((RAM[i+1] << 8) & 0x0000FF00) | ((RAM[i+2] << 16) & 0x00FF0000) | ((RAM[i+3] << 24) & 0xFF000000);
			printf("║");
			dec2bin(aux);
			cout << " │ ";
			center(aux, 8);
			cout << " │ Variável " << j << " ║" << endl;
			j++;
		}

		cout << "╚════════════════════════════════════════════════════════════════╝" << endl;
	}

	cout << endl;

	cout << "╔═══════════════════════════════════════════════════════════════╗" << endl;
	cout << "║                         REGISTRADORES                         ║	" << endl;
	cout << "╟───────────────────────────────────────────────────────────────╢	" << endl;
	// MPC
	printf("║");
	dec2bin(mpc);
	printf(" │ ");
	center(mpc, 14);
	cout << " │ MPC  ║" << endl;

	// Registrador MBR
	printf("║");
	dec2bin(mbr);
	printf(" │ ");
	center(mbr, 14);
	cout << " │ MBR  ║" << endl;

	// Registrador MAR
	printf("║");
	dec2bin(mar);
	printf(" │ ");
	center(mar, 14);
	cout << " │ MAR  ║" << endl;

	// Registrador MDR
	printf("║");
	dec2bin(mdr);
	printf(" │ ");
	center(mdr, 14);
	cout << " │ MDR  ║" << endl;

	// Registrador PC
	printf("║");
	dec2bin(pc);
	printf(" │ ");
	center(pc, 14);
	cout << " │  PC  ║" << endl;

	// Registrador SP
	printf("║");
	dec2bin(sp);
	printf(" │ ");
	center(sp, 14);
	cout << " │  SP  ║" << endl;

	// Registrador LV
	printf("║");
	dec2bin(lv);
	printf(" │ ");
	center(lv, 14);
	cout << " │  LV  ║" << endl;

	// Registrador CPP
	printf("║");
	dec2bin(cpp);
	printf(" │ ");
	center(cpp, 14);
	cout << " │ CPP  ║" << endl;

	// Registrador TOS
	printf("║");
	dec2bin(tos);
	printf(" │ ");
	center(tos, 14);
	cout << " │ TOS  ║" << endl;

	// Registrador OPC
	printf("║");
	dec2bin(opc);
	printf(" │ ");
	center(opc, 14);
	cout << " │ OPC  ║" << endl;

	// Registrador H
	printf("║");
	dec2bin(h);
	printf(" │ ");
	center(h, 14);
	cout << " │  H   ║" << endl;

	cout << "╚═══════════════════════════════════════════════════════════════╝" << endl;
	printf("\n\n");
	
	cout << "╔═══════════════════════════════════════════════════════════════╗" << endl;
	cout << "║                          BARRAMENTOS                          ║	" << endl;
	cout << "╟───────────────────────────────────────────────────────────────╢	" << endl;
	printf("║");
	center(bA, 44);
	cout << " │ Barramento A ║" << endl;
	printf("║");
	center(bB, 44);
	cout << " │ Barramento B ║" << endl;
	printf("║");
	center(bC, 44);
	cout << " │ Barramento C ║" << endl;

	cout << "╚═══════════════════════════════════════════════════════════════╝" << endl;
}

int main() {
	
	carregar_microprograma();
	carregar_operacao("prog.exe");
	
    while(1) {

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
