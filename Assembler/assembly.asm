main: NOP
      IADD
      ISUB
      IAND
      IOR
      DUP
      POP
      SWAP
      BIPUSH 25
      ILOAD k
      ISTORE k
      WIDE
      WIDE_ILOAD
      WIDE_ISTORE
      LDC_W 9
      IINC
loop: GOTO loop
      IFLT
      IFEQ
      IF_ICMPEQ
      INVOKEVIRTUAL
      IRETURN