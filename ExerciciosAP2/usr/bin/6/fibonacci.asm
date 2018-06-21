	org 0x7c00
	bits 16

	mov ax,0
	mov ds,ax

	cli


	mov ax,0 ;ax vai ser o meu anterior
	mov bx,1 ;bx vai guardar o valor do próximo

	mov cx,22

loop: or cx,cx ;faz um ou lógico com cx e cx
	jz fim ;se cx for zero ele vai para o fim

	;guardo os valores das variáveis
	push ax
	push bx
	push cx
	push dx

	;printa um espaço
	mov ah,0x0e
	mov al, ' '
	int 0x10

	mov cx,0 ;conta quantos dígitos o número que vou imprimir tem
	mov ax,bx ;ax recebe o número que eu quero imprimir
	mov bx,10 ;bx recebe 10

print: mov dx,0 ;zera dx
	or ax,ax ;faz um ou lógico de ax com ax
	jz desempilha ;se o resultado desse ou for zero vai para desempilha
	idiv bx ;aqui se divide ax por 10, o resto é colocado em dx e o quociente em ax
	mov dh,0x0e ;coloco em dh o comando de printar
	push dx ;coloco dx na pilha, onde dh contem o comando de printar e o dl possui o bit que será printado futuramente
	inc cx ;incremento o contador de dígitos
	jmp print

	;Agora todos os dígitos do número que queros printar estão na pilha
	;o desempilha irá desempilha-los e printalos

desempilha: or cx,cx 
	jz continuacao ;se o ou lógico da linha anterior for zero pule para continuacao
	pop ax ;recebe o o comando 0x0e em ah e o dígito que queremos printar em al
	add al,48 ;soma 48 a al
	int 0x10 ;printa o valor de al
	dec cx ;decrementa o contador de dígitos
	jmp desempilha	

continuacao: 
	;restituo os valores dos registradores
	pop dx
	pop cx
	pop bx
	pop ax

	mov dx, bx ; move para dx o valor do próximo
	add bx, ax ; somo o anterior com o próximo, gerando o novo próximo
	mov ax,dx  ; movo para ax o novo anterior

	dec cx
	jmp loop



fim: hlt

	times 510 - ($-$$) db 0
	dw 0xaa55