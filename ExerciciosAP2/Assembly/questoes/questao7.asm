	org 0x7c00
	bits 16

	mov ax, 0
	mov ds, ax

	cli

	mov ax, 0x7e00
	call entrada

	call calcular

	jmp fim

	; A sub-rotina ENTRADA recebe os valores do teclado (número em forma de string) e transforma em inteiro, após isso empilha os valores, separados de acordo com o sistema de numeração decimal (unidade, dezena, centena ...). Depois que os números são recebidos e montados, eles são colocados no endereço 0x7e00 do segmento 0.
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

	; O método de cálculo funciona através de várias divisões e verificações. Iniciamos um iterador no 2 e dividimos o valor por ele. Caso o iterador seja igual ao número isso significa que ele só pode ser primo (divisível por 1 ou por ele mesmo). Caso o resto da divisão do número recebido com o iterador seja igual a 0 então o número não é primo. 
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

	; Método que mostra o número com a mensagem que ele é primo
ehprimo:
	call mostrar 
	mov si, msg1
loop1:
	lodsb
	or al, al
	jz fim
	int 0x10
	jmp loop1


	; Método que mostra o número com a mensagem que ele não é primo
naoprimo:
	call mostrar 
	mov si, msg2
loop2:
	lodsb
	or al, al
	jz fim
	int 0x10
	jmp loop2

	; Sub-rotina que transforma o número inteiro do endereço 0x7e00 e segmento 0 em string para mostrar na tela. Funciona de forma análoga á sub-rotina ENTRADA.
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