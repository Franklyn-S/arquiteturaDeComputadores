


asm = open('assembly.asm', 'r')

mp = ''

dic = {
  "IADD": [2,4,6,8]
}

def Interpreter(_str):
  _cmd = ''
  _arg = ''
  _flag = ''
  curChar = 0
  hasFlag = False
  EOL = False
  cmdFound = False

  while curChar < len(_str):
    if (_str[curChar].isalpha()):
      if not hasFlag:
        _flag += _str[curChar]
      else:
        _cmd += _str[curChar]
    elif _str[curChar].isspace():
      if hasFlag:
        cmdFound = True
      hasFlag = True
    elif cmdFound:
      _arg = _arg + _str[curChar]
    else:
      exit()
    curChar += 1

  return _flag, _cmd, _arg

cmds = []

for l in asm.readlines():
  _flag, _cmd, _arg = Interpreter(l)
  cmds.append([_flag, _cmd, _arg])

print(cmds)

asm.close()