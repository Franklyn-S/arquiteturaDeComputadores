;programa para ler o segundo setor do disco e colocar na memÃ³ria de vÃ­deo (exibindo o conteÃºdo em caracteres)
    org 0x7c00
    bits 16

    xor ax, ax
    mov ds, ax 
    cli

inicio:

    ;leitura do segundo setor do disco, onde estÃ¡ o texto a ser exibido

    int 13h            ;interrupÃ§Ã£o de disco (inicializa)

    mov ah, 0x02       ;ler setores
    mov al, 1          ;quantidade de setores a serem lidos (1 setor)
    mov ch, 0          ;cilindro (0)
    mov dh, 0          ;cabeÃ§ote (0)
    mov cl, 2          ;ler a partir de qual setor? (a partir do setor 2)
    mov bx, 0x7E00     ;endereÃ§o de memÃ³ria onde gravar o(s) setor(es) lido(s)
    int 13h            ;interrupÃ§Ã£o de disco

    ;a partir daqui copia os bytes lidos para a memÃ³ria de vÃ­deo, exibindo o texto

    mov si, bx    
    mov bx, 0xB800
    mov es, bx

    mov ax, 0
    mov bx, 0
.string:
    lodsb
    mov di, bx
    mov [es:di], al
    add bx, 2
    or ax, ax
    jnz .string

    hlt
    times 510 - ($-$$) db 0
    dw 0xaa55