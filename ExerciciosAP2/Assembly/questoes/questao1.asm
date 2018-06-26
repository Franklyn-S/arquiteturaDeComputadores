	org 0x7c00
	bits 16

	mov ax, 0x00
	mov ds, ax

	cli

	; define o modo gráfico
	mov al, 0x13
	int 0x10

	; carrega a imagem que ocupa 32 setores para a memoria no endereço 0x7e00
	int 13h
	mov ah, 0x02
	mov al, 32
	mov ch, 0
	mov dh, 0
	mov cl, 2
	mov bx, 0x7e00
	int 13h

	; define o endereço da placa de vídeo
	mov si, bx
	mov bx, 0xa000
	mov es, bx

	mov ax, 0
	mov bx, 0
	mov cx, 64000

	; carrega a imagem que está no endereço 0x7e00
img:
	lodsb
	mov di, bx
	mov [es:di], al
	inc bx
	dec cx
	jnz img

	hlt

	times 510 - ($-$$) db 0
	dw 0xaa55