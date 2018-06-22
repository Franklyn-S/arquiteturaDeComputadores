;Programa para saudar o usuÃ¡rio com entrada de string
	org 0x7c00
	bits 16

	mov ax, 0
	mov ds, ax

	mov ax, perg
	call prints

	mov ax, 0x7e00
	call gets

	mov ax, respi
	call prints

	mov ax, 0x7e00
	call prints

	mov ax, respf
	call prints
	
	jmp fim

;Subrotina para pegar uma string digitada (atÃ© o enter) usando a interrupÃ§Ã£o 0x16 (teclado), gravando as letras no endereÃ§o indicado pelo registrador ax
gets:	push ax
	push di
	mov di, ax
.loop2: mov ah, 0 		;laÃ§o para gravar cada letra digitada atÃ© encontrar o enter
	int 0x16
	cmp al, 13
	je .ret2
	mov [ds:di], al
	inc di
	mov ah, 0x0e
	int 0x10
	jmp .loop2
.ret2:	mov ah, 0x0e 		;finaliza quebrando a linha
	int 0x10
	mov al, 10
	int 0x10
	mov [ds:di], byte 0 	;grava o byte 0 no final da string
	pop di
	pop ax
	ret

;subrotina para escrever na tela a string gravada no endereÃ§o indicado pelo registrador ax utilizando a interrupÃ§Ã£o 0x10 (vÃ­deo)
prints:	push ax
	push si
	mov si, ax
	mov ah, 0x0e
.loop1:	lodsb			;laÃ§o para ler a string escrevendo letra por letra
	or al, al
	jz .ret1
	int 0x10
	jmp .loop1	
.ret1:	pop si
	pop ax
	ret

fim:	hlt

;strings constantes
perg:	db "Oi! Qual o seu nome?", 10, 13, 0
respi:	db "Ola, ", 0
respf:  db "!", 10 , 13, 0

	times 510 - ($-$$) db 0
	dw 0xaa55