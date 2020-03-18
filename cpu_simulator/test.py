'''
@Description: 
@Author: Fishermanykx
@Date: 2020-03-18 16:28:16
@LastEditors: Fishermanykx
@LastEditTime: 2020-03-18 21:13:44
'''
path = "D:/Materials_Study/Computer_Science/Computer_Architecture/Exercises/Y86-64_CPU_Simulator/cpu_simulator/testbench"

instruction_memory = ''
inf = open(path + ".bin", 'r')
while True:
  line = inf.readline()
  if line == '':
    break
  line = line.strip()[4:]
  instruction_memory += line
print(instruction_memory)
self_instruction_memory = []
for bit in range(0, len(instruction_memory), 2):
  self_instruction_memory.append(instruction_memory[bit] +
                                 instruction_memory[bit + 1])
print(self_instruction_memory[26])