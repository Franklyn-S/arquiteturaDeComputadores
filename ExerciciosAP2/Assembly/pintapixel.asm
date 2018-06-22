     org 0x7c00
     bits 16
     ;programa para pintar a tela toda de vermelho no modo grÃ¡fico pixel a pixel

     ;AtribuiÃ§Ã£o de 0 ao registrador "Data Segment" (ds)
     mov ax, 0x00
     mov ds, ax 
     ;limpa interrupÃ§Ãµes
     cli

     ;com AH = 0x00 e AL = 0x13, a interrupÃ§Ã£o 0x10 coloca o vÃ­deo no modo grÃ¡fico VGA 320x200 com 8 bits por pixel (256 cores)
     mov al, 0x13
     int 0x10

     ;AtribuiÃ§Ã£o do endereÃ§o 0xA000 ao registrador "Extra Segment" (es), para determinar o segmento de memÃ³ria correspondente Ã  memÃ³ria de vÃ­deo no modo grÃ¡fico
     mov ax, 0xA000
     mov es, ax

     ;Registrador cx para contagem do laÃ§o (repetiÃ§Ã£o de 64000 vezes)
     mov cx, 64000
     ;Usar registrador bx como contador para definir o deslocamento de memÃ³ria no registrador "Destination Index" (di)
     mov bx, 0

     ;laÃ§o que preenche as 64000 posiÃ§Ãµes de memÃ³ria a partir do endereÃ§o 0xA000 com o byte 40 (ou seja, atribui a cor vermelha a todos os pixels da tela de 320x200).
loop:
     mov di, bx
     mov [es:di], byte 40
     inc bx
     dec cx
     jnz loop

     hlt

     times 510 - ($-$$) db 0
     dw 0xaa55