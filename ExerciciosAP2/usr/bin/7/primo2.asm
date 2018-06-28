	org 0x7c00
	bits 16

	cli




getint:

	mov ah, 0
	mov bx, 0
loop:
	int 0x16
	cmp al, 13
	je ehprimo

	mov ah, 0x0e
	imul bx, 10
	sub al, 48
	add bl, al
	int 0x10
	jmp loop

ehprimo:
	push cx
	push dx
	mov ax, bx

	cmp ax, 1
	je retornof

	mov bx, ax
	mov cx, ax

loop3:
	mov ax, cx
	dec bx
	cmp bx, 1
	je retornov

	mov dx, 0
	idiv bx
	
	cmp dx, 0
	je retornof
	jmp loop3

retornov:
	pop dx
	pop cx
	mov si, primo
	mov ah, 0x0e
.loop:
	lodsb
    or al, al
    jz fim
    int 0x10
    jmp .loop

retornof:
	pop dx
	pop cx
	mov si, nprimo
	mov ah, 0x0e
.loop2:
	lodsb
    or al, al
    jz fim
    int 0x10
    jmp .loop2



fim:hlt
primo: db 'eh primo!', 0
nprimo: db 'nao eh primo!', 0

	times 510 - ($-$$) db 0
	dw 0xaa55