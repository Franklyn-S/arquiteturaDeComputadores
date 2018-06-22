	org 0x7c00
	bits 16

	mov ax, 0
	mov ds, ax

	cli

entrada:
	mov ah, 0
	int 0x16
	cmp al, 13
	je inverter
	mov ah, 0x0e
	int 0x10
	push ax
	jmp entrada
inverter:
	mov ah,0x0e
	mov al, 13
	int 0x10
	mov al, 10
	int 0x10
loop:
	pop ax
	or al, al
	jz fim
	mov ah, 0x0e
	int 0x10
	jmp loop

fim:
	hlt

	times 510 - ($-$$) db 0
	dw 0xaa55