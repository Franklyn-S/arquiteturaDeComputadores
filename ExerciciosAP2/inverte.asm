;nasm -f bin inverte.asm -o inverte.bin Comando para compilar
	org 0x7c00
	bits 16

	;Atribuicao de 0 ao registrador "Data Segment" (ds)
	mov ax, 0
	mov ds, ax

	mov ax, 0x7e00
	call gets

	mov ax, 0x7e00
	call prints



	cli
	
;Subrotina para pegar uma string digitada (até o enter) usando a interrupção 0x16 (teclado), gravando as letras no endereço indicado pelo registrador ax

gets:	push ax
		;push di
		mov di, ax
		
.loop:	mov ah, 0 ;coloco 0 em "ah" para chamar a int de entrada de teclado(0x16)
		int 0x16 ;pego o valor do teclado e coloco em "al"
		cmp al, 13 ;compare "al" com enter(13)
		je .ret1 ; pule se "al" for enter
		mov [ds:di], al ; coloque al nem ds[di](ds na posição di)
		inc di
		mov ah, 0x0e
		int 0x10
		jmp .loop

		 
.ret1:	mov ah, 0x0e ;digo que quero printar
		int 0x10 ;print o valor de al(13) mover cursor para o inicio
		mov al, 10 ; coloco 10 em al que significa mover o cursor para baixo
		int 0x10 ; pri
		mov [ds:di], byte 0 ; grava o byte 0 no final da string
		;pop di
		pop ax
		ret

;subrotina para escrever na tela a string gravada no endereço indicado pelo registrador ax utilizando a interrupção 0x10 (ví­deo)

prints:	push ax
		mov ah, 0x0e ; digo que vou imprimir
.loop2:	
		mov [ds:di], al
		dec di
		or al, al
		jz .ret2
		int 0x10
		jmp .loop2
.ret2:	pop ax
		ret

	
	
	times 510 - ($-$$) db 0
	dw 0xAA55
	
	
