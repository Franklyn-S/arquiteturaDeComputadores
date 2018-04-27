      ILOAD j
      ILOAD k
      IADD
      ISTORE i
      ILOAD i
      BIPUSH 3
      IF_ICMPEQ L1
      ILOAD j
      BIPUSH 1
      ISUB
      ISTORE j
      GOTO L2
L1:   BIPUSH 0
      ISTORE k
L2:   NOP