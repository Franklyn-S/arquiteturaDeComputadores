	org 0x7c00
	bits 16

	mov ax, 0
	mov ds, ax

	cli
	
	mov si, msg

	mov ah, 0x0E

loop:
	lodsb
	or al, al
	jz fim
	int 0x10
	jmp loop

fim:
	hlt

msg: 
	db "Ola, tudo bem?"

	times 510 - ($-$$) db 0
	dw 0xaa55