	org 0x7c00
	bits 16

	mov ax, 0x00
	mov ds, ax

	cli

	; define o modo grafico
	mov al, 0x13
	int 0x10

	;Atribuição do endereço 0xA000 ao registrador "Extra Segment" (es), para determinar o segmento de memória correspondente à  memória de vídeo no modo gráfico
reiniciar:
	mov ax, 0xa000
	mov es, ax
	mov dx, 0
	mov ax, 0

zerar:
	mov cx, 64000
	mov bx, 0

	; Define a cor na posição [es:di]. Quando cx zera, ou seja, ocupa todas as posições da tela, as variáveis são zeradas e o Ax incrementado, pois é ele que define qual a cor que inicializa em cada loop. Quando o Ax é igual a 255, valor máximo de cores da paleta, reiniciamos o processo.
	
loop:
	mov di, bx
	mov [es:di], dx
	inc bx
	inc dx
	dec cx
	jnz loop
	inc ax
	mov dx, ax
	cmp ax, 255
	je reiniciar
	jmp zerar

	hlt

	times 510 - ($-$$) db 0
	dw 0xaa55