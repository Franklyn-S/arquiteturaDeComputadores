	org 0x7c00
	bits 16
	cli

	mov ax, 0 ;anterior
	mov bx, 1 ; proximo

	mov cx, 22 ;contador


loop:
	or cx, cx
	jz fim

	push ax
	push bx
	push cx
	push dx

	;printa um espaço
	mov ah, 0x0e
	mov al, ' '
	int 0x10

	mov cx, 0 ;contador de digitos
	mov ax, bx ;movo para ax o valor que eu quero printar
	mov bx, 10 ; movo 10 para bx para dividir

print:
	mov dx, 0
	or ax, ax ;verifico se ax é zero
	jz desempilha
	idiv bx ;divido ax por 10 colocando o resto em dx e o quociente em ax
	mov dh, 0x0e
	push dx ;coloco na pilha o valor que quero printar
	inc cx ;incrementa o contador de digitos
	jmp print

desempilha:
	or cx, cx
	jz continua
	pop ax
	add al, 48
	int 0x10
	dec cx
	jmp desempilha
	


continua:
	;restituo os valores dos registradores
	pop dx
	pop cx
	pop bx
	pop ax

	mov dx, bx ;movo o novo anterior para um auxiliar
	add bx, ax
	mov ax, dx
	dec cx
	jmp loop



fim:hlt
	times 510 - ($-$$) db 0
	dw 0xaa55