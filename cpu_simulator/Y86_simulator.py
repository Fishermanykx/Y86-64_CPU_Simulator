'''
@Description: 
@Author: Fishermanykx
@LastEditors: Fishermanykx
@LastEditTime: 2020-03-16 17:17:29
'''
from pprint import pprint


class CPUSimulator:

  def __init__(self, filename):
    "载入含机器码的文件"
    # 初始化寄存器文件
    self.regFile = {}  # 寄存器文件，编号依次为0~7
    for i in range(8):
      self.regFile[i] = 0
    # 初始化内存
    self.memory = [0] * 1000  # 内存
    self.rip = 0  # instruction pointer
    # 构建地址-代码表
    self.codes = {}
    inf = open(filename + ".bin", "r")
    while True:
      line = inf.readline()
      if line == '':
        break
      line = line.split()
      address = line[0]
      self.codes[address] = line[1]
    inf.close()

    # pprint(self.codes)

    def main_process(self):
      pass


if __name__ == "__main__":
  simulator = CPUSimulator(
      "D:/Materials_Study/Computer_Science/Computer_Architecture/Exercises/Y86-64_CPU_Simulator/cpu_simulator/testbench"
  )  # Windows
  # simulator = CPUSimulator(
  #     "/media/fisher/DATA/Materials_Study/Computer_Science/Computer_Architecture/Exercises/Y86-64_CPU_Simulator/cpu_simulator/testbench"
  # )  # Linux
  print(simulator.regFile[0])  # 结果的值在rax里
