	org 0x7c00
	bits 16

	mov ax, 0
	mov ds, ax

	cli

	mov ah, 0x0e
	mov al, 0x0

	mov bl, 0x9

loop:
	and bl, al
	je fim
	add al, 1
	int 0x10

fim:
	hlt

	times 510 - ($-$$) db 0
	dw 0xaa55
