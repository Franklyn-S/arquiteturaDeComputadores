		org 0x7c00
		bits 16

		cli

		push 0; para parar o loop
		

loop1:	mov ah, 0
		int 0x16
		mov ah, 0x0e
		int 0x10

		cmp al, 13
		je print

		push ax
		
		jmp loop1	

print:
		mov al, 10
		mov ah, 0x0e
		int 0x10
loop2:
		pop ax
		mov ah, 0x0E
		int 0x10
		or al, al
		jz fim
		jmp loop2

fim:	hlt

		times 510 - ($-$$) db 0
		dw 0xaa55