	org 0x7c00
	bits 16

	mov ax, 0
	mov ds, ax

	cli

	mov ax, 0x7e00
	call entrada
	call saida

fim:
	hlt

entrada:
	push ax
	push di
	mov di, ax
loop:
	mov ah, 0
	int 0x16
	cmp al, 13
	je retorna
	mov [ds:di], al
	inc di
	mov ah, 0x0e
	int 0x10
	jmp loop
retorna:
	mov ah, 0x0e
	int 0x10
	mov al, 10
	int 0x10
	mov [ds:di], byte 0
	pop di
	pop ax
	ret

saida:
	mov si, ax
	mov ah, 0x0e
loop2:
	lodsb
	or al, al
	jz retorna2
	push ax
	jmp loop2
retorna2:
	pop ax
	or al, al
	jz fim
	int 0x10
	jmp retorna2

	times 510 - ($-$$) db 0
	dw 0xaa55