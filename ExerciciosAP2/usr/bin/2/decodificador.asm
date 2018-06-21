	org 0x7c00
	bits 16

	mov ax,0
	mov ds,ax

	cli
	
	;Aqui chamamos a interrupção para ler no disco
	int 0x13
	mov ah,0x02 ;Comando para ler
	mov al,1 ;número de setores que leremos
	mov ch,0 ;cilindro a ser lido
	mov dh,0 ;cabeçote a ser lido
	mov cl,2 ;ler a partir do setor 2
	mov bx,0x7E00 ; endereço de memória onde será gravado o dado lido
	int 0x13

	mov si,mat ; passo para si o endereço do primeiro caracter da minha matrícula

loop:
	mov al,[bx] ;movo para al o valor que está no endereço bx
	or al,al 
	jz fim ; se o ou der zero significa que não há mais texto no arquivo a ser lido e vou para o fim do programa
	mov dx,[si] ;movo para dx um dos números da minha matrícula
	cmp dx,10 ;comparo esse número com 10
	je reiniciar ;se for igual a 10 significa que presciso voltar para o primeiro dígito da minha matrícula
	sub al,dl ; subtraio de al o valor de dl
	mov ah,0x0E 
	int 0x10 ; printo o valor que está em al
	inc bx ; incremento bx para pegar o endereço do próximo dígito que está no arquivo
	inc si ; incremento si para pegar o próximo bit que está em mat
	jmp loop

reiniciar:
	mov si,mat ;passa para si o primeiro endereço de mat
	jmp loop

fim: hlt

mat: db 4,0,0,5,0,1,10	
	times 510 - ($-$$) db 0
	dw 0xaa55