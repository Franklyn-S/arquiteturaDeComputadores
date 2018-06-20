;nasm -f bin inverte.asm -o inverte.bin Comando para compilar
	org 0x7c00
	bits 16

	;Atribuicao de 0 ao registrador "Data Segment" (ds)
	mov ax, 0
	mov ds, ax

	cli

	push ax
	push di
	mov di, ax
		
loop:	mov ah, 0 ;coloco 0 em "ah" para chamar a int de entrada de teclado(0x16)
		int 0x16 ;pego o valor do teclado e coloco em "al"
		cmp al, 13 ;compare "al" com enter(13)
		je ret1 ; pule se "al" for enter

		mov [ds:di], al ; coloque al em ds[di](ds na posição di)
		inc di
		mov ah, 0x0e
		int 0x10
		jmp loop

		 
ret1:	dec di
		mov al, [ds:di]
		
		mov ah, 0x02
		mov dh, 1
		int 0x10
		or di, di
		jz final
		jmp ret1

		

final:	pop ax
		hlt
	
	times 510 - ($-$$) db 0
	dw 0xAA55
	
	
