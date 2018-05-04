'''
    A lista abaixo refere-se a lista dos tipos de TOKENS que o assembler suporta
    Token é todo e qualquer conjunto de caracteres com significado semântico
    para a linguagem
    WORD - Conjunto alfanumético de caractéres
    LPAREN - Parêntese abrindo "("
    RPAREN - Parêntese fechando ")"
    EOF - Fim de linha
    COLON - Dois pontos ":"
    SPACE - Espaço em branco " "
'''
WORD, LPAREN, RPAREN, EOF, COLON, SPACE = "WORD", "(", ")", "EOF", ":", " "


'''
    O dicionário abaixo mapeira o binário de cada comando
    com o seu tamanho completo, o qual engloba o tamanho, 
    em bytes, do mnemônic e seus argumentos
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
    O dicionário abaixo mapeira cada mnemônico com
    o seu respectivo código binário
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
        (linha atual do arquivo que está sendo lindo).
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
            '''
                Se o caractére atual é um espaço, chama o método
                'skip_whitespace', pula todos os demais e continua
                com a execução.
            '''
            if (self.current_char.isspace() or self.current_char == '\t') and self.pos != 0:
                self.skip_whitespace()
                continue

            '''
                Se o caractére atual é um alfanumérico, chama o método
                'getWord' e retorna um Token do tipo WORD, com o valor
                da string capturada.
            '''
            if self.current_char.isalpha() or self.current_char.isdigit():
                word = self.getWord()
                return Token(WORD, word)

            '''
                Se o caractére atual é um '(', avança um caratére
                e retorna um Token do tipo LPAREN, com o valor '('.
            '''
            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            '''
                Se o caractére atual é um ')', avança um caratére
                e retorna um Token do tipo RPAREN, com o valor '('.
            '''
            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            '''
                Se o caractére atual é um ':', avança um caratére
                e retorna um Token do tipo COLON, com o valor ':'.
            '''
            if self.current_char == ':':
                self.advance()
                return Token(COLON, ':')

            '''
                Se o caractére atual é um ' ' e a posição atual de
                leitura é zero (o que difere do primeiro IF), ou seja,
                está no início da linha, avança um caratére, e
                retorna um Token do tipo SPACE, com o valor ' '.
            '''
            if self.current_char.isspace() and self.pos == 0:
                self.advance()
                return Token(SPACE, ' ')

            # Se o caractére atual é validade em nenhuma checagem
            # um erro sintático é retornado
            self.error()

        # Se o loop deu-se fim, entende-se que chegou-se ao fim da linha.
        # Logo, retorna-se um Token do tipo EOF, com valor None (null)
        return Token(EOF, None)


class Interpreter(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Deixa de ser abestado')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def argument(self):
        token = self.current_token
        
        if token.type == WORD:
            argument = token.value
            self.eat(WORD)
            return argument
        elif token.type == LPAREN:
            self.eat(LPAREN)
            result = self.argument()
            self.eat(RPAREN)
            return result
        elif token.type == EOF:
            return ''

    def mnemonic(self):
        if self.current_token.type == WORD:
            mnemonic = self.current_token.value
            self.eat(WORD)
            return mnemonic.lower()
        else:
            self.error()

    def flag(self):
        _flag = ''
        if self.current_token.type == WORD:
            _flag += self.current_token.value
            self.eat(WORD)
            _flag += self.current_token.value
            self.eat(COLON)
            return _flag
        elif self.current_token.type == SPACE:
            self.eat(SPACE)
            return ''
        self.error()
  
    def cmd(self):
        result = [None, None, None, None]
        result[0] = self.flag()
        result[1] = self.mnemonic()
        result[2] = self.argument()
        result[3] = self.argument()
        
        return result

class Mounter(object):
    def __init__(self):
        self.cmds = []
        self.vars = []
        self.binary = bytearray()

    def get_mnemonics(self):
        return list(map(lambda x: x[1], self.cmds))

    def get_vars(self):
        for cmd in self.cmds:
            if cmd[1] in ['iload']:
                if cmd[2] not in self.vars:
                    self.vars.append(cmd[2])
        return self.vars
    
    def count_vars(self):
        vars_list = self.get_vars()
        vars_dic = {}
        count = 0;
        for var in vars_list:
            vars_dic[var] = count
            count += 1
        return vars_dic
        
    def convert_labels_to_offset(self):
        count = 0
        gotos_dic = {}
        labels_dic = {}
        for i, cmd in enumerate(self.cmds):
            mnemonic = cmd[1]
            label = cmd[0]
            count += mnemonics[mnemonic][1]
            if mnemonic in ['goto', 'if_icmpeq']:
                gotos_dic[i] = count
            if label != '':
                labels_dic[label.strip(':')] = count - mnemonics[mnemonic][1] + 1

        converted_cmds = self.cmds
        for i, cmd in enumerate(self.cmds):
            mnemonic = cmd[1]
            if mnemonic in ['goto', 'if_icmpeq']:
                label = cmd[2]
                converted_cmds[i][2] = labels_dic[label] - gotos_dic[i] + 2

        self.cmds = converted_cmds

    def replace_vars(self):
        replaced_cmds = self.cmds;
        counted_vars = self.count_vars()
        for i, cmd in enumerate(self.cmds):
            arg = cmd[2]
            if arg in counted_vars:
                replaced_cmds[i][2] = int(counted_vars[arg])
        self.cmds = replaced_cmds

    def replace_mnemonics(self):
        prev_cmds = self.cmds;
        for i, cmd in enumerate(prev_cmds):
            self.cmds[i][1] = mnemonics[cmd[1]][0]

    def mount(self):
        self.replace_vars()
        self.convert_labels_to_offset()
        self.replace_mnemonics()

    def read_file(self, file_name):
        asm = open(file_name, 'r')

        cmds = []

        for l in asm.readlines():
            lexer = Lexer(l)
            interpreter = Interpreter(lexer)
            cmds.append(interpreter.cmd())

        asm.close()

        self.cmds = cmds
        
    def write_file(self, file_name):
        self.mount()
        
        def split_bytes(number):
            y1, y2, y3, y4 = (number & 0xFFFFFFFF).to_bytes(4, 'little')
            return [y1, y2, y3, y4]

        def append_list_to_bytearray(list):
            for b in list:
                self.binary.append(b)

        vars_num = len(self.vars)

        last_bytes = split_bytes(0x1001 + vars_num)

        program_init = [
            0x00, 0x73, 0x00, 0x00,
            0x06, 0x00, 0x00, 0x00,
            0x01, 0x10, 0x00, 0x00,
            0x00, 0x04, 0x00, 0x00,
            *last_bytes
        ]

        program = bytearray()
        for cmd in self.cmds:
            for i, byte in enumerate(cmd[1:]):
                if byte != '' and byte != " ":
                    byte = int(byte)
                    if i >= 1 and size_per_cmd[cmd[1]] > 2:
                        rgt = (byte << 8) >> 8
                        lft = byte >> 8
                        program.append(lft)
                        program.append(rgt)
                    else:
                        program.append(byte)

        program_length = split_bytes(len(program) + 20)
        append_list_to_bytearray(program_length)
        append_list_to_bytearray(program_init)
        append_list_to_bytearray(program)
        
        binary = open(file_name, 'wb')
        binary.write(self.binary)
        binary.close()

def main():
    mounter = Mounter()
    mounter.read_file('assembly_ex2.asm')
    mounter.write_file('binary_ex2.exe')

if __name__ == '__main__':
    main()
