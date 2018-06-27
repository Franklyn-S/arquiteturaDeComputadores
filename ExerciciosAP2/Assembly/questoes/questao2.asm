    org 0x7c00
    bits 16

    mov ax, 0
    mov ds, ax 
    cli

inicio:

    ;leitura do segundo setor do disco, onde está o texto a ser exibido

    int 13h            ;interrupção de disco (inicializa)

    mov ah, 0x02       ;ler setores
    mov al, 1          ;quantidade de setores a serem lidos (1 setor)
    mov ch, 0          ;cilindro (0)
    mov dh, 0          ;cabeçote (0)
    mov cl, 2          ;ler a partir de qual setor? (a partir do setor 2)
    mov bx, 0x7e00     ;endereço de memória onde gravar o(s) setor(es) lido(s)
    int 13h            ;interrupção de disco


    ; Mover o texto para o registrador 'si'
    mov ah, 0x0e
    mov si, bx


    ; Mover a matrícula para o registrador 'di'
    mov di, mat
    jmp mensagem
    
    ; loop que sempre reseta a matrícula quando ela chega no final
matricula:
    mov di, mat
    jmp numeros

    ; loop que carrega os bytes da mensagem
mensagem:
    lodsb

    cmp al, 0x00
    je fim

    ; loop que carrega os bytes da matrícula, faz as devidas verificações e decripta a mensagem
numeros:
    mov cl, [di]
    inc di
    
    cmp cl, 0
    je numeros

    cmp cl, 10
    je matricula

    add al, cl
    int 0x10
    jmp mensagem

fim:
    hlt

    ; label contendo a matricula. o 10 representa o fim da matricula
mat:
    db 4, 0, 0, 0, 9, 7, 10

    times 510 - ($-$$) db 0
    dw 0xaa55