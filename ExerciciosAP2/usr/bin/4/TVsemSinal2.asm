		org 0x7c00
		bits 16

		cli

		mov ah, 0
		mov al, 0x13
		int 0x10

		mov ax, 0xA000
		mov es, ax

		mov cl, 0 ; cor

		;Printa a tela toda
loop2:	mov dx, 0 ;indice VRAM
		mov bx, 64000 ;printar tela toda
		inc cl
		
loop3:	mov di, dx ;indice
		mov [es:di], cl
		inc cl

		dec bx
		or bx, bx
		jz loop2
		
		inc dx
		jmp loop3

		times 510 - ($-$$) db 0
		dw 0xaa55