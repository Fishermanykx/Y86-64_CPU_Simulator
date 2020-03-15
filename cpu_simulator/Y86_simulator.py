'''
@Description: 
@Author: Fishermanykx
@LastEditors: Fishermanykx
@LastEditTime: 2020-03-15 23:58:34
'''


class CPUSimulator:

  def __init__(self, filename):
    "载入含机器码的文件"
    self.regFile = [0] * 8  # 寄存器文件，编号依次为0~7
    self.memory = [0] * 1000  # 内存
    self.rip = 0
    inf = open(filename + ".bin", "r")
    while True:
      line = inf.readline()
      if line == '':
        break
      line = line.split()
      address = int(line[0])

    inf.close()


if __name__ == "__main__":
  simulator = CPUSimulator("testbench")
  print(simulator.regFile[0])  # 结果的值在rax里
