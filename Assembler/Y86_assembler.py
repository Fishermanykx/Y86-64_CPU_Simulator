'''
@Description: 将Y86汇编代码转换为机器码，地址默认从1开始
@Author: Fishermanykx
@LastEditors: Fishermanykx
@LastEditTime: 2020-03-15 17:47:38
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
    # pprint(self.codes)

  def ConvertSingleInstruction(self, ins):
    "假设传入的均为合法指令且均已处理成列表"
    res = ''
    op = ins[0]
    if ins[0] == "halt" or ins[0] == "nop":
      res += self.opcode_table[ins[0]]
    elif op == "rrmovq":
      res = self.opcode_table[op] + self.reg_table[ins[1]] + self.reg_table[
          ins[2]]
    elif op == "irmovq":
      res = self.opcode_table[op] + self.reg_table["None"] + self.reg_table[
          ins[2]]
      # 符号扩展操作数至4字节
      immediate_num = ins[1][0] * (8 - len(ins[1])) + ins[1]
      # 转换成小端法表示
      imm_v = ""
      for i in range(6, 0, -2):
        imm_v = imm_v + immediate_num[i] + immediate_num[i + 1]
      res += imm_v
    elif op in ["xorq", "addq", "subq"]:  # 计算
      pass

    return res


if __name__ == "__main__":
  assembler = Assembler("testbench")