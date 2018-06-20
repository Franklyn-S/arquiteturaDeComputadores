		org 0x7c00
		bits 16

		cli

		;coloca no modo gráfico
		mov ah, 0
		mov al, 0x13
		int 0x10 
		;acessa o endereço da VRAM
		mov ax, 0xA000
		mov es, ax

		mov cx, 64000 ;contador do laço
		mov bx, 0 ; contador do deslocamento de memória no di

loop:	
		mov ah, 0
		int 0x16
.loop2:

		

		

		jmp loop

		times 510 - ($-$$) db 0
		dw 0xaa55