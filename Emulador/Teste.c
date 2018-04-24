#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void main() {

	typedef unsigned long int microInstrucao;

	FILE *arquivo;
	microInstrucao microprograma[513];

	arquivo = fopen("microprog.rom","rb");

	if(arquivo == NULL) {
		printf("Não foi possível abrir o arquivo");
	}
	else {

		fread(microprograma,sizeof(microInstrucao),512,arquivo);

		for(int i = 0;i<513;i++){

			printf("\n%li\n",microprograma[i]);
		}
		fclose(arquivo);
	}

}