;programa que pede um valor e imprime seu dobro
	org 0x7c00
	bits 16

	mov ax, 0
	mov ds, ax

	;pede nÃºmero e grava no endereÃ§o 0x7e00
	mov ax, 0x7e00
	call geti

	;pega valor digitado, que estÃ¡ gravado no endereÃ§o 0x7e00, leva para o registrador ax, calcula o dobro e devolve resultado para o endereÃ§o 0x7e00
	mov ax, [0x7e00]
	imul ax, 2
	mov [0x7e00], ax

	;escreve nÃºmero que estÃ¡ no endereÃ§o 0x7e00
	mov ax, 0x7e00
	call printi	
	
	jmp fim

;funÃ§Ã£o que pega um valor numÃ©rico digitado e grava no endereÃ§o de memÃ³ria indicado no registrador ax
;tal funÃ§Ã£o realiza o cÃ¡lculo que transforma a string digitada no nÃºmero inteiro correspondente, calculando dÃ­gito a dÃ­gito
;para cada caractere, acumula-se o resultado e multiplica-se por 10 sempre que um novo for digitado.
geti:   push ax
	mov di, ax
	mov ax, 0
	push ax
loop1:	mov ah, 0x00  ;loop para calcular o nÃºmero final dÃ­gito a dÃ­gito,
	int 0x16
	mov ah, 0x0e
	int 0x10      ;exibe dÃ­gito digitado
	cmp al, 13
	je  term1
	sub al, 48    ;transforma caractere no valor numÃ©rico correspondente
	mov dl, al
	pop ax
	imul ax, 10
	add ax, dx
	push ax
	jmp loop1
term1:  mov al, 10    ;faz a quebra de linha e grava o nÃºmero calculado, que estÃ¡ no registrador ax, na memÃ³ria
	int 0x10
        pop ax
	mov [ds:di], ax
	pop ax
	ret

;funÃ§Ã£o que pega um valor numÃ©rico no endereÃ§o de memÃ³ria indicado no registrador ax e exibe a string correspondente
;tal funÃ§Ã£o gera a string caractere a caractere pegando cada dÃ­gito do nÃºmero inteiro atravÃ©s do resto da divisÃ£o
;atenÃ§Ã£o para o uso da pilha na inversÃ£o dos dÃ­gitos, pois o cÃ¡lculo extrai do menos significativo para o mais significativo
;entretanto, a escrita na tela Ã© feita do mais significativo para o menos significativo.
printi: push ax
	mov si, ax
	mov ax, [ds:si]
	mov bx, 10
	mov cx, 0
loop2:	mov dx, 0     ;loop para extrair cada dÃ­gito, colocando na pilha
	idiv bx
	add dx, 48    ;calcula o caractere correspondente ao dÃ­gito (registrador dx guarda resto da divisÃ£o)
	push dx
	inc cx
	or ax, ax
	jnz loop2
loop3:	pop ax        ;loop para desempilhar dÃ­gitos, escrevendo-os na ordem correta
	mov ah, 0x0e
	int 0x10
	dec cx
	or cx, cx
	jnz loop3
	pop ax
	ret

fim:	hlt

	times 510 - ($-$$) db 0
	dw 0xaa55