000 sum
001   xorq rax rax 
002   irmovq $1 rbx  
003   irmovq $1 rdx  
004   irmovq $0x65 rcx 
005   irmovq $0x65 rsi
006   loop
007     addq rbx rax 
008     addq rdx rbx 
009   test
010     subq rbx rcx
011     rrmovq rsi rcx
012     jnz loop
013   ret