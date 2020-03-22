'''
@Description: 
@Author: Fishermanykx
@Date: 2020-03-18 16:28:16
@LastEditors: Fishermanykx
@LastEditTime: 2020-03-22 16:03:11
'''

# path = "D:/Materials_Study/Computer_Science/Computer_Architecture/Exercises/Y86-64_CPU_Simulator/cpu_simulator/testbench"


# instruction_memory = ''
# inf = open(path + ".bin", 'r')
# while True:
#   line = inf.readline()
#   if line == '':
#     break
#   line = line.strip()[4:]
#   instruction_memory += line
# print(instruction_memory)
# self_instruction_memory = []
# for bit in range(0, len(instruction_memory), 2):
#   self_instruction_memory.append(instruction_memory[bit] +
#                                  instruction_memory[bit + 1])
# print(self_instruction_memory[26])
def ConvertImmNum(num_str):
  '''
  @description: 将用小端法表示的立即数转换为十进制整数
  @param {type} num_str {str}
  @return: int
  '''
  '''
  >>> ConvertImmNum("10000000")
  16
  >>> ConvertImmNum("10100000")
  4112
  '''
  # 将立即数反转为正常顺序
  rev_str = ""
  for i in range(6, -1, -2):
    rev_str += (num_str[i] + num_str[i + 1])
  return int("0x" + rev_str, 16)


a = ConvertImmNum("01000000")
print(a)