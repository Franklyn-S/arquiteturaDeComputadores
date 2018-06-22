	org 0x7c00
	bits 16

	mov ax, 0
	mov ds, ax

	cli

	mov ax, 0x7e00
	call entrada

	call mostrar

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

mostrar:
	push ax
	mov si, ax
	mov ax, [ds:si]
	mov bx, ax
	mov cx, 2
calculando:
	mov dx, 0
	mov ax, bx
	;cmp cx, 5
	;je fim

	idiv cx

	cmp cx, bx
	je ehprimo

	cmp dx, 0
	je naoprimo

	inc cx
	jmp calculando

ehprimo:
	mov ax, bx 
	mov si, msg1
	mov ah, 0x0e
	int 0x10
loop1:
	lodsb
	or al, al
	;jz fim
	ret
	int 0x10
	jmp loop1


naoprimo:
	mov ax, bx 
	mov si, msg2
	mov ah, 0x0e
	int 0x10
loop2:
	lodsb
	or al, al
	jz fim
	;ret
	int 0x10
	jmp loop2


fim:
	hlt

msg1:
	db " eh primo!"

msg2:
	db " nao eh primo!"

	times 510 - ($-$$) db 0
	dw 0xaa55