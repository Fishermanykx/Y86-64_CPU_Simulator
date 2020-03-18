'''
@Description: 
@Author: Fishermanykx
@Date: 2020-03-18 16:28:16
@LastEditors: Fishermanykx
@LastEditTime: 2020-03-18 16:31:51
'''
path = "D:/Materials_Study/Computer_Science/Computer_Architecture/Exercises/Y86-64_CPU_Simulator/cpu_simulator/testbench"

instruction_memory = ''
inf = open(path + ".bin", 'r')
while True:
  line = inf.readline()
  if line == '':
    break
  line = line.strip()[4:]
  print(len(line))
  instruction_memory += line
print(instruction_memory)