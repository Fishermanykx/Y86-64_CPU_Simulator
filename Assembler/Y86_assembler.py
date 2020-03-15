'''
@Description: 将Y86汇编代码转换为机器码，地址默认从1开始
@Author: Fishermanykx
@LastEditors: Fishermanykx
@LastEditTime: 2020-03-15 11:46:49
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
    # pprint(self.codes)
    # 初始化寄存器表
    self.reg_table = {
        "rax": "0",
        "rcx": "1",
        "rdx": "2",
        "rbx": "3",
        "rsp": "4",
        "rbp": "5",
        "rsi": "6",
        "rdi": "7",
        "None": "F"
    }
    # 初始化opcode表
    self.opcode_table = {
        "halt": "00",
        "nop": "10",
        "rrmovq": "20",
        "cmovle": "21",
        "cmovl": "22",
        "cmove": "23",
        "cmovne": "24",
        "cmovge": "25",
        "cmovg": "26",
        "irmovq": "30",
        "rmmovq": "40",
        "mrmovq": "50",
        "addq": "60",
        "subq": "61",
        "andq": "62",
        "xorq": "63",
        "jmp": "70",
        "jle": "71",
        "jl": "72",
        "je": "73",
        "jne": "74",
        "jge": "75",
        "jg": "76",
        "call": "80",
        "ret": "90",
        "pushq": "A0",
        "popq": "B0"
    }
    # 初始化条件码表
    self.cc_table = {"ZF": 0, "SF": 0, "OF": 0}
    self.stat_table = ["AOK", "HLT", "ADR", "INS"]
    self.stat = "AOK"

  def ConvertSingleInstruction(self):
    res = ''


if __name__ == "__main__":
  assembler = Assembler("testbench")