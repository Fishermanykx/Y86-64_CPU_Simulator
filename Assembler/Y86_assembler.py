'''
@Description: 将Y86汇编代码转换为机器码，地址默认从1开始
@Author: Fishermanykx
@LastEditors: Fishermanykx
@LastEditTime: 2020-03-17 17:35:04
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
    self.filename = filename
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
    # 初始化标签-地址表
    self.dest_table = {}
    # pprint(self.codes)

  def ConvertSingleInstruction(self, ins):
    "假设传入的均为合法指令且均已处理成列表"
    res = ''
    op = ins[0]
    if ins[0] == "halt" or ins[0] == "nop":
      res += self.opcode_table[ins[0]]
    elif op in ["rrmovq", "xorq", "addq", "subq"]:  # 算术指令以及rrmovq的编码
      res = self.opcode_table[op] + self.reg_table[ins[1]] + self.reg_table[
          ins[2]]
    elif op == "irmovq":
      res = self.opcode_table[op] + self.reg_table["None"] + self.reg_table[
          ins[2]]
      # 符号扩展操作数至4字节
      signal = 0 if int(ins[1]) > 0 else 1
      immediate_num = str(signal) * (8 - len(ins[1])) + ins[1]
      # 转换成小端法表示
      imm_v = ""
      for i in range(6, -1, -2):
        imm_v = imm_v + immediate_num[i] + immediate_num[i + 1]
      res += imm_v
    elif op in ["jmp", "jle", "jl", "je", "jne", "jge", "jg",
                "call"]:  # 跳转及类跳转指令
      # 符号扩展操作数至4字节
      ins_1 = str(self.dest_table[ins[1]])
      immediate_num = '0' * (8 - len(ins_1)) + ins_1
      # 转换成小端法表示
      imm_v = ""
      for i in range(6, -1, -2):
        imm_v = imm_v + immediate_num[i] + immediate_num[i + 1]
      res = self.opcode_table[ins[0]] + imm_v
    else:
      print("Instruction Error!")

    return res

  def ConvertCodes(self):
    cnt_dest = 0  # 地址指针
    machine_codes = []
    # 逐行遍历并转换为机器码
    for i in range(len(self.codes)):
      # 预处理
      ins = self.codes[i].split()
      # 判断是否为标签
      if ins[0] not in list(self.opcode_table.keys()):
        self.dest_table[ins[0]] = cnt_dest
      else:
        res = ""
        # 检查元素合法性
        for j in range(len(ins)):
          if '$' in ins[j]:
            ins[j] = ins[j][3:]
        res = "%03d " % cnt_dest + self.ConvertSingleInstruction(ins) + "\n"
        machine_codes.append(res)
        cnt_dest += 1
    # 写入文件filename
    with open(self.filename + ".bin", "w") as outf:
      outf.writelines(machine_codes)


if __name__ == "__main__":
  assembler = Assembler(
      "D:/Materials_Study/Computer_Science/Computer_Architecture/Exercises/Y86-64_CPU_Simulator/Assembler/testbench"
  )
  assembler.ConvertCodes()
