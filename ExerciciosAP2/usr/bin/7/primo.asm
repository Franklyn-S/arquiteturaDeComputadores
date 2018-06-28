	org 0x7c00
	bits 16

	cli

	mov ax, 28
	call ehprimo

	cmp bx, 1
	je v
	cmp bx, 1
	jne f

v:
	mov si, primo	
	call print
	jmp fim
f:
	mov si, nprimo	
	call print
	jmp fim



getint:

	mov ah, 0
loop:
	int 0x16
	cmp al, 13
	je .retorno

	int ah, 0x0e
	push ax
	int 0x10

.retorno:



print:
	mov ah, 0x0e
.loop:
	lodsb
    or al, al
    jz .retornop
    int 0x10
    jmp .loop
   

.retornop:
    ret

fim:hlt

prints:
	push si
	mov ah, 0x0e
loop2:
	lodsd
	or al, al
	jz fim
	int 0x10
	jmp loop2

	pop si


ehprimo:
	push cx
	push dx

	cmp ax, 1
	je retornov

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
	mov bx, 1
	jmp retorno

retornof:
	mov bx, 0
	jmp retorno

retorno:
	pop dx
	pop cx

	ret

primo: db 'eh primo!', 0
nprimo: db 'nao eh primo!', 0

	times 510 - ($-$$) db 0
	dw 0xaa55