/******************************************************************************

                            Online C Compiler.
                Code, Compile, Run and Debug C program online.
Write your code in this editor and press "Run" button to compile and execute it.

*******************************************************************************/

#include <stdio.h>

int main()
{
    typedef unsigned int word;
    typedef unsigned char byte;
    
    word mar, mdr, pc, sp, lv, cpp, tos, opc, h, bA, bB, bC, bS;
    byte mbr;
    
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
        }
    }

    return 0;
}
