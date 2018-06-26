	org 0x7c00
	bits 16


	mov ax, 0
	mov ds, ax

	cli

	; define o modo grafico
	mov al, 0x13
	int 0x10

	;Atribuição do endereço 0xA000 ao registrador "Extra Segment" (es), para determinar o segmento de memória correspondente à  memória de vídeo no modo gráfico
	mov bx, 0xa000
	mov es, bx

	mov cx, 64000
	mov dx, 0

	; loop infinito que sempre espera o valor ser digitado para mostrar sua cor correspondente
receber:
	mov ax, 0x00

	int 0x16
	cmp al, 13
	je loop

loop:
	mov di, dx
	mov [es:di], al
	inc dx
	dec cx
	jnz loop
	jmp receber

	hlt

	times 510 - ($-$$) db 0
	dw 0xaa55