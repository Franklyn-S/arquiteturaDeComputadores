		org 0x7c00
		bits 16

		cli

		mov al, 0 ;anterior do anterior
		mov bl, 1 ;anterior

		mov cl, 0 ;contador
loop:	add al, bl
		
		mov ah, 0x0e
		int 0x10
		cmp cl, 22
		je fim

		push ax
		mov al, ' '
		mov ah, 0x0e
		int 0x10		
		pop ax

		push cx
		mov cl, bl ;auxiliar
		mov bl, al ;anterior = soma
		mov al, cl ;anterior do anterior = anterior
		pop cx

		jmp loop
fim:	hlt

		times 510 - ($-$$) db 0
		dw 0xaa55 