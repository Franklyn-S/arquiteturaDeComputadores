	org 0x7c00
	bits 16

	mov ax, 0
	mov ds, ax

	cli

	mov ax, 0x7e00
	call entrada

	call calcular

	jmp fim

entrada:
	push ax
	mov di, ax
	mov ax, 0 
	push ax
loop:
	mov ah, 0
	int 0x16
	mov ah, 0x0e
	int 0x10
	cmp al, 13
	je montar
	sub al, 48
	mov dl, al
	pop ax
	imul ax, 10
	add ax, dx
	push ax
	jmp loop
montar:
	pop ax
	mov [ds:di], ax
	pop ax
	ret

calcular:
	push ax
	mov si, ax
	mov ax, [ds:si]
	mov bx, ax
	mov cx, 2
calculando:
	mov dx, 0
	mov ax, bx

	idiv cx

	cmp cx, bx
	je ehprimo

	cmp dx, 0
	je naoprimo

	inc cx
	jmp calculando

ehprimo:
	call mostrar 
	mov si, msg1
loop1:
	lodsb
	or al, al
	jz fim
	int 0x10
	jmp loop1


naoprimo:
	call mostrar 
	mov si, msg2
loop2:
	lodsb
	or al, al
	jz fim
	int 0x10
	jmp loop2


mostrar:
	mov ax, [ds:si]
	mov bx, 10
	mov cx, 0
empilhando:
	mov dx, 0
	idiv bx
	add dx, 48
	push dx
	inc cx
	or ax, ax
	jnz empilhando
mostrando:
	pop ax
	mov ah, 0x0e
	int 0x10
	dec cx
	or cx, cx
	jnz mostrando

	ret


fim:
	hlt

msg1:
	db " eh primo!", 0

msg2:
	db " nao eh primo!", 0

	times 510 - ($-$$) db 0
	dw 0xaa55