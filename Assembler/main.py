import struct

WORD, LPAREN, RPAREN, EOF, COLON, SPACE = "WORD", "(", ")", "EOF", ":", " "

mnemonics = {
    "nop":            0x01,
    "iadd":           0x02,
    "isub":           0x05,
    "iand":           0x08,
    "ior":            0x0B,
    "dup":            0x0E,
    "pop":            0x10,
    "swap":           0x13,
    "bipush":         0x19,
    "iload":          0x1C,
    "istore":         0x22,
    "wide":           0x28,
    "ldc_w":          0x32,
    "iinc":           0x36,
    "goto":           0x3C,
    "iflt":           0x43,
    "ifeq":           0x47,
    "if_icmpeq":      0x4B,
    "invokevirtual":  0x55,
    "ireturn":        0x6B
}

compiledCmds = []

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
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def getWord(self):
        word = ''
        while self.current_char is not None and (self.current_char.isalpha() or self.current_char == '_' or self.current_char.isdigit()):
            word += self.current_char
            self.advance()
        return word
            
    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace() and self.pos != 0:
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
        result = [None, None, None]
        result[0] = self.flag()
        result[1] = self.mnemonic()
        result[2] = self.argument()

        return result

asm = open('assembly.asm', 'r')

cmds = []

for l in asm.readlines():
    lexer = Lexer(l)
    interpreter = Interpreter(lexer)
    cmds.append(interpreter.cmd())

asm.close()

print(
    "\n".join(
        list(
            map(
                lambda x: 
                " |".join(
                    list(
                        map(
                            lambda y: '{:^14s}'.format(y),
                            x
                        )
                    )
                ),
                cmds
            )
        )
    )
)

'''
binary = open('binary.bin', 'wb')

for cmd in cmds:
    print( mnemonics[cmd[1]])
    binary.write(struct.pack('i', mnemonics[cmd[1]]))

binary.close()
'''
