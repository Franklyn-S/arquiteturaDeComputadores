import struct

WORD, LPAREN, RPAREN, EOF, COLON, SPACE = "WORD", "(", ")", "EOF", ":", " "

def pretty_print(cmds):
    print(
        "\n".join(
            list(
                map(
                    lambda x: 
                    " ".join(
                        list(
                            map(
                                lambda y: '{:^4s}'.format(hex(int(y if y != '' else 0))),
                                x[1:]
                            )
                        )
                    ),
                    cmds
                )
            )
        )
    )


site_per_cmd = {
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

mnemonics = {}

for mnemonic in mnemonics_list:
    mnemonics[mnemonic] = [mnemonics_list[mnemonic], site_per_cmd[mnemonics_list[mnemonic]]]

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return self.__str__()


class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid token')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and (self.current_char.isspace() or self.current_char == '\t'):
            self.advance()

    def getWord(self):
        word = ''
        while self.current_char is not None and (self.current_char.isalpha() or self.current_char == '_' or self.current_char.isdigit()):
            word += self.current_char
            self.advance()
        return word
            
    def get_next_token(self):
        while self.current_char is not None:
            if (self.current_char.isspace() or self.current_char == '\t') and self.pos != 0:
                self.skip_whitespace()
                continue

            if self.current_char.isalpha() or self.current_char.isdigit():
                word = self.getWord()
                return Token(WORD, word)

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            if self.current_char == ':':
                self.advance()
                return Token(COLON, ':')

            if self.current_char.isspace() and self.pos == 0:
                self.advance()
                return Token(SPACE, ' ')

            self.error()

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
        count = 1;
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
                replaced_cmds[i][2] = counted_vars[arg]
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
        for cmd in self.cmds:
            for i, byte in enumerate(cmd[1:]):
                if byte:
                    byte = int(byte)
                    self.binary.append(byte)

                    if i > 1 and site_per_cmd[cmd[1]] > 2:
                        lft = (byte << 8) >> 8
                        rgt = byte >> 8
                        self.binary.append(rgt)
                        self.binary.append(lft)

        
        binary = open(file_name, 'wb')
        binary.write(self.binary)
        binary.close()


def main():
    mounter = Mounter()
    mounter.read_file('assembly.asm')
    mounter.write_file('binary.bin')

if __name__ == '__main__':
    main()