## Documentação

#### Propriedades

* unsigned int word - 32 bits
* unsigned char byte - 8 bits
* unsigned long int microInstrucao - 64 bits

O micro-programa possui 512 micro-instruções

#### Métodos

**decode**

Recebe como argumento uma instrução *word* e "quebra" ela em cinco partes passando para as respectivas variáveis a instrução correta.

**ler_registrador**

Recebe como argumento um registrador *byte* e passa para o barramento B o valor desse registrador.

**gravar_registrador**

Recebe como argumento um grupo de registradores *word* que atribui à esses registradores o valor do barramento C.

**ula**

Recebe como argumento uma operação *byte* e define qual operação será realizada entre os barramentos A(registrador H) e B. o barramento C recebe o valor da operação. Também executa o deslocamento de bits quando solicitado.

**next_function**

Recebe como argumentos a próxima micro-instrução *word* e o tipo de pulo *int*. Define qual a próxima micro-instrução será executada de acordo com o pulo recebido.

**dec2bin**

Recebe um número *int* como argumento e retorna seu binário correspondente, separando em grupos de 8 bits.

**debug**

Mostra os valores, tanto decimal quanto binário, dos registradores e da pilha.


## O que falta para implementar?
 	 
* Pilha
* Assembler