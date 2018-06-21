	org 0x7C00
	bits 16

	cli
	;Modo o modo para modo gráfico
	mov ah, 0x0 
	mov al,0x13
	int 0x10

	mov ax,0
	mov ds, ax

	;Leio os 32 setores onde está a imagem
	int 0x13
	mov ah,0x02
	mov al,32
	mov ch,0
	mov dh,0
	mov cl,2
	mov bx,0x7E00
	int 0x13


	mov ax,0xA000
	mov es,ax

	mov di,0
	;cx contém o número de bytes que serão printados
	mov cx,16000
view: mov dx,[bx] ;movo para dx o valor que está em bx
	or cx,cx 
	jz .fim ;verifico se cx é zero e se for vai para o fim
	mov [es:di],dx ;printo o valor que está em dx
	inc bx
	inc di
	dec cx
	jmp view

.fim: jmp .fim

	times 510 - ($-$$) db 0
	dw 0xaa55