'''
@Description: 将Y86汇编代码转换为机器码，地址默认从1开始
@Author: Fishermanykx
@LastEditors: Fishermanykx
@LastEditTime: 2020-03-15 11:12:51
'''
from pprint import pprint


class Assembler:
  """
  Y86汇编器，从文件中filename.s中读入汇编代码，将机器码写回到filename中
  """

  def __init__(self, filename):
    inf = open(filename + ".s", "r")
    codes = inf.readlines()
    inf.close()
    self.codes = [(elem[4:]).strip() for elem in codes]
    pprint(self.codes)


if __name__ == "__main__":
  assembler = Assembler("testbench")