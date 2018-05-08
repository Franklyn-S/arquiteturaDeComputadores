'''
    A lista abaixo refere-se a lista dos tipos de TOKENS que o assembler suporta
    Token é todo e qualquer conjunto de caracteres com significado semântico
    para a linguagem.

    WORD - Conjunto alfanumérico de caractéres
    LPAREN - Parêntese abrindo "("
    RPAREN - Parêntese fechando ")"
    EOF - Fim de linha
    COLON - Dois pontos ":"
    SPACE - Espaço em branco " "
'''
WORD, LPAREN, RPAREN, EOF, COLON, SPACE = "WORD", "(", ")", "EOF", ":", " "


'''
    O dicionário abaixo mapeia o binário de cada comando
    com o seu tamanho completo, o qual engloba o tamanho, 
    em bytes, do mnemônic e de seus argumentos.
'''
size_per_cmd = {
    0x01: 1,
    0x02: 1,
    0x05: 1,
    0x08: 1,
    0x0B: 1,
    0x0E: 1,
    0x10: 1,
    0x13: 1,
    0x19: 2,
    0x1C: 2,
    0x22: 2,
    0x28: 1,
    0x32: 2,
    0x36: 3,
    0x3C: 3,
    0x43: 2,
    0x47: 2,
    0x4B: 3,
    0x55: 1,
    0x6: 1
}


'''
    O dicionário abaixo mapeia cada mnemônico com
    o seu respectivo código binário.
'''
mnemonics_list = {
    'nop': 0x01,
    'iadd': 0x02,
    'isub': 0x05,
    'iand': 0x08,
    'ior': 0x0B,
    'dup': 0x0E,
    'pop': 0x10,
    'swap': 0x13,
    'bipush': 0x19,
    'iload': 0x1C,
    'istore': 0x22,
    'wide': 0x28,
    'ldc_w': 0x32,
    'iinc': 0x36,
    'goto': 0x3C,
    'iflt': 0x43,
    'ifeq': 0x47,
    'if_icmpeq': 0x4B,
    'invokevirtual': 0x55,
    'ireturn': 0x6,
}


'''
    O dicionário vazio abaixo será preenchido pelo
    loop posterior sendo deixado do seguinte formato:
    ...
    'MNEMONICO': [BINARIO_DO_MNEMONICO, TAMANHO_DO_COMANDO]

    Sendo:
    - O BINARIO_DO_MNEMONICO capturado através do 
      dicionário 'mnemonics_list'
    - O TAMANHO_DO_COMANDO capturado através do 
      dicionário 'size_per_cmd'

    Esse formato é usado pelos algoritmos posteriores
'''
mnemonics = {}

# loop citado no comentário acima
for mnemonic in mnemonics_list:
    mnemonics[mnemonic] = [mnemonics_list[mnemonic], size_per_cmd[mnemonics_list[mnemonic]]]


'''
    Classe Token:
    Será usada para armazenar os tokens do programa em
    assembly.
    Os seus atributos são:
    - type: referente à um elemento da lista dos tipos de tokens no início
            deste arquivo.
    - value: referente à string literal que o token representa,
             por exemplo, um token do tipo LPAREN tem um 
             valor '('.
'''
class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return self.__str__()

'''
    Classe Lexer:
    Esta classe é responsável por caracterizar a sintática
    da linguagem, ou seja, basicamente, quais tokens são
    ou não permitidos.
    Os seus atributos são:
    - text: armazenará o texto de cada comando (ou linha)
            do arquivo assembly.
    - pos: guardará a posição atual da leitura do 'text'
    - current_char: guarda o caractére atual da leitura,
                    ou seja, 'text[post]'.
'''
class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    '''
        Método error:
        Emite um erro quando um token inválido é encontrado,
        por exemplo, o caractére til '~', que não corresponde
        a nada.
    '''
    def error(self):
        raise Exception('Invalid token')

    '''
        Método advance:
        Avance um caracére na leitura por atributo text 
        (linha atual do arquivo que está sendo lido).
    '''
    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indica o fim da linha
        else:
            self.current_char = self.text[self.pos]

    '''
        Método skip_whitespace:
        Verifica se o caractére atual é um espaço em branco,
        e caso seja, pula todas as ocorrências deste.
    '''
    def skip_whitespace(self):
        while self.current_char is not None and (self.current_char.isspace() or self.current_char == '\t'):
            self.advance()

    '''
        Método getWord:
        Verifica se o caractére atual é um alfanumérico,
        e caso seja, guarda uma string 'word' com todas as
        seguintes ocorrências destes alfanuméricos e retorna 'word'.
    '''
    def getWord(self):
        word = ''
        while self.current_char is not None and (self.current_char.isalpha() or self.current_char == '_' or self.current_char.isdigit()):
            word += self.current_char
            self.advance()
        return word
            
    '''
        Método get_next_token:
        Verifica qual o tipo do Token ao qual pertence o
        caractére atual, chama os métodos responsáveis pelo
        tratamento de cada um, e retorna uma instância da classe
        Token com o valor e o tipo desta.
    '''
    def get_next_token(self):

        # Executa enquanto o caractére atual não for nulo,
        # ou seja, não chegar no fim da linha.
        while self.current_char is not None:
            if (self.current_char.isspace() or self.current_char == '\t') and self.pos != 0:
                '''
                    Se o caractére atual é um espaço, chama o método
                    'skip_whitespace', pula todos os demais e continua
                    com a execução.
                '''
                self.skip_whitespace()
                continue

            if self.current_char.isalpha() or self.current_char.isdigit():
                '''
                    Se o caractére atual é um alfanumérico, chama o método
                    'getWord' e retorna um Token do tipo WORD, com o valor
                    da string capturada.
                '''
                word = self.getWord()
                return Token(WORD, word)

            if self.current_char == '(':
                '''
                    Se o caractére atual é um '(', avança um caratére
                    e retorna um Token do tipo LPAREN, com o valor '('.
                '''
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                '''
                    Se o caractére atual é um ')', avança um caratére
                    e retorna um Token do tipo RPAREN, com o valor '('.
                '''
                self.advance()
                return Token(RPAREN, ')')

            if self.current_char == ':':
                '''
                    Se o caractére atual é um ':', avança um caratére
                    e retorna um Token do tipo COLON, com o valor ':'.
                '''
                self.advance()
                return Token(COLON, ':')

            if self.current_char.isspace() and self.pos == 0:
                '''
                    Se o caractére atual é um ' ' e a posição atual de
                    leitura é zero (o que difere do primeiro IF), ou seja,
                    está no início da linha, avança um caratére, e
                    retorna um Token do tipo SPACE, com o valor ' '.
                '''
                self.advance()
                return Token(SPACE, ' ')

            # Se o caractére atual é validade em nenhuma checagem
            # um erro sintático é retornado
            self.error()

        # Se o loop deu-se fim, entende-se que chegou-se ao fim da linha.
        # Logo, retorna-se um Token do tipo EOF, com valor None (null)
        return Token(EOF, None)


'''
    Classe Interpreter:
    Esta classe é responsável por caracterizar a semântica
    da linguagem, ou seja, basicamente, a valoração dada,
    condicionalmente, à sintática.
    Os seus atributos são:
    - lexer: o interpretador, para formar a semântica,
             recebe a sintática, ou seja, uma intância
             da classe Lexer.
    - current_token: o Token atual a ser tratado, por exemplo,
                     LPAREN, WORD, etc...
'''
class Interpreter(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    '''
        Método error:
        Emite um erro quando uma ordenação dada ao conjunto de
        Tokens for desrespeitado, por exemplo: 
            IADD label1: k
        Claramente, o comando acima está errado.
    '''
    def error(self):
        raise Exception('Semantic error')

    '''
        Método eat:
        Verifica se o tipo do Token recebido como parâmetro
        é igual ao Token atual (informação dada pelo atributo
        'current_token'), e caso seja, ele guarda o próximo Token
        (capturado atráves do método 'get_next_token', explicado
        posteriormente) no atributo 'current_token'. Caso não
        seja, retorna o erro.

        Basicamente, se for chamado eat(WORD), obrigatoriamente
        o Token atual deve ser uma 'word' e sendo passará para
        o próximo.
        
        Parâmetos:
        - token_type: Tipo do Token atual

    '''
    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    '''
        Método argument:
        Captura o argumento após capturar-se o label e 
        o mnemônico.
    '''
    def argument(self):
        # Captura qual o token atual
        token = self.current_token
        
        if token.type == WORD:
            '''
                Se o Token capturado for uma WORD
                é armazenado seu valor e retornado.
            '''
            argument = token.value
            self.eat(WORD)
            return argument

        elif token.type == LPAREN:
            '''
                Se o Token capturado for um LPAREN
                é chamado novamente 'argument()' afim de que
                caso o argumento esta entre vários parênteses, 
                como ((((k)))). Então, como a função é chamada
                recursivamete e ignorando os parênteses, ao fim, 
                apenas o 'k' é retornando.
            '''
            self.eat(LPAREN)
            result = self.argument()
            self.eat(RPAREN)
            return result

        elif token.type == EOF:
            '''
                Se o Token capturado for EOF, então quer dizer que não
                há argumento e um caratére vazio ('') é retornado.
            '''
            return ''


    '''
        Método mnemonic:
        Captura o argumento após capturar-se o label.
    '''
    def mnemonic(self):
        if self.current_token.type == WORD:
            '''
                Se o Token capturado for uma WORD
                é armazenado seu valor e retornado.
            '''
            mnemonic = self.current_token.value
            self.eat(WORD)
            return mnemonic.lower() # os caratéres do mnemônico são convertidos em lowercase

        else:
            '''
                Se o Token capturado não for uma WORD
                um erro é retornado
            '''
            self.error()


    '''
        Método label:
        Captura inicialmente o label do comando (linha).
    '''
    def label(self):
        # À princípio, o label é uma string vazia
        _label = ''


        if self.current_token.type == WORD:
            '''
                Se o Token atual for uma WORD
                é armazenado seu valor e concatenado à
                string do label.
                Após isso, deve ser capturado um COLON ':'
                e concatenado à string do label.
                Depois, o label é retornado
            '''
            _label += self.current_token.value
            self.eat(WORD)
            _label += self.current_token.value
            self.eat(COLON)
            return _label

        elif self.current_token.type == SPACE:
            '''
                Se o Token atual for uma espaço (SPACE),
                então não há label nesta linha, e portanto,
                um caratére vazio é retornado.
            '''
            self.eat(SPACE)
            return ''

        '''
            Se a execução chegar até aqui, então nada 
            foi retornado, nem uma WORD, nem um SPACE,
            logo um erro é retornado 
        '''
        self.error()


    '''
        Método cmd:
        Captura respectivamente, um label, um mnemônico,
        um argumneto e outro argumento (há comandos com dois
        argumentos).
        Isso é guardado em ordem em uma lista e esta é 
        retornada.
    '''
    def cmd(self):
        result = [None, None, None, None]
        result[0] = self.label()
        result[1] = self.mnemonic()
        result[2] = self.argument()
        result[3] = self.argument()
        
        return result

'''
    Classe Mounter:
    Classe responsável por:
    - Ler o arquivo .ASM (Assembly)
    - Exercutar o interpretador em cada linha
    - Pegar a matriz resultado da interpretação e montar 
      o binário (método 'mount')
    - Escrever o binário em um outro arquivo

    Parâmetros:
    - cmds: Matriz em que as linhas correspondem a cada
            linha do arquivo assembly, e cada coluna
            corresponde respectivamente ao label, mnemônico,
            argumento 1 e argumento 2.
    - vars: Lista das variáveis utilizadas no programa.
    - binary: bytearray responsável por armazenar todo o
              binário a ser escrito no programa resultado
              da montagem.
'''
class Mounter(object):
    def __init__(self):
        self.cmds = []
        self.vars = []
        self.binary = bytearray()

    '''
        Método get_mnemonics:
        Retorna a lista dos mnemônicos utilizados
        em ordem.
    '''
    def get_mnemonics(self):
        return list(map(lambda x: x[1], self.cmds))

    '''
        Método get_vars:
        Popula o parâmetro 'vars' com a lista das variáveis
        utilizadas em ordem, aplicando a operação 'distinct',
        ou seja, sem repetições.
    '''
    def get_vars(self):
        for cmd in self.cmds:
            # Sabe que o argumento é uma variável quando este 
            # é relacionado ao comando ILOAD
            if cmd[1] in ['iload']: 
                if cmd[2] not in self.vars:
                    self.vars.append(cmd[2])
        return self.vars

    '''
        Método count_vars:
        Retorna uma dicionário em que a chave é uma
        variável utilizada no programa assembly
        e o valor é o índice corresponde a sua
        aparição. Logo, se, por exemplo, 'k' é a terceira
        variável a aparecer no programa, o dicionário vai ser
        {
            'K': 3
        }
    '''
    def count_vars(self):
        # Lista todas as variáveis com o método 'get_vars'
        vars_list = self.get_vars()
        vars_dic = {}
        count = 0;
        for var in vars_list:
            vars_dic[var] = count
            count += 1
        return vars_dic

    '''
        Método convert_labels_to_offset:
        Responsável por substituir cada label como argumento
        pela distância em bytes da sua aparição até sua
        utilização como marcação do desvio.
        É importante ressaltar que essa distância em
        bytes também conta os bytes do próprio label.
    '''
    def convert_labels_to_offset(self):
        count = 0
        gotos_dic = {}
        labels_dic = {}

        '''
            Primeiro loop: responsável por mapear, em um
            primeiro dicionário, os labels (chave) com suas respectivas
            distâncias em byte desde o início do programa (valor).
            E por mapear em um segundo dicionário, os comandos que 
            correspondem a um desvio (GOTO, IF_ICMPEQ), também com suas respectivas
            distâncias em byte desde o início do programa (valor).
        '''
        for i, cmd in enumerate(self.cmds):
            mnemonic = cmd[1]
            label = cmd[0]
            count += mnemonics[mnemonic][1] # Utilizando o tamanho do comando, valor presente no dicionário 'mnemonics'
            if mnemonic in ['goto', 'if_icmpeq']:
                gotos_dic[i] = count
            if label != '':
                labels_dic[label.strip(':')] = count - mnemonics[mnemonic][1] + 1

        converted_cmds = self.cmds

        '''
            Segundo loop: responsável por percorrer os comandos,
            e substituir as aparições dos labels (como argumento)
            pelo difenração da posição em bytes deste label (primeiro
            dicionário, com a posição em byte do comando que o usa
            (segundo dicionário).
        '''
        for i, cmd in enumerate(self.cmds):
            mnemonic = cmd[1]
            if mnemonic in ['goto', 'if_icmpeq']:
                label = cmd[2]
                converted_cmds[i][2] = labels_dic[label] - gotos_dic[i] + 2 # Mais 2 referente ao próprio label

        # Todas as modidicações atuam sobre o parâmetro 'cmds'
        # Logo, ao final, este é atualizado
        self.cmds = converted_cmds

    '''
        Método replace_vars:
        Substitui a ocorrência das variavéis utilizadas
        com sua posições calculadas com a chamada do método
        'count_vars'.
    '''
    def replace_vars(self):
        replaced_cmds = self.cmds;
        counted_vars = self.count_vars()
        for i, cmd in enumerate(self.cmds):
            arg = cmd[2]
            if arg in counted_vars:
                replaced_cmds[i][2] = int(counted_vars[arg])

        # Todas as modidicações atuam sobre o parâmetro 'cmds'
        # Logo, ao final, este é atualizado
        self.cmds = replaced_cmds

    '''
        Método replace_mnemonics:
        Substitui a ocorrência dos mnemônicos por seus
        respectivos códigos binários.
        Informação presente no dicionário 'mnemonics'
        'count_vars'.
    '''
    def replace_mnemonics(self):
        prev_cmds = self.cmds;
        for i, cmd in enumerate(prev_cmds):
            self.cmds[i][1] = mnemonics[cmd[1]][0]

    '''
        Método mount:
        Responsável por:
        - Substituir as váriáveis pelo índice de sua ocorrência (método 'replace vars')
        - Converter os labels por sua posição (método 'convert_labels_to_offset')
        - Converter os mnemônicos por seus binário (método 'replace_mnemonicos')
    '''
    def mount(self):
        self.replace_vars()
        self.convert_labels_to_offset()
        self.replace_mnemonics()

    '''
        Método read_file:
        Lê o arquivo assembly passado como argumento
        e aplica o Interpretador a cada linha do programa,
        armazenando o resultado do seu método 'cmd'
        em uma lista de comandos, formando assim a matriz
        utilizada no escopo dessa classe.        
    '''
    def read_file(self, file_name):
        asm = open(file_name, 'r')

        cmds = []

        for l in asm.readlines():
            lexer = Lexer(l)
            interpreter = Interpreter(lexer)
            cmds.append(interpreter.cmd())

        asm.close()

        self.cmds = cmds

    '''
        Método write_file:
        Dados os comandos já separados e interpretados,
        é chamado o método 'mount' para mmontar o programa.
        Daí o binário é formado e escrito no arquivo binário
        passado como parâmetro.
    '''
    def write_file(self, file_name):
        self.mount()
        
        '''
            Função para, dado um número inteiro, 
            ser retornado uma lista de quatro elementos,
            que reprentam em ordem 'little endia', os bytes
            desse número.
        '''
        def split_bytes(number):
            b1, b2, b3, b4 = (number & 0xFFFFFFFF).to_bytes(4, 'little')
            return [b1, b2, b3, b4]
        
        '''
            Função para, dado uma lista de bytes, ela adicione
            cada byte ao byte array do parâmetro 'binary'.
        '''
        def append_list_to_bytearray(list):
            for b in list:
                self.binary.append(b)

        vars_num = len(self.vars) # Captura a quantidade de variáveis

        # Separa os bytes resultante da soma de 0x1001
        # com a quantidade de variáveis, e armazena.
        last_bytes = split_bytes(0x1001 + vars_num) 

        # Inicializam do programa
        program_init = [
            0x00, 0x73, 0x00, 0x00,
            0x06, 0x00, 0x00, 0x00,
            0x01, 0x10, 0x00, 0x00,
            0x00, 0x04, 0x00, 0x00,
            *last_bytes # Usa o splat operador para adicionar os últimos bytes ao vetor
        ]

        # Cria um bytearray apenas para o programa
        program = bytearray()

        # Pecorre cada comando do programa do programa já montado
        # e adiciona o binário do programa ao bytearray acima declarado
        for cmd in self.cmds:
            for i, byte in enumerate(cmd[1:]):
                if byte != '' and byte != " ":
                    byte = int(byte)
                    if i >= 1 and size_per_cmd[cmd[1]] > 2:
                        # O trecho abaixo pega o número de dois bytes,
                        # e separa seus bytes na ordem 'little endiam'.
                        rgt = (byte << 8) >> 8
                        lft = byte >> 8
                        program.append(lft)
                        program.append(rgt)
                    else:
                        program.append(byte)

        # Captura o tamanho do programa, pegando o tamanho
        # em bytes do bytearray 'program' e somando com
        # os 20 bytes da inicialização
        program_length = split_bytes(len(program) + 20)

        # Adiciona o tamanho do programa ao binário principal
        append_list_to_bytearray(program_length)
        # Após isso, adiciona a inicialização do programa
        append_list_to_bytearray(program_init)
        # E, por último, adiciona o próprio programa
        append_list_to_bytearray(program)
        
        # Escreve o binário principal no arquivo binário
        binary = open(file_name, 'wb')
        binary.write(self.binary)
        binary.close()

def main():
    # Instancia a classe Mounter
    mounter = Mounter()
    # Informa o arquivo a ser lido
    mounter.read_file('assembly_ex2.asm')
    # E o arquivo a ser escrito
    mounter.write_file('binary_ex2.exe')

if __name__ == '__main__':
    main()
