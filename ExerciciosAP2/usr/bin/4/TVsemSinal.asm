		org 0x7c00
		bits 16

		cli

		mov ah, 0
		mov al, 0x13
		int 0x10

		mov ax, 0xA000
		mov es, ax

loop4:	mov ax, 0 ;cor aux
loop2:	mov dx, 0 ;indice VRAM
		mov bx, 64000 ;printar tela toda
		inc ax
		cmp ax, 257
		je loop4
loop1:	mov cx, ax ;cor
		
loop3:	mov di, dx
		mov [es:di], cx
		inc cx
		dec bx
		or bx, bx
		jz loop2

		cmp cx, 257
		je loop1
		inc dx
		jmp loop3

		times 510 - ($-$$) db 0
		dw 0xaa55