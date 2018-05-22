	org 0x7c00
	bits 16
	
	mov ax, 0
	mov ds, ax
	
	cli
	
	mov si, msg
	mov cx, msg
	
loop:	lodsb
	or al, 0
	jz fim
	mov ah, 0x0E
	int 0x10
	inc cx
	mov si, cx
	jmp loop
	
fim: hlt

msg: db 'h', 'e', 'l', 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd', '!'

times 510 - ($-$$) db 0
dw 0xaa55