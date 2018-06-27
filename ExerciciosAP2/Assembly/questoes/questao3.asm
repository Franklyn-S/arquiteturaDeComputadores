	org 0x7c00
	bits 16

	mov ax, 0
	mov ds, ax

	cli

	; Loop que recebe e empilha os valores até a tecla 'enter' ser pressionada
entrada:
	mov ah, 0
	int 0x16
	cmp al, 13
	je inverter
	mov ah, 0x0e
	int 0x10
	push ax
	jmp entrada

	; Printa '/n/r' e depois entra em um laço que vai desempilhando os valores e mostrando na tela
inverter:
	mov ah, 0x0e
	mov al, 13
	int 0x10
	mov al, 10
	int 0x10
invertendo:
	pop ax
	or al, al
	jz fim
	mov ah, 0x0e
	int 0x10
	jmp invertendo

fim:
	hlt

	times 510 - ($-$$) db 0
	dw 0xaa55