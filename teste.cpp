#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <math.h>

typedef unsigned int word; //8bits
typedef unsigned char byte; //32bits
typedef unsigned long int microInstrucao; // 64bits

char bin[32];

void dec2bin(int decimal){
    int aux;
    for (aux = 31; aux >= 0; aux--) {
        if (decimal % 2 == 0) {
            bin[aux] = '0';
            decimal = decimal / 2;
        }
        else {
            bin[aux] = '1';
            decimal = decimal / 2;
        }
    }
	printf("%s\n", bin);
}

int main(){
	dec2bin(4);

	return 0;
}
