'''
@Description: Y86指令集CPU模拟器
@Author: Fishermanykx
@Date: 2020-03-17 20:59:08
@LastEditors: Fishermanykx
@LastEditTime: 2020-03-18 16:43:42
'''
from pprint import pprint


class CPUSimulator:

  def __init__(self, filename):
    ## 将内存分为不同的区域，每位代表一个数字(4bit)
    # 规定各部分大小
    self.max_ins_mem_size = 1024
    self.max_data_mem_size = 1024
    self.max_stack_size = 1024
    # 初始化内存各区域
    self.instruction_memory = ''  # 指令区域
    self.data_memory = [0] * self.max_data_mem_size
    # 初始化寄存器文件(str-int)
    self.regFile = {}  # 寄存器文件，编号依次为字符0~7
    for i in range(8):
      self.regFile[str(i)] = 0
    # 初始化栈区
    self.stack = []
    # 读入指令，并将其存储在instruction_memory中
    inf = open(filename + ".bin", "r")
    while True:
      line = inf.readline()
      if line == '':
        break
      line = line.strip()[4:]
      self.instruction_memory += line
    inf.close()
    # print(self.instruction_memory)
    ## 初始化条件码
    self.cc = {"ZF": 0, "SF": 0, "OF": 0}  # ZF: 为0；SF: 为负；OF: 溢出
    ## 初始化PC
    self.pc = 0
    ## 初始化状态码
    self.stat = "AOK"
    self.stat_list = ["AOK", "HLT", "ADR", "INS"]

  def MainCycle(self):
    # F-Register
    predPC = 0
    while self.stat == "AOK":
      pass

  def Fetch(self):
    '''
    @description: 取指阶段
    @param {type} 
    @return: 取出的二进制指令(str)
    '''
    try:
      ins = self.instruction_file[self.rip]
      self.rip += 1
    except:  # 若已经执行完毕，则传入气泡
      ins = "01"
    return ins

  def Decode(self, ins):
    '''
    @description: 译码阶段: 将二进制指令转换为opcode与操作数(十进制int)
    @param {type}: ins{str}
    @return: list
    '''
    opcode = ins[0:2]
    res = []
    # 根据指令类型切分
    op_type = int(opcode[0])
    if op_type == 0:
      self.has_next_ins = False
      res = ["00"]
    elif op_type == 1:
      res = ["00"]
    elif op_type == 2:
      res.append(opcode)
      res.append(self.regFile[int(ins[2])])
      res.append(self.regFile[int(ins[3])])
    elif op_type == 3:
      res.append(opcode)
      res.append(None)
      res.append(self.regFile[int(ins[3])])
      res.append(self.ConvertImmNum(ins[4:]))
    elif op_type == 4 or op_type == 5:
      res.append(opcode)
      res.append(self.regFile[int(ins[2])])
      res.append(self.regFile[int(ins[3])])
      res.append(self.ConvertImmNum(ins[4:]))
    elif op_type == 6:
      res.append(opcode)
      res.append(self.regFile[int(ins[2])])
      res.append(self.regFile[int(ins[3])])
    elif op_type == 7 or op_type == 8:
      res.append(opcode)
      res.append(self.ConvertImmNum(ins[2:]))
    elif op_type == 8:
      res.append(opcode)
    elif op_type == 10 or op_type == 11:
      res.append(opcode)
      res.append(self.regFile[int(ins[2])])
      res.append(None)
    else:
      print("Error: Illegal instruction. Exit code: INS")
      exit(1)
    return res

  def Execute(self, slided_ins):
    '''
    @description: 执行阶段
    @param {type} 根据opcode与操作数执行指令
    @return: 计算所得的结果
    '''

  def Memory(self):
    '''
    @description: 访存阶段
    @param {type} 
    @return: 将执行阶段的值写回内存或从内存中取出值
    '''
    pass

  def WriteBack(self):
    '''
    @description: 写回阶段
    @param {type} 
    @return: 将计算结果写回寄存器文件
    '''
    pass

  def ConvertImmNum(self, num_str):
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
    for i in range(6, 0, -2):
      rev_str += (num_str[i] + num_str[i + 1])
    return int("0x" + rev_str, 16)


if __name__ == "__main__":
  simulator = CPUSimulator(
      "D:/Materials_Study/Computer_Science/Computer_Architecture/Exercises/Y86-64_CPU_Simulator/cpu_simulator/testbench"
  )  # Windows
  # simulator = CPUSimulator(
  #     "/media/fisher/DATA/Materials_Study/Computer_Science/Computer_Architecture/Exercises/Y86-64_CPU_Simulator/cpu_simulator/testbench"
  # )  # Linux
  # simulator.MainProcess()
  reg = str(0)
  print(simulator.regFile[reg])  # 结果的值在rax里
