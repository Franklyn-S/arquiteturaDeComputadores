#include <stdio.h>

int main()
{
    typedef unsigned int word;
    typedef unsigned char byte;
    typedef unsigned long int microInstrucao;
    
    byte Z , N;
    word mar, mdr, pc, sp, lv, cpp, tos, opc, h, mpc;
    word bA, bB, bC, bS, bD;//o que seria bS?
    byte mbr;
    microInstrucao microPrograma[512];
    byte ram[16*1024];
    byte wr, rd, fetch;  //declara 

    while(1){
		//aqui roda o programa principal
	}
    
    void ler_registrador(byte ender){//endereço
        switch(ender){
            case 0: bB = mdr; break;
            case 1: bB = pc; break;
            case 2: bB = mbr; break;
            case 3: //mbru = mbr com extensão de sinal
            {
                word sinal = mbr >> 7;
                bB = (sinal) ? 0xFFFFFF0 : 0;
                bB = bB|mbr;
            }
            break;
            case 4: bB = sp; break;
            case 5: bB = lv; break;
            case 6: bB = cpp; break;
            case 7: bB = tos; break;
            case 8: bB = opc; break;
        }
    }

    void colocaBarramentoC(word operacao){
		
		bA = h;

		byte opUla = (operacao << 2)>>2;

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
		}

		if (bC == 0)
		{
			N = 0;
			Z = 1;
		}else{
			N = 1;
			Z = 0;
		}
	}

	word next_function(word next , int jam){

		if (jam == 0)
		{
			//return next; nao precisa pois não ha caso onde 000
		}
		if (jam == 1)
		{
			next = next | (Z<<8);
		}
		if (jam == 2)
		{
			next = next | (N<<8);
		}
		if (jam == 3)
		{
			/* code */
		}
		if (jam == 4)
		{
			next = next;
		}
		if (jam == 5)
		{
			/* code */
		}
		if (jam == 6)
		{
			/* code */
		}
		if (jam == 7)
		{
			/* code */
		}

		return next;
	}


return 0;
}