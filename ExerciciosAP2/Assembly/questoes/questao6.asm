	org 0x7c00
	bits 16

	mov ax, 0
	mov ds, ax

	cli

	mov cx, 22
	mov ax, 1
	
	push ax
	push 0

	call mostrar

loop:
	cmp cx, 0
	je fim
	pop ax
	pop bx
	add ax, bx
	push ax
	push bx
	call mostrar
	dec cx
	jmp loop

mostrar:
	push cx
	push bx
	push ax
	mov ah, 0x0e
	mov al, 32
	int 0x10
	pop ax
	mov bx, 10
	mov cx, 0
loop1:
	mov dx, 0
	idiv bx
	add dx, 48
	push dx
	inc cx
	or ax, ax
	jnz loop1
loop3:
	pop ax
	mov ah, 0x0e
	int 0x10
	dec cx
	or cx, cx
	jnz loop3
	pop bx
	pop cx
	ret

fim:
	hlt

	times 510 - ($-$$) db 0
	dw 0xaa55