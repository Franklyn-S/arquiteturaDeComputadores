		org 0x7c00
		bits 16

		cli

		;modo grafico
		mov ah, 0x0
		mov al, 0x13
		int 0x10

		;interrupção para ler setores
		int 0x13
		mov ah, 0x02 ;ler setores
		mov al, 32 ;quantos setores
		mov cl, 2 ;a partir do setor
		mov ch, 0 ;cilindro
		mov dh, 0 ;cabeçote
		mov bx, 0x7e00
		int 0x13

		;memória de vídeo
		mov ax, 0xA000
		mov es, ax

		;contadores
		mov di, 0
		mov cx, 16000

loop:	mov dx, [bx]
		cmp cx, 0
		jz fim
		mov [es:di], dx
		inc bx
		inc di
		dec cx
		jmp loop

fim:	hlt

		times 510 - ($-$$) db 0
		dw 0xaa55