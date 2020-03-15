# Calculate the sum from 1 to 100
sum
  xorq rax rax 
  irmovq 1 rbx  # 计数变量
  irmovq 1 rdx  # 加1
  irmovq 0x65 rcx # 101
  irmovq 0x65 rsi
  loop
    addq rbx rax 
    addq rdx rbx 
  test
    subq rbx rcx
    rrmovq rsi rcx # 恢复rcx的值
    jnz loop
  ret