	org 0x7c00
	bits 16

	mov ax, 0
	mov ds, ax

	cli

	; Inicializa os valores para calcular Fibonacci
	mov cx, 22
	mov ax, 1
	
	push ax
	push 0

	call mostrar

	; Calcula os valores de Fibonacci desempilhando os dois últimos números, somando-os e depois empilhando os novos valores
calcular:
	cmp cx, 0
	je fim
	pop ax
	pop bx
	add ax, bx
	push ax
	push bx
	call mostrar
	dec cx
	jmp calcular

	; Inicializa os registradores para printar os valores empilhados
mostrar:
	push cx
	push bx
	push ax
	mov ah, 0x0e
	mov al, 32 ; printa o espaço
	int 0x10
	pop ax
	mov bx, 10
	mov cx, 0

	; Monta os números, transformando-os em string
montar:
	mov dx, 0
	idiv bx
	add dx, 48
	push dx
	inc cx
	or ax, ax
	jnz montar

	; Depois de montados e empilhados, desempilha os valores e mostra na tela
mostrando:
	pop ax
	mov ah, 0x0e
	int 0x10
	dec cx
	or cx, cx
	jnz mostrando
	pop bx
	pop cx
	ret

fim:
	hlt

	times 510 - ($-$$) db 0
	dw 0xaa55